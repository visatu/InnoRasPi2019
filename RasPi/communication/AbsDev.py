class absBase:
    def __init__(self,name,devtype):
        self.name = name
        self.type = devtype
        self.displayName = self.name
class absDev(absBase):
    def __init__(self,name,devtype):
        absBase.__init__(self,name,devtype)
        self.sensorsList = {}

    def parseXBeeDev(self,XBeeDev):

    
    def addSensor(sensor):
        self.sensorsList.append(sensor)

class absSens(absBase):
    def __init__(self,name,senstype):
        absBase.__init__(self,name,senstype)
        self.value = None
        self.triggerTargets = {}
    def addTrigger(self,target,value):
        if not target in self.triggerTargets:
            self.triggerTargets.update(target:value)
        else:
            self.triggerTargets[target] = value
    def updateValue(self,value):
        self.value = value
        
    




