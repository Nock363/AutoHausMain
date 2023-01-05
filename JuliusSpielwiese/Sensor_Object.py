import sys
import board
from datetime import datetime
import pymongo
import time
from adafruit_extended_bus import ExtendedI2C as I2C
import busio
import adafruit_sgp30
from bmp280 import BMP280
import adafruit_ahtx0

i2cBus = 3






#Inititalisiere AHT20
# Create sensor object, communicating over the board's default I2C bus
i2c = I2C(i2cBus) # Device is /dev/i2c-1)  # uses board.SCL and board.SDA
# for i2c selection:https://docs.circuitpython.org/projects/extended_bus/en/latest/
sensor = adafruit_ahtx0.AHTx0(i2c)


#Inititalisiere BMP280
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

# Initialise the BMP280
bus = SMBus(i2cBus) #Set desired i2c Bus
bmp280 = BMP280(i2c_dev=bus)


#Initialisiere SGP30

sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

sgp30.set_iaq_baseline(0x8973, 0x8AAE)
sgp30.set_iaq_relative_humidity(celsius = 20, relative_humidity=60) #hier werte aus datenbank einpflegen





dt = datetime.now()

# Convert to two decimal places cleanly
# round() won't include trailing zeroes
def round_num(input):
   return '{:.2f}'.format(input)


""" Datenbank kram
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["SensorValues"]
mycol = mydb["TemperatureHumidity"]
"""


   
class Humidity_Sensor:
  def __init__(self, temperature, humidity, time):
    self.temperature = sensor.temperature
    self.humidity = sensor.relative_humidity
    self.time = datetime.now()

  def myfunc(self):
    print("The Humidity is ", self.humidity)



class Pressure_Sensor:
  def __init__(self, pressure, time):
    self.pressure = bmp280.get_pressure()
    self.time = datetime.now()


class Gas_Sensor:
  def __init__(self, CO2, H2, Ethanol, time):
    self.CO2 = sgp30.eCO2
    self.H2 = sensor.H2 = sgp30.H2
    self.Ethanol = sgp30.Ethanol
    self.time = datetime.now()
    
    
measure1 = Humidity_Sensor(1, 1, 1)
measure1.myfunc()

measure2 = Pressure_Sensor(1, 1)
print("Pressure: ", measure2.pressure)

measure3 = Gas_Sensor(1, 1, 1, 1)
print("H2: ", measure3.H2)
print("CO2: ", measure3.CO2)
print("Ethanol: ", measure3.Ethanol)