from bluepy.btle import Peripheral, Scanner, DefaultDelegate

# Eigene Implementierung des DefaultDelegates
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    # Wird aufgerufen, wenn ein neues Gerät gefunden wird
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Neues Gerät gefunden: {dev.addr} ({dev.addrType}), RSSI={dev.rssi} dB")

# Adresse des Geräts, mit dem du dich verbinden möchtest
device_address = "c0:00:00:01:9c:8e"

try:
    # Verbinde dich mit dem Gerät
    print(f"Verbinde mit {device_address}")
    peripheral = Peripheral(device_address)

    # Scanne nach Services und Charakteristiken
    print("Gefundene Services und Charakteristiken:")
    services = peripheral.getServices()
    for service in services:
        print(f"Service UUID: {service.uuid}")
        for char in service.getCharacteristics():
            print(f"  Charakteristik UUID: {char.uuid}")

    # Trenne die Verbindung zum Gerät
    peripheral.disconnect()
    print("Verbindung getrennt.")
except Exception as e:
    print(f"Fehler bei der Verbindung oder Datenabfrage: {e}")
