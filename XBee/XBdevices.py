from digi.xbee.io import IOLine, IOMode

# device type library with io pin lines and modes :D
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
        "DIO4": {"line": IOLine.DIO4_AD4,
                 "mode": IOMode.DIGITAL_IN},
    }
}
# could maybe add modifiers to get human readable values
# eg. multiplier for binary voltage value to get real measurement