from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class Action:
    id:	str = None
    source_system:	str = None #This is usually one of the cloud providers or something like AD
    source_id:	str = None #This is the identifier for the log from the source system 
    category: str = None
    correlationId:	str = None
    result:	str = None
    resultReason: str = None	
    activityDisplayName: str = None
    activityDateTime:	datetime = None
    loggedByService: str = None
    operationType: str = None
    #TODO: attribute for number of targets modified

    def extract_action(self, data):
        """Extracts action fields from a dictionary"""
        self.source_id = data['id']
        self.category = data ['category']
        self.source_system= "Azure Active Directory"
        self.correlationId = data['correlationId']
        self.result = data['result']
        self.resultReason= data['resultReason']
        self.activityDisplayName = data['activityDisplayName']
        self.activityDateTime = data['activityDateTime']
        self.loggedByService = data['loggedByService']
        self.operationType = data['operationType']


