import sys
sys.path.insert(0, '../')
from abc import ABC, abstractmethod
from Sensoren.Sensor import Sensor
from Handler.WirelessHandler import RadioHandler
from Utils import tools

class Controller():
    __mask : list[str]
    __lastValue = None


    def __init__(self,mask:list[str],config:dict = None):
        self.__mask = mask

        #validate config
        self.validateConfig(config)

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
    
    @abstractmethod
    def getConfigDescription(self) -> dict:
        raise NotImplementedError("getConfigDescription muss implementiert werden")

    def validateConfig(self,config:dict):
        configDesc = self.getConfigDescription()
        for (key,value) in config.items():
            
            if(configDesc[key]["type"] == list):
                elementDesc = configDesc[key]["element"]
                
                #iterate through elements in list
                for(element in config[key]):
                    if(not isinstance(element,elementDesc["type"])):
                        raise TypeError(f"Der Wert {element} für {key} ist nicht vom Typen {elementDesc['type']}"

                    #if type is str check if format exist in elementDesc and if it matches
                    if(elementDesc["type"] == str and "format" in elementDesc):
                        if(elementDesc["format"] == "time"):
                            if(not tools.isValidTimeFormat(element)):
                                raise ValueError(f"Der Wert {element} für {key} ist nicht vom Format {elementDesc['format']}")



            else(isinstance(value,configDesc[key]["type"])):
                raise TypeError(f"Der Wert {value} für {key} ist nicht vom Typen {configDesc[key]['type']}"

    def getInfo(self):
        controllerName = self.__class__.__name__
        
        configDesc = self.getConfigDescription()
        configDesc = tools.dictValuesToString(configDesc)

        return {
            "name": controllerName,
            "mask": self.__mask,
            "config": self.__config,
            "configDescription": configDesc,
        }

    def update(self,config:dict):
        pass