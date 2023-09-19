import sys
sys.path.insert(0, '../')
from Handler.WirelessHandler import RadioHandler
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator
import threading

class Plug433MhzPing_Actuator(Actuator):

    def __init__(self,name,collection,config:dict,*args,**kwargs):
        structure={"state":bool}
        super().__init__(name,collection,config,structure,*args,**kwargs)
        self.codeOn = config["codeOn"]
        self.codeOff= config["codeOff"]
        self.pulseLength = config["pulseLength"]     
        self.radioHandler = RadioHandler()
        self.initialState = config["initialState"]   
        self.pingIsRunning = False
        self.pingTime = config["pingTime"]
        

        self.set(config["initialState"])
        
    def set(self,state:bool):

        if(self.pingIsRunning == True):
            logging.debug(f"Plug433MhzPing_Actuator {super().name} pingt gerade und kann nicht geschaltet werden.")

        print(f"set {self.name} to {state}")

        if(state == True):
            code = self.codeOn
        else:
            code = self.codeOff
        
        success = self.radioHandler.sendCode(code=code,repeats=20,pulseLength=self.pulseLength)
        if(success):
            data = {"state":state}
            super().safeToMemory(data)    

            if(state != self.initialState):
                self.pingThread = threading.Timer(self.pingTime, self.__endPing, [])
                print("startPing")
                self.pingThread.start()
                self.pingIsRunning = True


    def __endPing(self):
        print("endPing")
        self.pingIsRunning = False
        self.set(self.initialState)

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