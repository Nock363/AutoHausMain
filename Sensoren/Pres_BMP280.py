import sys
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor

from bmp280 import BMP280
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


class Pres_BMP280(Sensor):

    def __init__(self,name:str,pinID:int,collection:str):
        super().__init__(name,collection=collection,queueDepth = 10,pinID=pinID)
        self.bmp280 = BMP280(i2c_dev=SMBus(self.i2cBus))

    def run(self):
        return super().createData({"pressure":self.bmp280.get_pressure()})
    