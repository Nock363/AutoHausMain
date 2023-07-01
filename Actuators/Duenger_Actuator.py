import sys
sys.path.insert(0, '../')
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator
import smbus
import struct



class Duenger_Actuator(Actuator):

    def __init__(self,name,collection,initialState,config:dict):
        dataStructure={"pump":float,"Ec":float}
        super().__init__(name,collection,initialState,config)
        self.__busID = config["pin"] + 2
        self.__pumpNumber = config["pumpNumber"]
        self.__pumpDuration = config["duration"]
        self.__bus = smbus.SMBus(self.__busID)
        self.__address = 0x8
        
        self.set(initialState)


    def set(self,state:bool):

        DATA_FORMAT = 'ii'  # Format string for a float and an integer
        data = struct.pack(DATA_FORMAT, self.__pumpNumber, self.__pumpDuration)
        self.__bus.write_i2c_block_data(self.__address, 0, list(data))

        data = {"pump":self.__pumpDuration}
        super().safeToMemory(data)
    

if __name__ == "__main__":
    duengerActuator = Duenger_Actuator(
        "DuengerPumpe1",
        "DuengerPumpe1",
        False,
        {
            "pin": 3,
            "pumpNumber": 1,
            "duration": 1000               
        }
    )

    duengerActuator.set(True)