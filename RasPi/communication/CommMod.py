#from XBclass import masterXBee
from uuid import uuid4, UUID
from datetime import datetime
import time
class message:
    def __init__(self,msgtype,name):
        self.type = msgtype
        self.name = name
        self.stamp = datetime.now()
        self.msgid = uuid4()

class msgValue(message):
    def __init__(self,name,value,request):
        message.__init__(self,1, name)
        self.value = value
        self.request = request

class msgDevChange(message):
    def __init__(self,name,new,device,sensors):
        message.__init__(self,2,name)
        self.new = new
        self.device = device
        self.sensors = sensors



def Commstart(qout,qin,port):
    i = 0
    while True:
        time.sleep(1)
        msg = msgValue("test",i,False)
        qout.put(msg)
        i = i+1

