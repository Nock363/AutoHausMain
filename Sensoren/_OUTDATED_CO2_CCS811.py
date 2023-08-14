import sys
import logging
import busio
import adafruit_ccs811
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

from Sensoren.Sensor import Sensor


#pip3 install adafruit_extended_bus
from adafruit_extended_bus import ExtendedI2C as I2C


class CO2_CCS811(Sensor):
    #TODO: Auf neue Sensor Struktur anpassen
    def __init__(self,name:str,pinID:int,collection:str):
        super().__init__(name,collection,queueDepth = 10,pinID=pinID)
        i2c = I2C(self.i2cBus)
        self.ccs =  adafruit_ccs811.CCS811(i2c)

    def run(self):
        return super().createData({"CO2":self.ccs.eco2,"TVOC":self.ccs.tvoc})
        