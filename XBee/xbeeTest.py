from digi.xbee.devices import XBeeDevice
device = XBeeDevice("COM5", 9600) # COM port of the sending module
device.open()
device.send_data_broadcast("Hello World!")
device.close()
# Check receiving device for results :D