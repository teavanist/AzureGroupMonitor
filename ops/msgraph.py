import ssl
from azure.identity import ClientSecretCredential
from msgraph.core import GraphClient
from datetime import datetime, timezone, timedelta
from common import logger 
# all database related functions 
from db.dbops import insert_action_to_DB
from db.dbops import insert_target_to_DB
from db.dbops import insert_modification_to_DB
from db.dbops import insert_initiator_to_DB
from db.dbops import insert_interpretation_to_DB
from db.dbops import check_ID_exists



from ops.interpreter import *

def getGroupLogs(config):
    """"Returns all logs related to groups from the tenant specified in the configuration file 
    Args:
        config (dictionary): Holds the configuration used to connect to Azure. The dictionary must contain the following:
            authority
            tenant_id
            client_id
            client_secret
            GRAPH_URL: graph API default scope 

    """

    clientcredential = ClientSecretCredential(tenant_id=config["tenant_id"], \
        client_id=config["client_id"], 
        client_secret=config["client_secret"], 
        authority=config["authority"])

    app_client = GraphClient(credential=clientcredential, scopes=[config["GRAPH_URL"]])
    

    targetdate = str(datetime.now(timezone.utc) - timedelta(hours=24))
    datetemp = datetime.fromisoformat(targetdate).replace(tzinfo=timezone.utc)
    datestr= datetemp.strftime("%Y-%m-%dT%H:%M:%SZ")

    logger.info('Downloading logs since: ' + str(datestr))


    msgraphquery = "/auditLogs/directoryAudits?$filter=category eq 'GroupManagement' and activityDateTime ge " + str(datestr)

    group_logs = app_client.get(msgraphquery)
    return group_logs.json() 


def processGroupLogs(data):
    #TODO: how to handle a scenario where the update fails midway
    #TODO: We need a JSON checker to see if the file follows our predefined structure 
    #TODO: validate if the JSON file was empty
    #TODO: What happens if there is an app + user, an app only or neither app nor user but something else?
    #TODO: is the action already logged 
    #TODO: code for condition when "code": "BadRequest" 

    from log.action import Action 
    from log.initiator import InitiatorClass
    from log.targetresource import TargetResource
    from log.modification import Modification

    # checks if there is any content in the log
    if len(data["value"]) == 0:
        logger.info('Log is empty')
        return 0

    
    for logentry in data["value"]:

        action = Action()
        action.extract_action(logentry)

        # check if the action is already saved in the database 
        # if it already exists we move to the next item in the log 

        if check_ID_exists(action.source_id):
            logger.info("The log with ID " + action.source_id + " already exists. Skipping to next item")
            continue 
        

        #2 Enter data extracted above to the database -- DONE

        logger.info("Inserting extracted action to database")
        top_parent = insert_action_to_DB(action)
        action.id = top_parent

        #3 Find initiator

        initiators = logentry ["initiatedBy"]
        if initiators:
            if initiators["app"] is None:
                initiator = initiators["user"]
            else: 
                #TODO: Raise an error here 
                pass
            
        inituser = InitiatorClass()
        inituser.extract_initiator(initiator,action.source_id,top_parent)
        inituserid = insert_initiator_to_DB(inituser)


        #4 Find target resources (will there be target resources without any )
        targets = logentry["targetResources"]

        #TODO: validate if the targets are empty
        
        #loop through the targets and insert each one to the database 
        for target in targets:
            tr = TargetResource()
            tr.extract_target(target,action.source_id,top_parent)
            targetid = insert_target_to_DB(tr)

            if tr.modified_items_count > 0:
                modificatons = target["modifiedProperties"]

                for modification in modificatons:
                    mo = Modification()
                    mo.extract_modifications(modification,tr.source_id, top_parent)
                    
                    pk = insert_modification_to_DB(mo)

        if action.result == "success":
            logger.info("Starting Interpretation: action.id({})".format(str(action.id)))
            logger.info("Starting Interpretation: action.category({})".format(str(action.category)))
            logger.info("Starting Interpretation: action.activityDisplayName({})".format(str(action.activityDisplayName)))
            interpretedresult = startInterpretation(action.id, action.category, action.activityDisplayName)
            #add the result to the database  
            interpretationpk = insert_interpretation_to_DB(action.id, interpretedresult)
            logger.info("Added record to Interpretation table: {}".format(str(interpretationpk)))


        
