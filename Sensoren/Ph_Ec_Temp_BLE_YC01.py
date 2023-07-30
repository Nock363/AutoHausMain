from bluepy.btle import Peripheral, Scanner, DefaultDelegate, UUID
import sys
import logging
import time
sys.path.insert(0, '../')
from Sensoren.Sensor import Sensor


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class Ph_Ec_Temp_PPM_mV_BLE_YC01(Sensor):

    def __init__(self,name:str,pinID,collection:str,*args, **kwargs):
        dataStructure={"PH":float,"EC":int,"Temperature":float}
        super().__init__(
            name=name,
            collection=collection,
            pinID = pinID,
            dataStructure=dataStructure,
            range=(0,15),               #TODO: Range nur für PH angewendet und nicht für ec
            *args,
            **kwargs)
        
        # MAC-Addresse der Poolsonde 
        # TODO: statt hardcoded durch scan finden anhand von Namen
        self.__device_address = "c0:00:00:01:9c:8e"
        self.__characteristic_uuid = "0000ff01-0000-1000-8000-00805f9b34fb"
        self.__peripheral = self.__connectToDevice(self.__device_address)


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

        #PPM Wert auslesen (byte 7 und 8)
        ppm = int(byteStream[7] << 8) + int(byteStream[8])

        #mV Wert auslesen (byte 9 und 10)
        mv = int(byteStream[9] << 8) + int(byteStream[10])

        #Temperatur auslesen (byte 13 und 14)
        temp = int(byteStream[13] << 8) + int(byteStream[14]) * 0.1


        output = {"ph":ph,"ec":ec,"ppm":ppm,"mV":mv,"temp":temp}
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
                self.__connectToDevice(tryBudget-1,device_address)
            else:
                raise Exception("Keine Verbindung zum Gerät möglich. Versuche aufgebraucht.")

    def __readDataFromDevice(self,tryBudget = 2):
        #try to read data. If not possible, try to reconnect
        try:
            data = read_characteristic_data(self.__peripheral, self.__characteristic_uuid)
            return data
        except Exception as e:
            logging.error(f"Keine Daten vom Gerät lesbar: {e}")
            if tryBudget > 0:
                logging.info(f"Erneuter Verbindungsversuch wird gestartet. Versuche übrig: {tryBudget-1}")
                self.__peripheral = self.__connectToDevice(self.__device_address)
                self.__readDataFromDevice(tryBudget-1)
            else:
                raise Exception("Keine Daten vom Gerät lesbar. Versuche aufgebraucht.")


    def run(self):
              
        raw  = self.__readDataFromDevice()
        decoded = self.__decode(raw)
        data = self.__interpretBytes(decoded)
        return super().createData(data)

        