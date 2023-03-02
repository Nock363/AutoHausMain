import sys
from queue import Queue
sys.path.insert(0, '../')
from Handler.DatabaseHandlers import MongoHandler
import logging
from datetime import datetime


class Actuator():

    __name : str
    __collection : str
    

    def __init__(self,name,collection,initialState,config:dict):
        self.__mongoHandler = MongoHandler()
        self.__name = name
        self.__collection = collection
        self.__state = initialState
        self.__config = config

    def safeToCollection(self,state):
        self.__state = state
        obj = {"time":datetime.now(),"name":self.__name,"state":state}
        self.__mongoHandler.writeToCollection(self.__collection,obj)
        return obj

    def hasStateChanged(self,state):
        return (state is not self.__state)

    @property
    def name(self):
        return self.__name