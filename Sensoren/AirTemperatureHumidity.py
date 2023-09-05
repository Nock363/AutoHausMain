import math
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor
from Handler.SerialHandler import SerialHandler

class AirTemperatureHumidity(Sensor):

    def __init__(self,name:str,collection:str,*args, **kwargs):
        dataStructure={
            "AirTemperature":{"dataType":float,"unit":"Grad","range":(-20,100)},
            "AirHumidity":{"dataType":float,"unit":"Percent","range":(0,100)},
        }
        
        super().__init__(name=name,
                        collection=collection,
                        dataStructure=dataStructure,
                        *args,
                        **kwargs)
        
        self.__deviceName = "SenseIT" #TODO AUslesen aus der Config anstatt hardcoded.
        self.__serialHandler = SerialHandler(baudrate=19200)
        #prüfe ob benötigtes Device vorhanden ist.
        if(self.__serialHandler.check_for_device(self.__deviceName) == False):
            raise Exception(f"Gerät {self.__deviceName} nicht vom SerialHandler gefunden")


    def run(self):
        command = {"command":"AHT20Value"}
        result = self.__serialHandler.send_dict(self.__deviceName,command,readResponse=True)
        #raise Exception(f"Gerät {self.__deviceName} schreibt: {result}")
        return super().createData(result)