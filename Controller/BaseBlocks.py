import sys
sys.path.insert(0, '../')

from Sensoren.Sensor import Sensor
from Handler.DatabaseHandlers import MongoHandler
from Handler.WirelessHandler import RadioHandler


class BaseBlock():
    __sensors : list[Sensor]
    def __init__(self,sensors:list[Sensor]):
        self.__sensors = sensors
        self.__mongo = MongoHandler()
#Fabian ist ein Penis mit micro Penis!        


class PowerPlugBlock(BaseBlock):

    __plug = dict()

    def __init__(self,sensors:list[Sensor],plugName):
        super().__init__(sensors)
        self.__radio = RadioHandler()
        self.__plug = self.__radio.getPowerPlug(plugName)
        
    
    
    
        	
