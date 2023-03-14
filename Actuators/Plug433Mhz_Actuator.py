import sys
sys.path.insert(0, '../')
from Handler.WirelessHandler import RadioHandler
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator


class Plug433Mhz_Actuator(Actuator):

    def __init__(self,name,collection,initialState,config:dict):
        super().__init__(name,collection,initialState,config)
        self.codeOn = config["codeOn"]
        self.codeOff= config["codeOff"]
        self.pulseLength = config["pulseLength"]     
        self.radioHandler = RadioHandler()   
        self.set(initialState)

    def set(self,state:bool):

        if(super().hasStateChanged(state) == True):
            if(state == True):
                code = self.codeOn
            else:
                code = self.codeOff
                
            success = self.radioHandler.sendCode(code=code,repeats=20,pulseLength=self.pulseLength)
            if(success):
                super().safeToCollection(state)
        