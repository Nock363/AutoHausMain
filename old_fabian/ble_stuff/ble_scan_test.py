from bluepy.btle import Scanner, DefaultDelegate

# Eigene Implementierung des DefaultDelegates
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    # Wird aufgerufen, wenn ein neues Gerät gefunden wird
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Neues Gerät gefunden: {dev.addr} ({dev.addrType}), RSSI={dev.rssi} dB")
        elif isNewData:
            print(f"Neue Daten von {dev.addr}: RSSI={dev.rssi} dB")

# Initialisiere den Scanner
scanner = Scanner().withDelegate(ScanDelegate())

# Scanne BLE-Geräte für 10 Sekunden
timeout = 10.0
devices = scanner.scan(timeout)

# Zeige die gefundenen Geräte an
print("Gefundene BLE-Geräte:")
for dev in devices:
    print(f"Name: {dev.getValueText(9)}")
    print(f"Adresse: {dev.addr}")
    print(f"RSSI: {dev.rssi} dB")
    print()
