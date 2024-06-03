from scapy.all import *

def scan_wifi():
    networks = []

    def packet_handler(packet):
        if packet.haslayer(Dot11Beacon):
            ssid = packet[Dot11Elt].info.decode()
            bssid = packet[Dot11].addr2
            if ssid not in [net['SSID'] for net in networks]:
                networks.append({'SSID': ssid, 'BSSID': bssid})

    print("Scanning for networks...")
    sniff(iface="wlan0", prn=packet_handler, timeout=10)
    
    return networks

networks = scan_wifi()
for network in networks:
    print(f"SSID: {network['SSID']}, BSSID: {network['BSSID']}")
