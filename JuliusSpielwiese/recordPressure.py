from bmp280 import BMP280
from datetime import datetime
import pymongo
import time


#Inititalisiere BMP280
#!/usr/bin/env python

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

# Initialise the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)



# Convert to two decimal places cleanly
# round() won't include trailing zeroes
def round_num(input):
   return '{:.2f}'.format(input)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["SensorValues"]
mycol = mydb["Pressure"]


while 1==1:
   dt = datetime.now()

   #Write Time Temperature Humidity MongoDB

   mydict = { "Time": dt, "Pressure": round_num(bmp280.get_pressure()),}
   x = mycol.insert_one(mydict)

   print("Done")
   print(str(dt))
   print(round_num(bmp280.get_pressure()))
   time.sleep(2)