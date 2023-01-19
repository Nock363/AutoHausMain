import sys
from queue import Queue
sys.path.insert(0, '../Handler/')
from DatabaseHandlers import MongoHandler
from collections import deque
import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class Sensor():

    def __init__(self,collection,pinID,queueDepth = 10):
        self.mongoHandler = MongoHandler()
        self.pin = self.mongoHandler.getPin(pinID)
        self.isI2c = (self.pin["mode"] == "I2C")
        if(self.isI2c):
            self.i2cBus = pinID + 2
        else:
            logging.debug("NO I2C CONFIG")
        self.collection = collection
        self.q = deque(maxlen=queueDepth)
        

    def addToQueue(self,obj):
        print("add element to queue:")
        print(obj)
        self.q.append(obj)

    def printQueue(self):
        print("clear and print queue:")
        for obj in self.q:
            print(obj)

    def safeToCollection(self,data):
        self.mongoHandler.writeToCollection(self.collection,data)
    


