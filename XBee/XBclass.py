from digi.xbee.io import IOLine, IOMode, IOValue
from digi.xbee.devices import XBeeDevice
# omat
from XBdevices import deviceTypes
import time


# Hypotethical class for a single sensor?
class XBeeSensor:
    "class for a single xbee pin/sensor. Has functions for reading and writing values!"
    def __init__(self, pin, xbee):
        self.xbee = xbee
        self.dvcType = xbee.get_node_id()
        self.ioPin = pin
        print("Setting pin " + str(pin) + " of " + self.dvcType, end="")
        self.pinLine = deviceTypes[self.dvcType][self.ioPin]["line"]
        self.pinMode = deviceTypes[self.dvcType][self.ioPin]["mode"]
        self.xbee.set_io_configuration(self.pinLine,self.pinMode)
        print(" ...OK!")
    def get_raw_value(self):
        value = None
        if self.pinMode == IOMode.ADC:
            value = self.xbee.get_adc_value(self.pinLine)
        elif self.pinMode == IOMode.DIGITAL_IN:
            value = self.xbee.get_dio_value(self.pinLine)
        else:
            print("invalid pin mode!")
        return value
    
    def write_dio(self, value):
        "function to write digital io values to pin"
        if self.pinMode == IOMode.DIGITAL_OUT_HIGH or self.pinMode == IOMode.DIGITAL_OUT_LOW:
            self.xbee.set_dio_value(self.pinLine, value)
        else:
            print("invalid pin mode!")

    def write_pwm(self, value):
        "function to write pwm value to pin"
        if self.pinMode == IOMode.PWM:
            if (0 < int(value) < 100):
                self.xbee.set_pwm_duty_cycle(self.pinLine, value)
            else:
                print("invalid value!")
        else:
            print("invalid pin mode!")


class masterXBee:
    '''
    Class for a local XBee device
    port = used COM/tty port
    baud = used baud rate
    deviceType = chosen device type from XBdevices.deviceTypes
    sensors = dict of all the devices in locals network and their sensors!
    '''
    sensors = {}
    def __init__(self, port, baud):
        print("Opening local device", port, baud)
        self.xb = XBeeDevice(port,baud)
        self.xb.open()
        self.deviceType = self.xb.get_node_id()
        self.remotes = self.getNetworkDevices()
        for device in self.remotes:
            deviceType = device.get_node_id()
            self.sensors.update({deviceType:{}})
            for pin in deviceTypes[deviceType]:
                sensor = XBeeSensor(pin, device)
                self.sensors[deviceType][pin] = sensor
    def getNetworkDevices(self):
        """
        Returns devices in the network of given local xBee device, including the local device
        type is RemoteXbeeDevice
        """
        print("Getting a list of network devices...")
        # Get devices in local xbee's network!
        self.xb.send_data_broadcast("Getting a list of everyone :D")
        network = self.xb.get_network()
        network.start_discovery_process()
        while network.is_discovery_running():
            time.sleep(.5)
        networkDevices = network.get_devices()
        print("Found the following devices:")
        for found in networkDevices:
            print(found)
        networkDevices.insert(0, self.xb)
        return networkDevices