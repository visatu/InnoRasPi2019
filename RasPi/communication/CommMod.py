from XBclass import masterXBee
from uuid import uuid4, UUID
from datetime import datetime
import CommMsg
import time

baud = 115200

def Commstart(qout,qin,port):
  #  master = masterXbee(port,baud)

    i = 0
    while True:
        time.sleep(1)
        msg = msgValue("test",i,False)
        qout.put(msg)
        i = i+1
def 
