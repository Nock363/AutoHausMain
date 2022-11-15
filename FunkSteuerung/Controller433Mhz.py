from rpi_rf import RFDevice
import time

class Controller433MHz():

    def __init__(self,rxPin=2,txPin=3,repeats = 10):
        self.rxPin = rxPin
        self.txPin = txPin
        self.rxDevice = RFDevice(rxPin)
        self.txDevice = RFDevice(txPin)
        self.txDevice.enable_tx()
        self.rxDevice.enable_rx()
    

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
                    print(f"Noch ein Code wurde gefunden! {counter}/{sameCodeRequirement}")
                    counter = counter + 1

                else:
                    counter = 0
                    lastCode = code
            time.sleep(0.01)

        print(f"Code wurde gefunden: {lastCode}")

    def findPlug(self):
        


        print("Starte Funksteckdosen erkennung\n")
        print("Bitte drücke auf der Verbedienung bitte die Taste zum anschalten und halte diese Gedrückt")
        code = self.findCode()


controller = Controller433MHz()
controller.findPlug()