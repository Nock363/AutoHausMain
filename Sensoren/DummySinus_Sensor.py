"""
Dieser Sensor hat keine Reale funktion. Er wird lediglich zu Testzwecken verwendet
"""

import math
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor

class DummySinus_Sensor(Sensor):

    def __init__(self,name:str,collection:str,*args, **kwargs):
        dataStructure={
            "sinus":{"dataType":float,"unit":None,"range":(-1.0,1.0)}
        }
        super().__init__(name=name,
                        collection=collection,
                        dataStructure=dataStructure,
                        *args,
                        **kwargs
        )
        self.step = 0.1
        self.counter = 0

    def run(self):
        self.counter = self.counter + self.step
        return super().createData({"sinus":math.sin(self.counter * math.pi)})