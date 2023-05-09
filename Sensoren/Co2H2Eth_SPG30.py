import sys
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor

from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_sgp30


class Co2H2Eth_SPG30(Sensor):

    def __init__(self,name:str,pinID:int,collection:str):
        super().__init__(name,collection="Co2H2Eth",queueDepth = 10,pinID=pinID)
        i2c = I2C(self.i2cBus)
        self.spg30 = adafruit_sgp30.Adafruit_SGP30(i2c)
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
        self.sgp30.set_iaq_baseline(0x8973, 0x8AAE)
        self.sgp30.set_iaq_relative_humidity(celsius = 20, relative_humidity=60) #hier werte aus datenbank einpflegen



    def run(self):
        return super().createData({"CO2":self.sgp30.eCO2,"H2":self.sgp30.H2,"Ethanol":self.sgp30.Ethanol})
    