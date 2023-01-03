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
sudo apt install python3-pip fail2ban ntpdate git libgpiod2

pip3 install --upgrade setuptools
pip3 install -r requirements.txt


sudo apt-get install python3-pip
sudo pip3 install --upgrade setuptools
cd ~
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py



sudo mkdir /mnt/ramdisk
sudo nano /etc/fstab

tmpfs /mnt/ramdisk tmpfs nodev,nosuid,size=20M 0 0
sudo mount -a
# ------------


blinkatest.py
# -----------------------------
import board
import digitalio
import busio

print("Hello blinka!")

# Try to great a Digital input
pin = digitalio.DigitalInOut(board.D4)
print("Digital IO ok!")

# Try to create an I2C device
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C ok!")

# Try to create an SPI device
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
print("SPI ok!")

print("done!")
# -----------------------------