#  _  __
# | |/ /___ ___ _ __  ___ _ _ ®
# | ' </ -_) -_) '_ \/ -_) '_|
# |_|\_\___\___| .__/\___|_|
#              |_|
#
# Keeper Commander
# Copyright 2018 Keeper Security Inc.
# Contact: ops@keepersecurity.com
#

keepass_instructions = """
libkeepass is not installed

Please see \'Install Keepass library\' section of README.md file for detailed instructions

pip3 install libkeepass

if above-mentioned command fails installing lxml package then install pre-compiled binary version of lxml

Download appropriate package from PyPI [https://pypi.org/project/lxml/#description]
or for Windows platform, from Unofficial Windows Binaries [https://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml]

For example: Python 3.5.0 for Windows 64 bit 
the library file name is going to be similar to \'lxml-4.2.3-cp35-cp35m-win-amd64.whl\'  

Install the downloaded package:
pip3 install lxml-4.2.3-cp35-cp35m-win-amd64.whl
pip3 install libkeepass
"""

try:
    import libkeepass
except:
    raise Exception(keepass_instructions)

import os
import base64
import getpass
import gzip
import io

from contextlib import contextmanager

from lxml import objectify, etree

from Cryptodome.Cipher import AES

from ..importer import path_components, PathDelimiter, BaseImporter, BaseExporter, \
    Record, Folder, SharedFolder, Permission, Attachment

class KeepassImporter(BaseImporter):

    @staticmethod
    def get_folder(group):
        g = group
        path = ''
        comp = ''
        while g.tag == 'Group':
            if comp:
                if len(path) > 0:
                    path = PathDelimiter + path
                path = comp + path
                comp = None

            if hasattr(g, 'Name'):
                nm = g.Name.text
                if nm is not None:
                    comp = nm.replace(PathDelimiter, PathDelimiter*2)
            g = g.getparent()
        return path

    def do_import(self, filename):
        password = getpass.getpass(prompt='...' + 'Keepass Password'.rjust(20) + ': ', stream=None)

        with libkeepass.open(filename, password=password) as kdb:
            root = kdb.obj_root.find('Root/Group')
            if root is not None:
                groups = [root]
                pos = 0
                while pos < len(groups):
                    g = groups[pos]
                    groups.extend(g.findall('Group'))
                    pos = pos + 1

                # Shared Folders
                for group in groups:
                    if hasattr(group, 'Keeper'):
                        keeper = group.Keeper
                        if hasattr(keeper, 'IsShared'):
                            if keeper.IsShared:
                                sf = SharedFolder()
                                sf.uid = base64.urlsafe_b64encode(base64.b64decode(group.UUID.text)).decode().rstrip('=')
                                sf.path = KeepassImporter.get_folder(group)
                                for sn in keeper.iterchildren():
                                    if sn.tag == 'ManageUsers':
                                        sf.manage_users = sn == True
                                    elif sn.tag == 'ManageRecords':
                                        sf.manage_records = sn == True
                                    elif sn.tag == 'CanEdit':
                                        sf.can_edit = sn == True
                                    elif sn.tag == 'CanShare':
                                        sf.can_share = sn == True
                                    elif sn.tag == 'Permission':
                                        perm = Permission()
                                        if sf.permissions is None:
                                            sf.permissions = []
                                        sf.permissions.append(perm)

                                        for p in sn.iterchildren():
                                            if p.tag == 'UUID':
                                                perm.uid = base64.urlsafe_b64encode(base64.b64decode(p.text)).decode().rstrip('=')
                                            elif p.tag == 'Name':
                                                perm.name = p.text
                                            elif p.tag == 'ManageUsers':
                                                perm.manage_users = p == True
                                            elif p.tag == 'ManageRecords':
                                                perm.manage_records = p == True
                                yield sf

                for group in groups:
                    entries = group.findall('Entry')
                    if len(entries) > 0:
                        folder = KeepassImporter.get_folder(group)
                        for entry in entries:
                            record = Record()
                            fol = Folder()
                            fol.path = folder
                            record.folders = [fol]
                            if hasattr(entry, 'UUID'):
                                record.record_uid = base64.urlsafe_b64encode(base64.b64decode(entry.UUID.text)).decode().rstrip('=')
                            if hasattr(entry, 'Keeper'):
                                for sn in entry.Keeper.iterchildren():
                                    if sn.tag == 'CanEdit':
                                        fol.can_edit = sn == True
                                    elif sn.tag == 'CanShare':
                                        fol.can_share = sn == True
                                    elif sn.tag == 'Link':
                                        f = Folder()
                                        for p in sn:
                                            if p.tag == 'Domain':
                                                f.domain = p.text
                                            elif p.tag == 'Path':
                                                f.path = p.text
                                            elif p.tag == 'CanEdit':
                                                f.can_edit = p == True
                                            elif p.tag == 'CanShare':
                                                f.can_share = p == True
                                        if f.domain or f.path:
                                            record.folders.append(f)

                            for node in entry.findall('String'):
                                sn = node.find('Key')
                                if sn is None:
                                    continue
                                key = sn.text
                                sn = node.find('Value')
                                if sn is None:
                                    continue
                                value = sn.text
                                if key == 'Title':
                                    record.title = value
                                elif key == 'UserName':
                                    record.login = value
                                elif key == 'Password':
                                    record.password = value
                                elif key == 'URL':
                                    record.login_url = value
                                elif key == 'Notes':
                                    record.notes = value
                                else:
                                    record.custom_fields[key] = value

                            if hasattr(kdb.obj_root.Meta, 'Binaries'):
                                for bin in entry.findall('Binary'):
                                    try:
                                        ref = bin.Value.get('Ref')
                                        if ref:
                                            binary = kdb.obj_root.Meta.Binaries.find('Binary[@ID="{0}"]'.format(ref))
                                            if binary:
                                                if record.attachments is None:
                                                    record.attachments = []
                                                atta = KeepassAttachment(binary)
                                                atta.name = bin.Key.text
                                                record.attachments.append(atta)
                                    except:
                                        pass


                            yield record

    def extension(self):
        return 'kdbx'

