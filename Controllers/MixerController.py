import sys
import time
from datetime import datetime, timedelta
sys.path.insert(0, '../')
from Controllers.Controller import Controller
import logging
from Utils import tools

class MixerController(Controller):

    def getConfigDescription(self):
        desc: {
            "ECValue":{"type":float,"desc":"EC goal mixed water"},
            "PHValue":{"type":float,"desc":"PH goal mixed water"},
            "ChlorineValue":{"type":float,"desc":"Chlorine goal mixed water"},
            "WaterVolume":{"type":float,"desc":"Water volume which is mixed"},
            "WaitAfterWatering":{"type":str,"desc":"Zeit die gewartet wird, nachdem Korrektur gegossen wurde. Angegeben in %H:%M:%S"},
        }
        return desc

    def __init__(self,config:dict = {"ECValue":500,"PHValue":6.5, "ChlorineValue":0.0,"WaterVolume":6.0,"WaitAfterWatering":"00:01:00"}):
        super().__init__(mask=["dataEC", "dataPH"],config=config)
        self.__eCValueTarget = config["ECValue"]
        self.__pHValueTarget = config["PHValue"]
        self.__chlorineValue = config["ChlorineValue"]
        self.__waterVolume = config["WaterVolume"]
        self.__waitAfterWatering = tools.castDeltatimeFromString(config["WaitAfterWatering"])
        self.__waitAfterCorrection = tools.castDeltatimeFromString("00:02:00")
        self.__nextCall = datetime(1970,1,1)    #TODO: muss überschrieben werden, sonst kann endlosschleife entstehen

    def run(self,inputData:dict) -> int: #TODO muss das int oder bool sein       
        #prüfe pf input data mit der maske übereinstimmt
        super().checkInputData(inputData)
        inputEC = inputData["dataEC"]
        inputPH = inputData["dataPH"]
        
        #erstelle dict als return Wert (In Python kann man jederzeit neue Einträge in dicts erzeugen.)
        returnDict = {}
        
        #prüfe ob controller wieder call-bar ist. (warte zeit zuende) 
        now = datetime.now() #+ tools.castDeltatimeFromString(cycleTime)
        self.__nextCall = now #Falls nicht korrekt eingestellt wird nach 45Sekunden neu gemessen
        pumpTime = int(self.__waterVolume/840*3600*1000) #TODO: Pumpzeit ist jetzt in Config Definiert
        #Start Julius Logik
        if(inputEC < 0):
            logging.info(f"Mixer Startet")            
            logging.info(f"Es werden {self.__waterVolume}L angemischt")
            self.__nextCall = now + self.__waitAfterCorrection
            returnDict = {"actuator":"InMixer", "value":pumpTime}
            return super().safeAndReturn(returnDict)
            
        if(self.__nextCall <= now):      
            if(inputEC < self.__eCValueTarget):
                self.__nextCall = now + self.__waitAfterCorrection
                #run DüngerPumpe EC 1,2
                logging.info(f"EC Anpassung")
                returnDict = {"actuator":"Duenger_Pumpe", "value":1000}
                return super().safeAndReturn(returnDict)

            else:
                if(inputPH > self.__pHValueTarget):
                    self.__nextCall = now + self.__waitAfterCorrection
                    #run DüngerPumpe PH
                    logging.info(f"PH Anpassung")
                    returnDict = {"actuator":"PH_Pumpe", "value":1000}
                    return super().safeAndReturn(returnDict)

                #if(inputChlorine < self.__ChlorineValue):
                #    #run DüngerPumpe CHlor
                #    logging.info(f"Chlorine Anpassung")

                else:
                    #run pump2 pumptime+5
                    logging.info(f"Bewässerung wird ausgeführt")
                    self.__nextCall = now + self.__waitAfterWatering
                    returnDict = {"actuator":"AusMixer", "value":pumpTime+5000}
                    return super().safeAndReturn(returnDict)
                    
        return


      

    def getNextScheduleTime(self) -> datetime:
        return self.__nextCall




    #self.__nextCall = now + 60 #self.__waitAfterWatering
    #    if(self.__nextCall <= now):

    #        #prüfe ob reagiert werdem muss 
    #        if( (input < 0)):
    #            self.__nextCall = now + self.__waitAfterWatering
    #            logging.warning(f"Poolsonde nicht im Wasser")     
    #            return super().safeAndReturn(False)
    #        elif(input > self.__maxValue):
    #            self.__nextCall = now + self.__waitAfterCorrection
    #            logging.info(f"input({input})>maxValue({self.__maxValue})")
    #            return super().safeAndReturn(self.__maxReaction)
    #        elif(input < self.__minValue):
    #            self.__nextCall = now + self.__waitAfterCorrection
    #            logging.info(f"input({input})<minValue({self.__minValue})")
    #            return super().safeAndReturn(self.__minReaction)
    #        
    #        else:
    #            #keine Korrektur nötig, 
    #            self.__nextCall = now + self.__waitWhenCorrect
    #            logging.info(f"Keine Korrektur nötig")
#
