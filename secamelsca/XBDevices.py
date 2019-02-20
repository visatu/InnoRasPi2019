from digi.xbee.io import IOLine, IOMode

deviceTypes = {
    "MASTER": {
        "NTC": {"line": IOLine.DIO0_AD0,
                "mode": IOMode.ADC},
        "BTN": {"line": IOLine.DIO4_AD4,
                "mode": IOMode.DIGITAL_IN},
        # "SND": {"line": IOLine.DIO12,
        #          "mode": IOMode.DIGITAL_IN},
        # "LIG": {"line": IOLine.DIO3_AD3,
        #          "mode": IOMode.ADC},
        # "TLT": {"line": IOLine.DIO1_AD1,
        #          "mode": IOMode.DIGITAL_IN},
    },
    "REMOTE": {
        "LED": {"line": IOLine.DIO4_AD4,
                "mode": IOMode.DIGITAL_OUT_HIGH},
        "AD0": {"line": IOLine.DIO0_AD0,
                "mode": IOMode.ADC},
    },
}
