from pymongo import MongoClient
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
import os.path
from sqlalchemy import create_engine,inspect, Column, Integer, String, Float, Boolean, DateTime, Index, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
from datetime import datetime
"""
Handler für den Aufbau und dem Verwalten von Verbindungen mit Datenbanken.
Aktuell nur ein MongoHandler für die MongoDB Datenbank, allerdings steht auch die Option einen Handler für einen anderen DB Typen zu entwickeln.
"""
import logging
logging.basicConfig(encoding='utf-8', level=logging.ERROR)

class SqliteHandler:
    dbPath = "/home/user/AutoHausMain/Databases/mainTest1.db"

    def __init__(self):
        self.__engine = create_engine('sqlite:///' + self.dbPath)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
        self.__base = declarative_base()

    def setupTable(self, name: str, structure: dict):
        # dict is like {"time": float, "d1": str, "d2": float, "d3": int}
        # create table if not exists
        inspector = inspect(self.__engine)
        existingTables = inspector.get_table_names()
        if name in existingTables:
            logging.debug("Table already exists")
            return False

        #if time is in structure remove, because it is added automatically with index
        if "time" in structure.keys():
            logging.debug("Time is in structure, removing because it is added automatically with index")
            structure.pop("time")

        # create table based on structure
        class Table(self.__base):
            __tablename__ = name
            id = Column(Integer, primary_key=True)
            time = Column(DateTime, default=datetime.utcnow, index=True)
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

        # #Check if the index already exists before creating it
        # index_name = 'time_index'
        # existing_indexes = inspector.get_indexes(name)
        # if not any(index['name'] == index_name for index in existing_indexes):
        #     index = Index(index_name, Table.time)
        #     index.create(self.__engine)

        # # create index
        # self.__base.metadata.create_all(self.__engine)

        return True
        
    def getAllTables(self):
        inspector = inspect(self.__engine)
        return inspector.get_table_names()        

    def addIndexToTable(self, table: str, index: str):
        inspector = inspect(self.__engine)
        # Check if the table exists in the database
        if table not in inspector.get_table_names():
            print(f"Tabelle '{table}' existiert nicht in der Datenbank.")
            return False

        # Check if the index already exists in the table
        existing_indexes = inspector.get_indexes(table)
        if any(existing_index['name'] == index for existing_index in existing_indexes):
            print(f"Der Index '{index}' existiert bereits in der Tabelle '{table}'.")
            return False

        # Create the index using the SQLAlchemy syntax
        index_object = Index(index, self.__base.metadata.tables[table].c[index])
        index_object.create(self.__engine)

        print(f"Der Index '{index}' wurde zur Tabelle '{table}' hinzugefügt.")
        return True

    def getIndexesFromTable(self, table):
        
        inspector = inspect(self.__engine)
        
        try:
            # Check if the table exists in the database
            if table not in inspector.get_table_names():
                print(f"Tabelle '{table}' existiert nicht in der Datenbank.")
                return None

            # Get the indexes for the specified table
            indexes = inspector.get_indexes(table)

            # Extract and return the index names
            index_names = [index['name'] for index in indexes]

            return index_names
        except Exception as e:  # Catch any SQLAlchemy exceptions
            print(f"Fehler beim Abrufen der Indexe für die Tabelle '{table}': {e}")
            return None

    def writeToTable(self,table:str,data:dict):
        
        inspector = inspect(self.__engine)
        #check if table exists
        if table not in inspector.get_table_names():
            logging.error("Kann nicht in Tabelle schreiben, da diese nicht existiert")
            return False
        
        #check if time is in data and add if not
        if "time" not in data.keys():
            data["time"] = datetime.now()

        #check if data and table structure match
        columns = inspector.get_columns(table)
        #remove id from columns
        columns.pop(0)

        for column in columns:
            if column["name"] not in data.keys():
                logging.error(f"Kann nicht in Tabelle schreiben, da die Daten nicht mit der Struktur der Tabelle übereinstimmen. Fehlendes Attribut: {column['name']}")
                return False
            
        #write to table
        try:
            table = self.__base.metadata.tables[table]
            self.__session.execute(table.insert(), data)
            self.__session.commit()
            return True
        except Exception as e:
            logging.error(f"Fehler beim Schreiben in die Datenbank: {e}")
            return False



    def readFromTable(self, table, filter=None):
        if filter is None:
            return self.__session.query(table).all()
        else:
            return self.__session.query(table).filter_by(**filter).all()


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
    testTable = "sqlAlchemyTestTable5"
    print("setupTable")
    # print(sqliteHandler.setupTable(testTable,{"time":float,"d1":str,"d2":float,"d3":int}))
    
    print("getAllTables")
    # print(sqliteHandler.getAllTables())
    
    print("getIndexesFromTable")
    # sqliteHandler.addIndexToTable(testTable,"index_time")
    # print(sqliteHandler.getIndexesFromTable(testTable))
    print("writeToTable")
    sqliteHandler.writeToTable(testTable,{"time":101.0,"d1":"testStuff","d2":12,"d3":22})
    # print(sqliteHandler.readFromTable(testTable))
    #print(sqliteHandler.find("test",{"d1":"testStuff"}))
    print("done")