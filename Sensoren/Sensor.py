import sys
import threading
from queue import Queue
sys.path.insert(0, '../')
from Handler.DataHandler import DataHandler
from collections import deque
import logging
from Sensoren.Data import Data
import random

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class Sensor():


    def __init__(self,name:str,
                collection:str,
                pinID:int,
                dataStructure:dict,
                queueDepth = 5,
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

        self.__dataStructure = dataStructure
        dataStructure={
            "PH":{"dataType":float,"unit":None,"range":(0,14)},
            "EC":{"dataType":int,"unit":"uS","range":(0,15)},
            "Temperature":{"dataType":float,"unit":"Grad","range":(0,30.0)}
        }

        dataTypes = {key: value["dataType"] for key, value in dataStructure.items()}

        self.__dataHandler.setupDataStack(name=collection,structure=dataTypes)
        self.__active = active
        self.__queueDepth = queueDepth
        self.__lock = threading.Lock()
        self.__description = description

        #create random id for identification
        self.testID = random.randint(0,100000)

    @property
    def name(self):
        return self.__name

    @property
    def active(self):
        return self.__active

    @property
    def collection(self):
        return self.__collection

    def printHistory(self):
        #print("clear and print queue:")
        for obj in self.__history:
            print(obj)

    def safeToMemory(self,data:Data):
        with self.__lock:
            retDict = data.data.copy()
            retDict["time"] = data.time
            self.__dataHandler.safeData(self.__collection,data=retDict)

    def getHistory(self,lenght:int):
        
        #check if history is long enough
        if(len(self.__history) < lenght):

            pullLength = self.__queueDepth
            if(self.__queueDepth < lenght):
                pullLength = lenght



            #get data from dataHandler and fill up the queue. ckear the queue first
            data = self.__dataHandler.readData(self.__collection,pullLength)
            data.reverse()
            self.__history = deque(maxlen=pullLength)
            for obj in data:
                self.__history.append(obj)
            #return history as list

            # print("from getHistory(not long enough):")
            # self.printHistory()
       
        retList = list(self.__history)
        retList.reverse()
        returnData = retList[0:lenght]
        return retList[0:lenght]


    def __writeToHistory(self,obj):        
        with self.__lock:
            self.__history.append(obj)
        
    def getSensorConfigAsDict(self) -> dict:
        return {
                "active":self.__active,
                "name":self.__name,
                "collection":self.__collection,
                "pinID":self.__pin["pinID"],
                "class":self.__class__.__name__,
                "description":self.__description,
                "datastackSize": self.__dataHandler.getDataStackSize(self.__collection)
                }

    def createData(self,data) -> Data:
        obj =  Data(data)
        self.__writeToHistory(obj.asPlainDict())
        print("from createData:", self.testID)
        # self.printHistory()
        self.safeToMemory(obj)
        return obj


    