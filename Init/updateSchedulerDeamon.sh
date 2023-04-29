cat deamonConfig.txt > /etc/systemd/system/autohausScheduler.service
systemctl daemon-reload
sudo systemctl enable autohausScheduler.service
sudo systemctl start autohausScheduler.service