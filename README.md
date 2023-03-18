# WeatherPi Project

This Project is based on a Raspberry Pi (B+ and >) with a TK-BG-Shield with a MCP3008 Analog Chip.
Earlier i'm used a "SenseBox" arduino based Weather-Station. https://sensebox.de/
But i'm not really satisfied with the arduino solution.
- Because with every change in the code, you have to compile a new sketch, walk outside to the arduino and update the software.
- the parallel operation of a web server, multiple uploads to different APIs is very complex and hard to maintain.
- remote access is basically programmable, but not nice to implement and maintain. 

Now is the time to migrate the SenseBox to an Raspberry.

![Weather Station](/docs/ws.jpeg "Weather Station")

## Sensors

### Digital
- rain gauge - simple rain measurment based on interrupts counting
- wind anemometer - simple wind measurment based on interrupts counting

### I2C
- hdc1080 for air temperature and humidity
- bme280 for air pressure (temp. and humidity will not used)
- sps30 laser based for particular matters PM0.5, PM1.0, PM2.5, PM4.0, PM10 dense and particals count
- tsl45315 for brightness
- veml6070 for uv intensity

### Analog
- smt50 for soil temp. and humidity
- DFRobot environment volume measurement


## setup
use RaspiImager
- hostname: weatherpi
- user: weather
- pw: ...
- WIFI-Name: your wifi name
- WIFI-PW: your WIFI-Password

- reduce all write access to an absolute minimum to extend the lifetime of the microSD to a maximum 
- create ramdisk, disable logging

````shell
# sudo systemctl disable rsyslog
# sudo systemctl stop rsyslog

# update and install packages
sudo apt update && sudo apt upgrade -y
sudo apt install --upgrade python3-pip fail2ban ntpdate git libgpiod2 -y

# clone weatherpi repository
cd ~ && git clone https://github.com/drevil75/WeatherPi.git && cd WeatherPi

# install python libraries
pip3 install -r setup/requirements.txt

# install setuptools for adafruit shell
pip3 install --upgrade setuptools
sudo pip3 install --upgrade setuptools adafruit-python-shell
cd ~ && wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py

# create a ramdisk for cache files
sudo mkdir /mnt/ramdisk
sudo nano /etc/fstab

# ramdisk
tmpfs /mnt/ramdisk tmpfs nodev,nosuid,size=64M 0 0
# deactivate logging of last file access
/dev/mmcblk0p2 / ext4 defaults,nodiratime,noatime 0 1
# forward logfiles to ramdisk
none /var/log tmpfs size=5M,noatime 0

sudo mount -a

# deactivate swapping
sudo dphys-swapfile swapoff %% sudo systemctl disable dphys-swapfile && sudo apt-get purge dphys-swapfile
# ------------
````

Test the CircuitPython installation
````shell
python3
`````

````python
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

````

````shell

# edit the config with your IDs, PINs, Names...
nano config.cfg

# edit the .env file with your credentials
mv env.template .env
nano .env

````

create service for python script
````shell
sudo crontab -e
* * * * * chmod -R 777 /mnt/ramdisk

sudo nano /etc/systemd/system/weather.service

# paste into the editor
# ---------------
[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 main_ctrl.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

sudo systemctl daemon-reload && sudo systemctl enable weather && sudo systemctl start weather

````