import sys
sys.path.insert(0, '../')
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator
import smbus
import struct
from Handler.SerialHandler import SerialHandler


class Duenger_Actuator(Actuator):

    def __init__(self,name,collection,config:dict):
        structure={"pump":int,"runtime":int}
        super().__init__(name=name,collection=collection,config=config,dataStructure=structure)
        self.__deviceName = config["deviceName"]
        self.__pump = config["pump"]
        self.__runtime = config["runtime"]
        self.__serialHandler = SerialHandler(baudrate=19200)
        
        #prüfe ob benötigtes Device vorhanden ist.
        if(self.__serialHandler.check_for_device(self.__deviceName) == False):
            raise Exception(f"Gerät {self.__deviceName} nicht vom SerialHandler gefunden")


    def set(self,state:bool):
        if(state):
            command = {"command":"setPump","pump":self.__pump,"runtime":self.__runtime}
            self.__serialHandler.send_dict(self.__deviceName,command)
            #TODO: Eintragen in die Datenbank fixxen
            super().safeToMemory({"pump":self.__pump,"runtime":self.__runtime})

    def getInputDesc(self):
        return {
            "runtime":{"type":int,"desc":"Milliseconkunden, die die Pumpe laufen soll"}            
        }

    def getConfigDesc(self):
        return {
            "deviceName":{"type":str,"desc":"Name, den das Geräte hat, welches seriel angeschlossen ist. Wird vom geräte per command 'info' abgefragt."},
            "pump":{"type":int,"desc":"Pumpe, die benutzt werden soll (1-3)"},
            "runtime":{"type":int,"desc":"Zeit die die Pumpe laufen soll"}
        }

if __name__ == "__main__":
    duengerActuator = Duenger_Actuator(
        "DuengerPumpe_Serial",
        "DuengerPumpe_Serial",
        {
            "deviceName":"Düngeranlage",
            "pump": 1,
            "runtime": 1000               
        }
    )

    duengerActuator.set()