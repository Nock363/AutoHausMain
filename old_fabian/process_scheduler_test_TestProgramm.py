import sys
sys.path.insert(0, '../python_sensor_aht20/')
import AHT20
from datetime import datetime
import pymongo

import logging
import time

class Test():


    def __init__(self,sleepTime, signature):
        self.sleepTime = sleepTime
        self.signature = signature
        self.aht20 = AHT20.AHT20()
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client.test



    def run(self):
        while True:
            dt = datetime.now()
            #code goes here
            logging.info(self.signature)
            mydict = { "Time": dt, "Temperature": self.aht20.get_temperature(), "Humidity": self.aht20.get_humidity(), "Message":self.signature}
            self.db["processesTest"].insert_one(mydict)

            time.sleep(self.sleepTime)

