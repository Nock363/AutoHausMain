#!/bin/bash

# Funktion zum Überprüfen der Verbindung zum lokalen Netzwerk
check_ethernet() {
    # Überprüfe die Ausgabe von ifconfig auf das Vorhandensein einer IP-Adresse
    if ifconfig | grep -q "eth0"; then
        return 0 # Erfolgreich: Rückgabewert 0
    else
        return 1 # Fehlgeschlagen: Rückgabewert 1
    fi
}

check_wlan() {
    # Überprüfe die Ausgabe von ifconfig auf das Vorhandensein einer IP-Adresse
    if ifconfig | grep -q "wlan0"; then
        return 0 # Erfolgreich: Rückgabewert 0
    else
        return 1 # Fehlgeschlagen: Rückgabewert 1
    fi
}

check_hostapd_service() {
    # Überprüfe den Status des hostapd-Dienstes mit systemctl
    if systemctl is-active --quiet hostapd.service; then
        echo "Der Service hostapd läuft."
        return 0 # Erfolgreich: Rückgabewert 0
    else
        echo "Der Service hostapd läuft nicht."
        return 1 # Fehlgeschlagen: Rückgabewert 1
    fi
}




NETWORK_AVAILABLE=false
HOSTAPD_RUNNING=false

# Hauptprogramm
if check_ethernet; then
    echo "ethernet vorhanden"
    NETWORK_AVAILABLE=true
fi

if check_wlan; then
    echo "wlan vorhanden"
    NETWORK_AVAILABLE=true
fi

if check_hostapd_service; then
    HOSTAPD_RUNNING=true
fi


# if $NETWORK_AVAILABLE; then
#     echo "Netzwerkverbindung vorhanden."
#     exit 0

if $HOSTAPD_RUNNING; then
    echo "hostapd läuft."
else
    echo "starte hostapd"
    sudo systemctl start hostapd
    sudo systemctl start dnsmasq
fi