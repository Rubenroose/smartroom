import RPi.GPIO as GPIO
import time

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import pigpio


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

servoPIN = 18

piGPIO = pigpio.pi()
piGPIO.set_PWM_frequency(servoPIN, 50)
piGPIO.set_PWM_dutycycle(servoPIN, (7.5/100)*255)


@socketio.on('knop')
def openSlagboom():
    piGPIO.set_PWM_dutycycle(servoPIN, (14 / 100) * 255)
    time.sleep(3)
    piGPIO.set_PWM_dutycycle(servoPIN, (7.5 / 100) * 255)



if __name__ == '__main__':
    socketio.run(app, debug=False, host="0.0.0.0", port=5000)
