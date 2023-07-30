import sys
import logging
import smbus

from Sensoren.Sensor import Sensor
#pip3 install adafruit_extended_bus
from adafruit_extended_bus import ExtendedI2C as I2C
#pip3 install adafruit-circuitpython-ahtx0
import adafruit_ahtx0

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class HudTemp_AHT20(Sensor):

    def __init__(self,name:str,pinID:int,collection:str,*args, **kwargs):
        dataStructure={"Hud":float,"Temp":float}
        super().__init__(
            name=name,
            collection=collection,
            pinID = pinID,
            dataStructure=dataStructure,
            range=(0,100),               #TODO: Range nur für Hud angewendet und nicht für Temp
            *args,
            **kwargs)
        #I2C Settings old   
        i2c = I2C(self.i2cBus)
        self.aht20 = adafruit_ahtx0.AHTx0(i2c)
        
        # Define I2C bus number and Arduino slave address
        #self.bus = smbus.SMBus(pinID+2)
        #self.address = 0x38

        
    def run(self):
        humidity = self.aht20.relative_humidity
        temperature = self.aht20.temperature
        return super().createData({"Hud":humidity,"Temp":temperature})
        