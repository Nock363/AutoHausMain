#!/bin/bash

# Copy the watchdog.conf file to /etc
cp "$(dirname "$0")/watchdog.conf" /etc/watchdog.conf