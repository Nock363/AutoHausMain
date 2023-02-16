import os
import json


class ConfigHandler():
#this class is used to load different configs stored in json files in Autohausmain/Configs

    def __init__(self):
        pass

    def getSensors(self):
        #load sensors.json and return it as a list of dicts
        sensors = json.load(open(os.path.join(os.path.dirname(__file__),"../Configs/sensors.json")))
        sensors = [sensor for sensor in sensors if sensor["active"] == True]
        return sensors  

    def getActuators(self):
        actuators = json.load(open(os.path.join(os.path.dirname(__file__),"../Configs/actuators.json")))
        actuators = [actuator for actuator in actuators if actuator["active"] == True]
        return actuators
    
    def getLogics(self):
        logics = json.load(open(os.path.join(os.path.dirname(__file__),"../Configs/logics.json")))
        logics = [logic for logic in logics if logic["active"] == True]
        return logics