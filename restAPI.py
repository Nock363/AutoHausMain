from flask import Flask, request, jsonify
from Handler.DatabaseHandlers import MongoHandler
from Handler.JsonHandlers import ConfigHandler
from multiprocessing import Event
from Scheduler import Scheduler

class RestAPI():


    __app : Flask = None
    __scheduler : Scheduler

    def __init__(self,scheduler = None):
        self.__app = Flask(__name__)
        self.__mongoHandler = MongoHandler()
        self.__configHandler = ConfigHandler()
        self.__scheduler = scheduler

        self.__app.route("/pins",methods=["GET"])(self.getPins)
        self.__app.route("/sensors",methods=["GET"])(self.getSensors)
        self.__app.route("/actuators",methods=["GET"])(self.getActors)
        self.__app.route("/logics",methods=["GET"])(self.getLogics)
        self.__app.route("/data/<collection>/<length>",methods=["GET"])(self.getDataFromCollection)
        self.__app.route("/stopScheduler",methods=["GET"])(self.stopScheduler)
        self.__app.route("/startScheduler",methods=["GET"])(self.startScheduler)
        

    def getPins(self):
        result = list(self.__mongoHandler.getAllPins())
        for r in result:
            r.pop("_id")
        print(result)
        return jsonify(result)        

    def getSensors(self):
        result = list(self.__configHandler.getSensors())
        return jsonify(result)

    def getActors(self):
        result = list(self.__configHandler.getActuators())
        return jsonify(result)
    
    def getLogics(self):
        result = list(self.__configHandler.getLogics())
        return jsonify(result)
    
    def getDataFromCollection(self, collection:str, length : int):
        result = list(self.__mongoHandler.getDataFromCollection(collection,int(length)))
        for r in result:
            r.pop("_id")   
        return jsonify(result)

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
    



    def run(self):
        self.__app.run()
    
