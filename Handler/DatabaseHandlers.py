from pymongo import MongoClient
import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class MongoHandler():

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db  = self.client.main 

    
    def getPin(self,pinID):
        pins = self.db.pins
        return pins.find_one({'pinID':6})

    def getAllPins(self, mode="all", order=1):
        """Gibt alle Pins aus der Datenbank wieder
           mode = [all|I2C] Standard "all"
           Filtert nach dem Modus des Pins
           order =[1|-1] Standard 1
           Sortiert nach der Pin-Nummer aufsteigned(1) oder absteigend(-1)
        """

        pins = self.db.pins

    

        if(mode == "all"):
            ret =pins.find()
        else:
            ret =pins.find(filter={"mode":mode})

        return ret.sort("pinID",order)


    def addPowerPlugToWireless(self,name,codeOn,codeOff):
        radioDevices = self.db.radioDevices
        radioDevices.insert_one({"type":"plug","name":name,"codeOn":codeOn,"codeOff":codeOff,"mode":-1,"lastUsed":0})

    def getWirelessDevices(self,filter={}):
        radioDevices = self.db.radioDevices
        return radioDevices.find(filter=filter)


# def main():
#     mongoHandler = MongoHandler()
#     pinData = mongoHandler.getPin(6)
#     logging.info(f"found pin: {pinData}")
# main()