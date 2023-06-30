"""
Dieser Sensor hat keine Reale funktion. Er wird lediglich genutzt um zu testen, ob das System passend mit fehlern getriggert von einem sensor arbeiten kann
"""

import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor

class ErrorTest_Sensor(Sensor):

    def __init__(self,name:str,pinID,collection:str):
        super().__init__(name,collection=collection, pinID = pinID, dataStructure={})


    def run(self):
        #throw error
        raise Exception("Test Error. Getriggert von ErrorTest_Sensor")
        return None