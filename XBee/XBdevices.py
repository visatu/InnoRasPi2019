from digi.xbee.devices import XBeeDevice,RemoteXBeeDevice
from digi.xbee.io import IOLine, IOMode
import time

# device type library with io pin lines and modes :D
deviceTypes = {
    "ANALOG": {

        "DIO4": {
            "line": IOLine.DIO4_AD4,
            "mode": IOMode.DIGITAL_IN
        },

        "AD3": {
            "line": IOLine.DIO3_AD3,
            "mode": IOMode.ADC
        }
    }
}
# could maybe add modifiers to get human readable values
# eg. multiplier for binary voltage value to get real measurement 


def getNetworkDevices(localDevice):
    """
    Returns dictionary of devices in the network of given local xBee device.
    Dictionary keys are XBees' node IDs
    """
    # Get devices in local xbee's network!
    localDevice.send_data_broadcast("Getting a list of everyone :D")
    network = localDevice.get_network()
    network.start_discovery_process()
    while network.is_discovery_running():
        time.sleep(.5)
    networkDevices = network.get_devices() 
    networkDevices.insert(0,localDevice)
    # create dict of devices listed by device name/type
    devices = {}    
    for member in networkDevices:
        name = str(member.get_node_id())
        devices[name] = member
    # DONE!
    return devices