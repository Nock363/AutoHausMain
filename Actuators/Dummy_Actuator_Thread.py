import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator
import threading

class Dummy_Actuator_Thread(Actuator):

    def __init__(self,name,collection,config:dict,*args,**kwargs):
        structure = {"state":bool}
        super().__init__(name=name,collection=collection,config=config,dataStructure=structure,*args,**kwargs)

    def set(self,state:bool):
        if state:
            print("Thread Acturator: True")
            threading.Timer(3, self.set, args=[False]).start()
        else:
            print("Thread Acturator: False")            

        
        
    @staticmethod
    def getConfigDesc():
        return {
        }
    
    @staticmethod
    def getInputDesc():
        return {
            "state":{"type":bool,"desc":"Zustand auf welchen der Aktor gesetzt werden soll"}
        }
    
