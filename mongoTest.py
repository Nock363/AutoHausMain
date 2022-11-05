from pymongo import MongoClient
from datetime import datetime


iterations = 3


datetimeObj = datetime.now()
collectionName = "collection_" +  datetimeObj.strftime("%d_%m__%H_%M")

print(collectionName)

client = MongoClient('mongodb://localhost:27017/')

index = 0;
timestamp = datetime.now().timestamp()
timeSinceLastInsert = 0

with client:
    db = client.test
    collection = db[collectionName]

    baseInput = {"index": index,"timestamp":timestamp,"timeSinceLastInsert":timeSinceLastInsert}
    
    collection.insert_one(baseInput)
    print("im here")

    for i in range(0,iterations):
        lastResult = collection.find_one()
        index = lastResult["index"] + 1
        timestamp = datetime.now().timestamp()
        oldTimestamp = lastResult["timestamp"]
        timeSinceLastInsert = timestamp - oldTimestamp
        input = {"index": index,"timestamp":timestamp,"timeSinceLastInsert":timeSinceLastInsert}
        collection.insert_one(input)