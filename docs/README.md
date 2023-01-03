RaspiImager
hostname: weatherpi
user: weather
pw: ...
WIFI: your wifi credentials

# alle Schreibzugriffe bis auf ein Minimum reduzieren. Das verlängert erheblich die begrenzte Lebensdauer einer microSD card
# disable logging
sudo systemctl disable rsyslog
sudo systemctl stop rsyslog

sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip fail2ban ntpdate git

pip3 install -r requirements.txt

sudo mkdir /mnt/ramdisk
sudo nano /etc/fstab

tmpfs /mnt/ramdisk tmpfs nodev,nosuid,size=20M 0 0
sudo mount -a
# ------------