import sys
sys.path.insert(0, '../')
from Handler.DatabaseHandlers import MongoHandler
from rpi_rf import RFDevice
import time

import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

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

    
    def addPowerPlug(self,name):
        """Fügt neue Objekte des Types PowerPlug zur Datenbank hinzu"""
        
        logging.info("suche nach Code zum ANSCHALTEN")
        
        on = self.findCode()
        codeOn = on["code"]
        pulseOn = on["pulseLength"]
        logging.info("suche nach Code zum AUSSCHALTEN")
        off = self.findCode()
        codeOff = off["code"]
        pulseOff = off["pulseLenght"]
        

        #prüfe die Datenbank nach Objekten mit selben Namen oder selben Codes
        filter = {"$or":[{"codeOn":codeOn},{"codeOff":codeOff},{"name":name}]}
        results = list(self.mongoHandler.getWirelessDevices())
        if(len(results) == 0):
            self.mongoHandler.addPowerPlugToWireless(name,codeOn,codeOff)
            logging.info("neuer Stecker hinzugefügt")
        else:
            logging.info("Überschneidung mit bereits exisitierenden Elementen in der Datenbank")
            logging.info(results)

    def getPowerPlug(self,name):
        filter = {"type":"plug","name":name}
        result = list(self.mongoHandler.getWirelessDevices(filter))
        if(len(result) > 1):
            logging.error(f"Mehr als ein Plug mit dem Name {name}")
        return result[0]

    def findCode(self):
        timestamp = None
        lastCode = 0
        counter = 0
        pulseLength = 0
        sameCodeRequirement = 10
        while True:
            if(self.rxDevice.rx_code_timestamp != timestamp):
                timestamp = self.rxDevice.rx_code_timestamp
                code = self.rxDevice.rx_code
                if(code == lastCode):
                    if(counter == sameCodeRequirement):
                        break
                    logging.info(f"Noch ein Code wurde gefunden! {counter}/{sameCodeRequirement}")
                    counter = counter + 1
                    pulseLength = pulseLength + self.rxDevice.rx_pulselength

                else:
                    counter = 0
                    pulseLength = 0
                    lastCode = code
            time.sleep(0.01)
        pulseLength = pulseLength/sameCodeRequirement

        logging.info(f"Code wurde gefunden: {lastCode}, Pulslänge: {pulseLength}")
        return {"code":lastCode,"pulseLength":pulseLength}

    def sendCode(self,code,repeats,pulseLength):
        try:
            self.txDevice.tx_repeat = repeats
            self.txDevice.tx_code(code, 1, pulseLength, 24)
            return True
        except Exception as err:
            logging.error("Etwas ist in RadioHandler.sendCode schiefgelaufen :(")
            logging.error(err)
            return False

        