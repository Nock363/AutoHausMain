from DatabaseHandlers import MongoHandler
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
        codeOn = self.findCode()
        logging.info("suche nach Code zum AUSSCHALTEN")
        codeOff = self.findCode()

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
        return list(self.mongoHandler.getWirelessDevices(filter))

    def findCode(self):
        timestamp = None
        lastCode = 0
        counter = 0
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

                else:
                    counter = 0
                    lastCode = code
            time.sleep(0.01)

        logging.info(f"Code wurde gefunden: {lastCode}")
        return lastCode



