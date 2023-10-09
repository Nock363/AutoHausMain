import sys
from abc import ABC, abstractmethod
from queue import Queue
sys.path.insert(0, '../')
from Handler.DataHandler import DataHandler
import logging
from datetime import datetime
from Utils.Status import Status

class Actuator(ABC):

    __name : str
    __collection : str
    status: Status

    def __init__(self,
                name,
                collection,
                config:dict,
                dataStructure:dict,
                description:str="",
                active:bool = True
                ):

        self.__dataHandler = DataHandler()
        self.__name = name
        self.__collection = collection
        self.__config = config
        self.__active = active
        self.__description = description
        self.__dataHandler.setupDataStack(name=collection,structure=dataStructure)
        self.__lastState = None
        self.status = Status.READY

    def safeToMemory(self,data):
        
        retDict = data.copy()
        retDict["time"] = datetime.now()
        self.__lastState = retDict
        self.__dataHandler.safeData(self.__collection,data=retDict)
        return retDict

    def getInfos(self) -> dict:
        return {
                "active":self.__active,
                "name":self.__name,
                "collection":self.__collection,
                "class":self.__class__.__name__,
                "description":self.__description,
                "config":self.__config,
                "state":self.__lastState
                }

    def getHistory(self,length):
        result = self.__dataHandler.readData(self.__collection,length)
        return result



    @property
    def active(self):
        return self.__active

    @property
    def name(self):
        return self.__name

    @staticmethod
    @abstractmethod
    def getConfigDesc():
        pass

    @staticmethod
    @abstractmethod
    def getInputDesc():
        pass
