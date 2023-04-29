import os
import json
import logging
logging.basicConfig(encoding='utf-8', level=logging.ERROR)

class ConfigHandler():
#this class is used to load different configs stored in json files in Autohausmain/Configs

    def __init__(self):
        pass

    def getSensors(self,onlyActive = True):
        #load sensors.json and return it as a list of dicts
        sensors = json.load(open(os.path.join(os.path.dirname(__file__),"../Configs/sensors.json")))
        if(onlyActive):
            sensors = [sensor for sensor in sensors if sensor["active"] == True]
        return sensors  

    def addSensor(self, name: str, pinID: int, className: str, active: bool=True):
        json_file = os.path.join(os.path.dirname(__file__), "../Configs/sensors.json")
        with open(json_file, "r") as f:
            data = json.load(f)

        # check if name already exists
        if any((sensor["name"] == name) for sensor in data):
            logging.error(f"Name {name} already exists!")
            return False

        # add new actuator
        new_sensor = {"active": active, "name": name, "pinID": pinID, "class": className}
        data.append(new_sensor)

        # write data back to file but keep file readable with \n
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)
            f.write("\n")
    
        return True
        

    def getActuators(self,onlyActive = True):
        actuators = json.load(open(os.path.join(os.path.dirname(__file__),"../Configs/actuators.json")))
        if(onlyActive):
            actuators = [actuator for actuator in actuators if actuator["active"] == True]
        return actuators
    
    def addActuator(self, name: str, type: str, collection: str, config: dict, active: bool=True,configIsUnique=True):
        json_file = os.path.join(os.path.dirname(__file__), "../Configs/actuators.json")
        with open(json_file, "r") as f:
            data = json.load(f)

        # if config is unique, check if config already exists
        if configIsUnique:
            for entry in data:
                if entry["config"] == config:
                    logging.error(f"Config already exists!\n{entry}")
                    return False
        

        # check if name already exists
        if any((actuator["name"] == name) for actuator in data):
            logging.error(f"Name {name} already exists!")
            return False

        

        # add new actuator
        new_actuator = {"active": active, "name": name, "type": type, "collection": collection, "config": config}
        data.append(new_actuator)

        # write data back to file but keep file readable with \n
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)
            f.write("\n")
    

        return True


    def getLogics(self):
        logics = json.load(open(os.path.join(os.path.dirname(__file__),"../Configs/logics.json")))
        logics = [logic for logic in logics if logic["active"] == True]
        return logics