import sys
import time
sys.path.insert(0, '../')
from Handler.WirelessHandler import RadioHandler
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator
from enum import Enum
import RPi.GPIO as GPIO

'''
Demo Config:
{
    "active": true,
    "name": "Pumpe 1",
    "type": "Plug433Mhz_Actuator",
    "collection": "GPIO_Perestaltik_Actuator",
    "config": {
        "initialState": false,
        "pin":2
    }
}


'''

pins=[22,9,23,24,8]


#create Enums for the different pins
class GPIO_Pins(Enum):
    #pin 1 is gpio 22
    PIN1 = 22
    PIN2 = 9
    PIN3 = 23
    PIN4 = 24
    PIN5 = 8


class GPIO_Perestaltik_Actuator(Actuator):

    def __init__(self,name,collection,config:dict,*args,**kwargs):
        structure={"state":bool}
        super().__init__(name,collection,config,structure,*args,**kwargs)
        
        if(not "pin" in config):
            raise ValueError("No pin specified")
        
        if(not "initialState" in config):
            raise ValueError("No initialState specified")

        pinID = config["pin"]
        if(pinID <= 0 or pinID > len(pins)):
            raise ValueError("Pin ID out of range")
        
        self.gpioPin = pins[pinID-1]

        self.initialState = config["initialState"]

        self.runtime = config["runtime"]


        #set the pin to output
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpioPin,GPIO.OUT)

        #set the initial state
        self.set(self.initialState)

    def set(self,state:bool):

        if(state == "false"):
            state = False
            GPIO.output(self.gpioPin,state)

        elif(state == "true"):
            state = True
        elif(type(state) == str):
            raise TypeError(f"State '{state}' ist kein bool und auch kein 'true'/'false'")

        #set the pin to the given state
        GPIO.output(self.gpioPin,state)
        time.sleep(self.runtime)
        GPIO.output(self.gpioPin,False)
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