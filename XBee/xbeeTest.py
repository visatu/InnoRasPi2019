#
# Example code to test functionality of XBee
#

# Send hello world to network
from digi.xbee.devices import XBeeDevice
import time
device = XBeeDevice("COM6", 115200) # COM port of the sending module
device.open()
device.send_data_broadcast("Hello World!") # Check receiving device for results :D

# Getting network device list
network = device.get_network()
network.start_discovery_process() # Start discovery process, wait for finish
while network.is_discovery_running():
    time.sleep(.5)
devicesInNetwork = network.get_devices() # Get list of devices in network
print("Devices in network:")
for dvc in devicesInNetwork:
    print(str(dvc) + '\n')

# Looking for a device with a specific NODE ID:
dvcName = "JOIN"
remote = network.discover_device(dvcName)
if remote:
    print("Found \"" + str(remote) + "\" !! :D")
else:
    print("Device not found :(")

# Discover the remote devices whose node IDs are BOB and JANE
remote_list = network.discover_devices(["BOB", "JANE"])
if remote_list:
    print("Found the following devices:")
    for dvc in remote_list:
        print(str(dvc) + '\n')
else:
    print("Couldn't find listed devices :(")
# Remember to close connection after use!
device.close()