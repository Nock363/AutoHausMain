from pymongo import MongoClient
import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

"""
Handler für den Aufbau und dem Verwalten von Verbindungen mit Datenbanken.
Aktuell nur ein MongoHandler für die MongoDB Datenbank, allerdings steht auch die Option einen Handler für einen anderen DB Typen zu entwickeln.
"""


class MongoHandler():

    """
    Handler für die lokale MongoDB Datenbank
    Für weitere Anleitungen: https://www.w3schools.com/python/python_mongodb_getstarted.asp
    """

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db  = self.client.main 
        self.protectedCollections = ["pins","radioDevices"]
    
    def getPin(self,pinID):
        pins = self.db.pins
        return pins.find_one({'pinID':pinID})

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

    def writeToCollection(self,collection,data):
        if(collection in protectedCollections):
            print(f"Collection {collection} ist nicht editierbar!")
            return False
        self.db[collection].insert_one(data)


# def main():
#     mongoHandler = MongoHandler()
#     pinData = mongoHandler.getPin(6)
#     logging.info(f"found pin: {pinData}")
# main()