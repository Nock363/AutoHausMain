import sys
sys.path.insert(0, '../')
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator
import smbus
import struct



class Duenger_Actuator(Actuator):

    def __init__(self,name,collection,config:dict):
        structure={"pump":int,"duration":float}
        super().__init__(name=name,collection=collection,config=config,dataStructure=structure)
        self.__busID = config["pin"] + 2
        self.__pumpNumber = config["pumpNumber"]
        self.__bus = smbus.SMBus(self.__busID)
        self.__address = 0x8
        

    def set(self,duration):
        DATA_FORMAT = 'ii'  # Format string for a float and an integer
        data = struct.pack(DATA_FORMAT, self.__pumpNumber, int(duration))
        logging.debug(f"Set Duenger_Actuator: pump {self.__pumpNumber} for {duration} milliseconds")
        self.__bus.write_i2c_block_data(self.__address, 0, list(data))
        data = {"pump":self.__pumpNumber,"duration":duration}
        super().safeToMemory(data)
    
    def getInputDesc(self):
        return {
            "duration":{"type":int,"desc":"Milliseconkunden, die die Pumpe laufen soll"}            
        }

    def getConfigDesc(self):
        return {
            "pin":{"type":int,"desc":"Pin an dem die Pumpe angeschlossen ist(Steht auf der Box)"},
            "pumpNumber":{"type":int,"desc":"Pumpe, die benutzt werden soll (1-3)"}
        }

if __name__ == "__main__":
    duengerActuator = Duenger_Actuator(
        "DuengerPumpe1",
        "DuengerPumpe1",
        {
            "pin": 3,
            "pumpNumber": 1,
            "duration": 1000               
        }
    )

    duengerActuator.set(1000)