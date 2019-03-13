#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# importing from subdirectory "XBee" that has __init__.py file inside so it's recognised!
from XBclass import masterXBee
# This file spins up the flask web server and handles serving sites etc stuff
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import random, sys, socket
######### FLASK PART ######################
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
    return(render_template("devices.html", title="Hello World!", devices=master.devicedata))


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
    socketio.emit("sensordata_out", master.sensordata)


def callbackfunction(sensor, value):
    if sensor == "DOORBELL":
        if value == "LOW":
            master.general_io(master.devices["0013A200418724A6"].sensors["DOORBELL_BUZZER"], "HIGH")
        elif value == "HIGH":
            master.general_io(master.devices["0013A200418724A6"].sensors["DOORBELL_BUZZER"], "LOW")
    # else:
    #     if value == "LOW":
    #         master.general_io(master.devices["0013A20041873060"].sensors["WGT_LED"], "LOW")
    #     elif value == "HIGH":
    #         master.general_io(master.devices["0013A20041873060"].sensors["WGT_LED"], "HIGH")

def get_local_ip():
    # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("1.1.1.1", 80))
    local_ip = sock.getsockname()[0]
    sock.close()
    return local_ip

if __name__ == "__main__":
    # check how many arguments were given (first one is always this script!)
    # first argument given should be port to use for xbee device!
    print("startup args:", sys.argv)
    argcount = len(sys.argv)
    if argcount > 3:
        print("Too many arguments!")
        sys.exit()
    elif argcount == 3:
        # second argument to port
        xb_port = sys.argv[1]
        xb_baud = sys.argv[2]
    else:
        print("Check your startup arguments!")
        print("Defaulting to COM6 921600...")
        # Default to com6 ":D" at 921600
        xb_port = "COM6"
        xb_baud = 921600
    # open local "master" xbee :D
    master = masterXBee(port=xb_port, baud=xb_baud, callback_handler=callbackfunction)
    # register DOOR device's DOORBELL sensor as a callback
    master.register_callback("0013A200418734DC",["DOORBELL"])

    master.polling_start(interval=0.5)
    #run flask site
    print("Local IP:", get_local_ip())
    print("Starting Flask...")
    socketio.run(site, debug=True, use_reloader=False, host="0.0.0.0")
