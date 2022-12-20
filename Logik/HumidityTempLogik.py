import sys
sys.path.insert(0, '../Handler/')
from DatabaseHandlers import MongoHandler
sys.path.insert(0, '../libs/AHT20')
import AHT20

import logging
import time
import datetime



class HumidityTempLogik():

    

    def __init__(self, pinID):
        self.mongoHandler = MongoHandler()
        result = self.mongoHandler.getPin(pinID)
        self.sda = result["dataPin1"]
        self.scl = result["dataPin2"]
        self.aht20 = AHT20.AHT20(3)

    def run(self,humidity=True,temperature=True):

        retValue = {}

        retValue["datetime"] = datetime.datetime.now()

        if(humidity):
            retValue["humidity"] = self.aht20.get_humidity()
        else:
            retValue["humidity"] = -1

        if(temperature):
            retValue["temperature"] = self.aht20.get_temperature()
        else:
            retValue["humidity"] = -1

        return retValue

        

#test
print("start test")
humidityTempLogik = HumidityTempLogik(7)
for n in range(10):
    print(humidityTempLogik.run())
    time.sleep(1)