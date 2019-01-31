from digi.xbee.io import IOLine, IOMode, IOValue
from XBdevices import deviceTypes


# Hypotethical class for a single sensor?
class XBeePin:
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
        else:
            print("invalid pin mode!")
        return value
    
    def write_pin(self, value):
        if self.pinMode == IOMode.PWM:
            if (0 < int(value) < 100):
                self.xbee.set_pwm_duty_cycle(self.pinLine, value)
            else:
                print("invalid value!")
        elif self.pinMode == IOMode.DIGITAL_OUT_HIGH or self.pinMode == IOMode.DIGITAL_OUT_LOW:
            if value == 0:
                outValue = IOValue.LOW
            elif value == 1:
                outValue = IOValue.HIGH
            else:
                print("Invalid value!")
            self.xbee.set_dio_value(self.pinLine, outValue)
        else:
            print("invalid pin mode!")

