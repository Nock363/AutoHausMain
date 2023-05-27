"""
Dieser Sensor hat keine Reale funktion. Er wird lediglich zu Testzwecken verwendet
"""

import math
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor

class DummySinus_Sensor(Sensor):

    def __init__(self,name:str,pinID,collection:str):
        dataStructure = {"sinus":float}
        super().__init__(name,collection=collection, pinID = pinID, dataStructure=dataStructure)
        self.step = 0.1
        self.counter = 0

    def run(self):
        self.counter = self.counter + self.step
        return super().createData({"sinus":math.sin(self.counter * math.pi)})