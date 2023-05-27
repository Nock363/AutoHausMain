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
    
    def writeToDB(self,collection,data):
        return self.__sqliteHandler.writeToTable(table=collection,data=data)
    
    def safe(self,dest:str,data:dict):
        return self.__sqliteHandler.writeToTable(table=dest,data=data)