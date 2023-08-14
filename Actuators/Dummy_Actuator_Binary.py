import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator


class Dummy_Actuator_Binary(Actuator):

    def __init__(self,name,collection,config:dict):
        structure = {"state":bool}
        super().__init__(name=name,collection=collection,config=config,dataStructure=structure)

    def set(self,state:bool):
        data = {"state":state}
        super().safeToMemory(data)
        logging.debug(f"Set Dummy_Actuator '{super().name}' to {state}")

    @staticmethod
    def getConfigDesc():
        return {
        }
    
    @staticmethod
    def getInputDesc():
        return {
            "state":{"type":bool,"desc":"Zustand auf welchen der Aktor gesetzt werden soll"}
        }