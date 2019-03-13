# InnoRasPi2019
Innovation project 2019 by:

Aleksi Alatalo, Aldo Heino, Tuomas Paakkunainen, Joonatan Sohkanen, Visa Tuominen

The goal was to explore the Raspberry Pi as a teaching platform. Our group chose to work with Digi XBee3 devices using the RPi mainly as a central hub for the XBee network, controlling the network's "master" device, reading values from connected devices etc.

The end result was a network of connected XBee devices, each having multiple sensors connected and their values being updated to the main program running on the RPi. The RPi hosts a web interface for monitoring connected devices as well as their sensors' values.

The following Python 3 libraries were used:
- **digi-xbee**: library for using XBee devices in API mode
- **Flask**: web application framework for Python
- **Flask-SocketIO**: socketIO extension for Flask. This enables real time communication between the web interface host and a connected client.

Other used stuff:
- **Bootstrap4**: open source web development toolkit. Makes creating decent looking websites a bit easier
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


## ETC

### Sensorit mitä valmiina
- lämpötila
- valoisuus
- äänenvoimakkuus/voimakkaiden äänien tunnistus (clapper?)
- kallistuksen tunnistus
- general DIO
- painosensori "pressure plate" tyylil
