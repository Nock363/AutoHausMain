from flask import Flask, request, jsonify, g
from flask_cors import CORS
from Handler.DataHandler import DataHandler
from multiprocessing import Event, Queue
from MainSystem import MainSystem
from flask import send_from_directory
import os
import time
import threading
from datetime import datetime

class RestAPI():

    __app : Flask = None
    __mainSystem : MainSystem

    def __init__(self,reqChannel,respChannel,mainSystem = None,errorChannel = None,errorCount = None):
        self.__app = Flask(__name__)
        CORS(self.__app)
        self.__mainSystem = mainSystem#TODO Purge that shit!
        self.__dataHandler = DataHandler()

        with self.__app.app_context():
            g._dataHandler = DataHandler()
            
        self.__reqChannel = reqChannel
        self.__respChannel = respChannel
        self.__requestID = 1

        self.__errorChannel = errorChannel
        self.__errorCount = errorCount


        self.__userInterfacePath = "AutoHaus_UserInterface/"

        self.__app.route("/pins",methods=["GET"])(self.getPins)
        self.__app.route("/sensors",methods=["GET"])(self.getSensors)
        self.__app.route("/sensorsWithData/<length>",methods=["GET"])(self.getSensorsWithData)
        self.__app.route("/actuators",methods=["GET"])(self.getActuators)
        self.__app.route("/actuatorsWithData/<length>",methods=["GET"])(self.getActuatorsWithData)
        self.__app.route("/logics",methods=["GET"])(self.getLogics)
        self.__app.route("/data/<collection>/<length>",methods=["GET"])(self.getDriectFromDB)#legacy
        self.__app.route("/sensorHistory", methods=["GET"])(self.getSensorHistory)
        self.__app.route("/sensorHistoryByTimespan", methods=["GET"])(self.getSensorHistoryByTimespan)
        self.__app.route("/collections",methods=["GET"])(self.getAllCollections)
        self.__app.route("/stopScheduler",methods=["GET"])(self.stopScheduler)
        self.__app.route("/startScheduler",methods=["GET"])(self.startScheduler)
        self.__app.route("/schedulerInfo",methods=["GET"])(self.getSchedulerInfo)
        self.__app.route("/systemInfo",methods=["GET"])(self.getSystemInfo)
        self.__app.route("/setActuator",methods=["GET"])(self.setActuator)
        self.__app.route("/startBrokenSensor",methods=["GET"])(self.startBrokenSensor)
        self.__app.route("/errorTest",methods=["GET"])(self.errorTest)
        self.__app.route("/getErrors",methods=["GET"])(self.getErrors)
        self.__app.route("/testDB",methods=["GET"])(self.testDB)
        self.__app.route("/actuatorHistory", methods=["GET"])(self.getActuatorHistory)


    def __requestMainSystem(self,request:dict):
        #Diese Funktion regelt die komminaktion mit dem MainSystem
        
        id = time.time()

        #Stelle Anfrage an Server
        self.__reqChannel.append({"id":id,"request":request})
        

        #Empfange antwort
        while(True):
            if(len(self.__respChannel) > 0):
                for i, response in enumerate(self.__respChannel):
                    if(response["id"] == id):
                        del self.__respChannel[i]
                        return response["response"]

    def getDataHandler(self):
        return self.__dataHandler

    def getSensorHistory(self):
        sensor = request.args.get('sensor')
        length = int(request.args.get('length'))
        result = self.__requestMainSystem({"command":"sensorHistory", "sensor":sensor,"length":length})
        # print(result)
        return jsonify(result)

    def getActuatorHistory(self):
        actuator = request.args.get('actuator')
        length = int(request.args.get('length'))
        result = self.__requestMainSystem({"command":"actuatorHistory", "actuator":actuator,"length":length})
        return jsonify(result)

    def getSensorHistoryByTimespan(self):
        sensor = request.args.get('sensor')
        startTime = request.args.get('startTime')
        startTime = startTime.replace("_"," ")
        endTime = request.args.get('endTime')
        endTime = endTime.replace("_"," ")
        result = self.__requestMainSystem({"command":"sensorHistoryByTimespan", "sensor":sensor,"startTime":startTime,"endTime":endTime})
        # print(result)
        return jsonify(result)

    def getPins(self):
        handler = self.getDataHandler()
        result = list(handler.getAllPins())
        return jsonify(result)        

    def getSensors(self):
        handler = self.getDataHandler()
        result = list(handler.getSensors(onlyActive=False))
        return jsonify(result)

    def getSensorsWithData(self,length):
        result = self.__requestMainSystem({"command":"sensorsWithData", "length":length})
        return result

    def getActuators(self):
        handler = self.getDataHandler()
        result = list(handler.getActuators())
        return jsonify(result)
    
    def setActuator(self):

        state = request.args.get("state")
        actuator = request.args.get("actuator")

        if(actuator == None):
            return jsonify({"success":False,"error":"actuator needed as argument"})

        #check if state is a bool
        if(state == "true"):
            stateBool = True
        elif(state == "false"):
            stateBool = False
        else:
            return jsonify({"success":False,"error":"state must be true or false"})

        #send request to main system
        response = self.__requestMainSystem({"command":"setActuator","actuator":actuator,"state":stateBool})
        return response

    def getActuatorsWithData(self,length):
        handler = self.getDataHandler()
        actuators = list(handler.getActuators(onlyActive=False))
        for actuator in actuators:
            actuator["data"] = list(handler.readData(actuator["collection"],int(length)))
            actuator["collectionSize"] = handler.getDataStackSize(actuator["collection"])
        return jsonify(actuators)

    def getLogics(self):
        handler = self.getDataHandler()
        result = list(handler.getLogics())
        return jsonify(result)
    
    def getDriectFromDB(self, collection:str, length : int):
        handler = self.getDataHandler()
        result = handler.readData(collection,length)
        return jsonify(result)

    def getAllCollections(self):
        handler = self.getDataHandler()
        result = list(handler.listDataStacks())
        return jsonify(result)

    def getSchedulerInfo(self):
        result = self.__requestMainSystem({"command":"schedulerInfo"})
        return jsonify(result)

    def startScheduler(self):
        result = self.__requestMainSystem({"command":"startScheduler"})
        return jsonify(result)

    def stopScheduler(self):
        result = self.__requestMainSystem({"command":"stopScheduler"})
        return jsonify(result)

    def getSystemInfo(self):
        result = self.__requestMainSystem({"command":"systemInfo"})
        if(self.__errorCount != None):
            result["errorCount"] = self.__errorCount.value
        else:
            result["errorCount"] = -1
        return jsonify(result)
    
    def startBrokenSensor(self):
        #get sensor from request
        sensor = request.args.get('sensor')
        #send request to main system
        response = self.__requestMainSystem({"command":"startBrokenSensor","sensor":sensor})
        return jsonify(response)

    # def run(self):
    #     self.__app.run(host="0.0.0.0")

    def errorTest(self):
        raise Exception("Test Fehler")

    def getErrors(self):
        if(self.__errorChannel == None):
            return jsonify({"error":"kein ErrorChannel deklariert."})
        result = []
        for error in self.__errorChannel:
            result.append(error)
        return jsonify(result)

    def testDB(self):
        #get sensor from request
        sensor = request.args.get('sensor')
        length = 5000
        n = 30
        #first send use main system n times and measure time
        result = self.__requestMainSystem({"command":"sensorHistory", "sensor":sensor,"length":length})
        start = datetime.now()
        for i in range(n):
            result = self.__requestMainSystem({"command":"sensorHistory", "sensor":sensor,"length":length})
        end = datetime.now()
        
        #then use data handler n times and measure time
        handler = self.getDataHandler()
        start2 = datetime.now()
        for i in range(n):
            result = handler.readData(sensor,length)
        end2 = datetime.now()

        #calculate average call time in ms and return them as json
        time1 = (end-start).total_seconds()*1000/n
        time2 = (end2-start2).total_seconds()*1000/n
        return jsonify({"avgMainSystemTime":time1,"avgDataHandlerTime":time2})


    def run(self):
        thread = threading.Thread(target=self.__app.run, kwargs={"host": "0.0.0.0"})
        thread.start()

if __name__ == "__main__":
    restApi = RestAPI()
    restApi.run()
