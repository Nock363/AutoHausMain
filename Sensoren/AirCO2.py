import math
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor
from Handler.SerialHandler import SerialHandler

class AirCO2(Sensor):

    def __init__(self,name:str,pinID,collection:str,*args, **kwargs):
        dataStructure={
            "AirCO2":{"dataType":float,"unit":"ppm","range":None},
            "TVOC":{"dataType":float,"unit":"?","range":None}
        }
        
        super().__init__(name=name,
                        collection=collection,
                        pinID = pinID,
                        dataStructure=dataStructure,
                        *args,
                        **kwargs)
        
        self.__deviceName = "SenseIT" #TODO AUslesen aus der Config anstatt hardcoded.
        self.__serialHandler = SerialHandler(baudrate=19200)
        #prüfe ob benötigtes Device vorhanden ist.
        if(self.__serialHandler.check_for_device(self.__deviceName) == False):
            raise Exception(f"Gerät {self.__deviceName} nicht vom SerialHandler gefunden")


    def run(self):
        command = {"command":"CCS811Value"}
        result = self.__serialHandler.send_dict(self.__deviceName,command,readResponse=True)
        #raise Exception(f"Gerät {self.__deviceName} schreibt: {result}")
        return super().createData(result)