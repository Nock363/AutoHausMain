from typing import Tuple
import sys
sys.path.insert(0, '../')
from Controllers.Controller import Controller
import logging
from datetime import datetime, timedelta
from Utils import tools

class TimerController(Controller):

    def getConfigDescription(self):
        desc = {
            "times": [{"start": "12:00:00", "runTime": "00:01:00"}],
        }
        return desc

    def __init__(self, config: dict = {"times": [{"start": "12:00:00", "runTime": "00:01:00"}]}):
        super().__init__(mask=[],config=config)
        self.__times = []
        now = datetime.now()
        #for every entry in config times create a dict with starttime(datetime),endtime(datetime),runtime(timedelta). 
        # starttime and endtime have the date of today but the time of the config entry
        
        #if config["times"] is empty rais error
        if len(config["times"]) == 0:
            raise ValueError("TimerController: Zeitplan ist leer")

        times = []

        for time_entry in config["times"]:
            start_time = datetime.strptime(time_entry["start"], "%H:%M:%S")
            start_time = start_time.replace(year=now.year, month=now.month, day=now.day)
            runTime = tools.castDeltatimeFromString(time_entry["runTime"])
            end_time = start_time + runTime
            times.append({"start_time": start_time, "end_time": end_time})

        #sort times by start_time
        times.sort(key=lambda x: x["start_time"])

        #check if times overlap
        for i in range(len(times) - 1):
            if times[i]["end_time"] > times[i + 1]["start_time"]:
                raise ValueError("TimerController: Zeitpläne dürfen sich nicht überlappen")
        
        
        
        #add one day to every time in the past
        for time_entry in times:
            if time_entry["start_time"] < now and time_entry["end_time"] < now:
                time_entry["start_time"] += timedelta(days=1)
                time_entry["end_time"] += timedelta(days=1)

        #sort times again by start_time
        times.sort(key=lambda x: x["start_time"])
        self.__times = times
        self.__isOn = False

        #check if system should run right now
        if now > self.__times[0]["start_time"] and now < self.__times[0]["end_time"]:
            self.__isOn = True


    def run(self, inputData: dict) -> bool:
        now = datetime.now()
        if self.__isOn:
            nextTime = self.__times[0]["end_time"]
            if now < nextTime:
                return True
            else:
                self.__isOn = False
                temp = self.__times.pop(0)
                temp["start_time"] += timedelta(days=1)
                temp["end_time"] += timedelta(days=1)
                self.__times.append(temp)
                return False
        
        else:
            nextTime = self.__times[0]["start_time"]
            if now < nextTime:
                return False
            else:
                self.__isOn = True
                return True

            



        

    def getNextScheduleTime(self) -> datetime:
        if self.__isOn:
            return self.__times[0]["end_time"]
        else:
            return self.__times[0]["start_time"]
