import sys
sys.path.insert(0, '../')
from Controllers.Controller import Controller
import logging
from datetime import datetime

class WaterpumpController(Controller):

    """
    Der WaterpumpController soll vorallem für das schalten der Wasserpumpe zuständig sein.
    Diese ist besonders kritisch, da sie auf keinenfall durchlaufen sollte. 
    """

    def __init__(self,config:dict = {"threshold":0,"invert":False}):
        super().__init__(["data"])
        self.__threshold = config["threshold"]
        self.__invert = config["invert"]
        self.__lastCall = datetime(1970,1,1,0,0,0,0)
        self.__pumpDuration = config["pumpDuration"]
        self.__pumpTimes = config["pumpTimes"]
        self.__nextPumpTime = None

    def getConfigDescription(self):
        desc: {
            "pumpDuration":{"type":float,"desc":"Wie lange soll die Pumpe pumpen?"},
            "pumpTimes":{"type":list],"desc":"Auflistung der Zeiten zu denen gepumpt werden soll"},
            
        }
        return desc

    def __setNextPumpTime(self):
        #find next pump time. pump
        


    def run(self,inputData:dict) -> bool:
        super().checkInputData(inputData)
        
        
        