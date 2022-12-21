import sys
sys.path.insert(0, 'Handler/')
from DatabaseHandlers import MongoHandler

import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class SoftwareI2CSetup():

    configFile = []
    softwareI2C_Start = -1
    softwareI2C_End = -1

    startTag = "#SOFTWARE_I2C START"
    endTag = "#SOFTWARE_I2C END"


    def __init__(self):
        self.mongoHandler = MongoHandler()

    def readAndClear(self):
        with open("/home/user/AutoHausMain/config_backup_test.txt") as file:
            configFile = file.readlines()
            for i, line in enumerate(configFile):
                
                if self.startTag in line:
                    self.softwareI2C_Start = i
                if self.endTag in line:
                    self.softwareI2C_End = i

            print(f"start: {self.softwareI2C_Start}, end: {self.softwareI2C_End}")

            configFile.pop(0:2)

            # print("_______________")
            # for n in range(self.softwareI2C_Start+1,self.softwareI2C_End):
            #     print(configFile.pop(n))
            # print("_______________")

            for i, line in enumerate(configFile):
                print(f"{i}|{line}")

    # def clearI2CPart(self):







setup = SoftwareI2CSetup()
setup.readAndClear()