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
````


```shell
sudo su -

cat >> /etc/systemd/system/weather_bme280.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 get_bme280.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF


cat >> /etc/systemd/system/weather_hdc1080.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 get_hdc1080.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF


cat >> /etc/systemd/system/weather_mics6814.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 get_mics6814.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF

cat >> /etc/systemd/system/weather_mq131.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 get_mq131.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF

cat >> /etc/systemd/system/weather_rain.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 get_rain.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF

cat >> /etc/systemd/system/weather_scd30.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 get_scd30.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF


cat >> /etc/systemd/system/weather_smt50.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 get_smt50.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF

cat >> /etc/systemd/system/weather_soundlevel.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 get_soundlevel.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF


cat >> /etc/systemd/system/weather_sps30.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 get_sps30.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF


cat >> /etc/systemd/system/weather_tsl45315.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 get_tsl45315.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF


cat >> /etc/systemd/system/weather_veml6070.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 get_veml6070.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF

cat >> /etc/systemd/system/weather_wifi.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 get_wifi_signal_strength.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF


cat >> /etc/systemd/system/weather_wind.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 get_wind.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF

cat >> /etc/systemd/system/weather_transferData.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 transferData.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF


cat >> /etc/systemd/system/weather_fanControl.service << EOF

[Unit]
Description=WeatherPi
After=network.target

[Service]
User=weather
WorkingDirectory=/home/weather/WeatherPi/
ExecStart=python3 fan_controller.py
Restart=always

[Install]
WantedBy=multi-user.target
# -----------

EOF



sudo systemctl daemon-reload
sudo systemctl enable weather_bme280 && sudo systemctl start weather_bme280 && sudo systemctl status weather_bme280
sudo systemctl enable weather_hdc1080 && sudo systemctl start weather_hdc1080 && sudo systemctl status weather_hdc1080
sudo systemctl enable weather_mics6814 && sudo systemctl start weather_mics6814 && sudo systemctl status weather_mics6814
sudo systemctl enable weather_mq131 && sudo systemctl start weather_mq131 && sudo systemctl status weather_mq131
sudo systemctl enable weather_rain && sudo systemctl start weather_rain && sudo systemctl status weather_rain
sudo systemctl enable weather_scd30 && sudo systemctl start weather_scd30 && sudo systemctl status weather_scd30
sudo systemctl enable weather_smt50 && sudo systemctl start weather_smt50 && sudo systemctl status weather_smt50
sudo systemctl enable weather_soundlevel && sudo systemctl start weather_soundlevel && sudo systemctl status weather_soundlevel
sudo systemctl enable weather_sps30 && sudo systemctl start weather_sps30 && sudo systemctl status weather_sps30
sudo systemctl enable weather_tsl45315 && sudo systemctl start weather_tsl45315 && sudo systemctl status weather_tsl45315
sudo systemctl enable weather_veml6070 && sudo systemctl start weather_veml6070 && sudo systemctl status weather_veml6070
sudo systemctl enable weather_wifi && sudo systemctl start weather_wifi && sudo systemctl status weather_wifi
sudo systemctl enable weather_wind && sudo systemctl start weather_wind && sudo systemctl status weather_wind
sudo systemctl enable weather_transferData && sudo systemctl start weather_transferData && sudo systemctl status weather_transferData
sudo systemctl enable weather_fanControl && sudo systemctl start weather_fanControl && sudo systemctl status weather_fanControl

sudo systemctl stop weather_bme280
sudo systemctl stop weather_hdc1080
sudo systemctl stop weather_mics6814
sudo systemctl stop weather_mq131
sudo systemctl stop weather_rain
sudo systemctl stop weather_scd30
sudo systemctl stop weather_smt50
sudo systemctl stop weather_soundlevel
sudo systemctl stop weather_sps30
sudo systemctl stop weather_tsl45315
sudo systemctl stop weather_veml6070
sudo systemctl stop weather_wifi
sudo systemctl stop weather_wind
sudo systemctl stop weather_transferData
sudo systemctl stop weather_fanControl

sudo systemctl stop syslog.service
sudo systemctl disable syslog.service
```