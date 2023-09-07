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

    def __init__(self,reqChannel,respChannel,mainSystem = None):
        self.__app = Flask(__name__)
        CORS(self.__app)
        self.__mainSystem = mainSystem#TODO Purge that shit!
        self.__dataHandler = DataHandler()

        with self.__app.app_context():
            g._dataHandler = DataHandler()
            
        self.__reqChannel = reqChannel
        self.__respChannel = respChannel
        self.__requestID = 1

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
    
    def setActuator(self,name,state):

        stateBool = (state.lower() == "true")
        
        ret = self.__mainSystem.setActuator(name,stateBool)
        if(ret == True):
            return jsonify({"success":True})
        else:
            return jsonify({"success":False,"error":ret})

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
        return jsonify(result)
    
    def startBrokenSensor(self):
        #get sensor from request
        sensor = request.args.get('sensor')
        #send request to main system
        response = self.__requestMainSystem({"command":"startBrokenSensor","sensor":sensor})
        return jsonify(response)

    # def run(self):
    #     self.__app.run(host="0.0.0.0")

    def run(self):
        thread = threading.Thread(target=self.__app.run, kwargs={"host": "0.0.0.0"})
        thread.start()

if __name__ == "__main__":
    restApi = RestAPI()
    restApi.run()
