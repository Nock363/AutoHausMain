"""
Dieser Sensor hat keine Reale funktion. Er wird lediglich zu Testzwecken verwendet
"""

import math
import logging
import time
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor


class DummySetup_Sensor(Sensor):

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
        
        
        if(super().active):
            #delay die initialisierung künstlich
            logging.info("DummySetup_Sensor:Delay setup for 10 seconds.")
            time.sleep(10)
            logging.info("DummySetup_Sensor:Setup done.")
        else:
            logging.debug("DummySetup_Sensor deaktiviert, deswegen kein Delay")

    def run(self):
        return super().createData({"const":1})