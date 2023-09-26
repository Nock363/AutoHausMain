import sys
sys.path.insert(0, '../')
from Handler.DataHandler import DataHandler
from rpi_rf import RFDevice
import time
import threading
import logging

"""
Alle möglichen Handler, welche zur Verwaltung von drahtlosen Schnittstellen gebraucht werden.
"""
logging.getLogger("rpi_rf").setLevel(logging.WARNING)

class RadioHandler():
    """Verwaltet den 433 MHz Kanal"""
    rxPin = 5
    txPin = 6

    lock = threading.Lock()

    def __init__(self):
        self.rxDevice = RFDevice(self.rxPin)
        self.txDevice = RFDevice(self.txPin)
        self.txDevice.enable_tx()
        self.dataHandler = DataHandler()
        # self.configHandler = ConfigHandler()

        #initiate logger for this module who can be disabled
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARNING)
        self.logger.info("RadioHandler wurde initialisiert")

    
    def addPowerPlug(self,name):
        """Fügt neue Objekte des Types PowerPlug zur Datenbank hinzu"""
        self.rxDevice.enable_rx()
        #TODO: passend deaktivieren
        print("suche nach Code zum ANSCHALTEN")
        
        on = self.findCode()
        codeOn = on["code"]
        pulseOn = on["pulseLength"]
        print("Code gefunden!")
        time.sleep(2)
        print("suche nach Code zum AUSSCHALTEN")
        off = self.findCode()
        codeOff = off["code"]
        pulseOff = off["pulseLength"]
        

        result = self.dataHandler.addActuator(name=name,type="Plug433Mhz_Actuator",collection="Plugs433Mhz",config={"codeOn":codeOn,"codeOff":codeOff,"pulseLength":pulseOn,"initialState":False})

        if(result):
            print("neuer Stecker hinzugefügt")
        else:
            print("Stecker wurde nicht hinzugefügt!")
        
        return result

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
                    print(f"Noch ein Code wurde gefunden! {counter}/{sameCodeRequirement}")
                    counter = counter + 1
                    pulseLength = pulseLength + self.rxDevice.rx_pulselength

                else:
                    counter = 0
                    pulseLength = 0
                    lastCode = code
            time.sleep(0.01)
        pulseLength = pulseLength/sameCodeRequirement

        print(f"Code wurde gefunden: {lastCode}, Pulslänge: {pulseLength}")
        return {"code":lastCode,"pulseLength":pulseLength}

    def sendCode(self,code,repeats,pulseLength):
        try:
            #deaktiviere receiver, damit keine nervigen logs kommen
            #self.rxDevice.disable_rx()
            with self.lock:
                self.txDevice.tx_repeat = repeats
                self.txDevice.tx_code(code, 1, pulseLength, 24)

            #aktiviere receiver wieder
            #self.rxDevice.enable_rx()

            return True
        except Exception as err:
            self.logger.error("Etwas ist in RadioHandler.sendCode schiefgelaufen :(")
            self.logger.error(err)
            return False

        