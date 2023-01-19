import sys

#pip3 install adafruit_extended_bus
from adafruit_extended_bus import ExtendedI2C as I2C
#pip3 install adafruit-circuitpython-ahtx0
import adafruit_ahtx0

import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


from Sensor import Sensor

class HudTemp_AHT20(Sensor):

    def __init__(self,pinID):
        super().__init__(collection="HumidityTemp",queueDepth = 10,pinID=pinID)
        i2c = I2C(self.i2cBus)
        self.aht20 = adafruit_ahtx0.AHTx0(i2c)


    def captureData(self):
        data = {"humidity":self.aht20.relative_humidity,"temperature":self.aht20.temperature}
        return data

    def run(self):
        print("run")
        print(self.captureData())