# Tän filun ku pyörittää voi kattoo tota nettisivu pohjaa
# pöräyttää käyntii weppi servun local hostille

from flask import Flask, render_template
import random
app = Flask(__name__)

# dict to store random data
sensor_values = {
    "temp1" : 23.4,
    "temp2" : 23.2,
    "plate" : "HIGH",
    "sound" : "LOW",
    "button": "HIGH",
}

# functions for different pages we want to have
@app.route('/')
def keksittynimi():
    return(render_template("home.html", title="Home"))

@app.route("/helloworld")
def testi2():
    return(render_template("helloworld.html", title="Hello World!"))

@app.route("/sensors")
def sensors():
    sensor_values["temp1"] = "{:.1f}".format(random.random() * 100)
    sensor_values["temp2"] = "{:.1f}".format(random.random() * 100)
    sensor_values["plate"] = random.choice(["LOW", "HIGH"])
    sensor_values["sound"] = random.choice(["LOW", "HIGH"])
    sensor_values["button"] = random.choice(["LOW", "HIGH"])
    return(render_template("sensors.html", values=sensor_values, title="Sensors"))
    # give new values for sensors



# this runs the app
if __name__ == "__main__":
    app.run(debug=True,)