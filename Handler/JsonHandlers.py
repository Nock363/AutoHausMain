import os
import json


class ConfigHandler():
#this class is used to load different configs stored in json files in Autohausmain/Configs

    def __init__(self):
        pass

    def getSensors(self):
        #load sensors.json and return it as a list of dicts
        sensors = json.load(open(os.path.join(os.path.dirname(__file__),"Configs/sensors.json")))
        return sensors    
