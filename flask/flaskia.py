# This file spins up the flask web server and handles serving sites etc stuff

from flask import Flask, render_template
from flask_socketio import SocketIO
import random
app = Flask(__name__)
socketio = SocketIO(app)

# dict to store random "sensor" data
sensor_values = {
    "temp1" : 23.4,
    "temp2" : 23.2,
    "plate" : "HIGH",
    "button": "HIGH",
}

############ different pages we want to have  #############
# the function names dont seem to matter as long
# as they all have different names :D

# homepage
@app.route('/')
def keksittynimi(): 
    return(render_template("home.html", title="Home"))

# helloworld :)
@app.route("/helloworld")
def testi2():
    return(render_template("helloworld.html", title="Hello World!"))

# sensors list page
@app.route("/sensors")
def sensors():
    # this function gives random values to sensors page each time it gets loaded
    # see sensors.html for how the flask/jinja code handles the given dict variable.
    sensor_values["temp1"] = "{:.1f}".format(random.random() * 100)
    sensor_values["temp2"] = "{:.1f}".format(random.random() * 100)
    sensor_values["plate"] = random.choice(["LOW", "HIGH"])
    sensor_values["button"] = random.choice(["LOW", "HIGH"])
    return(render_template("sensors.html", values=sensor_values, title="Sensors"))
    # give new values for sensors

# socket io test page !!!
@app.route("/sockettest")
def socket_testi_sivu():
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


# this runs the app (with socketio enabled)
if __name__ == "__main__":
    socketio.run(app, debug=True)