from RPi import GPIO
import time

GPIO.setmode(GPIO.BCM)

delay = .5
value = 0
ldr = 19

servoPIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization



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
        if (value <= 200):
            print("gordijn is open")
            p.ChangeDutyCycle(7.5)
        else:
            print("gordijn is dicht")
            p.ChangeDutyCycle(2.5)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()