from Handler.DatabaseHandlers import MongoHandler
handler = MongoHandler()


#Füge AHT20 Sensor auf Pin 7 hinzu:
inputs = [{"sensor":"AHT20_Single","data":("humidity","temperature")}]
outputs = [{"actuator":"plugA"}]

handler.addLogic("AHT20_Single","FanController",inputs,outputs)


logics = handler.getAllLogics()
for l in logics:
    print(l["inputs"])