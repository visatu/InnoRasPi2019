from digi.xbee.io import IOLine, IOMode
from XBdevices import deviceTypes


# Hypotethical class for a single sensor?
class XBeeSensor:
    """
    Class for single xbee sensor:
        device = sensor's xbee device
        dvcType = device type
        pin = pin where sensor is connected.
    """
    def __init__(self, device, dvcType, pin):
        self.dvcType = dvcType
        self.xbee = device
        self.ioPin = pin
        self.pinLine = deviceTypes[self.dvcType][self.ioPin]["line"]
        self.pinMode = deviceTypes[self.dvcType][self.ioPin]["mode"]
        self.xbee.set_io_configuration(self.pinLine,self.pinMode)


    def get_raw_value(self):
        value = None
        if self.pinMode == IOMode.ADC:
            value = self.xbee.get_adc_value(self.pinLine)
        elif self.pinMode == IOMode.DIGITAL_IN:
            value = self.xbee.get_dio_value(self.pinLine)
        return value


