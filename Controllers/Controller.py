import sys
sys.path.insert(0, '../')
from abc import ABC, abstractmethod
from Sensoren.Sensor import Sensor
from Handler.WirelessHandler import RadioHandler


class Controller():
    __mask : list[str]
    __lastValue = None


    def __init__(self,mask:list[str],config:dict = None):
        self.__mask = mask
        self.__config = config

    def checkInputData(self,inputData:dict):
        for m in self.__mask:
            if m not in inputData:
              raise KeyError(f"'{m}' wurde nicht in den Inputs gefunden. Benötigte Inputs: {self.__mask}") 

    def safeAndReturn(self,ret):
        self.__lastValue = ret
        return ret

    @abstractmethod
    def getNextScheduleTime(self):
        return None
    
    def getInfo(self):
        controllerName = self.__class__.__name__
        return {
            "name": controllerName,
            "mask": self.__mask,
            "config": self.__config
        }