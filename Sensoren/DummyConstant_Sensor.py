"""
Dieser Sensor hat keine Reale funktion. Er wird lediglich zu Testzwecken verwendet
"""

import math
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor

class DummyConstant_Sensor(Sensor):

    def __init__(self,name:str,pinID,collection:str,*args, **kwargs):
        dataStructure = {"const":float}
        super().__init__(name=name,
                        collection=collection,
                        pinID = pinID,
                        dataStructure=dataStructure,
                        range=(-1,1),
                        *args,
                        **kwargs
        )
        

    def run(self):
        return super().createData({"const":1})