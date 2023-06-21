import sys
import threading
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
        self.__active = active
        self.__queueDepth = queueDepth
        self.__lock = threading.Lock()

    @property
    def name(self):
        return self.__name

    @property
    def active(self):
        return self.__active

    @property
    def collection(self):
        return self.__collection

    def getInfo(self):
        ret = {"name":self.__name}
        return ret


    def printQueue(self):
        #print("clear and print queue:")
        for obj in self.__history:
            print(obj)

    def safeToMemory(self,data:Data):
        with self.__lock:
            retDict = data.data.copy()
            retDict["time"] = data.time
            self.__dataHandler.safeData(self.__collection,data=retDict)

    def getHistory(self,lenght:int):
        with self.__lock:
            #check if history is long enough
            # if(len(self.__history) < lenght):

            pullLength = self.__queueDepth
            if(self.__queueDepth < lenght):
                pullLength = lenght

            #get data from dataHandler and fill up the queue. ckear the queue first
            tempDataHandler = DataHandler() #TODO fix "only in single thread  usable bla bla"
            data = tempDataHandler.readData(self.__collection,pullLength)
            #self.__history = deque(maxlen=pullLength)
            for obj in data:
                self.__history.append(obj)
            #return history as list
            return list(self.__history)
            # else:
            #     retList = list(self.__history)[0:lenght]
            #     return retList


    def __writeToHistory(self,obj):        
        with self.__lock:
            self.__history.append(obj)
        

    def createData(self,data) -> Data:
        obj =  Data(data)
        self.__writeToHistory(obj.asPlainDict())
        self.safeToMemory(obj)
        return obj


    