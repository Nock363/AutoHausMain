"""
Dieser Sensor hat keine Reale funktion. Er wird lediglich zu Testzwecken verwendet
"""

import math
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor
from Handler.SerialHandler import SerialHandler

class DuengerPump_Sensor(Sensor):

    def __init__(self,name:str,collection:str,*args, **kwargs):
        dataStructure={
            "runtimePump1":{"dataType":int,"unit":"ms","range":None},
            "runtimePump2":{"dataType":int,"unit":"ms","range":None},
            "runtimePump3":{"dataType":int,"unit":"ms","range":None}
        }
        
        super().__init__(name=name,
                        collection=collection,
                        dataStructure=dataStructure,
                        *args,
                        **kwargs)
        
        self.__deviceName = "Düngeranlage" #TODO Auslesen aus der Config anstatt hardcoded.
        
        if(super().active):
            self.setup()
            
    def setup(self):
        self.__serialHandler = SerialHandler(baudrate=19200)
        #prüfe ob benötigtes Device vorhanden ist.
        if(self.__serialHandler.check_for_device(self.__deviceName) == False):
            raise Exception(f"Gerät {self.__deviceName} nicht vom SerialHandler gefunden")

        


    def genData(self):
        if(super().active):
            command = {"command":"pumpStatus"}
            result = self.__serialHandler.send_dict(self.__deviceName,command,readResponse=True)
            return super().createData(result)
        else:
            logging.error(f"{self.__name} ist nicht aktiv, wurde aber versucht per run() ausgeführt werden. Das sollte nicht passieren.")
        