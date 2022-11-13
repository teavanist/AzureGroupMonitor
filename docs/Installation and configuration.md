
# Installation and configuration guide 
This installation guide covers all steps from installation to configuration to get Azure Group Monitor started. 

## STEP 1: Clone this repo 

```
git clone https://github.com/teavanist/AzureGroupMonitor.git 
```

## STEP 2: Installing pre-requisites 

```
cd directory/
python3 -m venv myappenv
```
Once you are in the virtual environment, install the pre-requisites: 
```
pip3 install -r requirements.txt
```
## STEP 3: Setting up the database

### 1. Install postgresql database 

The official guide from Postgresql on how to install the database: 

[https://www.postgresql.org/download/](https://www.postgresql.org/download/)

I use Ubuntu servers and I found the following article from Digital Ocean to be better written than the official one:  

[https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04)


### 2. Setup the postgresql database 

#### Create user (someuser)

```
    sudo su postgres
    createuser --interactive -P someuser
    Enter password for new role:
    Enter it again:
    Shall the new role be a superuser? (y/n) n
    Shall the new role be allowed to create databases? (y/n) y
    Shall the new role be allowed to create more new roles? (y/n) n
```

#### Create database (booksdb)
```
    sudo su postgres
    createdb -O someuser booksdb
    exit 
```

#### import the dump 
There is a dump file provided to create the database schema and this is present in the root folder. Use this file in the following command:

```
sudo su postgres
psql -U someuser -h 127.0.0.1 booksdb < dump.sql
```

## STEP 4: Find your Tenant ID
You will need to know your Tenant ID as it is needed later in the configuration. 

To view your tenant, follow the instructions in this [link](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-how-to-find-tenant)

## STEP 5: Creating an app with the appropriate permissions in Azure 
You will need to register an app in Azure with the appropriate permissions for this to work. 

1. Follow the steps in this [Microsoft documentation](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app) and register an app. During the process, make sure that you select *Accounts in this organizational directory only* option. 

2. Create a [client secret](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-a-client-secret).  

3. Provide the following the [API permissions](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-configure-app-access-web-apis) to the app that you created. Ensure that you grant admin consent for these permissions. 
- AuditLog.Read.All
- AuditLog.Read.All
- Directory.Read.All
- Group.Read.All
- GroupMember.Read.All
- User.Read.All

## STEP 6: Configuring the YAML file
Configure the *config.yaml* file in the *config* directory using the following examples as a guide:
```
authority: "https://login.microsoftonline.com"
graphurl: "https://graph.microsoft.com/.default"
DB_HOST: "localhost"
DB_NAME: "yourdbname"
DB_USER: "someuser"
DB_PASS: "password"
SECRET_KEY: "your_random_secret_key"
tenant_id: "u2zb9z7i-9pf4-4doo-2k2k-dabolvm8080q"
client_id: "s0meran4-0m70-j007-mi60-jamesvm7070q"
client_secret: "xUjzs~2ZLH1597MQ65C31S9YQMU577EAO2-OjGrC"
mail_username: "mailusername"
mail_password: "mailpassword"
logfile_savelocation: "/path/to/save/azurelogs/"
interval_minutes: 60
mail_server: "smtp.somemailserver.com"
mail_port: 2525
mail_use_tls: True
mail_use_ssl: False
mail_default_sender: ""
mail_max_emails: None
mail_ascii_attachments: False
mail_sender: "AzuregroupmonitorApp@somecompanyname.com"
mail_recipient: "azureadmins@somecompanyname.com"
```

Notes: 

- Use a good random string generator for *SECRET_KEY* 
- *interval_minutes* refers to how frequently you wish to synch with Azure. 
- *logfile_savelocation* refers a directory where the app will download and save the log files. I plan to remove this functionality in the future. 
