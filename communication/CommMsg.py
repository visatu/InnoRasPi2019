from uuid import uuid4, UUID
from datetime import datetime


class message:
    def __init__(self,msgtype,name):
        self.type = msgtype
        self.name = name
        self.stamp = datetime.now()
        self.msgid = uuid4()

class msgValue(message):
    def __init__(self,devName,sensName,value, digital):
        message.__init__(self,1, devName + ";" + sensName)
        self.devName = devName
        self.sensName = sensName
        self.value = value
        self.digital = digital
        

class msgDevChange(message):
    def __init__(self,name,device):
        message.__init__(self,2,name)        
        self.device = device
        

   

