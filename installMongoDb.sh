# Install the MongoDB 4.4 GPG key:
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

# Add the source location for the MongoDB packages:
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

# Download the package details for the MongoDB packages:
sudo apt-get update

# Install MongoDB:
sudo apt-get install -y mongodb-org

echo "Damit die DB im Netzwerk erreichbar ist bitte die Schlusskommentare ausführen"

# Change the bindIp to '0.0.0.0' in /etc/mongod.conf:
#net:
#   port: 27017
#   bindIp: 0.0.0.0
#
# Dann mongo neustarten:
#sudo systemctl restart mongod
# Und in Firewall zulassen
sudo ufw allow 27017/tcp