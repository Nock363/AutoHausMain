import sys
sys.path.insert(0, '../')
from Controllers.Controller import Controller
import logging
from datetime import datetime, time
from Utils import tools

class PingController(Controller):

    """
    Dieser Controller gibt zu angegeben zeitpunkten ein Ping-Signal aus. Das heißt es wird einmalig True als state ausgegeben.
    """

    def __init__(self,config:dict = {"threshold":0,"invert":False}):
        super().__init__(["data"])
        self.__threshold = config["threshold"]
        self.__invert = config["invert"]
        self.__lastCall = datetime(1970,1,1,0,0,0,0)
        self.__pumpDuration = config["pumpDuration"]
        self.__pingTimes = config["pingTimes"]
        self.__nextPumpTime = None
        self.__rawPingTimes = config["pingTimes"]
        self.__pingTimes = []
        
        for pingTimestr in self.__rawPingTimes:
            self.__pingTimes.append(tools.timeFromString(pingTimestr))

        if self.__pingTimes == []:
            raise Exception("No pingTimes found in config")

    def __getTimeUntilNextPump(self):

        #find next pumpTime in pingTimes (list of datetime.time objects). when no time is found take the first time of the next day
        now = datetime.now()
        nowTime = now.time()
        nextPumpTime = None
        for pumpTime in self.__pingTimes:
            if pumpTime > nowTime:
                nextPumpTime = pumpTime
                break
        
        if nextPumpTime == None:
            nextPumpTime = self.__pingTimes[0]

        #calculate time until next pump
        timeUntilNextPump = datetime.combine(datetime.now().date(),nextPumpTime) - datetime.combine(datetime.now().date(),nowTime)
        return timeUntilNextPump

    def __findNextPumpTime(self):

        #find next pumpTime in pingTimes (list of datetime.time objects). when no time is found take the first time of the next day
        now = datetime.now()
        nowTime = now.time()
        nextPumpTime = None
        for pumpTime in self.__pingTimes:
            if pumpTime > nowTime:
                nextPumpTime = pumpTime
                break
        
        if nextPumpTime == None:
            nextPumpTime = self.__pingTimes[0]

    def getConfigDescription(self):
        desc:{
            "pumpDuration":{"type":float,"desc":"Wie lange soll die Pumpe pumpen?"},
            "pingTimes":{"type":list,"desc":"Auflistung der Zeiten zu denen gepumpt werden soll"}
        }
        return desc



    def run(self,inputData:dict) -> bool:
        super().checkInputData(inputData)
        
        #find next pumpTime
        timeUntilNextPump = self.__getTimeUntilNextPump()
        
        #check if timeUntilNextPump is smaller than pumpDuration
        if timeUntilNextPump < self.__pumpDuration:
            pass

    def getNextScheduleTime(self) -> datetime:
        pass

