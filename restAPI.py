from flask import Flask, request, jsonify
from Handler.DatabaseHandlers import MongoHandler
from Handler.JsonHandlers import ConfigHandler


class RestAPI():


    __app : Flask = None

    def __init__(self):
        self.__app = Flask(__name__)
        self.__mongoHandler = MongoHandler()
        self.__configHandler = ConfigHandler()


        self.__app.route("/pins",methods=["GET"])(self.getPins)
        self.__app.route("/sensors",methods=["GET"])(self.getSensors)
        self.__app.route("/actuators",methods=["GET"])(self.getActors)
        self.__app.route("/logics",methods=["GET"])(self.getLogics)
        self.__app.route("/data/<collection>/<length>",methods=["GET"])(self.getDataFromCollection)

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




    def run(self):
        self.__app.run()
    
