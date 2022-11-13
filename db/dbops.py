from db import get_db
import psycopg2.extras

from common import logger 

def insert_affectedparties_to_DB(actionid,affectedpartieslist):

    logger.info("Beginning DB entry for affectedpartieslist into objects-action-mapping table")
    conn = get_db()
    cur = conn.cursor()

    for objectid in affectedpartieslist: 
        SQL = "INSERT INTO objects_actions_mapping (top_parent_id,sourceobjectid) values (%s,%s) RETURNING id" 

        input_data = (actionid, objectid)

        cur.execute(SQL, input_data)
        last_id = cur.fetchone()[0]
        conn.commit()
        logger.info("Entered in objects-action-mapping table record#: " + str(last_id))

    
    cur.close()
    conn.close()

    return last_id

def insert_interpretation_to_DB(actionid,interpretationtext):

    logger.info("Beginning DB entry for interpretation")
    conn = get_db()
    cur = conn.cursor()

    SQL = "INSERT INTO interpretations (top_parent_id,interpretation) values (%s,%s) RETURNING id" 

    input_data = (actionid, interpretationtext)

    cur.execute(SQL, input_data)
    last_id = cur.fetchone()[0]
    conn.commit()

    logger.info("Entered in interpretations table record#: " + str(last_id))
    
    cur.close()
    conn.close()

    return last_id

def insert_action_to_DB(action):

    logger.info("Beginning DB entry for actions table")
    conn = get_db()
    cur = conn.cursor()

    SQL = "INSERT INTO actions (source_system,\
        source_id,category,correlationid,result,resultreason,activitydisplayname,\
        activitydatetime,loggedbyservice,operationtype\
        ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id" 

    input_data = (action.source_system,action.source_id, action.category, action.correlationId,action.result,action.resultReason, action.activityDisplayName, action.activityDateTime, action.loggedByService,action.operationType)

    cur.execute(SQL, input_data)
    last_id = cur.fetchone()[0]
    conn.commit()

    logger.info("Entered in actions table record#: " + str(last_id))

    cur.close()
    conn.close()

    return last_id

def insert_initiator_to_DB(initiator):

    logger.info("Beginning DB entry for Initiator")
    conn = get_db()
    cur = conn.cursor()

    SQL = "INSERT INTO initiators (\
        top_parent_id, \
        parent_action_id,\
        source_id,\
        displayName,\
        userPrincipalName,\
        ipAddress,\
        userType,\
        homeTenantId,\
        homeTenantName\
        ) \
        values (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id" 

    input_data = (
    initiator.top_parent_id,
    initiator.parent_action_id,
    initiator.source_id,
    initiator.displayName,
    initiator.userPrincipalName,
    initiator.ipAddress,
    initiator.userType,
    initiator.homeTenantId,
    initiator.homeTenantName
    )

    cur.execute(SQL, input_data)
    last_id = cur.fetchone()[0]
    conn.commit()

    logger.info("Entered in initiators table record#: " + str(last_id))
    
    cur.close()
    conn.close()

    return last_id

def insert_target_to_DB(target):

    logger.info("Beginning DB entry for targets")
    conn = get_db()
    cur = conn.cursor()

    SQL = "INSERT INTO targets (\
        top_parent_id, \
        parent_action_id,\
        source_id,\
        displayName,\
        type,\
        userPrincipalName,\
        groupType,\
        modified_items_count\
        ) \
        values (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id" 

    input_data = (
    target.top_parent_id,
    target.parent_action_id,
    target.source_id,
    target.displayName,
    target.type,
    target.userPrincipalName,
    target.groupType,
    target.modified_items_count)

    cur.execute(SQL, input_data)
    last_id = cur.fetchone()[0]
    conn.commit()

    logger.info("Entered in targets table record#: " + str(last_id))
    
    cur.close()
    conn.close()

    return last_id

def insert_modification_to_DB(modification):

    logger.info("Beginning DB entry for modifications")
    conn = get_db()
    cur = conn.cursor()

    SQL = "INSERT INTO modifications (\
        top_parent_id, \
        parent_target_id,\
        displayName,\
        oldValue,\
        newValue\
        ) \
        values (%s,%s,%s,%s,%s) RETURNING id" 

    input_data = (
        modification.top_parent_id,
        modification.parent_target_id,
        modification.displayName,
        modification.oldValue,
        modification.newValue
    )

    cur.execute(SQL, input_data)
    last_id = cur.fetchone()[0]
    conn.commit()

    logger.info("Entered into modifications table record#: " + str(last_id))
    
    cur.close()
    conn.close()

    return last_id

def get_actions_overview():
        
    conn = get_db()
    cur = conn.cursor()

    SQL = "select * from view_for_actionoverview" 
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)    
    cur.execute(SQL)
    actionoverview = cur.fetchall()
    cur.close()
    conn.close()

    return actionoverview

def check_ID_exists(id):

    logger.info("Checking in DB if id exists: " + str(id))
    #We assume the ID does not exist and hence the possible return value will be False 
    rowcount = False

    conn = get_db()
    cur = conn.cursor()

    SQL = "select count(*) from actions where source_id  = %s"

    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)    
    input_data = (id, )

    cur.execute(SQL, input_data)

    result = cur.fetchone()
    if  result['count'] == 0:
        rowcount = False
    else: 
        rowcount = True

    cur.close()
    conn.close()

    return rowcount

def get_unnotified_changes():
        
    logger.info('Checking DB for changes that are not yet notified')
    conn = get_db()
    cur = conn.cursor()

    SQL = "select * from view_for_pendingnotifications" 
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)    
    cur.execute(SQL)
    result = cur.fetchall()
    cur.close()
    conn.close()

    return result

def update_notification_status(id, notifieddatetime):

    logger.info('DB entry for notification status of interpretation with ID: ' + str(id))
    conn = get_db()
    cur = conn.cursor()


    SQL = "UPDATE interpretations SET notificationtime=%s, isnotificationsent=%s where id=%s" 

    input_data = (notifieddatetime,True, id)

    cur.execute(SQL, input_data)

    conn.commit()

    logger.info("Notification time updated")

    cur.close()
    conn.close()

