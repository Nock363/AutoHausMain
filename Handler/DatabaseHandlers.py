from pymongo import MongoClient
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
import os.path
import sqlite3
import time
from datetime import datetime
"""
Handler für den Aufbau und dem Verwalten von Verbindungen mit Datenbanken.
Aktuell nur ein MongoHandler für die MongoDB Datenbank, allerdings steht auch die Option einen Handler für einen anderen DB Typen zu entwickeln.
"""

class SqliteHandler():

    dbPath = "/home/user/AutoHausMain/Databases/main.db"

    def __init__(self):
        self.__connection = sqlite3.connect(self.dbPath)
        self.__cursor = self.__connection.cursor()
        self.__insertQuerries = self.genInsertQuerries(self.dbPath)

    def genInsertQuerries(self,database_name):
    
        cursor = self.__cursor       
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()

        insert_queries = []

        # INSERT-Queries für jede Tabelle generieren
        for table in table_names:


            table_name = table[0]
            if(table_name == "sqlite_sequence"):
                continue

            # Spaltennamen abrufen
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns if column[1] != 'id']

            # Platzhalter für Werte generieren
            value_placeholders = ", ".join(['?'] * len(column_names))

            # INSERT-Query für jeden Datensatz generieren
            insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({value_placeholders})"

            # Query zur Liste hinzufügen
            insert_queries.append({"name":table_name,"querry":insert_query,"columns":column_names})

        return insert_queries


    def find(self,table:str,filter:dict):
        #find all entries in table where time is between 100 and 200
        filter = {"time":(100,200)}
        query = f"SELECT * FROM {table} WHERE time BETWEEN 100 AND 200"
        self.__cursor.execute(query)
        return self.__cursor.fetchall()
    

    def setupTable(self,name:str,structure:dict):
        #dict is like {"time":time,"d1":str,"d2":float,"d3":int}
        #create table if not exists

        #translate python data types to sql data types
        sqlTypes = {str:"TEXT",float:"REAL",int:"INTEGER"}
        for key,value in structure.items():
            
            if(value not in sqlTypes):
                structure[key] = "UNKNOWN"
            else:
                structure[key] = sqlTypes[value]


        if("time" not in structure):
            structure["time"] = "DATETIME"

        #add id to structure as primary key and autoincrement

        query = f"CREATE TABLE IF NOT EXISTS {name} (id INTEGER PRIMARY KEY AUTOINCREMENT, " + ",".join([f"{key} {value}" for key,value in structure.items()]) + ")"

        self.__cursor.execute(query)
        self.__cursor.execute(f'CREATE INDEX IF NOT EXISTS time_index ON {name} (time)')
        self.__connection.commit()

        self.__insertQuerries = self.genInsertQuerries(self.dbPath)

    def addIndexToTable(self, table, index):
        try:
            self.__cursor.execute(f'CREATE INDEX IF NOT EXISTS {index}_index ON {table} ({index})')
            self.__connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Fehler beim Hinzufügen des Indexes zur Tabelle '{table}': {e}")
            return False
     

    def checkForIndex(connection, table, index):
        try:
            self.__cursor.execute(f"PRAGMA index_info({index}_index)")
            index_info = self.__cursor.fetchall()
            print("index_info: ", index_info)
            if len(index_info) > 0:
                return True
            else:
                return False
        except sqlite3.Error as e:
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
                raise Exception("Key not in table")
        

        #order values in the same order as the columns
        values = [tableData[key] for key in querry["columns"]]

        #insert data
        for q in self.__insertQuerries:
            if(q["name"] == table):
                self.__cursor.execute(q["querry"],values)
                break


        
        self.__connection.commit()


    def readFromTable(self,table,filter:dict=None):
        if(filter == None):
            self.__cursor.execute(f"SELECT * FROM {table}")
        else:
            #TODO: implement filter
            pass

        returnData = self.__cursor.fetchall()
        #transform return data to dict
        print(returnData)
        type(returnData)

        
        return 


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
        #sql version
        query = f"SELECT * FROM {table} DESC LIMIT {length}"
        self.__cursor.execute(query)
        data = self.__cursor.fetchall()
        names = [desc[0] for desc in self.__cursor.description]
        result = []
        for row in data:
            row_dict = {}
            for i, value in enumerate(row):
                name = names[i]
                row_dict[name] = value
            result.append(row_dict)

            # Rückgabe der Daten
        return result
    
    def listTables(self):
        self.__cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #return as list
        return [table[0] for table in self.__cursor.fetchall()]


    def getTableSize(self, table):
        querry = f"SELECT COUNT(*) AS length FROM {table}"
        self.__cursor.execute(querry)
        return self.__cursor.fetchone()[0]


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

    sqliteHandler.setupTable("test2",{"time":time,"d1":str,"d2":float,"d3":int})
    sqliteHandler.writeToTable("test2",{"time":101,"d1":"testStuff","d2":12,"d3":22})
    # sqliteHandler.readFromTable("test")
    #print(sqliteHandler.find("test",{"d1":"testStuff"}))