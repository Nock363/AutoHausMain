import enum
from datetime import time

class Type(enum.Enum):
    #primitive types
    INT = int,
    FLOAT = float,
    BOOL = bool,
    STR = str

class Config():


    def __init__(self):
        self.__elements = {}


    def addElement(self,name:str,type,description:str):
        
        #check if name is already in use
        if(name in self.__elements):
            raise Exception(f"Config besitzt bereits ein Elment mit dem namen {name}")

        self.__elements[name] = {"type":type,"description":description}
        

if __name__ == "__main__":
    
    testConfig1 = Config()
    testConfig1.addElement(name="threshold",type=float,description="Threshold, ab dem True ausgegeben wird")
    testConfig1.addElement(name="invert",type=bool,description="invertiert die Entscheidung")

    testConfig2 = Config()
    element = Config()
    element.addElement(name="start",type=time,description="Startzeit des Zeitplans. Format: 'HH:MM:SS'")
    
    testConfig2.addList(name="times")


    dictDesc1 = {
        "threshold": {
                "type": float,
                "description": "Threshold, ab dem True ausgegeben wird"
            },
            "invert": {
                "type": bool,
                "description": "invertiert die Entscheidung"
        }}

    dictDesc2 = {
        "times":{
            "type":list,
            "element":{
                "type":dict,
                "desc":{
                    "start":{"type":str,"desc":"Startzeit des Zeitplans. Format: 'HH:MM:SS'","format":"time"},
                    "runTime":{"type":str,"desc":"Laufzeit des Zeitplans. Format: 'HH:MM:SS'","format":"time"}
                }
            }
        }
    }


