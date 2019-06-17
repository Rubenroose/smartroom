from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from DP1Database import Database
import RPi.GPIO as GPIO
import time
import ldr
import vochtig
import beweging
import pigpio
from PCF8574A import LCDScreen
lcd = LCDScreen(False, 21, 20, 22, 5, 6, 27, 17, 25, 12, 16)  # init van lcd
lcd.LCD_init()  # init van LCD (2

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
conn = Database(app=app, user='ruben', password='rubenroose', db='project1')
vochtigheid = vochtig.Vochtig(conn)




@socketio.on('getTemp')
def temp():
    temp = conn.get_data("SELECT Value FROM project1.Historiek WHERE project1.Historiek.Sensor_SensorID = 2 ORDER BY project1.Historiek.HistoriekID DESC LIMIT 1;")
    socketio.emit('giveTemp', str(temp[0]['Value']))

@socketio.on('getVocht')
def temp():
    vocht = conn.get_data("SELECT Value FROM project1.Historiek WHERE project1.Historiek.Sensor_SensorID = 1 ORDER BY project1.Historiek.HistoriekID DESC LIMIT 1;")
    socketio.emit('giveVocht', str(vocht[0]['Value']))

@socketio.on('getGraad')
def graad():
    graad = conn.get_data("SELECT Value FROM project1.Historiek WHERE project1.Historiek.Sensor_SensorID = 2 ORDER BY project1.Historiek.HistoriekID DESC LIMIT 1;")
    socketio.emit('giveGraad', str(graad[0]['Value']))

@socketio.on('getProcent')
def temp():
    procent = conn.get_data("SELECT Value FROM project1.Historiek WHERE project1.Historiek.Sensor_SensorID = 2 ORDER BY project1.Historiek.HistoriekID DESC LIMIT 1;")
    socketio.emit('giveProcent', str(procent[0]['Value']))







lopen = beweging.Beweging(conn)
licht = ldr.Licht(conn)


lcd.send_line('Smartroom')
lcd.second_row()
lcd.statusip1()


servopin = 26
servoPIN = 18

piGPIO = pigpio.pi()
piGPIO.set_PWM_frequency(servoPIN, 50)
piGPIO.set_PWM_dutycycle(servoPIN, (14/100)*255)


@socketio.on('knop')
def openGordijn():
    piGPIO.set_PWM_dutycycle(servoPIN, (7.5 / 100) * 255)
    time.sleep(30)

piGPIO.set_PWM_frequency(servopin, 50)
piGPIO.set_PWM_dutycycle(servopin, (14/100)*255)

@socketio.on('button')
def openDeur():
    piGPIO.set_PWM_dutycycle(servopin, (7.5 / 100) * 255)
    time.sleep(30)
#
#
# @socketio.on('button2')
# def geklikt():
#     h.ChangeDutyCycle(7.5)
#     time.sleep(5)
#     h.ChangeDutyCycle(2.5)
#     time.sleep(1)
















if __name__ == '__main__':
    socketio.run(app, debug=False, host="0.0.0.0", port=5000)