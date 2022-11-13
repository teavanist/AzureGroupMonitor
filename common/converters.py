import yaml
import json
import os 

def writeToJSON(filename, content):
    with open(filename, 'w') as f:
        json.dump(content, f)


def readFromJSON(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data 


def getInterval(path_to_yaml_file):
    with open(path_to_yaml_file, 'r') as file:
        configuration = yaml.safe_load(file)

    config = {
    "interval_minutes" : configuration['interval_minutes']
    }

    return config



def getAzureConfig(path_to_yaml_file):
    with open(path_to_yaml_file, 'r') as file:
        configuration = yaml.safe_load(file)

    azure_config = {
    "tenant_id" : configuration["tenant_id"],
    "client_id" : configuration["client_id"],
    "client_secret" : configuration["client_secret"],
    
    "authority" : configuration['authority'],
    "GRAPH_URL" : configuration['graphurl']
    }

    return azure_config

def getLogFileSavePath(path_to_yaml_file):
    with open(path_to_yaml_file, 'r') as file:
        configuration = yaml.safe_load(file)

    return configuration['logfile_savelocation']


def getMailConfig(path_to_yaml_file):
    with open(path_to_yaml_file, 'r') as file:
        configuration = yaml.safe_load(file)

    mail_config = {
        "MAIL_SERVER" : configuration['mail_server'],
        "MAIL_PORT" : configuration['mail_port'],
        "MAIL_USE_TLS" : configuration['mail_use_tls'],
        "MAIL_USE_SSL" : configuration['mail_use_ssl'],
        "MAIL_DEBUG" : configuration['mail_debug'],
        "MAIL_USERNAME" : configuration["mail_username"],
        "MAIL_PASSWORD" : configuration["mail_password"],
        "MAIL_DEFAULT_SENDER" : configuration['mail_default_sender'],
        "MAIL_MAX_EMAILS" : configuration['mail_max_emails'],
        "MAIL_SUPPRESS_SEND" : configuration['mail_suppress_send'],
        "MAIL_ASCII_ATTACHMENTS" : configuration['mail_ascii_attachments'],
        "MAIL_SENDER": configuration['mail_sender'],
        "MAIL_RECIPIENT": configuration['mail_recipient'],
    }
    return mail_config
            
def getSecretKey(path_to_yaml_file):
    with open(path_to_yaml_file, 'r') as file:
        configuration = yaml.safe_load(file)

    return configuration['SECRET_KEY']

def convert_to_pandas(data, ):
    """"
    data in a dictionary format
    """
    import json
    import pandas as pd

    # read file
    with open('users_response.json', 'r') as myfile:
        data=myfile.read()



    df=pd.DataFrame(columns=[\
        'source_log_ID',
        'source',
        'activityDisplayName',
        'result',
        'activityDateTime',
        'Performed By',
        'ipAddress',
        'operationType',
        'p2_displayName',
        'p2_oldValue',
        'p2_newValue',
        ])

    # parse file
    obj = json.loads(data)
    number_of_items = len(obj['value'])

    audit_content = obj['value'][0]

    affected_resources_count = len(audit_content['targetResources'])
    affected_resources = audit_content['targetResources'][0]['modifiedProperties']


    new_row = {
    'source_log_ID':audit_content['id'],
    'source':'Azure',
    'activityDisplayName':audit_content['activityDisplayName'],
    'result':audit_content['result'],
    'activityDateTime':audit_content['activityDateTime'],
    'Performed By':audit_content['initiatedBy']['user']['userPrincipalName'],
    'ipAddress':audit_content['initiatedBy']['user']['ipAddress'],
    'operationType':audit_content['operationType'],
    'p2_displayName':affected_resources[1]['displayName'],
    'p2_oldValue':affected_resources[1]['oldValue'],
    'p2_newValue':affected_resources[1]['newValue'],
    }

    df = df.append(new_row, ignore_index=True)


