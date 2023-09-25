import json
from datetime import datetime,timedelta

def is_json_serializable(obj):
    # Allow strings as they are already JSON serializable
    if isinstance(obj, str):
        return True
    
    try:
        json.dumps(obj)
        return True
    except (TypeError, ValueError):
        return False

def checkDictForJsonSerialization(d:dict, path=None):
    if path is None:
        path = []

    #iterate over all keys
    for key in d.keys():
        #if the key is not  a dict or list, check if it is serializable
        if not isinstance(d[key], dict) and not isinstance(d[key], list):
            if not is_json_serializable(d[key]):
                print("Not serializable: {}".format(path + [key]))
                break
        #if the key is a dict, check the dict
        elif(isinstance(d[key], dict)):
            checkDictForJsonSerialization(d[key], path + [key])
        elif(isinstance(d[key], list)):
            checkListForJsonSerialization(d[key], path + [key])

def checkListForJsonSerialization(l:list, path=None):
    if path is None:
        path = []

    #iterate over all elements
    for i in range(len(l)):
        #if the element is not  a dict or list, check if it is serializable
        if not isinstance(l[i], dict) and not isinstance(l[i], list):
            if not is_json_serializable(l[i]):
                print("Not serializable: {}".format(path + [i]))
                break
        #if the element is a dict, check the dict
        elif(isinstance(l[i], dict)):
            checkDictForJsonSerialization(l[i], path + [i])
        elif(isinstance(l[i], list)):
            checkListForJsonSerialization(l[i], path + [i])

def castDeltatimeFromString(timeString:str,stringFormat="%H:%M:%S")->timedelta:
    return datetime.strptime(timeString,stringFormat)-datetime.strptime("00:00:00",stringFormat)
    