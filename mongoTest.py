from pymongo import MongoClient
from datetime import datetime
import logging
import threading

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


def runMongoTest(iterations = 10000,collectionName = "testCollection"):
    iterations = 10000
    datetimeObj = datetime.now()
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



def threadTest(text):
    logging.info(f"Thread is  running: {text}")

def runParallelMongoTests(threadCount = 4,iterations = 1000):
    logging.info("Start parallel Mongotests")
    threads = []
    for i in range(0,threadCount):
        collectionName = f"parallelTestCollection_{i}"
        t = threading.Thread(target=runMongoTest,args=("iterations",collectionName,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

#runSingleThreadTest()

#if __name__ == "__main__":
logging.info("Test Log")
#threadTest("Test")
runParallelMongoTests(2,100)