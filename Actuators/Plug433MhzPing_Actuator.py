import sys
sys.path.insert(0, '../')
from Handler.WirelessHandler import __radioHandler
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator
import time

class Plug433MhzPing_Actuator(Actuator):

    def __init__(self,name,collection,config:dict,*args,**kwargs):
        structure={"state":bool}
        super().__init__(name,collection,config,structure,*args,**kwargs)
        self.codeOn = config["codeOn"]
        self.codeOff= config["codeOff"]
        self.__pulseLength = config["pulseLength"]     
        self.__radioHandler = __radioHandler()
        self.__initialState = config["initialState"]   
        self.__pingIsRunning = False
        self.__pingTime = config["pingTime"]
        self.__repeats = config["repeats"]

        self.__setState(self.__initialState)

    def __setState(self,state:bool):
        if(state == True):
            code = self.codeOn
        else:
            code = self.codeOff
        
        success = self.__radioHandler.sendCode(code=code,repeats=self.__repeats,pulseLength=self.__pulseLength)
        if(success):
            data = {"state":state}
            super().safeToMemory(data)
    
    def set(self,state:bool):

        if(state == False):
            logging.error("Plug433MhzPing_Actuator springt nur auf True als input state an. Wurde allerdings mit False als State aufgerufen.")
            return
        
        self.__setState(True)
        self.__setState(True)
        time.sleep(self.__pingTime)
        self.__setState(True)
        self.__setState(True)
        

        

    @staticmethod  
    def getConfigDesc():
        return {
            "initialState":{"type":bool,"desc":"Initialer Zustand des Aktors. Dieser Zustand ist der standard zustand. Welcher gilt wenn der ping nicht läuft."},
            "codeOn":{"type":str,"desc":"Code welcher gesendet wird wenn der Aktor eingeschaltet werden soll"},
            "codeOff":{"type":str,"desc":"Code welcher gesendet wird wenn der Aktor ausgeschaltet werden soll"},
            "pulseLength":{"type":int,"desc":"Länge des Pulses welcher gesendet wird"},
            "pingTime":{"type":float,"desc":"Zeit in Sekunden zwischen zwei Pings"}
        }
    
    @staticmethod
    def getInputDesc():
        return {
            "state":{"type":bool,"desc":"Zustand auf welchen der Aktor gesetzt werden soll"}
        }