class KeepassExporter(BaseExporter):

    def do_export(self, filename, records):
        print('Choose password for your Keepass file')
        master_password = getpass.getpass(prompt='...' + 'Keepass Password'.rjust(20) + ': ', stream=None)

        sfs = []  # type: [SharedFolder]
        rs = []   # type: [Record]
        for x in records:
            if type(x) is Record:
                rs.append(x)
            elif type(x) is SharedFolder:
                sfs.append(x)

        template_file = os.path.join(os.path.dirname(__file__), 'template.kdbx')

        with libkeepass.open(template_file, password='111111') as kdb:
            root = kdb.obj_root.Root.Group
            for sf in sfs:
                comps = list(path_components(sf.path))
                node = root
                for i in range(len(comps)):
                    comp = comps[i]
                    sub_node = node.find('Group[Name=\'{0}\']'.format(comp))
                    if sub_node is None:
                        sub_node = objectify.Element('Group')
                        sub_node.UUID = base64.b64encode(os.urandom(16)).decode()
                        sub_node.Name = comp
                        node.append(sub_node)
                    if i == len(comps) - 1:  # store Keeper specific info
                        keeper = sub_node.find('Keeper')
                        if keeper is None:
                            keeper = objectify.Element('Keeper')
                            sub_node.append(keeper)
                        else:
                            keeper.clear()
                        keeper.IsShared = True
                        keeper.ManageUsers = sf.manage_users
                        keeper.ManageRecords = sf.manage_records
                        keeper.CanEdit = sf.can_edit
                        keeper.CanShare = sf.can_share
                        if sf.permissions:
                            for perm in sf.permissions:
                                permission = objectify.Element('Permission')
                                if perm.uid:
                                    permission.UUID = base64.b64encode(base64.urlsafe_b64decode(perm.uid + '==')).decode()
                                permission.Name = perm.name
                                permission.ManageUsers = perm.manage_users
                                permission.ManageRecords = perm.manage_records
                                keeper.append(permission)
                    node = sub_node

            for r in rs:
                try:
                    node = kdb.obj_root.Root.Group
                    fol = None
                    if r.folders:
                        fol = r.folders[0]
                        for is_shared in [True, False]:
                            path = fol.domain if is_shared else fol.path
                            if path:
                                comps = list(path_components(path))
                                for i in range(len(comps)):
                                    comp = comps[i]
                                    sub_node = node.find('Group[Name=\'{0}\']'.format(comp))
                                    if sub_node is None:
                                        sub_node = objectify.Element('Group')
                                        sub_node.UUID = base64.b64encode(os.urandom(16)).decode()
                                        sub_node.Name = comp
                                        node.append(sub_node)
                                    node = sub_node
                    entry = None
                    entries = node.findall('Entry')
                    if len(entries) > 0:
                        for en in entries:
                            title = ''
                            login = ''
                            password = ''
                            if hasattr(en, 'String'):
                                for sn in en.String:
                                    if hasattr(sn, 'Key') and hasattr(sn, 'Value'):
                                        key = sn.Key.text
                                        value = sn.Value.text
                                        if key == 'Title':
                                            title = value
                                        elif key == 'UserName':
                                            login = value
                                        elif key == 'Password':
                                            password = value
                            if title == r.title and login == r.login and password == r.password:
                                entry = node
                                break

                    strings = {
                        'URL': r.login_url,
                        'Notes': r.notes
                    }
                    if r.custom_fields:
                        for cf in r.custom_fields:
                            strings[cf] = r.custom_fields[cf]

                    if entry is None:
                        entry = objectify.Element('Entry')
                        if r.uid:
                            entry.UUID = base64.b64encode(base64.urlsafe_b64decode(r.uid + '==')).decode()
                        else:
                            entry.UUID = base64.b64encode(os.urandom(16)).decode()
                        node.append(entry)

                        strings['Title'] = r.title,
                        strings['UserName'] = r.login,
                        strings['Password'] = r.password,
                    else:
                        for str_node in entry.findall('String'):
                            if hasattr(str_node, 'Key'):
                                key = str_node.Key
                                if key in strings:
                                    value = strings[key]
                                    if value:
                                        str_node.Value = value
                                        strings.pop(key)
                    if not fol is None:
                        if fol.domain:
                            keeper = entry.find('Keeper')
                            if keeper is None:
                                keeper = objectify.Element('Keeper')
                                entry.append(keeper)
                            else:
                                keeper.clear()

                            keeper.CanEdit = fol.can_edit
                            keeper.CanShare = fol.can_share
                            for f in r.folders[1:]:
                                link = objectify.Element('Link')
                                keeper.append(link)
                                if f.domain:
                                    link.Domain = f.domain
                                    link.CanEdit = f.can_edit
                                    link.CanShare = f.can_share
                                if f.path:
                                    link.Path = f.Path

                    for key in strings:
                        value = strings[key]
                        if value:
                            s_node = objectify.Element('String')
                            s_node.Key = key
                            s_node.Value = value
                            entry.append(s_node)

                    if r.attachments:
                        for atta in r.attachments:
                            max_size = 1024 * 1024
                            if atta.size < max_size:
                                bins = None
                                bId = 0
                                if hasattr(kdb.obj_root.Meta, 'Binaries'):
                                    bins = kdb.obj_root.Meta.Binaries
                                    elems = bins.findall('Binary')
                                    bId = len(elems)
                                else:
                                    bins = objectify.Element('Binaries')
                                    kdb.obj_root.Meta.append(bins)
                                    bId = 0
                                with atta.open() as s:
                                    buffer = s.read(max_size)
                                    if len(buffer) >= 32:
                                        iv = buffer[:16]
                                        cipher = AES.new(atta.key, AES.MODE_CBC, iv)
                                        buffer = cipher.decrypt(buffer[16:])
                                        if len(buffer) > 0:
                                            out = io.BytesIO()
                                            with gzip.GzipFile(fileobj=out, mode='w') as gz:
                                                gz.write(buffer)
                                            bin = objectify.E.Binary(base64.b64encode(out.getvalue()).decode(), Compressed=str(True), ID=str(bId))
                                            bins.append(bin)

                                            bin = objectify.Element('Binary')
                                            bin.Key=atta.name
                                            bin.Value = objectify.Element('Value', Ref=str(bId))
                                            entry.append(bin)
                            else:
                                print('Warning: File \'{0}\' was skipped because it exceeds the 1MB Keepass filesize limit.'.format(atta.name))

                except Exception as e:
                    pass

            objectify.deannotate(root, xsi_nil=True)
            etree.cleanup_namespaces(root)

            kdb.clear_credentials()
            kdb.add_credentials(password=master_password)
            with open(filename, 'wb') as output:
                kdb.write_to(output)

    def has_shared_folders(self):
        return True

    def has_attachments(self):
        return True

    def extension(self):
        return 'kdbx'


class KeepassAttachment(Attachment):
    def __init__(self, binary):
        Attachment.__init__(self)
        self.binary = binary

    @contextmanager
    def open(self):
        data = base64.b64decode(self.binary.text)
        if self.binary.get('Compressed'):
            out = io.BytesIO()
            out.write(data)
            out.seek(0)
            with gzip.GzipFile(fileobj=out, mode='rb') as gz:
                data = gz.read()
        out = io.BytesIO()
        out.write(data)
        out.seek(0)
        yield out







