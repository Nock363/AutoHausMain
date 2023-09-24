"""
Dieser Sensor hat keine Reale funktion. Er wird lediglich zu Testzwecken verwendet
"""

import math
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor
import random

class DummyRandomFailure_Sensor(Sensor):

    def __init__(self,name:str,collection:str,*args, **kwargs):
        dataStructure={
            "const":{"dataType":float,"unit":None,"range":(1,1)}
        }
        super().__init__(name=name,
                        collection=collection,
                        dataStructure=dataStructure,
                        *args,
                        **kwargs
        )

        self.failProbability=0.8 #TODO: setup over config

    def genData(self):

        #run fails with a certain probability
        if random.random() < self.failProbability:
            logging.debug("DummyRandomFailure_Sensor wird nun mit absicht einen Fehler erzeugen")
            raise Exception("DummyRandomFailure_Sensor ist absichtlich gescheitert.")

        logging.debug("DummyRandomFailure_Sensor ist nicht gescheitert")

        return super().createData({"const":1})