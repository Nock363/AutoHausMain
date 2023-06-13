import sys
from queue import Queue
sys.path.insert(0, '../')
from Handler.DataHandler import DataHandler
from collections import deque
import logging
from Sensoren.Data import Data

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class Sensor():

    def __init__(self,name:str,
                collection:str,
                pinID:int,
                dataStructure:dict,
                queueDepth = 10,
                unit:str="",
                range:tuple=(0,100),
                description:str=""):

        self.__dataHandler = DataHandler()
        self.__pin = self.__dataHandler.getPin(pinID)
        self.__name = name
        self.isI2c = (self.__pin["mode"] == "I2C")
        if(self.isI2c):
            self.i2cBus = pinID + 2
        else:
            logging.debug("NO I2C CONFIG")
        self.__collection = collection
        self.__q = deque(maxlen=queueDepth)
        self.__dataHandler.setupDataStack(name=collection,structure=dataStructure)




    


    def getInfo(self):
        ret = {"name":self.__name}
        return ret

    def addToQueue(self,obj:Data):
        #print("add element to queue:")
        self.__q.append(obj)

    def printQueue(self):
        #print("clear and print queue:")
        for obj in self.__q:
            print(obj)

    def safeToMemory(self,data:Data):
        
        retDict = data.data().copy()
        retDict["time"] = data.time()
        self.__dataHandler.safeData(self.__collection,data=retDict)


    #noch da?ja
    #die arduino werte sind immernoch strings, aber ich type caste die doch
    #benutze ja sogar die format funktion
    def createData(self,data) -> Data:
        obj =  Data(data)
        self.addToQueue(obj)
        self.safeToMemory(obj)
        return obj

    