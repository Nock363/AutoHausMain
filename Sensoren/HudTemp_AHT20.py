import sys
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor


#pip3 install adafruit_extended_bus
from adafruit_extended_bus import ExtendedI2C as I2C
#pip3 install adafruit-circuitpython-ahtx0
import adafruit_ahtx0


class HudTemp_AHT20(Sensor):

    def __init__(self,name:str,pinID:int):
        super().__init__(name,collection="HumidityTemp",queueDepth = 10,pinID=pinID)
        i2c = I2C(self.i2cBus)
        self.aht20 = adafruit_ahtx0.AHTx0(i2c)

    def run(self):
        return super().createData({"humidity":self.aht20.relative_humidity,"temperature":self.aht20.temperature})
        