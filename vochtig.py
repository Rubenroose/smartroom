import Adafruit_DHT
import time
from threading import Thread

# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor = Adafruit_DHT.DHT11

# Set GPIO sensor is connected to
gpio = 13

# Use read_retry method. This will retry up to 15 times to
# get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)


class Vochtig(Thread):
    def __init__(self, mysqlcon):
        Thread.__init__(self)
        self.daemon = True
        self.conn = mysqlcon



        self.sensor_id_humidity = self.conn.get_data('select * from  Sensor where SensorNaam="humidity"')
        if not self.sensor_id_humidity:
            self.sensor_id_humidity = self.conn.set_data('insert into Sensor values (NULL, "humidity", "%")')
        else:
            self.sensor_id_humidity = int(self.sensor_id_humidity[0]['SensorID'])



        self.sensor_id_temperature = self.conn.get_data('select * from Sensor where SensorNaam="temperature"')
        if not self.sensor_id_temperature:
            self.sensor_id_temperature = self.conn.set_data('insert into Sensor values (NULL, "temperature", "°C")')
        else:
            self.sensor_id_temperature = int(self.sensor_id_temperature[0]['SensorID'])

        self.start()

    def run(self):
        while True:
            print('Temp={0}*C  Humidity={1}%'.format(temperature, humidity))
            time.sleep(10)

            self.conn.set_data('insert into Historiek values(NULL, NOW(), %s,%s, NULL)', [temperature, self.sensor_id_temperature])
            self.conn.set_data('insert into Historiek values(NULL, NOW(), %s, %s, NULL)', [humidity, self.sensor_id_humidity])

# Reading the DHT11 is very sensitive to timings and occasionally
# the Pi might fail to get a valid reading. So check if readings are valid.







