from pymongo import MongoClient
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
import os.path

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
        self.__db  = self.client.main 
        self.protectedCollections = ["pins","radioDevices"]
    
    def getPin(self,pinID):
        pins = self.__db.pins
        return pins.find_one({'pinID':pinID})

    def getAllPins(self, mode="all", order=1):
        """Gibt alle Pins aus der Datenbank wieder
           mode = [all|I2C] Standard "all"
           Filtert nach dem Modus des Pins
           order =[1|-1] Standard 1
           Sortiert nach der Pin-Nummer aufsteigned(1) oder absteigend(-1)
        """
        pins = self.__db.pins
        if(mode == "all"):
            ret =pins.find({},{ "field_to_exclude": 0 })
        else:
            ret =pins.find(filter={"mode":mode},projection={ "_id": 0 })

        return ret.sort("pinID",order)

    def writeToCollection(self,collection,data):
        if(collection in self.protectedCollections):
            print(f"Collection {collection} ist nicht editierbar!")
            return False
        self.__db[collection].insert_one(data)

    def addSensor(self,name:str,pinID:int,sensorClass:str,intervall:float=1.0,active:bool=True):


        # if(os.path.isfile(script) == False):
        #     debugger.error(f"'{script}' existiert nicht!(Gebe den Pfad des skriptes an)")
        #     return False

        filter = {"name":name}
        if(self.__db.sensors.find_one(filter) != None):
            logging.error(f"Der Name {name} existiert bereits!")
            return False

        self.__db.sensors.insert_one({"active":active,"name":name,"pinID":pinID,"class":sensorClass,"intervall":intervall})
        return True

    def getAllSensors(self,filter={}):
        sensors = self.__db.sensors
        return sensors.find(filter)

    def getSensors(self,active:bool=True):
        filter = {"active":True}
        sensors = self.__db.sensors
        return sensors.find(filter)

    def getSinlgeSensor(self,filter):
        sensors = self.__db.sensors
        return sensors.find_one(filter)

    def addActuator(self,name:str,type:str,collection:str,config:dict,active:bool=True):
        filter = {"name":name}
        if(self.__db.actuators.find_one(filter) != None):
            logging.error(f"Der Name {name} existiert bereits!")
            return False

        self.__db.actuators.insert_one({"active":active,"name":name,"type":type,"collection":collection,"config":config})
        return True

    def getActuators(self,active:bool=True):
        filter = {"active":True}
        actuators = self.__db.actuators
        return actuators.find(filter)

    def getAllActuators(self):
        actuators = self.__db.actuators
        return actuators.find()


    def getSingleActuator(self,filter):
        actuators = self.__db.actuators
        return actuators.find_one(filter)

    def addLogic(self,name,controller:str,inputs:list[dict],outputs:list[dict],active:bool=True):
        filter = {"name":name}
        if(self.__db.logics.find_one(filter) != None):
            logging.error(f"Der Name {name} existiert bereits!")
            return False

        self.__db.logics.insert_one({"active":active,"name":name,"controller":controller,"inputs":inputs,"outputs":outputs})
        return True

    def getAllLogics(self):
        return self.__db.logics.find()

    def getDataFromCollection(self,collection:str,length:int):
        data = self.__db[collection].find().sort("time",-1).limit(length)
        return data

# def main():
#     mongoHandler = MongoHandler()
#     pinData = mongoHandler.getPin(6)
#     logging.info(f"found pin: {pinData}")
# main()