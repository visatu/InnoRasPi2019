from digi.xbee.devices import XBeeDevice
### own stuff , check em out!
from XBclass import XBeeSensor
from XBdevices import getNetworkDevices

# functional :D
devicetype = "ANALOG"
pin = "AD3"
local_xbee = XBeeDevice("COM6", 921600)
local_xbee.open()
remoteXbees = getNetworkDevices(local_xbee)
adcSensor = XBeeSensor(remoteXbees[devicetype],devicetype,pin)
while True:
    print(adcSensor.get_raw_value())
local_xbee.close()