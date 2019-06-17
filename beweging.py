from time import sleep
import HYSRF05
import RPi.GPIO as GPIO
import time
from threading import Thread
import pigpio



ultrasonic_sensor = HYSRF05.UltraSonic_Sensor(trigger_pin=23, echo_pin=24, number_of_samples=10)
# while True:
#    print ("avg : {0}".format(ultrasonic_sensor.get_reading()))
#    sleep(1)




class Beweging(Thread):
   def __init__(self, mysqlcon):
      Thread.__init__(self)
      self.daemon = True
      self.conn = mysqlcon
      self.servopin = 26
      GPIO.setmode(GPIO.BCM)

      self.piGPIO = pigpio.pi()
      self.piGPIO.set_PWM_frequency(self.servopin, 50)
      self.piGPIO.set_PWM_dutycycle(self.servopin, (14 / 100) * 255)

      self.sensor_id_beweging = self.conn.get_data('select * from  Sensor where SensorNaam="beweging"')
      if not self.sensor_id_beweging:
         self.sensor_id_beweging = self.conn.set_data('insert into Sensor values (NULL, "deur", "open")')
      else:
         self.sensor_id_beweging = int(self.sensor_id_beweging[0]['SensorID'])



      self.start()

   def run(self):
      while True:


         print("{0}".format(ultrasonic_sensor.get_reading()))
         sleep(10)
         if ultrasonic_sensor.get_reading() >= "30":
            self.piGPIO.set_PWM_dutycycle(self.servopin, (7.5 / 100) * 255)
            print("open")
            time.sleep(5)
            self.piGPIO.set_PWM_dutycycle(self.servopin, (14 / 100) * 255)
            time.sleep(1)
         else:
            print("gesloten")
         self.conn.set_data('insert into Historiek values(NULL, NOW(), %s,%s, "open")',[ultrasonic_sensor.get_reading(), self.sensor_id_beweging])