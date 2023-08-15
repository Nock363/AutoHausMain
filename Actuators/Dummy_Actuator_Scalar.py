import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator


class Dummy_Actuator_Scalar(Actuator):

    def __init__(self,name,collection,config:dict,*args,**kwargs):
        structure = {"state":int}
        super().__init__(name=name,collection=collection,config=config,dataStructure=structure,*args,**kwargs)

    def set(self,state:int):
        data = {"state":state}
        super().safeToMemory(data)
        logging.debug(f"Set Dummy_Actuator '{super().name}' to {state}")

    @staticmethod
    def getInputDesc():
        return {
            "state":{"type":int,"desc":"Demo Wert, der eh keine Verwendung findet"}
        }

    @staticmethod
    def getConfigDesc():
        return {
            "initialState":{"type":bool,"desc":"Initialer Zustand des Aktors"} 
        }