import sys
sys.path.insert(0, '../')

from Sensoren.Sensor import Sensor
from Handler.DatabaseHandlers import MongoHandler
from Handler.WirelessHandler import RadioHandler


class BaseBlock():
    __mask : list[str]
    __lastValue = None


    def __init__(self,mask:list[str]):
        self.__mongo = MongoHandler()
        self.__mask = mask

    def checkInputData(self,inputData:dict):
        for m in self.__mask:
            if m not in inputData:
              raise KeyError(f"'{m}' wurde nicht in den Inputs gefunden. Benötigte Inputs: {self.__mask}") 

    def safeAndReturn(self,ret):
        self.__lastValue = ret
        return ret
