import sys
# from HudTemp_AHT20 import HudTemp_AHT20
sys.path.insert(0, '../Handler/')
from DatabaseHandlers import MongoHandler


handler = MongoHandler()


#Füge AHT20 Sensor auf Pin 7 hinzu:
handler.addSensor("AHT20_Single",1,"HudTemp_AHT20")
handler.addSensor("Dummy",3,"Dummy_Sensor")
handler.addSensor("Co2H2Eth_SPG30",2,"Co2H2Eth_SPG30")