import json
from flask import jsonify
from datetime import datetime,timedelta,time

def is_json_serializable(obj):
    # Allow strings as they are already JSON serializable
    if isinstance(obj, str):
        return True
    
    try:
        json.dumps(obj)
        return True
    except (TypeError, ValueError):
        return False

def toJson(obj):
    try:
        json = jsonify(obj)
        return json
    except Exception as e:
        if(isinstance(obj, dict)):
            print("dict")
            checkDictForJsonSerialization(obj)
        elif(isinstance(obj, list)):
            print("list")
            checkListForJsonSerialization(obj)
        else:
            print("other")
            print(obj)
            raise TypeError("Object is not serializable")

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

def getSecondsUntilTime(time:datetime)-> float:
    now = datetime.now()
    return (time - now).total_seconds()

def timeFromString(timeStr:str):
    h,m,s = map(int, timeStr.split(":"))
    return time(h,m,s)    

def timeDiffSeconds(startTime:time,endTime:time):
    #calculate time difference in seconds (negative is allowed)
    return (datetime.combine(datetime.today(), endTime) - datetime.combine(datetime.today(), startTime)).total_seconds()

def dictValuesToString(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = dictValuesToString(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = dictValuesToString(data[i])
    else:
        data = str(data)
    return data

def compareDictsByKeys(dictA:dict,dictB:dict):

    for(key,value) in dictA.items():
        if key in dictB:
            if isinstance(value,dict):
                if not compareDictsByKeys(value,dictB[key]):
                    return False
            elif isinstance(value,list):
                if not compareListsByElementStructure(value,dictB[key]):
                    return False
            else:
                #return false then types of values are not equal
                if not isinstance(value,type(dictB[key])):
                    return False
        else:
            return False

    return True

def compareDictByDesc(configDict:dict,descDict:dict):
    pass

def checkListForConsistency(inputList:list):

    if len(inputList) == 0:
        return True
    
    #check if 0 element is a dict
    if not isinstance(inputList[0],dict):
        #check if all elements are of the same type
        for element in inputList:
            if not isinstance(element,type(inputList[0])):
                return False
    else:
        #check if all dicts have the same keys
        for element in inputList:
            if not compareDictsByKeys(inputList[0],element):
                return False

    return True
    
def compareListsByElementStructure(listA:list,listB:list):
    if(len(listA) == 0 or len(listB) == 0):
        return True

    #check if both lists are consistent
    if not checkListForConsistency(listA) or not checkListForConsistency(listB):
        return False
    
    firstElementA = listA[0]
    firstElementB = listB[0]

    #return false if types of first elements are not equal
    if not isinstance(firstElementA,type(firstElementB)):
        return False
    
    #if first element is a dict, check if all dicts have the same keys
    if isinstance(firstElementA,dict):
        if not compareDictsByKeys(firstElementA,firstElementB):
            return False
    
    return True

def isValidTimeFormat(timeString:str):
    try:
        datetime.strptime(timeString, "%H:%M:%S")
        return True
    except ValueError:
        return False


#write test to test getSecondsUntilTime. Most important test what happens then time is in the past
if __name__ == "__main__":
    # pastTime = datetime.now() - timedelta(hours=1)
    # futureTime = datetime.now() + timedelta(hours=1)
    # print("pastTime: {}".format(pastTime))
    # print("futureTime: {}".format(futureTime))
    # print("Seconds until pastTime: {}".format(getSecondsUntilTime(pastTime)))
    # print("Seconds until futureTime: {}".format(getSecondsUntilTime(futureTime)))

    # print("timeFromStringTest:")
    # time1 = timeFromString("10:20:00")
    # time2 = timeFromString("10:20:10")
    # print("time1:",time1)
    # print("time2:",time2)

    data = {
        'name': 'John',
        'age': 30,
        'address': {
            'street': 123,
            'city': 'Anytown',
        },
        'hobbies': ['reading', 'swimming', {'type': 'indoor', 'name': 'chess'}]
    }

    expected_result = {
        'name': 'John',
        'age': '30',
        'address': {
            'street': '123',
            'city': 'Anytown',
        },
        'hobbies': ['reading', 'swimming', {'type': 'indoor', 'name': 'chess'}]
    }

    print("Test dictValuesToString")
    result = dictValuesToString(data)
    assert result == expected_result


    dict1 = {
    'name': 'John',
    'age': 30,
    'address': {
        'street': '123 Main St',
        'city': 'Exampleville'
    },
    'hobbies': ['reading', 'sports']
    }

    dict2 = {
        'name': 'Pepe',
        'age': 33,
        'address': {
            'street': '123 Main St',
            'city': 'Exampleville'
        },
        'hobbies': ['reading', 'sports']
    }

    print("Test compareDictsByKeys")
    result = compareDictsByKeys(dict1, dict2)
    assert result == True

    print("All tests passed")