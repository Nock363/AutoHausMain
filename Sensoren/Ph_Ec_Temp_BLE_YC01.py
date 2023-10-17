from bluepy.btle import Peripheral, Scanner, DefaultDelegate, UUID
import sys
import logging
import time
sys.path.insert(0, '../')
from Sensoren.Sensor import Sensor


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class Ph_Ec_Temp_BLE_YC01(Sensor):
    
    def dataStructure(self):
        return {
            "PH":{"dataType":float,"unit":None,"range":(0,14)},
            "EC":{"dataType":int,"unit":"uS","range":(0,1500)},
            "Temperature":{"dataType":float,"unit":"Grad","range":(0,30.0)},
            "mV":{"dataType":int,"unit":"mV","range":(0,1500)}
        }
    
    #TODO: Prüfen ob Ec korrekt angezeigt wird wenn mS statt uS
    # def __init__(self,name:str,collection:str,*args, **kwargs):
        
    #     super().__init__(
    #         name=name,
    #         collection=collection,
    #         dataStructure=dataStructure,
    #         *args,
    #         **kwargs)
        
    #     # MAC-Addresse der Poolsonde 
    #     # TODO: statt hardcoded durch scan finden anhand von Namen
    #     if(super().active):
    #         self.setup()
    
    def setup(self):
        self.__device_address = "c0:00:00:01:9c:8e"
        self.__characteristic_uuid = "0000ff01-0000-1000-8000-00805f9b34fb"
        self.__peripheral = self.__connectToDevice(self.__device_address,tryBudget=100)

        #System need second connection run after first request. So start request.
        time.sleep(1)
        self.run()



    def __del__(self):
        if(super().active):
            print("BLE Poolsonde wird gelöscht")
            self.__peripheral.disconnect()

    def __decode(self,pValue):
        pValue = bytearray(pValue)  # Convert to mutable bytearray
        len_pValue = len(pValue)

        for i in range(len_pValue - 1, 0, -1):
            tmp = pValue[i]
            hibit1 = (tmp & 0x55) << 1
            lobit1 = (tmp & 0xAA) >> 1
            tmp = pValue[i - 1]
            hibit = (tmp & 0x55) << 1
            lobit = (tmp & 0xAA) >> 1

            pValue[i] = (hibit1 | lobit)
            pValue[i - 1] = (hibit | lobit1)

        negatedByteStream = bytearray()
        for b in bytes(pValue):
            negB = ~b
            #cast negB as byte
            negB = negB & 0xFF
            negatedByteStream.append(negB)
        return negatedByteStream

    def __interpretBytes(self,byteStream):

        #PH Wert auslesen (byte 3 und 4)
        ph_int = int(byteStream[3] << 8) + int(byteStream[4])
        ph = ph_int*0.01

        #EC Wert auslesen (byte 5 und 6)
        ec = int(byteStream[5] << 8) + int(byteStream[6])

        #falls angabe in mS statt uS umrechnen: LSB von Byte 17.
        if(byteStream[17] & 0x01 == 1):
            ec = ec*1000

        #prüfen ob ec = 0 ist. Das bedeutet, dass die Sonde nicht im Wasser ist. es wird ein Fehler getriggert
        if(ec == 0):
            raise Exception("Poolsonde befindet sich nicht im wasser!. Der EC Wert ist 0")

        #PPM Wert auslesen (byte 7 und 8)
        ppm = int(byteStream[7] << 8) + int(byteStream[8])

        #mV Wert auslesen (byte 9 und 10)
        mv = int(byteStream[9] << 8) + int(byteStream[10])

        #Temperatur auslesen (byte 13 und 14)
        temp = int(byteStream[13] << 8) + int(byteStream[14]) * 0.1


        output = {"PH":ph,"EC":ec,"Temperature":temp,"mV":mv}
        print(output)
        return output

    def __connectToDevice(self,device_address,tryBudget = 5):
        try:
            peripheral = Peripheral(device_address)
            return peripheral
        except Exception as e:
            logging.error(f"Keine Verbindung zum Gerät möglich: {e}")
            if tryBudget > 0:
                logging.info(f"Erneuter Verbindungsversuch wird gestartet. Versuche übrig: {tryBudget-1}")
                self.__connectToDevice(device_address,tryBudget-1)
            else:
                raise Exception("Keine Verbindung zum Gerät möglich. Versuche aufgebraucht.")

    def __readDataFromDevice(self,tryBudget = 2):
        #try to read data. If not possible, try to reconnect
        try:
            service_uuid = UUID(self.__characteristic_uuid)
            service = self.__peripheral.getServiceByUUID(service_uuid)
            characteristic = service.getCharacteristics()[0]
            data = characteristic.read()
            return data
        except Exception as e:
            logging.error(f"Keine Daten vom Gerät lesbar: {e}")
            if tryBudget > 0:
                logging.info(f"Erneuter Verbindungsversuch wird gestartet. Versuche übrig: {tryBudget-1}")
                self.__peripheral = self.__connectToDevice(self.__device_address,tryBudget=tryBudget)
                return self.__readDataFromDevice(tryBudget-1)
            else:
                raise Exception("Keine Daten vom Gerät lesbar. Versuche aufgebraucht.")

    def genData(self):
        if(super().active):
            raw  = self.__readDataFromDevice(tryBudget = 100)
            decoded = self.__decode(raw)
            data = self.__interpretBytes(decoded)
            return super().createData(data)
        # else:
        #     logging.error(f"Pool Sonde ist nicht aktiv, wurde aber versucht per run() ausgeführt werden. Das sollte nicht passieren.")
        