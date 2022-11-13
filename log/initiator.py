from dataclasses import dataclass

@dataclass
class InitiatorClass:
    id:	str = None #Unique identifier for the modification
    top_parent_id: int = None #This is the primary key for the action entry that is associated with this record
    parent_action_id: str = None #This refers to the source ID of the Action  
    source_id: str = None #ID that is given for this entry in the log  
    displayName: str = None
    userPrincipalName:	str = None
    ipAddress:	str = None
    userType:	str = None
    homeTenantId:	str = None
    homeTenantName:	str = None

    def extract_initiator(self,data, parent_action_id, top_parent):
        self.top_parent_id = top_parent
        self.parent_action_id = parent_action_id
        self.source_id = data["id"]
        self.displayName = data["displayName"]
        self.userPrincipalName = data["userPrincipalName"]
        self.ipAddress = data["ipAddress"]
        self.userType = data["userType"]
        self.homeTenantId = data["homeTenantId"]
        self.homeTenantName = data["homeTenantName"]

