from dataclasses import dataclass

@dataclass
class Modification:
    id:	str = None #Unique identifier for the modification
    top_parent_id: int = None #This is the primary key for the action entry that is associated with this record
    parent_target_id: str = None #This refers to the ID of the targetresource on which the modification is done 
    displayName: str = None
    oldValue:	str = None
    newValue:	str = None

    def extract_modifications(self,data, parent_id, top_parent):
        self.top_parent_id = top_parent
        self.parent_target_id = parent_id
        self.displayName = data["displayName"]
        self.oldValue = data["oldValue"]
        self.newValue = data ["newValue"]
