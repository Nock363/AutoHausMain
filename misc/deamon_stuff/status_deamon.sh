#!/bin/bash

# Name des Systemd-Dienstes
SERVICE_NAME="autohaus.service"

# Status des Systemd-Dienstes prüfen
sudo systemctl status "$SERVICE_NAME"
