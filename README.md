# WeatherPi Project

This Project is based on a Raspberry Pi (B+ and >) with a TK-BG-Shield with a MCP3008 Analog Chip.
Earlier i'm used a "SenseBox" arduino based Weather-Station. https://sensebox.de/
But i'm not really satisfied with the arduino solution.
- Because with every change in the code, you have to compile a new sketch, walk outside to the arduino and update the software.
- the parallel operation of a web server, multiple uploads to different APIs is very complex and hard to maintain.
- remote access is basically programmable, but not nice to implement and maintain. 

Now is the time to migrate the SenseBox to an Raspberry.

## Sensors

### Digital
- dht22 for air temperature and humidity
- rain gauge - simple rain measurment based on interrupts counting
- wind anemometer - simple wind measurment based on interrupts counting

### I2C
- bme280 for air pressure (temp. and humidity will not used)
- sps30 laser based for particular matters PM0.5, PM1.0, PM2.5, PM4.0, PM10 dense and particals count
- tsl45315 for brightness
- veml6070 for uv intensity

### Analog
- sht50 for soil temp. and humidity
- DFRobot environment volume measurement


## setup
use RaspiImager
- hostname: weatherpi
- user: weather
- pw: ...
- WIFI: your wifi credentials

- reduce all write access to an absolute minimum to extend the microSD to the maximum - disable logging for that purpose

````shell
sudo systemctl disable rsyslog
sudo systemctl stop rsyslog

sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip fail2ban ntpdate git libgpiod2

pip3 install --upgrade setuptools
sudo pip3 install --upgrade setuptools

cd ~
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py

# create a ramdisk for cache files
sudo mkdir /mnt/ramdisk
sudo nano /etc/fstab

tmpfs /mnt/ramdisk tmpfs nodev,nosuid,size=20M 0 0
sudo mount -a
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
cd ~
git clone https://github.com/drevil75/WeatherPi.git
cd WeatherPi

# edit the config with your IDs, PINs, Names...
nano config.cfg

# start the single scripts i.e.
python3 get_dht22.py

# or the main_ctrl.py to start all scripts
python3 main_ctrl.py
````
