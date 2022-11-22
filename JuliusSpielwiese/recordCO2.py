from datetime import datetime
import time
import pymongo
import board
import busio
import adafruit_sgp30


#i2c Initialisierung
i2c_bus = busio.I2C(board.SCL, board.SDA, frequency=100000)  #frequenz problem?

#Inititalisiere sensor
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c_bus)

#setze sensor Baseline
#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#mydb = myclient["SensorValues"]
#mycol = mydb["TemperatureHumidity"]

#celsius = mycol.find().limit(1).sort([('$natural',-1)])
#print(celsius)

sgp30.set_iaq_baseline(0x8973, 0x8AAE)
sgp30.set_iaq_relative_humidity(celsius = 20, relative_humidity=60) #hier werte aus datenbank einpflegen


#aktuelle zeit
dt = datetime.now()

# Convert to two decimal places cleanly
# round() won't include trailing zeroes
def round_num(input):
   return '{:.0f}'.format(input)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["SensorValues"]
mycol = mydb["GasValues"]



while 1==1:
   dt = datetime.now()

   #Write MongoDB

   mydict = { "Time": dt, "CO2": sgp30.eCO2, "H2": sgp30.H2, "Ethanol": sgp30.Ethanol}
   x = mycol.insert_one(mydict)

   print("Done")
   print(str(dt))
   time.sleep(60)