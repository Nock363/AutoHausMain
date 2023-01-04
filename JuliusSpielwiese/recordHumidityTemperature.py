import sys
import board
import adafruit_ahtx0
from datetime import datetime
import pymongo
import time
from adafruit_extended_bus import ExtendedI2C as I2C



#Inititalisiere AHT20
# Create sensor object, communicating over the board's default I2C bus
i2c = I2C(3) # Device is /dev/i2c-1)  # uses board.SCL and board.SDA
# for i2c selection:https://docs.circuitpython.org/projects/extended_bus/en/latest/
sensor = adafruit_ahtx0.AHTx0(i2c)

dt = datetime.now()

# Convert to two decimal places cleanly
# round() won't include trailing zeroes
def round_num(input):
   return '{:.2f}'.format(input)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["SensorValues"]
mycol = mydb["TemperatureHumidity"]


while 1==1:
   dt = datetime.now()

   #Write Time Temperature Humidity MongoDB

   mydict = { "Time": dt, "Temperature": round_num(sensor.temperature), "Humidity": round_num(sensor.relative_humidity)}
   x = mycol.insert_one(mydict)

   print("Done")
   print(str(dt))
   time.sleep(60)