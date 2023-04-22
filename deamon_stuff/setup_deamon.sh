#!/bin/bash

# Name des Systemd-Dienstes
SERVICE_NAME="autohaus.service"

# Pfad zum Python-Skript
SCRIPT_PATH="/home/user/AutoHausMain/main.py"

# Benutzername
USERNAME="user"

# Beschreibung des Dienstes
DESCRIPTION="Autohaus System mit RestAPI und Scheduler"

# Systemd-Dienst-Datei
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME"

# Inhalt der Systemd-Dienst-Datei
SERVICE_CONTENT="[Unit]
Description=$DESCRIPTION

[Service]
User=$USERNAME
ExecStart=/usr/bin/python $SCRIPT_PATH
Restart=always

[Install]
WantedBy=multi-user.target"

# Systemd-Dienst-Datei erstellen
echo "$SERVICE_CONTENT" | sudo tee "$SERVICE_FILE" >/dev/null

# Systemd-Dienst starten
sudo systemctl start "$SERVICE_NAME"

# Systemd-Dienst automatisch starten lassen
sudo systemctl enable "$SERVICE_NAME"

# Status des Systemd-Dienstes prüfen
sudo systemctl status "$SERVICE_NAME"
