from pymongo import MongoClient
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
import os.path
from sqlalchemy import create_engine,inspect, Column, Integer, String, Float, Boolean, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
from datetime import datetime
"""
Handler für den Aufbau und dem Verwalten von Verbindungen mit Datenbanken.
Aktuell nur ein MongoHandler für die MongoDB Datenbank, allerdings steht auch die Option einen Handler für einen anderen DB Typen zu entwickeln.
"""


Base = declarative_base()

class SqliteHandler:
    dbPath = "/home/user/AutoHausMain/Databases/main.db"

    def __init__(self):
        self.__engine = create_engine('sqlite:///' + self.dbPath)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
        self.__base = declarative_base()
        self.__inspector = inspect(self.__engine)

    def setupTable(self,name:str,structure:dict):
        #dict is like {"time":time,"d1":str,"d2":float,"d3":int}
        #create table if not exists
        existingTables = self.__inspector.get_table_names()
        if(name in existingTables):
            return False
            logging.debug("Table already exists")
        

        #if time is not in structure add it
        if("time" not in structure.keys()):
            structure["time"] = float


        #create table based on structure
        class Table(Base):
            __tablename__ = name
            id = Column(Integer, primary_key=True)
        for key,value in structure.items():
            if(value == str):
                setattr(Table,key,Column(String))
            elif(value == float):
                setattr(Table,key,Column(Float))
            elif(value == int):
                setattr(Table,key,Column(Integer))
            elif(value == bool):
                setattr(Table,key,Column(Boolean))
            else:
                #set to unknown
                setattr(Table,key,Column(String))

        #create index for time
        index = Index('time_index', Table.time)
        
        #create table and index
        self.__base.metadata.create_all(self.__engine)
        self.__base.metadata.create_all(self.__engine)
        return True
        
    def getAllTables(self):
        return self.__inspector.get_table_names()        


    
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
        data = self.__db[collection].find({}, {"_id": 0}).sort("time",-1).limit(length)
        return data

    def getAllCollections(self):
        return self.__db.list_collection_names()
        
    def getDataStackSize(self,collection):
        return self.__db[collection].count_documents({})


if __name__ == "__main__":
    sqliteHandler = SqliteHandler()

    print(sqliteHandler.setupTable("sqlAlchemyTestTable",{"time":time,"d1":str,"d2":float,"d3":int}))
    print(sqliteHandler.getAllTables())
    # sqliteHandler.writeToTable("test2",{"time":101,"d1":"testStuff","d2":12,"d3":22})
    # sqliteHandler.readFromTable("test")
    #print(sqliteHandler.find("test",{"d1":"testStuff"}))