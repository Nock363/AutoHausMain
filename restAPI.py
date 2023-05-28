from flask import Flask, request, jsonify, g
from flask_cors import CORS
from Handler.DataHandler import DataHandler
from multiprocessing import Event
from Scheduler import Scheduler
from flask import send_from_directory
import os

class RestAPI():

    __app : Flask = None
    __scheduler : Scheduler

    def __init__(self,scheduler = None):
        self.__app = Flask(__name__)
        CORS(self.__app)
        self.__scheduler = scheduler

        with self.__app.app_context():
            g._dataHandler = DataHandler()
            


        self.__userInterfacePath = "AutoHaus_UserInterface/"

        self.__app.route("/pins",methods=["GET"])(self.getPins)
        self.__app.route("/sensors",methods=["GET"])(self.getSensors)
        self.__app.route("/sensorsWithData/<length>",methods=["GET"])(self.getSensorsWithData)
        self.__app.route("/actuators",methods=["GET"])(self.getActuators)
        self.__app.route("/actuatorsWithData/<length>",methods=["GET"])(self.getActuatorsWithData)
        self.__app.route("/logics",methods=["GET"])(self.getLogics)
        self.__app.route("/data/<collection>/<length>",methods=["GET"])(self.getFromBD)
        self.__app.route("/collections",methods=["GET"])(self.getAllCollections)
        self.__app.route("/stopScheduler",methods=["GET"])(self.stopScheduler)
        self.__app.route("/startScheduler",methods=["GET"])(self.startScheduler)
        self.__app.route("/schedulerInfo",methods=["GET"])(self.getSchedulerInfo)
        self.__app.route("/systemInfo",methods=["GET"])(self.getSystemInfo)
        self.__app.route("/setActuator/<name>/<state>")(self.setActuator)

    def getDataHandler(self):
        handler = getattr(g, '_dataHandler', None)
        if handler is None:
            handler = DataHandler()
            g._dataHandler = handler
        return handler


    def getPins(self):
        handler = self.getDataHandler()
        result = list(handler.getAllPins())
        return jsonify(result)        

    def getSensors(self):
        handler = self.getDataHandler()
        result = list(handler.getSensors(onlyActive=False))
        return jsonify(result)

    def getSensorsWithData(self,length):
        handler = self.getDataHandler()
        sensors = list(handler.getSensors(onlyActive=False))
        for sensor in sensors:
            sensor["data"] = list(handler.read(sensor["collection"],int(length)))
            sensor["collectionSize"] = handler.getCollectionSize(sensor["collection"])
        return jsonify(sensors)

    def getActuators(self):
        handler = self.getDataHandler()
        result = list(handler.getActuators())
        return jsonify(result)
    
    def setActuator(self,name,state):
        
        stateBool = (state.lower() == "true")
        
        ret = self.__scheduler.setActuator(name,stateBool)
        if(ret == True):
            return jsonify({"success":True})
        else:
            return jsonify({"success":False,"error":ret})

    def getActuatorsWithData(self,length):
        handler = self.getDataHandler()
        actuators = list(handler.getActuators(onlyActive=False))
        for actuator in actuators:
            actuator["data"] = list(handler.read(actuator["collection"],int(length)))
            actuator["collectionSize"] = handler.getCollectionSize(actuator["collection"])
        return jsonify(actuators)

    def getLogics(self):
        handler = self.getDataHandler()
        result = list(handler.getLogics())
        return jsonify(result)
    
    def getFromBD(self, collection:str, length : int):
        handler = self.getDataHandler()
        result = handler.read(collection,length)
        return jsonify(result)

    def getAllCollections(self):
        handler = self.getDataHandler()
        result = list(handler.listCollectionStacks())
        return jsonify(result)

    def getSchedulerInfo(self):
        if(self.__scheduler == None):
            return jsonify({"success":False,"error":"Kein Scheduler konfiguriert"})
        return jsonify({"status":self.__scheduler.statusProcess()})

    def startScheduler(self):
        if(self.__scheduler == None):
            return jsonify({"success":False,"error":"Kein Scheduler konfiguriert"})
        
        self.__scheduler.startProcess()
        return jsonify({"success":True})

    def stopScheduler(self):
        if(self.__scheduler == None):
            return jsonify({"success":False,"error":"Kein Scheduler konfiguriert"})
        
        self.__scheduler.stopProcess()
        return jsonify({"success":True})
    

    def getSystemInfo(self):
        handler = self.getDataHandler()
        result = {}
        actuators = list(handler.getActuators(onlyActive=False))
        for actuator in actuators:
            actuator["data"] = list(handler.read(actuator["collection"],1))
            actuator["collectionSize"] = handler.getCollectionSize(actuator["collection"])

        sensors = list(handler.getSensors(onlyActive=False))
        for sensor in sensors:
            sensor["data"] = list(handler.read(sensor["collection"],1))
            sensor["collectionSize"] = handler.getCollectionSize(sensor["collection"])

        logics = list(handler.getLogics())

        scheduler = {"status":self.__scheduler.statusProcess(),"available":(self.__scheduler != None)}
            
        return jsonify({"scheduler":scheduler,"sensors":sensors,"actuators":actuators,"logics":logics})


    def run(self):
        self.__app.run(host="0.0.0.0")

if __name__ == "__main__":
    restApi = RestAPI()
    restApi.run()
