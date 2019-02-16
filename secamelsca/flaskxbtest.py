# importing from subdirectory "XBee" that has __init__.py file inside so it's recognised!
from XBee.XBclass import masterXBee
# This file spins up the flask web server and handles serving sites etc stuff
from flask import Flask, render_template
from flask_socketio import SocketIO
import random

# conf
xbPort = "com6"
baud = 115200

# open local "master" xbee :D
master = masterXBee(xbPort, baud)
# gotta tear down class for flask output :D
devicedata = {}
for device in master.devices:
        dvcID = master.devices[device].id
        dvcType = master.devices[device].type
        sensorlist = []
        for sensor in master.devices[device].sensors:
                sensorlist.append(sensor)
        devicedata.update({dvcID : {
                "type" : dvcType,
                "sensors" : sensorlist,
                }
        })
print(devicedata)
######### FLASK PART #######################
site = Flask(__name__)
socketio = SocketIO(site)

############ different pages we want to have  #############
# the function names dont seem to matter as long
# as they all have different names :D

# homepage
@site.route('/')
def homepage(): 
    return(render_template("home.html", title="Home"))

# helloworld :)
@site.route("/devices")
def devicepage():
    return(render_template("devices.html", title="Hello World!",
        devices=devicedata))

# sensors list page
@site.route("/sensors")
def sensorpage():
    # this function gives random values to sensors page each time it gets loaded
    # see sensors.html for how the flask/jinja code handles the given dict variable.
    sensor_values["temp1"] = "{:.1f}".format(random.random() * 100)
    sensor_values["temp2"] = "{:.1f}".format(random.random() * 100)
    sensor_values["plate"] = random.choice(["LOW", "HIGH"])
    sensor_values["button"] = random.choice(["LOW", "HIGH"])
    return(render_template("sensors.html", values=sensor_values, title="Sensors"))
    # give new values for sensors

# socket io test page !!!
@site.route("/sockettest")
def socket_test_page():
    return(render_template("sockettest.html", title="SocketIO Test Page!"))


############  SocketIO event callbacks ##############################
# event names are decided by the emitter of the event, and
# receiver should have a callback responding to the same event name:

# reaction to "hello" event:
@socketio.on("hello")
def get_hello(received):
    # just print received message on the console
    print("received hello message:" + str(received["data"]))

# reaction to request for updated value 
@socketio.on("give data")
def send_data():
    # respond with "ok here" and with a dict containing updated value
    socketio.emit("ok here", {"value" : random.randint(1,10)} )


# this runs the site (with socketio enabled)
if __name__ == "__main__":
    socketio.run(site, debug=True, use_reloader=False)