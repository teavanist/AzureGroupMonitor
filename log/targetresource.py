from dataclasses import dataclass
import db

@dataclass
class TargetResource:
    id:	str = None
    top_parent_id: int = None #This is the primary key for the action entry that is associated with this record
    parent_action_id:	str = None  # This refers to the ID of the action
    source_id:	str = None  # This is the identifier for the item from the source system
    displayName: str = None
    type: str = None
    userPrincipalName:	str = None
    groupType:	str = None
    modified_items_count: int = None

    def extract_target(self, data, parentid,top_parent):
        self.top_parent_id = top_parent
        self.parent_action_id = parentid
        self.source_id = data["id"]
        self.displayName = data["displayName"]
        self.type =data["type"]
        self.userPrincipalName = data["userPrincipalName"]
        self.groupType = data["groupType"]
        self.modified_items_count = len(data["modifiedProperties"])

        