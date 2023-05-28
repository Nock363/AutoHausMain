import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator


class Dummy_Actuator(Actuator):

    def __init__(self,name,collection,initialState,config:dict):
        structure = {"state":bool}
        super().__init__(name=name,collection=collection,initialState=initialState,config=config,dataStructure=structure)
        self.set(initialState)

    def set(self,state:bool):
        data = {"state":state}
        super().safeToMemory(data)
        logging.debug(f"Set Dummy_Actuator '{super().name}' to {state}")
