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
    dbPath = "/home/user/AutoHausMain/Databases/mainTest1.db"

    def __init__(self):
        self.__engine = create_engine('sqlite:///' + self.dbPath)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
        self.__base = declarative_base()
        self.__inspector = inspect(self.__engine)

    def setupTable(self, name: str, structure: dict):
        # dict is like {"time": float, "d1": str, "d2": float, "d3": int}
        # create table if not exists
        existingTables = self.__inspector.get_table_names()
        if name in existingTables:
            logging.debug("Table already exists")
            return False

        # if time is not in structure, add it
        if "time" not in structure.keys():
            structure["time"] = float

        # create table based on structure
        class Table(self.__base):
            __tablename__ = name
            id = Column(Integer, primary_key=True)
        for key, value in structure.items():
            if value == str:
                setattr(Table, key, Column(String))
            elif value == float:
                setattr(Table, key, Column(Float))
            elif value == int:
                setattr(Table, key, Column(Integer))
            elif value == bool:
                setattr(Table, key, Column(Boolean))
            else:
                # set to unknown
                setattr(Table, key, Column(String))

        #create table
        self.__base.metadata.create_all(self.__engine)

        # Check if the index already exists before creating it
        # index_name = 'time_index'
        # existing_indexes = self.__inspector.get_indexes(name)
        # if not any(index['name'] == index_name for index in existing_indexes):
        #     index = Index(index_name, Table.time)
        #     index.create(self.__engine)

        # # create index
        # self.__base.metadata.create_all(self.__engine)
        return True
        
    def getAllTables(self):
        return self.__inspector.get_table_names()        

    def addIndexToTable(self, table, index):
        try:
            # Check if the table exists in the database
            if table not in self.__inspector.get_table_names():
                print(f"Tabelle '{table}' existiert nicht in der Datenbank.")
                return False

            # Create the index using the SQLAlchemy syntax
            index_name = f"{index}_index"
            index_column = index
            index_object = Index(index_name, index_column)
            index_object.create(self.__engine)

            return True
        except Exception as e:  # Catch any SQLAlchemy exceptions
            print(f"Fehler beim Hinzufügen des Indexes zur Tabelle '{table}': {e}")
            return False

    def getIndexesFromTable(self, table):
        
        #self.__base = declarative_base()
        # self.__inspector = inspect(self.__engine)
        
        try:
            # Check if the table exists in the database
            if table not in self.__inspector.get_table_names():
                print(f"Tabelle '{table}' existiert nicht in der Datenbank.")
                return None

            # Get the indexes for the specified table
            indexes = self.__inspector.get_indexes(table)

            # Extract and return the index names
            index_names = [index['name'] for index in indexes]

            return index_names
        except Exception as e:  # Catch any SQLAlchemy exceptions
            print(f"Fehler beim Abrufen der Indexe für die Tabelle '{table}': {e}")
            return None

    def writeToTable(self,table,data:dict):
        # data = {"time": 1234567890.0, "d1": "test", "d2": 1.0, "d3": 1}
        # check if table exists
        if table not in self.__inspector.get_table_names():
            logging.debug(f"Table {table} does not exist")
            return False

        # check if all keys are in table
        columns = self.__inspector.get_columns(table)
        for key in data.keys():
            if key not in columns:
                logging.debug(f"Column {key} does not exist in table {table}")
                return False

        # add data to table
        newEntry = self.__base.classes[table](**data)
        self.__session.add(newEntry)
        self.__session.commit()
        return True

    def readFromTable(self,table,filter=None):
        if(filter == None):
            return self.__session.query(self.__base.classes[table]).all()
        else:
            return self.__session.query(self.__base.classes[table]).filter_by(**filter).all()


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

    print(sqliteHandler.setupTable("sqlAlchemyTestTable15",{"time":time,"d1":str,"d2":float,"d3":int}))
    print(sqliteHandler.getAllTables())
    print(sqliteHandler.getIndexesFromTable("sqlAlchemyTestTable15"))
    # sqliteHandler.writeToTable("sqlAlchemyTestTable6",{"time":101,"d1":"testStuff","d2":12,"d3":22})
    # print(sqliteHandler.readFromTable("sqlAlchemyTestTable6"))
    #print(sqliteHandler.find("test",{"d1":"testStuff"}))