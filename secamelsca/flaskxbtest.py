# importing from subdirectory "XBee" that has __init__.py file inside so it's recognised!
from XBee.XBclass import masterXBee
# This file spins up the flask web server and handles serving sites etc stuff
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import random

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
    return(render_template("devices.html", title="Hello World!", devices=master.get_device_data()))


############  SocketIO event callbacks ##############################
# event names are decided by the emitter of the event, and
# receiver should have a callback responding to the same event name:

# reaction to "hello" event:
@socketio.on("hello")
def get_hello(received):
    # just print received message on the console
    print("received hello message:" + str(received["data"]))


@socketio.on("sensordata")
def send_sensor_values():
    socketio.emit("sensordata_out", master.get_sensor_data())

if __name__ == "__main__":
    
    # open local "master" xbee :D
    master = masterXBee(port="com6", baud="921600")
    # start polling sensors in a new thread
    xbeethread = Thread(target=master.polling_start, args=(0.01,))
    xbeethread.start()
    # this runs the site (with socketio enabled)    
    socketio.run(site, debug=True, use_reloader=False)