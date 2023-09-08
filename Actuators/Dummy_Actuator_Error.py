import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator


class Dummy_Actuator_Error(Actuator):

    def __init__(self,name,collection,config:dict,*args,**kwargs):
        structure = {"state":bool}
        super().__init__(name=name,collection=collection,config=config,dataStructure=structure,*args,**kwargs)

    def set(self,state:bool):
        print("Dummy Actuator Error triggert jetzt absichtlich einen Fehler!")
        raise Exception("Dummy_Actuator_Error hat mit absicht einen Fehler erzeut. Für Testzwecke.")

    @staticmethod
    def getConfigDesc():
        return {
        }
    
    @staticmethod
    def getInputDesc():
        return {
            "state":{"type":bool,"desc":"Zustand auf welchen der Aktor gesetzt werden soll"}
        }