import sys
from HudTemp_AHT20 import HudTemp_AHT20
sys.path.insert(0, '../Handler/')
from DatabaseHandlers import MongoHandler


handler = MongoHandler()


#Füge AHT20 Sensor auf Pin 7 hinzu:
handler.addSensor("AHT20_Single",7,"/home/user/AutoHausMain/Sensoren/HudTemp_AHT20.py")