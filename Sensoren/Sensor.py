import sys
import threading
from queue import Queue
sys.path.insert(0, '../')
from Handler.DataHandler import DataHandler
from collections import deque
import logging
import random
from datetime import datetime

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class Sensor():


    def __init__(self,
                name:str,
                collection:str,
                dataStructure:dict,
                queueDepth = 5,
                config:dict = None,
                description:str="",
                active:bool = True
                ):

        self.__dataHandler = DataHandler()
        self.__config = config
        self.__name = name
        self.__collection = collection
        self.__history = deque(maxlen=queueDepth)

        self.__dataStructure = dataStructure
        # dataStructure={
        #     "PH":{"dataType":float,"unit":None,"range":(0,14)},
        #     "EC":{"dataType":int,"unit":"uS","range":(0,15)},
        #     "Temperature":{"dataType":float,"unit":"Grad","range":(0,30.0)}
        # }

        dataTypes = {key: value["dataType"] for key, value in self.__dataStructure.items()}

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

    def safeToMemory(self,data:dict):
        with self.__lock:
            self.__dataHandler.safeData(self.__collection,data=data)

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

    def getHistoryByTimespan(self,startTime:datetime,endTime:datetime):
        
        startTimeMS = startTime.timestamp()
        endTimeMS = endTime.timestamp()

        #check if endTime is in the past. if so return directly from the DataHandler
        if(endTimeMS < datetime.now().timestamp()):
            data = self.__dataHandler.readDataByTimeSpan(self.__collection,startTime,endTime)
            data.reverse()
            return data

        #check if last entry is in timespan
        historyLength = len(self.__history)
        oldestTime = self.__history[0]["time"]
        oldestTimeMS = oldestTime.timestamp()
        if(len(self.__history) == 0 or oldestTimeMS > startTimeMS):
            #get data from dataHandler and fill up the queue. ckear the queue first
            #convert startTime and end time to string like 2023-08-13 00:00:00
            startTimeStr = startTime.strftime("%Y-%m-%d %H:%M:%S")
            endTimeStr = endTime.strftime("%Y-%m-%d %H:%M:%S")
            data = self.__dataHandler.readDataByTimeSpan(self.__collection,startTimeStr,endTimeStr)
            data.reverse()

            pullLength = self.__queueDepth
            if(self.__queueDepth < len(data)):
                pullLength = len(data)

            self.__history = deque(maxlen=pullLength)
            for obj in data:
                self.__history.append(obj)
        
        #return all elements in timespan
        retList = list(self.__history)
        retList.reverse()
        returnData = []
        for obj in retList:
            if(obj["time"] >= startTime and obj["time"] <= endTime):
                returnData.append(obj)
        return returnData

    def __writeToHistory(self,obj):        
        with self.__lock:
            self.__history.append(obj)
        
    def getInfos(self) -> dict:
        return {
                "active":self.__active,
                "name":self.__name,
                "collection":self.__collection,
                "class":self.__class__.__name__,
                "description":self.__description,
                "config":self.__config,
                "datastackSize": self.__dataHandler.getDataStackSize(self.__collection)
                }
    
    def getConfig(self) -> dict:
        return {
                "active":self.__active,
                "name":self.__name,
                "collection":self.__collection,
                "class":self.__class__.__name__,
                "config":self.__config,
                "description":self.__description
                }

    def createData(self,data) -> dict:
        data["time"] = datetime.now()
        self.__writeToHistory(data)
        self.safeToMemory(data)
        return data


    