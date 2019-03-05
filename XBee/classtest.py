from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.io import IOValue
### own stuff , check em out!
from XBclass import masterXBee
import time, math
# conf
xbPort = "/dev/ttyUSB0"
baud = 115200

# open local "master" xbee :D
master = masterXBee(xbPort, baud)
# list of connected devices
print(master.devices)
# write digital value to pin
while True: # loop
    print(master.devices["LOCAL"]["TMP"].get_ntc_temp(),end=" | ")
    print(master.devices["LOCAL"]["BTN"].get_raw_value(),end=" | ")
    print(master.devices["LOCAL"]["SND"].get_raw_value(),end=" | ")
    print(master.devices["LOCAL"]["LIG"].get_raw_value(),end=" | ")
    print(master.devices["LOCAL"]["TLT"].get_raw_value())
    time.sleep(.5)