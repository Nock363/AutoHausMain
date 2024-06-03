import netifaces

def check_network():
    # Überprüfe alle verfügbaren Schnittstellen
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        # Erhalte Informationen über die Schnittstelle
        addrs = netifaces.ifaddresses(interface)
        # Überprüfe, ob eine IP-Adresse vorhanden ist
        if netifaces.AF_INET in addrs:
            # Es wurde eine IP-Adresse gefunden, also ist das Netzwerk vorhanden
            return True
    # Keine IP-Adresse gefunden, also ist kein Netzwerk vorhanden
    return False

def setup_own_network():
    # Füge hier den Code ein, um dein eigenes WLAN-Netzwerk aufzusetzen
    pass

if __name__ == "__main__":
    if check_network():
        print("Ein Netzwerk ist bereits vorhanden.")
    else:
        print("Kein Netzwerk gefunden. Richte eigenes Netzwerk ein.")
        setup_own_network()
