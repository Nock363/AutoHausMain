import sys
sys.path.insert(0, '../')
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator
import smbus
import struct
from Handler.SerialHandler import SerialHandler


class Duenger_Actuator(Actuator):

    def __init__(self,name,collection,config:dict,*args,**kwargs):
        structure={"pump":int,"runtime":int}
        super().__init__(name=name,collection=collection,config=config,dataStructure=structure,*args,**kwargs)
        self.__deviceName = config["deviceName"]
        self.__pump = config["pump"]
        self.__runtime = config["runtime"]
        
        if(super().active):
            self.__serialHandler = SerialHandler(baudrate=19200)
            #prüfe ob benötigtes Device vorhanden ist.
            if(self.__serialHandler.check_for_device(self.__deviceName) == False):
                raise Exception(f"Gerät {self.__deviceName} nicht vom SerialHandler gefunden")


    def set(self,state):
        if(super().active):
            
            #HOTFIX TODO: Typsichere Lösung finden
            
            if(type(state) == str):
                try:
                    state = int(state)
                except:
                    pass
                    
            if(type(state) == bool):
                if(state):
                    command = {"command":"setPump","pump":self.__pump,"runtime":self.__runtime}
                    self.__serialHandler.send_dict(self.__deviceName,command)
                    super().safeToMemory({"pump":self.__pump,"runtime":self.__runtime})
            elif(type(state) == int):
                command = {"command":"setPump","pump":self.__pump,"runtime":state}
                self.__serialHandler.send_dict(self.__deviceName,command)
                super().safeToMemory({"pump":self.__pump,"runtime":state})
                
        else:
            logging.error(f"{self.__name} ist nicht aktiv, wurde aber versucht per run() ausgeführt werden. Das sollte nicht passieren.")
        

    @staticmethod
    def getInputDesc():
        return {
            "runtime":{"type":int,"desc":"Milliseconkunden, die die Pumpe laufen soll"}            
        }

    @staticmethod
    def getConfigDesc():
        return {
            "deviceName":{"type":str,"desc":"Name, den das Geräte hat, welches seriel angeschlossen ist. Wird vom geräte per command 'info' abgefragt."},
            "pump":{"type":int,"desc":"Pumpe, die benutzt werden soll (1-3)"},
            "runtime":{"type":int,"desc":"Zeit die die Pumpe laufen soll"},
            "defaultValue":{"type":int,"desc":"Standard Wert, der verwendet werden kann, wenn man den Aktor vom UserInterface steuern möchte"} 
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