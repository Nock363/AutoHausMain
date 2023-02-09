import sys
sys.path.insert(0, '../')

from Sensoren.Sensor import Sensor
from Handler.DatabaseHandlers import MongoHandler
from Handler.WirelessHandler import RadioHandler


class BaseBlock():
    __inputs : dict
    __mask : list[str]
    __lastValue = None


    def __init__(self,inputs:dict,mask:list[str]):
        self.__inputs = sensors
        self.__mongo = MongoHandler()
    
    def checkInputData(self,inputData:dict):
        for m in self.__mask:
            if m not in inputData:
              raise KeyError(f"'{m}' wurde nicht in den Inputs gefunden. Benötigte Inputs: {self.__mask}") 

    def safeAndReturn(self,ret):
        self.__lastValue = ret
        return ret

class PowerPlugBlock(BaseBlock):

    __plug = dict()

    def __init__(self,sensors:list[Sensor],plugName):
        super().__init__(sensors)
        self.__radio = RadioHandler()
        self.__plug = self.__radio.getPowerPlug(plugName)
        
    
    
    
        	
