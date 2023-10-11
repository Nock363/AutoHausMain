import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator


class Dummy_Actuator_Scalar(Actuator):

    def __init__(self,name,collection,config:dict,*args,**kwargs):
        structure = {"state":int}
        super().__init__(name=name,collection=collection,config=config,dataStructure=structure,*args,**kwargs)
        self.__defaultValue = config["defaultValue"]

    def set(self,state):
        
        if(type(state) == bool):
            if(state == True):
                state = self.__defaultValue
                logging.info(f"Dummy_Actuator '{super().name}' wurde mit True angesprochen. Da skalarer Aktor wird der Standardwert {state} verwendet.")
            else:
                logging.info(f"Dummy_Actuator '{super().name}' wurde mit False angesprochen. Da skalarer Aktor wird nichts gemacht.")
                return # do nothing
        
        data = {"state":state}
        super().safeToMemory(data)
        logging.debug(f"Set Dummy_Actuator '{super().name}' to {state}")

    @staticmethod
    def getInputDesc():
        return {
            "state":{"type":int,"desc":"Demo Wert, der eh keine Verwendung findet. aber skalar."}
        }

    @staticmethod
    def getConfigDesc():
        return {
            "defaultValue":{"type":int,"desc":"Standard Wert, der verwendet wird, wenn der Aktor mit True angesprochen wird."} 
        }