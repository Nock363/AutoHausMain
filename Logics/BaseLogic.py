import sys 
sys.path.insert(0, '../')

from Handler.DatabaseHandlers import MongoHandler
from Controllers.BaseBlocks import BaseBlock
from Sensoren.Sensor import Sensor
#from Sensoren.Data import Data
class BaseLogic():

    __mongo = MongoHandler()
    __name : str
    __controller : BaseBlock
    __inputs : list[dict]
    __outputs : list[dict]


    def __init__(self,name:str,controller:BaseBlock,inputs:list[dict],outputs:list[dict]):
        self.__mongo = MongoHandler()
        self.__name = name
        self.__controller = controller
        self.__inputs = inputs
        self.__outputs = outputs
        

    def run(self):
        #create input dict for controller by iterating through inputs
        inputData = {}
        for input in self.__inputs:
            data = input["object"].run().data()
            inputData[input["parameter"]] = data[input["input"]]
            
        result = self.__controller.run(inputData)
        
        for output in self.__outputs:
            output["object"].set(result)
