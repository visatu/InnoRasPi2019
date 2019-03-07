from /../../secamelsca/XBclass import XBeeDev, XBeeSensor

class absBase:
    def __init__(self, name, devtype):
        self.name = name
        self.type = devtype
        self.displayName = self.name
class absDev(absBase):
    def __init__(self, name, devtype, protocol):
        absBase.__init__(self,name,devtype)
        self.sensorsList = {}
        self.protocol = protocol

    




    
    def addSensor(self,sensor):
        self.sensorsList.append(sensor.name:sensor)
    def updateSensorValue(self,sensName, value):
        if sensName in self.sensorsList:
            return self.sensorsList[sensName].updateValue(value)

class absSens(absBase):
    def __init__(self,name,senstype):
        absBase.__init__(self,name,senstype)
        self.value = None
        self.triggerTargets = {}
    def addTrigger(self,triggerString):
        #trigger string format: targetdev:targetsens:triggertype:
        if not target in self.triggerTargets:
            self.triggerTargets.update(target:value)
        else:
            self.triggerTargets[target] = value
    def updateValue(self,value):
        self.value = value
      #  for target in self.triggerTargets:
       #     if 
        
class absTrigger:
    def __init__(self,target,triggerType,lowerLimit = 0, higherLimit = 0 ):
        #triggerTypes: 0 analog, 1 digital normally closed, 2 digital normally open
        self.target = target
        self.triggerType = triggerType
        self.lowerLimit = lowerLimit
        self.higherLimit = higherLimit
        self.singleLimit = False
        self.state = 0
        self.firstStateChange = False
        self.normallyOpen = False

        if (self.lowerLimit == self.higherLimit):
            self.singleLimit = True
        elif (self.lowerLimit > self.higherLimit):
            self.singleLimit , self.higherLimit = self.higherLimit, self.lowerLimit

        if (self.triggerType == 2):
            self.normallyOpen = True



    def checkValue(self,value):
        if (self.triggerType == 0):
            return value

        tempState = -1
        if self.singleLimit:
            if (value < self.lowerLimit != not self.normallyOpen):
                tempState = 0
            else:
                tempState = 1
        else:
            if ((value < self.lowerLimit or value > self.higherLimit) != not self.normallyOpen):
                tempState = 0
            else:
                tempState = 1
        if (tempState == -1):
            return
        if (self.state != tempState or self.firstStateChange):
            self.state = 0
            return self.state
                

                
    




