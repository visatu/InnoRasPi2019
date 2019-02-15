# Tän filun ku pyörittää voi kattoo tota nettisivu pohjaa
# pöräyttää käyntii weppi servun local hostille

from flask import Flask, render_template
from flask_socketio import SocketIO
import random, time


app = Flask(__name__)
socketio = SocketIO(app)

# main page
@app.route('/')
def root():
    return(render_template("sockettest.html", title="Socket test :D"))



############  socketio events #################################
# hello event :)
@socketio.on("hello")
def get_hello(received):
    print("received hello message:" + str(received))

@socketio.on("give data")
def send_data():
    socketio.emit("ok here", {"value" : random.randint(1,10)} )
