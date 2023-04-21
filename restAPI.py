from flask import Flask, request, jsonify
from flask_cors import CORS
from Handler.DatabaseHandlers import MongoHandler
from Handler.JsonHandlers import ConfigHandler
from multiprocessing import Event
from Scheduler import Scheduler
from flask import send_from_directory
import os

class RestAPI():

    __app : Flask = None
    __scheduler : Scheduler

    def __init__(self,scheduler = None):
        # self.__app = Flask(__name__, static_folder='AutoHaus_UserInterface')
        self.__app = Flask(__name__, static_folder='AutoHaus_UserInterface')
        
        CORS(self.__app)
        self.__mongoHandler = MongoHandler()
        self.__configHandler = ConfigHandler()
        self.__scheduler = scheduler

        self.__userInterfacePath = "AutoHaus_UserInterface/"

        print(f"static folder path: {self.__app.static_folder}")
    
        static_files = [f for f in os.listdir(self.__app.static_folder) if os.path.isfile(os.path.join(self.__app.static_folder, f))]
        print(static_files)


        self.__app.route("/home",methods=["GET"])(self.getHome)
        self.__app.route("/pins",methods=["GET"])(self.getPins)
        self.__app.route("/sensors",methods=["GET"])(self.getSensors)
        self.__app.route("/sensorsWithData/<length>",methods=["GET"])(self.getSensorsWithData)
        self.__app.route("/actuators",methods=["GET"])(self.getActuators)
        self.__app.route("/actuatorsWithData/<length>",methods=["GET"])(self.getActuatorsWithData)
        self.__app.route("/logics",methods=["GET"])(self.getLogics)
        self.__app.route("/data/<collection>/<length>",methods=["GET"])(self.getDataFromCollection)
        self.__app.route("/collections",methods=["GET"])(self.getAllCollections)
        self.__app.route("/stopScheduler",methods=["GET"])(self.stopScheduler)
        self.__app.route("/startScheduler",methods=["GET"])(self.startScheduler)
        self.__app.route("/schedulerInfo",methods=["GET"])(self.getSchedulerInfo)
        self.__app.route("/systemInfo",methods=["GET"])(self.getSystemInfo)
        

    def getPins(self):
        result = list(self.__mongoHandler.getAllPins())
        for r in result:
            r.pop("_id")
        print(result)
        return jsonify(result)        

    def getSensors(self):
        result = list(self.__configHandler.getSensors(onlyActive=False))
        return jsonify(result)

    def getSensorsWithData(self,length):
        sensors = list(self.__configHandler.getSensors(onlyActive=False))
        for sensor in sensors:
            sensor["data"] = list(self.__mongoHandler.getDataFromCollection(sensor["collection"],int(length)))
            sensor["collectionSize"] = self.__mongoHandler.getCollectionSize(sensor["collection"])
        return jsonify(sensors)

    def getActuators(self):
        result = list(self.__configHandler.getActuators())
        return jsonify(result)
    
    def getActuatorsWithData(self,length):
        actuators = list(self.__configHandler.getActuators(onlyActive=False))
        for actuator in actuators:
            actuator["data"] = list(self.__mongoHandler.getDataFromCollection(actuator["collection"],int(length)))
            actuator["collectionSize"] = self.__mongoHandler.getCollectionSize(actuator["collection"])
        return jsonify(actuators)

    def getLogics(self):
        result = list(self.__configHandler.getLogics())
        return jsonify(result)
    
    def getDataFromCollection(self, collection:str, length : int):
        result = list(self.__mongoHandler.getDataFromCollection(collection,int(length)))
        # for r in result:
        #     r.pop("_id")   
        return jsonify(result)

    def getAllCollections(self):
        result = list(self.__mongoHandler.getAllCollections())
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
        result = {}
        actuators = list(self.__configHandler.getActuators(onlyActive=False))
        for actuator in actuators:
            actuator["data"] = list(self.__mongoHandler.getDataFromCollection(actuator["collection"],1))
            actuator["collectionSize"] = self.__mongoHandler.getCollectionSize(actuator["collection"])

        sensors = list(self.__configHandler.getSensors(onlyActive=False))
        for sensor in sensors:
            sensor["data"] = list(self.__mongoHandler.getDataFromCollection(sensor["collection"],1))
            sensor["collectionSize"] = self.__mongoHandler.getCollectionSize(sensor["collection"])

        logics = list(self.__configHandler.getLogics())

        scheduler = {"status":self.__scheduler.statusProcess(),"available":(self.__scheduler != None)}
            
        return jsonify({"scheduler":scheduler,"sensors":sensors,"actuators":actuators,"logics":logics})


    def run(self):
        self.__app.run(host="0.0.0.0")
    

if __name__ == "__main__":
    restApi = RestAPI()
    restApi.run()