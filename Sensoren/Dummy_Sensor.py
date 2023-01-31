"""
Dieser Sensor hat keine Reale funktion. Er wird lediglich zu Testzwecken verwendet
"""

import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor

class Dummy_Sensor(Sensor):

    def __init__(self,pinID):
        super().__init__(collection="DummySensor", pinID = pinID)


    def run(self):
        return super().createData({"dummmy":42})