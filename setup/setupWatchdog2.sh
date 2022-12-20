#Diesen Part nach setupWatchdog1.sh ausführen.

sudo apt-get update
sudo apt-get install watchdog
sudo su
echo 'watchdog-device = /dev/watchdog' >> /etc/watchdog.conf
echo 'watchdog-timeout = 15' >> /etc/watchdog.conf
echo 'max-load-1 = 24' >> /etc/watchdog.conf
sudo systemctl enable watchdog
sudo systemctl start watchdog

#Ausführen um zu prüfen, ob der Watchdog läuft.
sudo systemctl status watchdog