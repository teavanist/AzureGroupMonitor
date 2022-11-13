#get database connection
from db import get_db
import psycopg2.extras


def startInterpretation(action_id, action_category, action_activityDisplayName):


    interpretedresult =""

    #All group mangament related checks:
    if action_category == "GroupManagement":

        if action_activityDisplayName == "Add member to group":
            interpretedresult = simplify_add_member_from_group(action_id)

        elif action_activityDisplayName == "Remove member from group":
            interpretedresult = simplify_remove_member_from_group(action_id)
        
        elif action_activityDisplayName == "Update group":
            interpretedresult = simplify_update_group(action_id)

        elif action_activityDisplayName == "Add owner to group":
            interpretedresult, affectedparties = simplify_add_group_owner(action_id)

        elif action_activityDisplayName == "Add group":
            interpretedresult = simplify_group_creation(action_id)

        else:

            interpretedresult ="Unknown Action: " + str(action_activityDisplayName)
    
    return interpretedresult

def simplify_group_creation(action_identifier):
    interpretation=""

    conn = get_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)    
    SQL = "select * from action_initiator_target_modifications a where a.actionid = %s"
    criteria = (action_identifier,)

    cur.execute(SQL, criteria)

    rows = cur.fetchall()

    for item in rows:
        if item["Property"]=="DisplayName":

            group_name = str(item["Newvalue"])
            group_name = group_name.replace("[","")
            group_name = group_name.replace("]","")

            interpretation= item["Initiator"] + \
               " created " + item["TargetType"] + \
                ": " + group_name


    cur.close()
    conn.close()
    return interpretation
    
def simplify_add_group_owner(action_identifier):
    interpretation=""
    ap = []

    conn = get_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)    
    SQL = "select * from action_initiator_target_modifications a where a.actionid = %s"
    criteria = (action_identifier,)

    cur.execute(SQL, criteria)

    rows = cur.fetchall()

    for item in rows:
        if item["Property"]=="Group.DisplayName":

            interpretation= str(item["Initiator"]) + \
               " added " + str(item["TargetType"]) + \
                " " + str(item["TargetUPN"]) + \
                " as owner of Group: " + str(item["Newvalue"])

    
    #find affected parties 
    # there are multiple possible affected users. 
    # todo: we need to add a count for the number of targets per action 
    # The first one one is always the one from the targets. We get that info below. 
    for item in rows:
        ap.append(item["TargetID"])
        #print(item)
        break

    # The second set we can get by looping the modifications list  
    
    for item in rows:
        print(item["Property"])
        t = str(item["Property"])
        t = t.split(".",1)
        if t[1]=="ObjectID":
            x = str(item["Newvalue"]).replace("\"","")
            ap.append(x)

    

    cur.close()
    conn.close()
    return interpretation, ap 
    
def simplify_remove_member_from_group(action_identifier):

    interpretation=""

    conn = get_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)    
    SQL = "select * from action_initiator_target_modifications a where a.actionid = %s"
    criteria = (action_identifier,)

    cur.execute(SQL, criteria)

    rows = cur.fetchall()

    for row in rows:
        #User was removed from the Group 
        if row["Property"] == "Group.DisplayName" and row["TargetType"] == 'User':

            interpretation= row["Initiator"] + " removed " + str(row["TargetType"]) + " " + str(row["TargetUPN"]) + " from " + str(row["Oldvalue"])

        #A group was removed from the Group 
        if row["Property"] == "Group.DisplayName" and row["TargetType"] == 'Group':
            interpretation= row["Initiator"] + " removed " + str(row["TargetType"]) + " " + str(row["TargetDisplayName"]) + " from " + str(row["Oldvalue"])


    cur.close()
    conn.close()
    return interpretation

def simplify_update_group(action_identifier):
    
    interpretation=""

    conn = get_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)    
    SQL = "select * from action_initiator_target_modifications a where a.actionid = %s"
    criteria = (action_identifier,)

    cur.execute(SQL, criteria)

    rows = cur.fetchall()

    for item in rows:
        if item["Oldvalue"] is None or item["Newvalue"] is None:
            continue 
        else:
            interpretation = item["Initiator"] + " changed " + item["Property"] + " of " + item["TargetType"] + " from " + str(item["Oldvalue"]) + " to " + str(item["Newvalue"])


    
    cur.close()
    conn.close()
    return interpretation

def simplify_add_member_from_group(action_identifier):
    #TODO: make the scenario where a group is added as a separate function 
    interpretation=""
    conn = get_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)    

    '''
    Group is added 

    type	:	Group
    userPrincipalName	:	null
    displayName	:	Innovation group

    '''

    SQL = "select * from action_initiator_target_modifications r where r.actionid =%s "
    criteria = (action_identifier,)

    cur.execute(SQL, criteria)

    print(action_identifier)

    rows = cur.fetchall()
    for row in rows:
        print(row)
        print("Property is " + str(row["Property"]))
        print("Targettype is " + str(row["TargetType"]))

        #User was added to the Group 
        if row["Property"] == "Group.DisplayName" and row["TargetType"] == 'User':
            interpretation = str(row["Initiator"]) + " added " + str(row["TargetType"]) + " " + str(row["TargetUPN"]) + " to " + str(row["Newvalue"])

        #Another group was added to the Group 
        if row["Property"] == "Group.DisplayName" and row["TargetType"] == 'Group':
            interpretation = str(row["Initiator"]) + " added " + str(row["TargetType"]) + " " + str(row["TargetDisplayName"]) + " to " + str(row["Newvalue"])

    print(interpretation)
    cur.close()
    conn.close()
    return interpretation