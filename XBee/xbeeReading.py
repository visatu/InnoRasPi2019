from digi.xbee.devices import XBeeDevice,RemoteXBeeDevice
from digi.xbee.io import IOLine, IOMode
import time

local = XBeeDevice("COM6", 115200) # COM port of the sending module
local.open()
local.send_data_broadcast("Imma ask for a reading pretty soon!") # Check receiving device for results :D

# Getting network device list
network = local.get_network()
# Looking for a device with a specific NODE ID and instantiate
remote = network.discover_device("BTN")
if remote:
    print(remote)
    remote.set_io_configuration(IOLine.DIO3_AD3, IOMode.ADC)
    while True:
        print(remote.get_adc_value(IOLine.DIO3_AD3))
else:
    print("Device not found :(")
local.close()
