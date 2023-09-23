import sys 
sys.path.insert(0, '../')

from Controllers.BaseBlocks import BaseBlock
from Sensoren.Sensor import Sensor
from datetime import datetime, timedelta

class BaseLogic():

    __name : str
    __controller : BaseBlock
    __inputs : list[dict]
    __outputs : list[dict]

    __lastInputData : dict
    __lastResult = None

    def __init__(self,name:str,controller:BaseBlock,inputs:list[dict],outputs:list[dict],active:bool=True,description:str="",intervall=10):
        self.__name = name
        self.__controller = controller
        self.__inputs = inputs
        self.__outputs = outputs
        self.__active = active
        self.__description = description
        self.__intervall = intervall
        self.__nextRun = None


    @property
    def active(self):
        return self.__active

    def run(self):
        #create input dict for controller by iterating through inputs
        inputData = {}
        for input in self.__inputs:
            sensor = input["object"]
            data = sensor.getHistory(1)[0]
            
            inputData[input["parameter"]] = data[input["input"]]
        
        self.__lastInputData = inputData
        result = self.__controller.run(inputData)
        self.__lastResult = result

        #if controller is BaseBlock, generate nextRun from intervall
        if(isinstance(self.__controller,BaseBlock)):
            self.__nextRun = datetime.now() + timedelta(seconds=self.__intervall)
        else:
            raise Exception("Not implemented yet")

        for output in self.__outputs:
            output["object"].set(result)

    def lastRunToString(self):
        return f"input: {self.__lastInputData}\tresult: {self.__lastResult}"

    def getInfos(self) -> dict:

        #remove 'object' from inputs and outputs but without changing the original list
        inputs = []
        for input in self.__inputs:
            inputs.append(input.copy())
            inputs[-1].pop("object")
        
        outputs = []
        for output in self.__outputs:
            outputs.append(output.copy())
            outputs[-1].pop("object")

        
            


        return {
                "active":self.__active,
                "name":self.__name,
                "inputs":inputs,
                "outputs":outputs,
                "description":self.__description
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