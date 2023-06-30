#!/bin/bash

# Name des Systemd-Dienstes
SERVICE_NAME="autohaus.service"

# Systemd-Dienst stoppen
sudo systemctl stop "$SERVICE_NAME"

# Status des Systemd-Dienstes prüfen
sudo systemctl status "$SERVICE_NAME"
