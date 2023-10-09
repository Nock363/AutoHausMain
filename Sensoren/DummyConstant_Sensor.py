"""
Dieser Sensor hat keine Reale funktion. Er wird lediglich zu Testzwecken verwendet
"""

import math
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor

class DummyConstant_Sensor(Sensor):

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
        

    def genData(self):
        return super().createData({"const":1})