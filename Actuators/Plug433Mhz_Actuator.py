import sys
sys.path.insert(0, '../')
from Handler.WirelessHandler import RadioHandler
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator


class Plug433Mhz_Actuator(Actuator):

    def __init__(self,name,collection,config:dict,*args,**kwargs):
        structure={"state":bool}
        super().__init__(name,collection,config,structure,*args,**kwargs)
        self.codeOn = config["codeOn"]
        self.codeOff= config["codeOff"]
        self.pulseLength = config["pulseLength"]     
        self.radioHandler = RadioHandler()   
        
        if("repeats" in config.keys()):
            self.__repeats = config["repeats"]
        else:
            self.__repeats = 30

        if("sendNTimes" in config.keys()):
            self.__sendNTimes = config["sendNTimes"]
        else:
            self.__sendNTimes = 1

        self.set(config["initialState"])

    def set(self,state:bool):

        for i in range(self.__sendNTimes):
            print(f"set {self.name} to {state}")

            # if(super().hasStateChanged(state) == True):
            if(state == True):
                code = self.codeOn
            else:
                code = self.codeOff
                
            success = self.radioHandler.sendCode(code=code,repeats=self.__repeats,pulseLength=self.pulseLength)
            if(success):
                data = {"state":state}
                super().safeToMemory(data)

    @staticmethod  
    def getConfigDesc():
        return {
            "initialState":{"type":bool,"desc":"Initialer Zustand des Aktors"} 
        }
    
    @staticmethod
    def getInputDesc():
        return {
            "state":{"type":bool,"desc":"Zustand auf welchen der Aktor gesetzt werden soll"}
        }