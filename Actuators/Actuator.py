import sys
from abc import ABC, abstractmethod
from queue import Queue
sys.path.insert(0, '../')
from Handler.DataHandler import DataHandler
import logging
from datetime import datetime


class Actuator(ABC):

    __name : str
    __collection : str
    

    def __init__(self,name,collection,config:dict,dataStructure:dict):
        self.__dataHandler = DataHandler()
        self.__name = name
        self.__collection = collection
        self.__config = config
        self.__dataHandler.setupDataStack(name=collection,structure=dataStructure)

    def safeToMemory(self,data):
        retDict = data.copy()
        retDict["time"] = datetime.now()
        self.__dataHandler.safeData(self.__collection,data=retDict)
        return retDict

    @property
    def name(self):
        return self.__name

    @abstractmethod
    def getConfigDesc(self):
        pass

    @abstractmethod
    def getInputDesc(self):
        pass
