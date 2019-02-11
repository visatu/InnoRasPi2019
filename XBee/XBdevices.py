from digi.xbee.io import IOLine, IOMode

# device type library with io pin lines and modes :D
# this should be easier to use than memorizing each pins real name, since you can give whatever name you want to the pins. Using names from Grove board for now.
deviceTypes = {
    "ANALOG": {
        "DIO4": {"line": IOLine.DIO4_AD4,
                 "mode": IOMode.DIGITAL_OUT_HIGH},
        "AD3": {"line": IOLine.DIO3_AD3,
                "mode": IOMode.ADC},
        "PWM0": {"line": IOLine.DIO10_PWM0,
                 "mode": IOMode.PWM},
        },
    "BUTTON": {
        "DIO4": {"line": IOLine.DIO4_AD4,
                 "mode": IOMode.DIGITAL_IN},
        "DIO1": {"line": IOLine.DIO1_AD1,
                  "mode": IOMode.DIGITAL_IN},
        },
    "LOCAL":{
        "TMP": {"line": IOLine.DIO0_AD0,
                 "mode": IOMode.ADC},
        "BTN": {"line": IOLine.DIO4_AD4,
                 "mode": IOMode.DIGITAL_IN},
        "SND": {"line": IOLine.DIO12,
                 "mode": IOMode.DIGITAL_IN},
        "LIG": {"line": IOLine.DIO3_AD3,
                 "mode": IOMode.ADC},
        "TLT": {"line": IOLine.DIO1_AD1,
                 "mode": IOMode.DIGITAL_IN},
    }
}
# could maybe add modifiers to get human readable values
# eg. multiplier for 10 bit voltage value to get real measurement: 0-1023 --> temperature reading, for example