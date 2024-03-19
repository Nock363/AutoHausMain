import sys
import time
from datetime import datetime, timedelta
sys.path.insert(0, '../')
from Controllers.Controller import Controller
import logging
from Utils import tools

class TimedBinaryController(Controller):

    """
    Der BinaryController gibt als Ausgang True oder False aus.
    Dabei betrachtet  er den Wert 'threshold' und gibt False aus, 
    falls der Wert unter dem Threshold liegt und True fals der Wert
    über den Threshold liegt (invert invertiert die Entscheidung einmal)
    """

    def getConfigDescription(self):
        desc: {
            "minValue":{"type":float,"desc":"input niedriger => trigger"},
            "minReaction":{"type":bool,"desc":"Was soll getriggert werden, wenn minValue unterschritten?"},
            "maxValue":{"type":float,"desc":"input höher => trigger"},
            "maxReaction":{"type":bool,"desc":"Was soll getriggert werden, wenn maxValue überschritten?"},
            "waitAfterCorrection":{"type":str,"desc":"Zeit die gewartet wird, nachdem Korrektur vorgenommen wurde. Angegeben in %H:%M:%S"},
            "waitWhenCorrect":{"type":str,"desc":"Zeit die gewartet wird, Falls keine Korrektur nötig.  Angegeben in %H:%M:%S"},
        }
        return desc

    def __init__(self,config:dict = {"minValue":5.0,"minReaction":False, "minTime":300,"maxValue":6.0,"maxReaction":True,"maxTime":300,"waitAfterCorrection":60.0,"waitWhenCorrect":3600.0}):
        super().__init__(mask=["data"],config=config)
        self.__minValue = config["minValue"]
        self.__minReaction = config["minReaction"]
        self.__maxValue = config["maxValue"]
        self.__maxReaction = config["maxReaction"]
        self.__waitAfterCorrection = tools.castDeltatimeFromString(config["waitAfterCorrection"])
        self.__waitWhenCorrect = tools.castDeltatimeFromString(config["waitWhenCorrect"])
        self.__nextCall = datetime(1970,1,1)    #TODO: muss überschrieben werden, sonst kann endlosschleife entstehen

    def run(self,inputData:dict) -> bool:
        
        #prüfe pf input data mit der maske übereinstimmt
        super().checkInputData(inputData)
        input = inputData["data"]

        #prüfe ob controller wieder call-bar ist. (warte zeit zuende)
        now = datetime.now()
        if(self.__nextCall <= now):
            #prüfe ob reagiert werdem muss 
            if( (input < 0)):
                self.__nextCall = now + self.__waitAfterCorrection
                logging.warning(f"Poolsonde nicht im Wasser")     
                return super().safeAndReturn(False)
            elif(input > self.__maxValue):
                self.__nextCall = now + self.__waitAfterCorrection
                logging.info(f"input({input})>maxValue({self.__maxValue})")
                return super().safeAndReturn(self.__maxReaction)
            elif(input < self.__minValue):
                self.__nextCall = now + self.__waitAfterCorrection
                logging.info(f"input({input})<minValue({self.__minValue})")
                return super().safeAndReturn(self.__minReaction)
            
            else:
                #keine Korrektur nötig, 
                self.__nextCall = now + self.__waitWhenCorrect
                logging.info(f"Keine Korrektur nötig")

        return      

    def getNextScheduleTime(self) -> datetime:
        return self.__nextCall