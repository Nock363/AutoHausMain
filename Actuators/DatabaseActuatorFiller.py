import sys
# from HudTemp_AHT20 import HudTemp_AHT20
sys.path.insert(0, '../Handler/')
from DatabaseHandlers import MongoHandler


handler = MongoHandler()


#Füge AHT20 Sensor auf Pin 7 hinzu:
plugAConfig = {"codeOn":1361,"codeOff":1364,"pulseLength":320}
handler.addActuator(name="plugA",type="Plug433Mhz_Actuator",collection="Plugs433Mhz",config=plugAConfig)
