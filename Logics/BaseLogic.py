import sys 
sys.path.insert(0, '../')

from Controllers.BaseBlocks import BaseBlock
from Sensoren.Sensor import Sensor

class BaseLogic():

    __name : str
    __controller : BaseBlock
    __inputs : list[dict]
    __outputs : list[dict]

    __lastInputData : dict
    __lastResult = None

    def __init__(self,name:str,controller:BaseBlock,inputs:list[dict],outputs:list[dict]):
        self.__name = name
        self.__controller = controller
        self.__inputs = inputs
        self.__outputs = outputs
        

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

        for output in self.__outputs:
            output["object"].set(result)

    def lastRunToString(self):
        return f"input: {self.__lastInputData}\tresult: {self.__lastResult}"

    
    #getter for __name
    @property
    def name(self):
        return self.__name