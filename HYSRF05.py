import RPi.GPIO as GPIO
from datetime import datetime
import time
class UltraSonic_Sensor(object):
    def __init__(self, trigger_pin=23, echo_pin=24, number_of_samples=10):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.number_of_samples = number_of_samples
     # to change to BCM GPIO numbering
        GPIO.setmode(GPIO.BCM)
     # Setup our pins.
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
    def get_reading(self):
     # Due to the innacuracies of timing with a multi-process system were going to take a number of readings and average them together.
        reading_list = []
        for i in range(self.number_of_samples):
            if GPIO.input(self.echo_pin) :
                print("waiting for timeout")
                time.sleep(0.0050) # 50 ms is the maximum timout if nothing in range.
       # Set our trigger pin low.
       # can we get away without this ?
       #GPIO.output(self.trigger_pin, GPIO.LOW)
       #time.sleep(0.000002)
       # set our trigger high, triggering a pulse to be sent.
        GPIO.output(self.trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, GPIO.LOW)
        while not GPIO.input(self.echo_pin):
         # Wait for our pin to go high, suggesting its waiting for a response.
         pass
       # Now its high, get our start time
        start = datetime.now()
        while GPIO.input(self.echo_pin):
         # wait for our input to go low
         pass
       # Now its low, grab our end time
        end = datetime.now()
       # Store our delta.
        delta = end - start
        reading_list.append(delta.microseconds)
       # take a little break, it appears to help stabalise readings, I suspect due to less interfearance with previous readings
        time.sleep(0.000002)
        average_reading = sum(reading_list)/self.number_of_samples
        return "%s" % (average_reading)