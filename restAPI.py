from flask import Flask, request
from flask_restful import Resource, Api

class RestApi:
    def __init__(self, mongoHandler):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.mongoHandler = mongoHandler
        
        self.api.add_resource(Pins, '/pins', '/pins/<int:pinID>')
        self.api.add_resource(PowerPlug, '/power-plugs')
        self.api.add_resource(WirelessDevices, '/wireless-devices')
        self.api.add_resource(Sensors, '/sensors')
        self.api.add_resource(Actuators, '/actuators')
        self.api.add_resource(Logics, '/logics')
        
        self.app.run(debug=True)
        
class Pins(Resource):
    def get(self, pinID=None):
        mongo = restApi.mongoHandler
        if pinID:
            return mongo.getPin(pinID)
        else:
            mode = request.args.get('mode', 'all')
            order = int(request.args.get('order', 1))
            return list(mongo.getAllPins(mode, order))

class PowerPlug(Resource):
    def post(self):
        name = request.form['name']
        codeOn = request.form['codeOn']
        codeOff = request.form['codeOff']
        mongo = restApi.mongoHandler
        mongo.addPowerPlugToWireless(name, codeOn, codeOff)
        return {'message': 'Power plug added successfully'}, 201

class WirelessDevices(Resource):
    def get(self):
        filter = request.args.to_dict()
        mongo = restApi.mongoHandler
        return list(mongo.getWirelessDevices(filter))

class Sensors(Resource):
    def post(self):
        data = request.json
        name = data['name']
        pinID = data['pinID']
        sensorClass = data['class']
        intervall = data.get('intervall', 1.0)
        active = data.get('active', True)
        mongo = restApi.mongoHandler
        if mongo.addSensor(name, pinID, sensorClass, intervall, active):
            return {'message': 'Sensor added successfully'}, 201
        else:
            return {'error': f'Sensor {name} already exists'}, 400

    def get(self):
        active = request.args.get('active', 'true').lower() == 'true'
        mongo = restApi.mongoHandler
        return list(mongo.getSensors(active))

class Actuators(Resource):
    def post(self):
        data = request.json
        name = data['name']
        type = data['type']
        collection = data['collection']
        config = data['config']
        active = data.get('active', True)
        mongo = restApi.mongoHandler
        if mongo.addActuator(name, type, collection, config, active):
            return {'message': 'Actuator added successfully'}, 201
        else:
            return {'error': f'Actuator {name} already exists'}, 400

class Logics(Resource):
    def post(self):
        data = request.json
        name = data['name']
        controller = data['controller']
        inputs = data['inputs']
        outputs = data['outputs']
        active = data.get('active', True)
        mongo = restApi.mongoHandler
        if mongo.addLogic(name, controller, inputs, outputs, active):
            return {'message': 'Logic added successfully'}, 201
        else:
            return {'error': f'Logic {name} already exists'}, 400

    def get(self):
       return "hello"
