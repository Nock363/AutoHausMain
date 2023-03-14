import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Actuators.Actuator import Actuator


class Dummy_Actuator(Actuator):

    def __init__(self,name,collection,initialState,config:dict):
        super().__init__(name,collection,initialState,config)

    def set(self,state:bool):
        super().safeToCollection(state)
        logging.debug(f"Set Dummy_Actuator '{super().name}' to {state}")
