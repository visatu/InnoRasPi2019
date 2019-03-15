# InnoRasPi2019
**Innovation project by:**

**Aleksi Alatalo, Aldo Heino, Tuomas Paakkunainen, Joonatan Sohkanen, Visa Tuominen**


The goal was to explore the Raspberry Pi as a teaching platform. Our group chose to work with Digi XBee3 devices using the Raspberry Pi to run python code to monitor and command the XBee devices.

Features of the program:
- Monitor readings from sensors in the network, displayed in a dynamically created web interface.
- Set DIO pins according to value limits set in configuration files:
    
    User can set limits for values in sensor configuration, and a sensor to trigger when this limit is met or exceeded. For example, you could monitor room humidity and hook up a room humidifier control.

Planned features not implemented:
- Trigger configuration from web interface --> user configurable automation. This is currently achieved through editing deviceTypes file.
- MORE controllable stuff! Only blinking leds gets boring fast.


The following Python 3 libraries were used:
- **digi-xbee**: library for using XBee devices in API mode
- **Flask**: web application framework for Python
- **Flask-SocketIO**: socketIO extension for Flask. This enables real time communication between the web interface host and a connected client.

Other used stuff:
- **Bootstrap4**: open source web development toolkit. Makes creating decent looking websites a bit easier
- **socketIO** script on web interface for real time value updating

We used [Visual Studio Code](https://code.visualstudio.com/) for writing and it has pretty good integration with git and some great extensions for our project:
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) - python language  support
- [Jinja](https://marketplace.visualstudio.com/items?itemName=wholroyd.jinja) - flask templating language support
- [Git History](https://marketplace.visualstudio.com/items?itemName=donjayamanne.githistory) - nice way to track changes in repository
- [Bootstrap v4 Snippets](https://marketplace.visualstudio.com/items?itemName=Zaczero.bootstrap-v4-snippets) - super easy bootstrap templates!
- [VS Live Share](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare) - real time shared file editing!

-------------

## XBClass
### Instantiating masterXBee object & callback function
The master xbee object requires 3 arguments:
- port: COMX or dev/ttyUSBX port of local xbee device set to FORM network in XCTU
- baud: baud rate of local XBee
- callback_handler: function to handle callbacks. Should take 2 arguments:
  - sensor (str): name of the sensor that the value comes from
  - value (str): the actual value (number, "HIGH" or "LOW")

For example:
```python
def callbackFunction(sensor, value):
    print("Callback! Value from", sensor, ":", value)

master = masterXBee(port=COM8, baud=921600, callback_handler=callbackFunction)
```

### devices dictionary
On startup, the masterXBee class creates a dictionary of all XBees and sensors in the network in the following format:
```python
devices : {
    "DEVICE64BITADDRESS" : <XBeeDev object>
        sensors = {
            "DOORBELL_BUZZER"  : <XBeeSensor object>
            "LED_WGT"   : <XBeeSensor object>
            "LIGHT_SENSOR" <XBeeSensor object>
        }
    "SECOND64BITADDRESS" : <XBeedev object>
        sensors = {
            "WEIGHT_PLATE"  : <XBeeSensor object>
            "DOORBELL"   : <XBeeSensor object>
        }
    "SECOND
}
```

### Reading and writing values
The masterXBee object has a method called **general_io** for reading and writing values. The first argument should bee an XBeeSensor object, the optional second argument should only be given when writing values to sensors:
```python
# read value from WEIGHT_PLATE
wgtPlateVal = master.general_io(master.devices["SECOND64BITADDRESS"].sensors["WEIGHT_PLATE"])
# write HIGH to DOORBELL_BUZZER
master.general_io(master.devices["DEVICE64BITADDRESS"].sensors["DOORBELL_BUZZER"], "HIGH")

```
### Polling sensor values
The **masterXBee.start_polling(interval)** method will start updating the sensor values to a dictionary **masterXBee.sensordata** with given interval:

```python
# update sensor value data twice a second
master.polling_start(interval=0.5)

# stop polling!
master.polling_stop()
```

the sensordata dictionary format:

```python
sensordata = {
    "DEVICE64BITADDRESS" : {
        "DOORBELL_BUZZER" : "LOW",
        "LED_WGT" : "HIGH",
        "LIGHT_SENSOR" : 869
    }
}
```
this format is readable by javascript at least when sent through flask-socketIO.

### Registering callbacks
You might want to register callbacks for fast operation when some sensor changes value. User buttons are a good exapmle of this. We want to get the button press straight away instead of only getting value updates every second or so through polling.
```python
# register callback with the device ID and list of sensor names you want to monitor for changes:
# instant updates from doorbell and weight plate:
master.register_callback("SECONDE64BITADDRESS", ["DOORBELL", "WEIGHT_PLATE"])

# only from doorbell:
master.register_callback("SECONDE64BITADDRESS", ["DOORBELL"])

# clear callbacks from device
master.register_callback("SECONDE64BITADDRESS", None)

```

-------------

## Relevant links & documentation
### XBee
Wireless xbee modules were used as the main component for the whole project.
- XBee3 user guide: https://www.digi.com/resources/documentation/digidocs/PDFs/90002273.pdf
- XBee3 Hardware ref: https://www.digi.com/resources/documentation/digidocs/PDFs/90001543.pdf
- digi-XBee Python doc: https://xbplib.readthedocs.io/en/latest/
- Micropython guide: https://www.digi.com/resources/documentation/digidocs/PDFs/90002219.pdf
- Grove board: https://www.digi.com/resources/documentation/digidocs/pdfs/90001457-13.pdf

### Flask
- Flask documentation: http://flask.pocoo.org/docs/1.0/
- Flask tutorial youtube series: https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
- Flask-SocketIO documentation: https://flask-socketio.readthedocs.io/en/latest/

### Bootstrap
- Vakio bootstrap doku: https://getbootstrap.com/docs/4.3/getting-started/introduction/
- W3 tutoriaalei ja esimerkkei: https://www.w3schools.com/bootstrap4/default.asp

### Sensors
- Sensor kit used (originally bought from BangGood.com): https://www.instructables.com/id/Arduino-37-in-1-Sensors-Kit-Explained/
