import sys
sys.path.insert(0, '../python_sensor_aht20/')
import AHT20
from datetime import datetime
import pymongo
import time


#Inititalisiere AHT20
aht20 = AHT20.AHT20()
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

   mydict = { "Time": dt, "Temperature": round_num(aht20.get_temperature()), "Humidity": round_num(aht20.get_humidity())}
   x = mycol.insert_one(mydict)

   print("Done")
   print(str(dt))
   time.sleep(60)