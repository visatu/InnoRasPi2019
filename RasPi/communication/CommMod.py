from XBclass import masterXBee, XBeeDev, XBeeSensor
from uuid import uuid4, UUID
from datetime import datetime
from CommMsg import msgDevChange, msgValue
from AbsDev import absDev, absSens
import time

baud = 115200

def Commstart(qout,qin,port):
  handler = commHandler(qout,port)
  i = 0
  while True:
    handler.updateValue()
    try:
        msg = qin.get()
        handler.msgHandler(msg)
    except Exception as error:
        pass


  
class commHandler:
    devIndex = 0
    sensIndex = 0
    devCount = 0
    sensCount = 0
    def __init__(self,qout,port,period = 1):
        self.master = masterXbee(port,baud)
        self.qout = qout
        self.updateTime = time.time()
        self.period = period
        devCount = self.master.devices.count()
        for dev in self.master.devices:
            parseXBeeDev(self.master.devices[dev])
    def msgHandler(self,msg):
        if msg.type == 1:
            value = None
            if msg.digital:
                if msg.value == 0:
                    value = "LOW"
                else:
                    value = "HIGH"
            else:
                value = msg.value
            
            if msg.devName in self.master.devices:
                if msg.sensName in self.master.devices[msg.devName].sensors:
                    sensor = self.master.devices[msg.devName].sensors[msg.sensName]
                    self.master.general_io(sensor,value)
    def updateValue(self):
        if not (time.time() - self.updateTime) > self.period:
            return

        if self.devIndex < self.devCount:
            devName = list(self.master.devices)[devIndex]
            self.sensCount = self.master.devices[devName].sensors.count()
            if self.sensIndex < self.sensCount:                
                sensName = list(self.master.devices[devName].sensors)[sensIndex]
                sensor = self.master.devices[devName].sensors[sensName]
                self.sendMsg(sensor)
                self.sensIndex += 1
            else:
                self.sensIndex = 0
                self.devIndex += 1
        else:
            self.sensIndex = 0
            self.devIndex = 0
            self.updateTime = time.time()

    def sendMsg(self,sensor):
        value = self.master.general_io(self.master.devices[devName].sensors[sensName])
        digital = False
        if sensor.pinMode == IOmode.DIGITAL_IN or sensor.pinMode == IOMode.DIGITAL_OUT_HIGH or sensor.pinMode == IOMode.DIGITAL_OUT_LOW:
            digital = True
            if value == "HIGH":
                value = 1
            else:
                value = 0
        msg = msgValue(devName,sensName,value,digital)
        self.qout.put(msg)
    def parseXBeeDev(self,XBDev):
        absXb = absDev(XBDev.dvcID, XBDev.dvcType, "XBee")
    
        for sensor in XBDev.sensors:
            sensorObj = XBDev.sensors[sensor]

            sensType = -1
            if sensorObj.pinMode == IOmode.ADC):
                sensType = 0 #Analog in
            elif sensorObj.pinMode == IOMode.PWM:
                sensType = 1 #Analog out
            elif sensorObj.pinMode == IOmode.DIGITAL_IN:
                sensType = 2 #Digital in
            elif sensorObj.pinMode == IOMode.DIGITAL_OUT_HIGH or sensorObj.pinMode == IOMode.DIGITAL_OUT_LOW:
                sensType = 3 #Digital out
            
            if (sensType != -1):
                sensObj = absSens(sensor,sensType)
                absXb.addSensor(sensObj)
            else:
                print("Unknown sensor: " + sensor)
        msg = msgDevChange(absXb.name,absXb)
        self.qout.put(msg)