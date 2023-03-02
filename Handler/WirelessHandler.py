import sys
sys.path.insert(0, '../')
from Handler.DatabaseHandlers import MongoHandler
from rpi_rf import RFDevice
import time

import logging



logging.basicConfig(encoding='utf-8', level=logging.ERROR)

"""
Alle möglichen Handler, welche zur Verwaltung von drahtlosen Schnittstellen gebraucht werden.
"""


class RadioHandler():
    """Verwaltet den 433 MHz Kanal"""
    rxPin = 5
    txPin = 6



    def __init__(self):
        self.rxDevice = RFDevice(self.rxPin)
        self.txDevice = RFDevice(self.txPin)
        self.txDevice.enable_tx()
        self.rxDevice.enable_rx()
        self.mongoHandler = MongoHandler()


        #initiate logger for this module who can be disabled
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.info("RadioHandler wurde initialisiert")

    
    def addPowerPlug(self,name):
        """Fügt neue Objekte des Types PowerPlug zur Datenbank hinzu"""
        
        self.logger.info("suche nach Code zum ANSCHALTEN")
        
        on = self.findCode()
        codeOn = on["code"]
        pulseOn = on["pulseLength"]
        self.logger.info("suche nach Code zum AUSSCHALTEN")
        off = self.findCode()
        codeOff = off["code"]
        pulseOff = off["pulseLength"]
        

        #prüfe die Datenbank nach Objekten mit selben Namen oder selben Codes
        filter = {"$or":[{"config.codeOn":codeOn},{"config.codeOff":codeOff},{"name":name}]}
        print(filter)
        result = self.mongoHandler.getSingleActuator(filter)
        print(f"resultType: {type(result)}")
        if(result is None):
            #addActuator(self,name:str,type:str,collection:str,config:dict,active:bool=True):
            self.mongoHandler.addActuator(name=name,type="Plug433Mhz_Actuator",collection="Plugs433Mhz",config={"codeOn":codeOn,"codeOff":codeOff,"pulseLength":pulseOn})
            self.logger.info("neuer Stecker hinzugefügt")
        else:
            self.logger.info("Überschneidung mit bereits exisitierenden Elementen in der Datenbank")
            self.logger.info(result)

    def getPowerPlug(self,name):
        filter = {"type":"plug","name":name}
        result = list(self.mongoHandler.getWirelessDevices(filter))
        if(len(result) > 1):
            self.logger.error(f"Mehr als ein Plug mit dem Name {name}")
        return result[0]

    def findCode(self):
        timestamp = None
        lastCode = 0
        counter = 0
        pulseLength = 0
        sameCodeRequirement = 5
        while True:
            if(self.rxDevice.rx_code_timestamp != timestamp):
                timestamp = self.rxDevice.rx_code_timestamp
                code = self.rxDevice.rx_code
                if(code == lastCode):
                    if(counter == sameCodeRequirement):
                        break
                    self.logger.info(f"Noch ein Code wurde gefunden! {counter}/{sameCodeRequirement}")
                    counter = counter + 1
                    pulseLength = pulseLength + self.rxDevice.rx_pulselength

                else:
                    counter = 0
                    pulseLength = 0
                    lastCode = code
            time.sleep(0.01)
        pulseLength = pulseLength/sameCodeRequirement

        self.logger.info(f"Code wurde gefunden: {lastCode}, Pulslänge: {pulseLength}")
        return {"code":lastCode,"pulseLength":pulseLength}

    def sendCode(self,code,repeats,pulseLength):
        try:
            #deaktiviere receiver, damit keine nervigen logs kommen
            #self.rxDevice.disable_rx()

            self.txDevice.tx_repeat = repeats
            self.txDevice.tx_code(code, 1, pulseLength, 24)

            #aktiviere receiver wieder
            #self.rxDevice.enable_rx()

            return True
        except Exception as err:
            self.logger.error("Etwas ist in RadioHandler.sendCode schiefgelaufen :(")
            self.logger.error(err)
            return False

        