from RPi import GPIO
import time
from threading import Thread
import pigpio

GPIO.setmode(GPIO.BCM)

delay = .5
value = 0
ldr = 19



class Licht(Thread):
    def __init__(self, mysqlcon):
        self.servoPIN = 18
        GPIO.setmode(GPIO.BCM)



        Thread.__init__(self)
        self.daemon = True
        self.conn = mysqlcon

        self.piGPIO = pigpio.pi()
        self.piGPIO.set_PWM_frequency(self.servoPIN, 50)
        self.piGPIO.set_PWM_dutycycle(self.servoPIN, (14/100)*255)


        self.sensor_id_ldr = self.conn.get_data('select * from  Sensor where SensorNaam="ldr"')
        if not self.sensor_id_ldr:
            self.sensor_id_ldr = self.conn.set_data('insert into Sensor values (NULL, "ldr", "open")')
        else:
            self.sensor_id_ldr = int(self.sensor_id_ldr[0]['SensorID'])

        self.start()

    def run(self):

        def berekenen(ldr):
            count = 0
            GPIO.setup(ldr, GPIO.OUT)
            GPIO.output(ldr, 0)
            time.sleep(delay)
            GPIO.setup(ldr, GPIO.IN)
            while (GPIO.input(ldr) == 0):
                count += 1
            return count

        try:
            while True:

                value = berekenen(ldr)
                print(value)
                if (value <= 1000):
                    print("gordijn is open")
                    self.piGPIO.set_PWM_dutycycle(self.servoPIN, (7.5 / 100) * 255)

                else:
                    print("gordijn is dicht")
                    self.piGPIO.set_PWM_dutycycle(self.servoPIN, (14 / 100) * 255)




        except KeyboardInterrupt:
            pass
        finally:
            GPIO.cleanup()

        self.conn.set_data('insert into Historiek values(NULL, NOW(), %s,%s, "open")', [value, self.sensor_id_ldr])


# class Gservo(Thread):
#
#     def __init__(self):
#         Thread.__init__(self)
#         self.start()
#
#     def run(self):
#         p.ChangeDutyCycle(7.5)
#         time.sleep(5)
