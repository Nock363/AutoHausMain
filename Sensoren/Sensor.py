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
                queueDepth = 100,
                unit:str="",
                range:tuple=(0,100),
                description:str="",
                active:bool = True
                ):

        self.__dataHandler = DataHandler()
        self.__pin = self.__dataHandler.getPin(pinID)
        self.__name = name
        self.isI2c = (self.__pin["mode"] == "I2C")
        if(self.isI2c):
            self.i2cBus = pinID + 2
        else:
            logging.debug("NO I2C CONFIG")
        self.__collection = collection
        self.__history = deque(maxlen=queueDepth)
        self.__dataHandler.setupDataStack(name=collection,structure=dataStructure)

    @property
    def name(self):
        return self.__name

    def getInfo(self):
        ret = {"name":self.__name}
        return ret


    def printQueue(self):
        #print("clear and print queue:")
        for obj in self.__history:
            print(obj)

    def safeToMemory(self,data:Data):
        
        retDict = data.data.copy()
        retDict["time"] = data.time
        self.__dataHandler.safeData(self.__collection,data=retDict)

    def getHistory(self,lenght:int):
        #check if history is long enough
        if(len(self.__history) < lenght):
            #get data from dataHandler and fill up the queue. ckear the queue first
            data = self.__dataHandler.getData(self.__collection,lenght)
            self.__history = deque(maxlen=lenght)
            for obj in data:
                self.__history.append(obj)
            #return history as list
            return list(self.__history)
        else:
            return list(self.__history)[-lenght:]


        

    #noch da?ja
    #die arduino werte sind immernoch strings, aber ich type caste die doch
    #benutze ja sogar die format funktion
    def createData(self,data) -> Data:
        obj =  Data(data)
        self.__history.append(obj)
        self.safeToMemory(obj)
        return obj


    