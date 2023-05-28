import sys
sys.path.insert(0, '../')
from Handler.DatabaseHandlers import SqliteHandler
from Handler.JsonHandlers import ConfigHandler

class DataHandler():

    def __init__(self):

        self.__configHandler = ConfigHandler()
        self.__sqliteHandler = SqliteHandler()

    def setupMemory(self,name:str,structure:dict):
        return self.__sqliteHandler.setupTable(name,structure)

    def getPin(self,pinID):
        return self.__configHandler.getPin(pinID)
    
    def getAllPins(self, mode="all"):
        return self.__configHandler.getAllPins(mode)
    
        
    def safe(self,dest:str,data:dict):
        return self.__sqliteHandler.writeToTable(table=dest,data=data)

    def read(self,collection,length):
        return self.__sqliteHandler.getDataFromTable(table=collection,length=length)

    def getSensors(self,onlyActive = True):
        return self.__configHandler.getSensors(onlyActive)  

    def addSensor(self, name: str, pinID: int, className: str, active: bool=True):
        return self.__configHandler.addSensor(name, pinID, className, active)
        

    def getActuators(self,onlyActive = True):
        return self.__configHandler.getActuators(onlyActive)  
    
    def addActuator(self, name: str, type: str, collection: str, config: dict, active: bool=True,configIsUnique=True):
        return self.__configHandler.addActuator(name, type, collection, config, active,configIsUnique)


    def getLogics(self):
        return self.__configHandler.getLogics()

    def listCollectionStacks(self):
        return self.__sqliteHandler.listTables()
    
    def getCollectionSize(self,collection):
        return self.__sqliteHandler.getTableSize(table=collection)
        

if __name__ == "__main__":
    dataHander = DataHandler()

