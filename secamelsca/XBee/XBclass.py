from digi.xbee.io import IOLine, IOMode, IOValue
from digi.xbee.devices import XBeeDevice
# omat
from XBee.XBdevices import deviceTypes
import time,math

class XBeeSensor:
    "class for a single xbee pin/sensor. Has functions for reading and writing values!"
    def __init__(self, pinType, xbee):
        self.xbee = xbee
        self.dvcType = xbee.get_node_id()
        self.type = pinType
        
        print("Setting pin " + str(self.type) + " of " + self.dvcType, end="")
        self.pinLine = deviceTypes[self.dvcType][self.type]["line"]
        self.pinMode = deviceTypes[self.dvcType][self.type]["mode"]
        self.xbee.set_io_configuration(self.pinLine,self.pinMode)
        print(" ...OK!")

    def general_IO(self, value=None):
        """
        Function to read and write values from/to this sensor. Give value if you want to write, otherwise assumes you're reading stuff :D
        """
        # if we have a value as an input we want to write stuff :D
        if value:
            # Digital output
            if self.pinMode == IOMode.DIGITAL_OUT_HIGH or self.pinMode == IOMode.DIGITAL_OUT_LOW:
                return self.write_dio(value)
            # PWM output
            elif self.pinMode == IOMode.PWM:
                return self.write_pwm(value)
        # check if sensor type is "special"
        elif self.type == "NTC":
            return self.get_ntc_temp()
        # if not, just get raw value from sensor
        else:
            return self.get_raw_value()



    def get_raw_value(self):
        value = None
        if self.pinMode == IOMode.ADC:
            value = self.xbee.get_adc_value(self.pinLine)
        elif self.pinMode == IOMode.DIGITAL_IN:
            value = self.xbee.get_dio_value(self.pinLine)
        else:
            value = "ERROR INVALID PIN MODE"
        return value

    def write_dio(self, value):
        "function to write digital io values to pin"
        if self.pinMode == IOMode.DIGITAL_OUT_HIGH or self.pinMode == IOMode.DIGITAL_OUT_LOW:
            if value == IOValue.HIGH or value == IOValue.LOW:
                self.xbee.set_dio_value(self.pinLine, value)
                return "OK"
            else:
                return "ERROR INVALID VALUE"
        else:
            return "ERROR INVALID PIN MODE"


    def write_pwm(self, value):
        "function to write pwm value to pin"
        if self.pinMode == IOMode.PWM:
            if (0 < int(value) < 100):
                self.xbee.set_pwm_duty_cycle(self.pinLine, value)
                return "OK"
            else:
                return "ERRO INVALID VALUE"
        else:
            return "ERROR INVALID PIN MODE"


    def get_ntc_temp(self):
        """ Returns NTC read temperature in Celsius"""
        R1 = 10000          # series resistor
        R0 = 10000          # NTC starting value
        T0 = 273 + 25       # Temp reference value in kelvins (273.15+25)
        Vs = 3.3            # supply voltage
        Vref = 3.3          # voltage reference
        Bval = 3450         # NTC B value
        if self.pinMode == IOMode.ADC:
            # get ADC value
            ADC_value = self.get_raw_value()
            # convert to analog voltage
            Vt = ADC_value/1023 * Vref
            # Vs---R1---(Sense)---tempR---GND
            try:
                tempR = Vt / (Vs-Vt) * R1
            except ZeroDivisionError:
                return "ERROR NTC CANT EVEN"
            # https://en.wikipedia.org/wiki/Thermistor#B_or_%CE%B2_parameter_equation
            tempK = Bval / math.log(tempR / (R0 * math.exp(-1 * Bval / T0)))
            # convert back to Celsius
            tempC = tempK - 273
            # print("NTC_convert\tADC: %04i\tR: %5.00f\tT: %.02f" %(ADC_value, tempR ,tempC))
            return tempC
        else:
            return "ERROR INVALID PIN MODE"


class XBeeDev:
    "Class for a single xbee device connected in network. contains info about sensors and stuff"
    def __init__(self,XBee):
        self.XBee = XBee
        # get the type of the device (node id for now)
        self.type = XBee.get_node_id()
        # get unique identifier
        # binascii.hexlify(bytearray(array_alpha))
        self.id = bytes(self.XBee.get_64bit_addr()).hex()
        self.sensors = {}
        # loop through pins listed in deviceTypes dictionary, init pins on xbee accordinly
        for pin in deviceTypes[self.type]:
            sensor = XBeeSensor(pin, self.XBee)
            self.sensors.update({pin : sensor})
        
# visan paskaa ! poista homo


# visan paskat loppu :D
class masterXBee:
    '''
    Class for a local XBee device
    port = used COM/tty port
    baud = used baud rate
    deviceType = chosen device type from XBdevices.deviceTypes
    devices = dict of all the devices in locals network and their sensors!
    '''
    devices = {}
    def __init__(self, port, baud):
        print("Opening local device", port, baud)
        self.xb = XBeeDevice(port,baud)
        self.xb.open()
        self.xbees = self.getNetworkDevices()
        for device in self.xbees:
            # initiate new xbee device with its pins n stuff
            XBeeDevobj = XBeeDev(device)
            # add it to master class's device dict
            self.devices.update({XBeeDevobj.id : XBeeDevobj})


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