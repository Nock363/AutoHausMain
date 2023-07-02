import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator


class Dummy_Actuator_Scalar(Actuator):

    def __init__(self,name,collection,config:dict):
        structure = {"state":int}
        super().__init__(name=name,collection=collection,config=config,dataStructure=structure)

    def set(self,state:int):
        data = {"state":state}
        super().safeToMemory(data)
        logging.debug(f"Set Dummy_Actuator '{super().name}' to {state}")

    def getInputDesc(self):
        return {
            "state":{"type":int,"desc":"Demo Wert, der eh keine Verwendung findet"}
        }

    def getConfigDesc(self):
        return {
            "initialState":{"type":bool,"desc":"Initialer Zustand des Aktors"} 
        }