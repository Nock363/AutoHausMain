import sys
from queue import Queue
sys.path.insert(0, '../')
from Handler.DatabaseHandlers import MongoHandler
from collections import deque
import logging
from Sensoren.Data import Data

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class Sensor():

    def __init__(self,name:str,collection:str,pinID:int,queueDepth = 10):
        self.mongoHandler = MongoHandler()
        self.pin = self.mongoHandler.getPin(pinID)
        self.__name = name
        self.isI2c = (self.pin["mode"] == "I2C")
        if(self.isI2c):
            self.i2cBus = pinID + 2
        else:
            logging.debug("NO I2C CONFIG")
        self.__collection = collection
        self.__q = deque(maxlen=queueDepth)
        

    def addToQueue(self,obj:Data):
        #print("add element to queue:")
        self.__q.append(obj)

    def printQueue(self):
        #print("clear and print queue:")
        for obj in self.__q:
            print(obj)

    def safeToCollection(self,data:Data):
        
        obj = {"time":data.time(),"data":data.data()}
        self.mongoHandler.writeToCollection(self.__collection,obj)



    def createData(self,data) -> Data:
        obj =  Data(data)
        self.addToQueue(obj)
        self.safeToCollection(obj)
        return obj

    