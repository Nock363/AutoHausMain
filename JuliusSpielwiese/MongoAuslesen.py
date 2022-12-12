import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["SensorValues"]
mycol = mydb["TemperatureHumidity"]


temperatures = [] # create an empty list for IDs
# iterate pymongo documents with a for loop
for doc in mycol.find({}).sort([("$natural", -1)]).limit(5):

# append each document's ID to the list
    temperatures += [doc["Temperature"]]

# print out the Temperatures
length = len(temperatures)
print ("Temperatures:", temperatures)
print ("total Temperatures:", length)

temperature_average = 0.0
for i in range(0, length):
    temperature_average = float(temperatures[i]) + temperature_average

print(temperature_average/length)

