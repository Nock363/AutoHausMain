from sqlalchemy import text,create_engine
from pymongo import MongoClient
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
import os.path

import time
from datetime import datetime
"""
Handler für den Aufbau und dem Verwalten von Verbindungen mit Datenbanken.
Aktuell nur ein MongoHandler für die MongoDB Datenbank, allerdings steht auch die Option einen Handler für einen anderen DB Typen zu entwickeln.
"""
#TODO SQLAlchemy richtig implementieren, nicht nur einfach mit der billo variante wo die querries als string übergeben werden können.
class SqliteHandler():

    dbPath = "/home/user/AutoHausMain/Databases/main.db"

    def __init__(self):
        
        self.__engine = create_engine('sqlite:///' + self.dbPath)
        self.__insertQuerries = self.genInsertQuerries(self.dbPath)

    def __executeQuerry(self,query):
        with self.__engine.begin() as conn:
            result = conn.execute(text(query))
            #return as list
            return result

    def __executeInsertQuerry(self, query, values):
        # Replace ? in query with values; when value is string add ' around it
        for value in values:
            if isinstance(value, str):
                query = query.replace("?", f"'{value}'", 1)
            elif isinstance(value, datetime):
                query = query.replace("?", f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'", 1)
            else:
                query = query.replace("?", str(value), 1)

        with self.__engine.begin() as conn:
            result = conn.execute(text(query))
            # return as list
            return result

    def setupTable(self,name:str,structure:dict):
        #dict is like {"time":time,"d1":str,"d2":float,"d3":int}
        #create table if not exists

        #translate python data types to sql data types
        sqlTypes = {
            str: "TEXT",
            float: "REAL",
            int: "INTEGER",
            bool: "BOOLEAN",
            bytes: "BLOB"
        }


        for key,value in structure.items():
            
            if(value not in sqlTypes):
                structure[key] = "UNKNOWN"
            else:
                structure[key] = sqlTypes[value]


        if("time" not in structure):
            structure["time"] = "DATETIME"

        #add id to structure as primary key and autoincrement

        query = f"CREATE TABLE IF NOT EXISTS {name} (id INTEGER PRIMARY KEY AUTOINCREMENT, " + ",".join([f"{key} {value}" for key,value in structure.items()]) + ")"

        self.__executeQuerry(query)
        self.__executeQuerry(f'CREATE INDEX IF NOT EXISTS time_index ON {name} (time)')
        self.__insertQuerries = self.genInsertQuerries(self.dbPath)

    def genInsertQuerries(self,database_name):
    
            
        table_names = self.__executeQuerry("SELECT name FROM sqlite_master WHERE type='table';")
        insert_queries = []

        # INSERT-Queries für jede Tabelle generieren
        for table in table_names:


            table_name = table[0]
            if(table_name == "sqlite_sequence"):
                continue

            # Spaltennamen abrufen
            columns = self.__executeQuerry(f"PRAGMA table_info({table_name})")
            column_names = [column[1] for column in columns if column[1] != 'id']

            # Platzhalter für Werte generieren
            value_placeholders = ", ".join(['?'] * len(column_names))

            # INSERT-Query für jeden Datensatz generieren
            insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({value_placeholders})"

            # Query zur Liste hinzufügen
            insert_queries.append({"name":table_name,"querry":insert_query,"columns":column_names})

        return insert_queries

    def addIndexToTable(self, table, index):
        try:
            self.__executeQuerry(f'CREATE INDEX IF NOT EXISTS {index}_index ON {table} ({index})')
            return True
        except Exception as e:
            print(f"Fehler beim Hinzufügen des Indexes zur Tabelle '{table}': {e}")
            return False

    def checkForIndex(connection, table, index):
        try:
            index_info = self.__executeQuerry(f"PRAGMA index_info({index}_index)")
            print("index_info: ", index_info)
            if len(index_info) > 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Fehler beim Überprüfen des Indexes '{index}' in der Tabelle '{table}': {e}")
            return False

    def writeToTable(self,table,data:dict):

        # tableData = self.__dictToTable(data)
        tableData = data
        
        keys = tuple(tableData.keys())
        values = tuple(tableData.values())
        
        #find querry
        querry = None
        for q in self.__insertQuerries:
            if(q["name"] == table):
                querry = q
                break
        
        if(querry == None):
            raise Exception("Table not found")
        
        #check if all keys are in querry
        for key in keys:
            if(key not in querry["columns"]):
                raise Exception(f"Key not in table: {key} not in {querry['columns']}")
        

        #order values in the same order as the columns
        values = [tableData[key] for key in querry["columns"]]

        #insert data
        for q in self.__insertQuerries:
            if(q["name"] == table):
                self.__executeInsertQuerry(q["querry"],values)
                break

    def readFromTable(self,table,filter:dict=None):
        #TODO: implement filter
        returnCursor = self.__executeQuerry(f"SELECT * FROM {table}")
        #get column names from returnCursor
        columnNames = returnCursor.keys()
        #return data as list of dicts
        returnData = []
        for row in returnCursor:
            returnData.append(dict(zip(columnNames,row)))

        #transform return data to dict
        # print(returnData)
        type(returnData)

        
        return returnData

    def __dictToTable(self,data:dict):

        newData = {}
        #convert nested dict to un nested dict data:{'a':{'b':1}} -> data:{'a__b':1}. the dict can be nested infinite times
        
        def unnest(data:dict,preKey:str):
            for key,value in data.items():
                if(isinstance(value,dict)):
                    unnest(value,preKey+key+"__")
                else:
                    newData[preKey+key] = value

        unnest(data,"")
        return newData

    def __tableToDict(self, data: dict):
        newData = {}

        def nest_dict(key_value):
            key, value = key_value
            keys = key.split("__")
            current_dict = newData
            for k in keys[:-1]:
                if k not in current_dict or not isinstance(current_dict[k], dict):
                    current_dict[k] = {}
                current_dict = current_dict[k]
            current_dict[keys[-1]] = value

        for key, value in data.items():
            nest_dict((key, value))

        return newData

    def getDataFromTable(self,table:str,length:int):
        #TODO: implement filter
        returnCursor = self.__executeQuerry(f"SELECT * FROM {table} ORDER BY id DESC LIMIT {length}")
        #get column names from returnCursor
        columnNames = returnCursor.keys()
        #return data as list of dicts
        returnData = []
        for row in returnCursor:
            returnData.append(dict(zip(columnNames,row)))
       
        return returnData

    def getDataByTimeSpan(self, table:str, startTime:str, endTime:str):
        #TODO: implement filter
        returnCursor = self.__executeQuerry(f"SELECT * FROM {table} WHERE time BETWEEN '{startTime}' AND '{endTime}' ORDER BY id DESC")
        #get column names from returnCursor
        columnNames = returnCursor.keys()
        #return data as list of dicts
        returnData = []
        for row in returnCursor:
            returnData.append(dict(zip(columnNames,row)))

        return returnData

     

    def listTables(self):
        self.__cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #return as list
        return [table[0] for table in self.__cursor.fetchall()]

    def getTableSize(self, table):
        query = f"SELECT COUNT(*) AS length FROM {table}"
        ret = self.__executeQuerry(query)
        returnData = []
        for r in ret:
            returnData.append(r)
        return returnData[0][0]


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

    data = sqliteHandler.getDataByTimeSpan(table="Sinus1",startTime="2023-08-13 00:00:00",endTime="2023-08-15 00:00:00")
    print(data)
    #print(sqliteHandler.find("test",{"d1":"testStuff"}))