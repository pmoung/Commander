![](https://raw.githubusercontent.com/Keeper-Security/Commander/master/keepercommander/images/commander_logo_250x100.png)

----

Jump to:
* [Overview](#password-management-sdk-for-it-admins--developers)
* [Use Cases](#use-cases)
* [Installation](#installation---linux-and-mac)
* [Developer Setup](#developer-setup)
* [Command-line Usage](#command-line-usage)
* [Interactive Shell](#interactive-shell)
* [Keeper Command Reference](#keeper-command-reference)
* [Importing Data](#importing-records-into-keeper)
* [Advanced](#advanced-configuration-file)
* [Password Rotation](#targeted-password-rotations--plugins)
* [About Keeper](#about-our-security)
* [Enterprise Resources](#enterprise-resources)

### Password Management SDK for IT Admins & Developers

Keeper Security develops the world's most downloaded password manager and encrypted digital vault with millions of individual customers and thousands of enterprise customers worldwide.  Keeper is a zero-knowledge, native and cloud-based solution available on every mobile and desktop device platform. <a href="#about-keeper">Read more</a> about Keeper or visit the [Keeper Security](https://keepersecurity.com) website.

Keeper Commander is a command-line, interactive shell and SDK interface to [Keeper&reg; Password Manager](https://keepersecurity.com). Commander can be used to access and control your Keeper vault, rotate passwords and perform Keeper Enterprise administrative functions related to user onboarding and provisioning of vault records. Most features available in the Keeper Admin Console are available through Commander's interactive shell and SDK interface.

In addition to vault and administrative functionality, Commander can be used to perform targeted password rotations, integrate password management into your backend systems and eliminate the use of hardcoded passwords. Using our connector [plugins](https://github.com/Keeper-Security/Commander/tree/master/keepercommander/plugins), Commander can execute a password rotation directly to any common system or service account such as Unix systems, SQL Databases, Active Directory, Amazon AWS, local Administator accounts, network devices, etc...

Keeper Commander is an open source project written in Python, and it is under continuous development by the Keeper engineering team. As new features and capabilities are added to the Keeper platform, we add new commands and features to Commander.  If you need any assistance or require specific functionality, please contact ops@keepersecurity.com.

### Use Cases

* Access your Keeper vault through a command-line interface
* Perform bulk import and export of vault records 
* Manage records, folders and shared folders
* Customize integration into your backend systems
* Provision new Enterprise user accounts and shared folders
* Manage nodes, roles, teams and users
* Rotate passwords on service accounts or other targets
* Integrate Keeper into your existing backend systems
* Schedule and automate commands

### Installation - Linux and Mac

1. Get Python 3 from [python.org](https://www.python.org).
2. Install Keeper Commander with pip3:

```bash
$ pip3 install keepercommander
```

Important: Restart your terminal session after installation

### Installation - Windows 

1. Download and install [WinPython](https://winpython.github.io/)
2. From the install folder of WinPython, run the "WinPython Command Prompt" 
2. Install Keeper Commander with pip3:

```bash
$ pip3 install keepercommander
```

### Install Keepass library

If you plan to use the Keepass import or export features of Keeper Commander, please follow [these instructions](keepercommander/importer/keepass/README.md).

### Upgrading to Latest Code

```bash
$ pip3 install --upgrade keepercommander
```

Please do not upgrade a production system without validation in your test environment as commands and functionality is under rapid development.

### Developer Setup

This type of installation assumes you want to view/modify the Python source code (Compatible with Python 3.4+).

1. Clone/Download the Commander repository 
2. Install Python3 from python.org
3. Install virtualenv:
```bash
$ sudo pip3 install virtualenv
```
4. Create and activate the virtual environment for your keeper project:

```bash
$ cd /path/to/Commander
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
```

Keeper supports plugins for various 3rd party systems for password reset integration. Depending on the plugin, you will need to also install the modules required by that plugin. For example, our MySQL plugin requires the PyMySQL module.

See the [custom](https://github.com/Keeper-Security/Commander/tree/master/keepercommander/custom) folder for examples on creating your own custom scripts.

### Command-line Usage

Commander's command-line interface and interactive shell is a powerful and convenient way to access and control your Keeper vault and perform many administrative operations. To see all available commands, just type:

```
$ keeper

usage: keeper [--server SERVER] [--user USER] [--password PASSWORD]
              [--version] [--config CONFIG] [--debug]
              [command] [options [options ...]]

positional arguments:
  command               Command
  options               Options

optional arguments:
  --server SERVER, -ks SERVER
                        Keeper Host address.
  --user USER, -ku USER
                        Email address for the account.
  --password PASSWORD, -kp PASSWORD
                        Master password for the account.
  --version             Display version
  --config CONFIG       Config file to use
  --debug               Turn on debug mode
```

### Interactive Shell
To run a series of commands and stay logged in, you will enjoy using Commander's interactive shell.

```
$ keeper shell

  _  __
 | |/ /___ ___ _ __  ___ _ _
 | ' </ -_) -_) '_ \/ -_) '_|
 |_|\_\___\___| .__/\___|_|
              |_|

 password manager & digital vault

Logging in...
Syncing...
Decrypted [400] Records

My Vault>
```

Type ```h``` to display all commands and help information.

### Keeper Command Reference

Whether using the interactive shell, CLI or JSON config file, Keeper supports the following features specified by ```command```.  Each command supports additional parameters and options.  To get help on a particular command, use the ```-h``` flag.

**Basic Vault Commands**

* ```login``` Login to Keeper

* ```whoami``` Information about logged in user

* ```logout``` Logout from Keeper

* ```shell``` Use Keeper interactive shell

* ```sync-down``` or ```d``` Download, sync and decrypt vault

* ```list``` or ```l``` List all records or search with a regular expression.

* ```search``` or ```s``` Search all records with a regular expression.

* ```ls``` List folder contents (try ```ls -l``` as well)

* ```tree``` Display entire folder structure as a tree

* ```cd``` Change current folder

* ```get``` Retrieve and display specified Keeper Record/Folder/Team in printable or JSON format.

* ```download-attachment``` Download all file attachments in specified record

* ```upload-attachment``` Upload file attachments to the specified record

* ```list-sf``` or ```lsf``` Display all shared folders

* ```create-user``` Create Keeper vault account.
Note: If executed by an admin, the user will be provisioned to the Enterprise license.

* ```list-team``` or ```lt``` Display all teams

**Record Management Commands**

* ```add``` Add a record to the vault

* ```rm``` Remove record

* ```append-notes``` or ```an``` Append notes to existing record

**Folder Management Commands**

* ```mkdir``` Create folder

* ```rmdir``` Remove folder and its content

* ```mv``` Move record or folder

* ```ln``` Create a link between record or folder

**Password Rotation Commands**

* ```rotate``` or ```r``` Rotate password in record

**Import and Export Commands**

* ```import``` Import data from local file to Keeper (JSON, CSV, Keepass)

* ```export``` Export data from Keeper to local file or stdout (JSON, CSV, Keepass)

**Folder and Record Sharing Commands**

* ```share-record``` or ```sr``` Grant or revoke record's user access

* ```share-folder``` or ```sf``` Grant or revoke shared folder's user access or record permission

**Enterprise Console Management Commands**

* ```enterprise-info``` or ```ei```   Display enterprise information

    - ```--nodes``` Show node structure in a tree form
    - ```--users``` Show users in a list view
    - ```--roles``` Show all roles in a list view
    - ```--teams``` Show all teams in a list view
    - ```--node``` Specify a single node to limit view
    - ```--v``` Verbose mode 

* ```enterprise-user``` or ```eu```   Enterprise user management

    - ```--expire``` Expire the master password for the user
    - ```--lock``` Unlock the user account
    - ```--unlock``` Lock the user account 
    - ```--add``` Invite a new user to join the enterprise
    - ```--delete``` Delete the user and all stored vault records (use with caution)
    - ```--name``` Rename a user's display name
    - ```--node``` Move user into a node 
    - ```--add-role``` Add a user to a role
    - ```--remove-role``` Remove a user from a role
    - ```--add-team``` Add a user to a team
    - ```--remove-team``` Remove a user from a team

* ```enterprise-role``` or ```er```   Enterprise role management

    - ```--add-user``` Add a user to a specified role
    - ```--remove-user``` Remove a user from a specified role

* ```enterprise-team``` or ```et```   Enterprise team management

    - ```--add``` Create a new team in the root node
    - ```--node``` Move a team into the specified node
    - ```--add-user``` Add a user to a team
    - ```--remove-user``` Remove a user from a team
    - ```--name``` Change the Team name
    - ```--delete``` Delete a team
    - ```--restrict-edit``` Restrict record edit on the team
    - ```--restrict-share``` Restrict record re-sharing on the team
    - ```--restrict-view``` Restrict record viewing on the team 

* ```audit-log``` Export audit and event logs
    - ```--target=splunk``` Export events to Splunk HTTP Event Collector [See Details](#event-logging)

### Importing Records into Keeper

To import records into your vault, use the ```import``` command.  Supported import formats:

* JSON
* CSV 
* Keepass

JSON import files can contain records, folders, subfolders, shared folders, default folder permissions  and user/team permissions.
CSV import files contain records, folders, subfolders, shared folders and default shared folder permissions.
Keepass files will transfer records, file attachments, folders and subfolders. Option exists to make all folders as shared folders. File attachments are supported in both import and export with Keepass however they are limited to 1MB for each file based on keepass' structure.

**JSON Record Import**

Below is a JSON import file with 2 records. The first record is added to a folder called "My Servers". The second record is added to "My Servers" and also added to a shared folder called "Shared Servers". 

```bash
[{
    "title":"Dev Server",
    "folders": [
      {
        "folder": "My Servers"
      }
    ],
    "login": "root",
    "password": "lk4j139sk4j",
    "login_url": "https://myserver.com",
    "notes": "These are some notes.",
    "custom_fields": {"Security Group":"Private"}
},
{
    "title":"Prod Server",
    "folders": [
      {
        "folder": "My Servers"
      },
      {
       "shared_folder": "Shared Servers",
       "can_edit": true,
       "can_share": true
      }
    ],
    "login": "root",
    "password": "kj424094fsdjhfs4jf7h",
    "login_url": "https://myprodserver.com",
    "notes": "These are some notes.",
    "custom_fields": {"Security Group":"Public","IP Address":"12.45.67.8"}
}]
```

The format must be strict JSON or it will fail parsing. To import this file:

```bash
$ keeper import --format=json import.json
```

A more complex example that supports shared folders, folder permissions, user permissions and team permissions is located in the sample_data/ folder. To import the sample JSON file into your vault, type this command:

```bash
$ keeper import --format=json sample_data/import.json.txt
```

The sample file contains "permissions" objects that contain email address or team names.  If the email or team name exists in your Keeper enterprise account, they will be added to the shared folder, otherwise the information is ignored. 


**CSV Record Import**

Keeper supports .csv text file import using comma delimited fields.

File Format:
Folder,Title,Login,Password,Website Address,Notes,Shared Folder,Custom Fields

* To specify subfolders, use backslash "\\" between folder names
* To set shared folder permission on the record, use the #edit or #reshare tags as seen below 
* Enclose fields in quotes for multi-line or special characters
* Ensure files are UTF-8 encoded for support of international or double-byte characters 

Below is an example csv file that showcases several import features including personal folders, shared folders, subfolders, special characters and multi-line fields.

```
Business,Twitter,marketing@company.com,"a bad password",https://twitter.com,Some interesting notes!,,API Key,"131939-AAAEKJLE-491231$##%!",Date Created,2018-04-02
Subfolder1,Twitter,craig@gmail.com,xwVnk0hfJmd2M$2l4shGF#p,https://twitter.com,,Social Media\Customer1#edit#reshare
Subfolder2,Facebook,craig@gmail.com,TycWyxodkQw4IrX9VFxj8F8,https://facebook.com,,Social Media\Customer2#edit#reshare
,Google Dev Account,mydevaccount@gmail.com,"8123,9fKJRefa$!@#4912fkk!--3",https://accounts.google.com,"Google Cloud ID 448812771239122
Account Number 449128
This is multi-line",Shared Accounts#edit#reshare,2FA Phone Number,+19165551212
```

To import this file:
```bash
$ keeper import --format=csv test.csv
4 records imported successfully
```

The resulting vault will look like [this image](https://raw.githubusercontent.com/Keeper-Security/Commander/master/keepercommander/images/csv_import.png)

**Keepass Import**

Keeper supports importing the record and folder structure directly from an encrypted Keepass file. File attachments are also supported (up to 1MB per file).  Make sure to first follow [these instructions](keepercommander/importer/keepass/README.md) to install the necessary keepass modules.

```bash
$ keeper import --format=keepass test.kdbx
```

You can optionally make all top level folders as shared folder object with default permissions.

```bash
$ keeper import --format=keepass --shared --permissions=URES test.kdbx
```

For more options, see the help screen:
```bash
$ keeper import -h
```

### Event Logging

**Splunk HTTP Event Collector Push**

Keeper can post event logs directly to your on-prem or cloud Splunk instance. Please follow the below steps:

* Login to Splunk enterprise 
* Go to Settings -> Data Inputs -> HTTP Event Collector
* Click on "New Token" then type in a name, select an index and finish.
* At the last step, copy the "Token Value" and save it for the next step.
* Login to Keeper Commander shell

```bash
$ keeper shell
```

Next set up the Splunk integration with Commander. Commander will create a record in your vault that stores the provided token and Splunk HTTP Event Collector. This will be used to also track the last event captured so that subsequent execution will pick up where it left off.  Note that the default port for HEC is 8088.

```
$ keeper audit-log --format=splunk

Do you want to create a Keeper record to store audit log settings? [y/n]: y
Choose the title for audit log record [Default: Audit Log: Splunk]: <enter> 

Enter HTTP Event Collector (HEC) endpoint in format [host:port].
Example: splunk.company.com:8088
...           Splunk HEC endpoint: 192.168.51.41:8088
Testing 'https://192.168.51.41:8088/services/collector' ...Found.
...                  Splunk Token: e2449233-4hfe-4449-912c-4923kjf599de
```
You can find the record UID of the Splunk record for subsequent audit log exports:

```
My Vault> search splunk

  #  Record UID              Title              Login    URL
---  ----------------------  -----------------  -------  -----
  1  schQd2fOWwNchuSsDEXfEg  Audit Log: Splunk
```

Each subsequent audit log export can be performed with this command:

```bash
$ keeper audit-log --format=splunk --record=<your record UID>
```
or from the shell:

```bash
My Vault> audit-log --target=splunk --record=<your record UID>
```

### Advanced Configuration File

By default, Keeper will look for a file called ```config.json``` in the current working directory and it will use this file for reading and writing session parameters. For example, if you login with two factor authentication, the device token is written to this file. The configuration file loaded can also be customized through the ```config``` parameter. The config file can also be used to automate and schedule commands.

Below is a fully loaded config file. 

```bash
{
    "server":"https://keepersecurity.com/api/v2/",
    "user":"craig@company.com",
    "password":"your_password_here",
    "mfa_token":"filled_in_by_commander",
    "mfa_type":"device_token",
    "debug":false,
    "plugins":[],
    "commands":[],
    "timedelay":0,
}
```

Notes:

* ```server``` can be left blank and defaults to the United States data center. If your account is in the European data center then change the server domain from ```.com``` to ```.eu```.

* ```mfa_token``` will be set by Commander automatically after successful two-factor authentication.

* ```debug``` parameter can be set to ```true``` or ```false``` to enable detailed crypto and network logging.

* ```plugins``` parameter determines which password rotation plugin will be loaded. [Learn more](https://github.com/Keeper-Security/Commander/tree/master/keepercommander/plugins) about password rotation plugins for Commander.

* ```commands``` parameter is a comma-separated list of Keeper commands to run.  For example:
```"commands":["sync-down", "upload-attachment --file=\"/Users/craig/something.zip\" \"3PMqasi9hohmyLWJkgxCWg\"","share-record --email=\"somebody@gmail.com\" --write \"3PMqasi9hohmyLWJkgxCWg\""]``` will sync your vault, upload a file and then share the record with another user.

* ```timedelay``` parameter can be used to automatically run the specified commands every X seconds. For example:
```"timedelay":600``` will run the commands every 10 minutes.

* ```challenge``` parameter is the challenge phrase when using a Yubikey device to authenticate. 

To configure Yubikey device authentication, follow the [setup instructions](https://github.com/Keeper-Security/Commander/tree/master/keepercommander/yubikey).  In this mode, you will use a challenge phrase to authenticate instead of a master password.

* ```device_token_expiration``` can be set to ```true``` to expire 2FA device tokens after 30 days. By default, the 2FA device token will never expire. To manually force a 2FA token to expire, login to your Keeper vault (on desktop app, Web Vault or mobile app) and disable then re-enable your Two-Factor Authentication settings. This will invalidate all previously saved tokens across all devices.

### Batch Mode 

You can batch execute a series of commands and pipe the file to STDIN of Commander.  For example, create a text file called ```test.cmd``` with the following lines:

```
add --login=blah@gmail.com --pass=somemasterpass --url=https://google.com --force "Some Record Title"
upload-attachment --file="/path/to/some/file.txt" "Some Record Title"
share-record --email="user@company.com" --write "Some Record Title"
```

To run this file in a batch mode:
```bash
cat test.cmd | keeper --batch-mode shell
```

### Targeted Password Rotations & Plugins 

Keeper Commander can communicate to internal and external systems for the purpose of rotating a password and synchronizing the change to your Keeper Vault.  We accomplish this by associating a Keeper record with a physical system through the use of custom fields.  For example, you might want to rotate your MySQL password, Active Directory password and local Administrator password automatically.  To support a plugin, simply add a set of **custom field** values to the Keeper record. The custom field values tell Commander which plugin to use, and what system to communicate with when rotating the password.  To modify your Keeper record to include custom fields, login to Keeper on the [Web Vault](https://keepersecurity.com/vault) or [Keeper Desktop](https://keepersecurity.com/download.html) app.  

Example custom fields for MySQL password rotation:

```
Name: cmdr:plugin
Value: mysql

Name: cmdr:host
Value: 192.168.1.55

Name: cmdr:db
Value: testing
```

When a plugin is specified in a record, Commander will search in the plugins/ folder to load the module based on the name provided (e.g. mysql.py) then it will use the values of the Keeper record to connect, rotate the password and save the resulting data.

Check out the [plugins folder](https://github.com/Keeper-Security/Commander/tree/master/keepercommander/plugins) for all of the available plugins.  Keeper's team adds new plugins on an ongoing basis. If you need a particular plugin created, send us an email to ops@keepersecurity.com.

### Deep linking to records (Web Vault Hyperlink)

The Record UID that is displayed on password record output can be used for deep linking directly into the Keeper Web Vault only for privileged users. This Vault link can be stored and sent over unsecure channels because it only provides a reference to the record within your vault -- it does not provide access to the actual record content.  To access the content, you must still authenticate into the vault and decrypt the data.  The link is in the format `https://keepersecurity.com/vault#detail/XXXXXX` and you simply replace XXXXXX with the Record UID. Providing this link to another user does NOT initiate sharing.  To share a vault record, you must authenticate to your vault, open the record and click the "Share" feature.

### About Our Security

Keeper is a zero-knowledge platform.  This means that the server does not have access to your Keeper Master Password or the crypto keys used to encrypt and decrypt your data.  The cryptography is performed on the *client device* (e.g. iPhone, Android, Desktop, Commander).

When you create a Keeper account from our [web app](https://keepersecurity.com/vault) or [mobile/desktop app](https://keepersecurity.com/download), you are asked to create a Master Password and a security question.  The Keeper app creates your crypto keys, RSA keys and encryption parameters (iv, salt, iterations).  Your RSA private key is encrypted with your data key, and your data key is encrypted with your Master Password.  The encrypted version of your data key is stored in Keeper's Cloud Security Vault and provided to you after successful device authentication.

When you login to Keeper on any device (or on Commander), your Master Password is used to derive a 256-bit PBKDF2 key.  This key is used to decrypt your data key.  The data key is used to decrypt individual record keys, shared folder keys and team keys.  Record keys, shared folder keys and team keys are then used to decrypt each individual record in the vault.

When storing information to your vault, Keeper stores and synchronizes the encrypted data.

We strongly recommend that you enable Two-Factor Authentication on your Keeper account via the [web app](https://keepersecurity.com/vault) settings screen.  This can also be enforced at the Keeper Enterprise level. When logging into Commander with Two-Factor Authentication turned on, you will be asked for a one-time passcode.  After successful authentication, Commander receives a device token that can be used for subsequent requests without another two-factor auth request.

For more details on Keeper's security architecture, certifications and implementation details, visit the [Security Disclosure](https://keepersecurity.com/security.html) page of our website. If you have any specific questions related to security, email security@keepersecurity.com.

### Vulnerability Disclosure Program

Keeper has partnered with Bugcrowd to manage our vulnerability disclosure program. Please submit reports through https://bugcrowd.com/keepersecurity or send an email to security@keepersecurity.com.

### About Keeper

Keeper is the world's most downloaded password keeper and secure digital vault for protecting and managing your passwords and other secret information.  Millions of people and companies use Keeper to protect their most sensitive and private information.

Keeper's Features &amp; Benefits

* Manages all your passwords and secret info
* Protects you against hackers
* Encrypts everything in your vault 
* High-strength password generator
* Login to websites with one click
* Store private files, photos and videos
* Take private photos inside vault 
* Share records with other Keeper users
* Access on all your devices and computers
* Keeper DNA&trade; multi-factor authentication
* Login with Fingerprint or Touch ID
* Auto logout timer for theft prevention
* Unlimited backups
* Self-destruct protection
* Customizable fields
* Background themes
* Integrated Apple Watch App
* Instant syncing between devices
* AES-256 encryption
* Zero-Knowledge security architecture
* TRUSTe and SOC-2 Certified
* GDPR Compliant 

### Keeper Website
[https://keepersecurity.com](https://keepersecurity.com)

### Pricing
Keeper is free for local password management on your device.  Premium subscriptions provides cloud-based capabilites including multi-device sync, shared folders, teams, SSO integration and encrypted file storage. More info about our enterprise pricing plans can be found [here](https://keepersecurity.com/pricing.html?tab=business).

### Mobile Apps

[iOS - iPhone, iPad, iPod](https://itunes.apple.com/us/app/keeper-password-manager-digital/id287170072?mt=8)

[Android - Google Play](https://play.google.com/store/apps/details?id=com.callpod.android_apps.keeper&hl=en)

[Kindle and Amazon App Store](http://amzn.com/B00NUK3F6S)

[Windows Phone](https://www.microsoft.com/en-us/store/p/keeper-password-manager/9wzdncrdmpt6)

### Cross-Platform Desktop App

[Windows PC, 32-bit](https://keepersecurity.com/desktop_electron/Win32/KeeperSetup32.zip)

[Windows PC, 64-bit](https://keepersecurity.com/desktop_electron/Win64/KeeperSetup64.zip)

[Windows PC, 32-bit MSI Installer](https://keepersecurity.com/desktop_electron/Win32/KeeperSetup32.msi)

[Mac](https://keepersecurity.com/desktop_electron/Darwin/KeeperSetup.dmg)

[Linux](https://keepersecurity.com/download.html)

### Microsoft Store (Windows 10, Surface) Platform

[Microsoft Store Version - Windows 10](https://www.microsoft.com/en-us/store/p/keeper-password-manager/9wzdncrdmpt6)

### Web Vault and Browser Extensions

[Web App - Online Vault](https://keepersecurity.com/vault)

[KeeperFill for Chrome](https://chrome.google.com/webstore/detail/keeper-browser-extension/bfogiafebfohielmmehodmfbbebbbpei)

[KeeperFill for Firefox](https://addons.mozilla.org/en-US/firefox/addon/keeper-password-manager-digita/)

[KeeperFill for Safari](https://safari-extensions.apple.com/details/?id=com.keepersecurity.safari.KeeperExtension-234QNB7GCA)

[KeeperFill for Edge](https://www.microsoft.com/en-us/store/p/keeper-password-manager-digital-vault/9n0mnnslfz1t)

[Enterprise Admin Console](https://keepersecurity.com/console)

### Sales & Support 

[Enterprise Guide](https://keepersecurity.com/user-guides/enterprise-guide.html)

[White Papers & Data Sheets](https://keepersecurity.com/enterprise-resources.html)

[Contact Sales or Support](https://keepersecurity.com/contact.html)

We're here to help.  If you need help integrating Keeper into your environment, contact us at ops@keepersecurity.com.
