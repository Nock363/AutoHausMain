import sys 
sys.path.insert(0, '../')

from Controllers.Controller import Controller
from Sensoren.Sensor import Sensor
from datetime import datetime, timedelta
from Utils.Status import Status

class BaseLogic():

    __name : str
    __controller : Controller
    __inputs : list[dict]
    __outputs : list[dict]

    __lastInputData : dict
    __lastResult = None
    status : Status

    def __init__(self,name:str,controller:Controller,inputs:list[dict],outputs:list[dict],intervall=111,active:bool=True,description:str=""):
        
        self.__name = name
        self.__controller = controller
        self.__inputs = inputs
        self.__outputs = outputs
        self.__active = active
        self.__description = description
        self.__intervall = intervall
        self.__nextRun = None
        self.status = Status.READY

    @property
    def active(self):
        return self.__active

    def run(self):
        #create input dict for controller by iterating through inputs
        inputData = {}
        for input in self.__inputs:
            sensor = input["object"]
            data = sensor.getLastData()
            
            inputData[input["parameter"]] = data[input["input"]]
        
        self.__lastInputData = inputData
        result = self.__controller.run(inputData)
        self.__lastResult = result

        nextScheduleTime = self.__controller.getNextScheduleTime()

        #if controller is Controller, generate nextRun from intervall
        if(type(nextScheduleTime) == datetime):
            self.__nextRun = nextScheduleTime
        else:
            self.__nextRun = datetime.now() + timedelta(seconds=self.__intervall)

        for output in self.__outputs:
            output["object"].set(result)

    def lastRunToString(self):
        return f"input: {self.__lastInputData}\tresult: {self.__lastResult}"

    def getInfos(self) -> dict:

        #remove 'object' from inputs and outputs but without changing the original list
        inputs = []
        for input in self.__inputs:
            #Kopieren des Objectes
            inputs.append(input.copy())
            #Löschen des Objektes
            inputs[-1].pop("object")
        
        outputs = []
        for output in self.__outputs:
            #Kopieren des Objectes
            outputs.append(output.copy())
            #Löschen des Objektes
            outputs[-1].pop("object")

        nextScheduleTime = str(self.getNextScheduleTime())

        controller = self.__controller.getInfo()

        return {
                "active":self.__active,
                "name":self.__name,
                "controller":controller,
                "inputs":inputs,
                "outputs":outputs,
                "description":self.__description,
                "nextScheduleTime":nextScheduleTime
                }
    
    def getNextScheduleTime(self) -> datetime:
        if(self.__nextRun == None):
            return datetime.now() + timedelta(seconds=self.__intervall)
        nextRun = self.__nextRun
        self.__nextRun = None
        return nextRun

    #getter for __name
    @property
    def name(self):
        return self.__name