"""
This class works as a reference for XBClass.py for what sensors each device has.
The program will setup each sensor according to this dictionary,
and polling is done using this setup as well.
"""

from digi.xbee.io import IOLine, IOMode

deviceTypes = {
    "MASTER": {
        "POTENTIOMETER": {"line": IOLine.DIO0_AD0,
                "mode": IOMode.ADC},
        "USER_BUTTON": {"line": IOLine.DIO4_AD4,
                "mode": IOMode.DIGITAL_IN},
        "DOORBELL_BUZZER": {"line": IOLine.DIO12,
                "mode": IOMode.DIGITAL_OUT_LOW
                },
    },
    "ROOM": {
        "LED": {"line": IOLine.DIO4_AD4,
                "mode": IOMode.DIGITAL_OUT_HIGH},
        "LIGHTNESS": {"line": IOLine.DIO3_AD3,
                "mode": IOMode.ADC},
        "TEMP_NTC": {"line": IOLine.DIO0_AD0,
                "mode": IOMode.ADC,
                "trigger": {
                        "target": "LED",
                        "limit": 30
                        },
                },
    },
    "DOOR": {
        "DOORBELL": {
                "line": IOLine.DIO4_AD4,
                "mode": IOMode.DIGITAL_IN},
        "WEIGHT_PLATE": {
                "line": IOLine.DIO1_AD1,
                "mode": IOMode.DIGITAL_IN,
                "trigger": {
                        "target": "DOORBELL_BUZZER",
                        "limit": "LOW"
                        },
                },
    }
}