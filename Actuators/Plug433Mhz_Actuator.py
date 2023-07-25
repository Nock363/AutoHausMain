import sys
sys.path.insert(0, '../')
from Handler.WirelessHandler import RadioHandler
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator


class Plug433Mhz_Actuator(Actuator):

    def __init__(self,name,collection,config:dict):
        structure={"state":bool}
        super().__init__(name,collection,config,dataStructure=structure)
        self.codeOn = config["codeOn"]
        self.codeOff= config["codeOff"]
        self.pulseLength = config["pulseLength"]     
        self.radioHandler = RadioHandler()   
        self.set(config["initialState"])

    def set(self,state:bool):

        print(f"set {self.name} to {state}")

        # if(super().hasStateChanged(state) == True):
        if(state == True):
            code = self.codeOn
        else:
            code = self.codeOff
            
        success = self.radioHandler.sendCode(code=code,repeats=20,pulseLength=self.pulseLength)
        if(success):
            data = {"state":state}
            super().safeToMemory(data)
        
    def getConfigDesc(self):
        return {
            "initialState":{"type":bool,"desc":"Initialer Zustand des Aktors"} 
        }
    
    def getInputDesc(self):
        return {
            "state":{"type":bool,"desc":"Zustand auf welchen der Aktor gesetzt werden soll"}
        }