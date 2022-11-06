from pymongo import MongoClient
from datetime import datetime


iterations = 10000


datetimeObj = datetime.now()
collectionName = "collection_" +  datetimeObj.strftime("%d_%m__%H_%M")
# collectionName = "collection_06_11__14_54"
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
        lastResult = collection.find_one(sort=[( "index", -1 )])
        #print(lastResult)
        index = lastResult["index"] + 1
        timestamp = datetime.now().timestamp()
        oldTimestamp = lastResult["timestamp"]
        timeSinceLastInsert = timestamp - oldTimestamp
        input = {"index": index,"timestamp":timestamp,"timeSinceLastInsert":timeSinceLastInsert}
        collection.insert_one(input)
        

finishTime = datetime.now()

runningTime = finishTime - datetimeObj
avgTime = (runningTime/iterations).total_seconds() * 1000
print(f"Runningtime: {runningTime} for {iterations} iterations. Average Time: {avgTime} ms")