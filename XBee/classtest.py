from digi.xbee.devices import XBeeDevice
### own stuff , check em out!
from XBclass import XBeePin
from XBdevices import getNetworkDevices

# functional :D

local_xbee = XBeeDevice("/dev/ttyUSB6", 921600)
local_xbee.open()
remoteXbees = getNetworkDevices(local_xbee)
adcSensor = XBeePin(remoteXbees["ANALOG"],"ANALOG","AD3")
btnSensor = XBeePin(remoteXbees["ANALOG"],"ANALOG", "DIO4")
pwmPin = XBeePin(remoteXbees["ANALOG"], "ANALOG", "PWM0")

# pwm pin 66% duty cycle
pwmPin.write_pin(50)
while True:
    print(adcSensor.get_raw_value(), btnSensor.get_raw_value())

local_xbee.close()