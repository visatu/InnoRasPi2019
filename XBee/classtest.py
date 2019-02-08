from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.io import IOValue
### own stuff , check em out!
from XBclass import masterXBee
import time, math
# conf
xbPort = "com6"
baud = 115200

# open local "master" xbee :D
master = masterXBee(xbPort, baud)
# list of connected devices
print(master.devices)
# write digital value to pin
master.devices["ANALOG"]["DIO4"].write_dio(IOValue.HIGH)
while True: # loop
    # get raw ADC value
    print(master.devices["ANALOG"]["AD3"].get_raw_value())
    # function to get raw digital value
    #master.devices["ANALOG"]["DIO4"].get_raw_value()
    # function to get NTC value (will print out result in console as well)
    master.devices["ANALOG"]["AD3"].get_ntc_temp()
    time.sleep(.5)