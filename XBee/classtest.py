from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
### own stuff , check em out!
from XBclass import masterXBee
# conf
xbPort = "COM6"
baud = 921600

# open local "master" xbee :D
local = masterXBee(xbPort, baud)
while True:
    # reading values from sensors
    btnVal = local.sensors["BUTTON"]["DIO1"].get_raw_value()
    print(local.sensors["ANALOG"]["AD3"].get_raw_value(),end=" | ")
    print(btnVal)
    # light up pin on ANALOG board when button on BUTTON pressed!
    local.sensors["ANALOG"]["DIO4"].write_dio(btnVal)