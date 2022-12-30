#sudo apt install Adafruit-DHT RPi.GPIO
# pip3 install ephem

import Adafruit_DHT
import RPi.GPIO as GPIO
import configparser
# import sendvaluesapi

config = configparser.ConfigParser()
cfgFile = './config.cfg'
config.read(cfgFile)
sections = config.sections()

sensortype = int(config['dht22']['sensortype'])
sensorpin = int(config['dht22']['sensorpin'])

GPIO.setmode(GPIO.BCM)

# Sensortype DHT11=11, DHT22=22
humi, temp = Adafruit_DHT.read_retry(22, 5)
humi, temp = round(humi,1), round(temp,1)
print(humi, temp)


if type(temp) is not float:
    temp = 0.0

if type(humi) is not float:
    humi = 0.0

# sendvaluesapi.write2api('temperature.air', temp)
# sendvaluesapi.write2api('humidity.air', humi)


