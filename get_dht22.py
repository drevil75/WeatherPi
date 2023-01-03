#sudo apt install Adafruit-DHT RPi.GPIO
# pip3 install ephem

import Adafruit_DHT
import RPi.GPIO as GPIO
import configparser
import datetime, time
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *

config = configparser.ConfigParser()
cfgFile = './config.cfg'
config.read(cfgFile)
sections = config.sections()

sensortype = int(config['dht22']['sensortype'])
sensorpin = int(config['dht22']['sensorpin'])

GPIO.setmode(GPIO.BCM)

# Sensortype DHT11=11, DHT22=22
for i in range(5):
    humi, temp = Adafruit_DHT.read_retry(sensortype, sensorpin)
    time.sleep(1)
    humi, temp = Adafruit_DHT.read_retry(sensortype, sensorpin)
    humi, temp = round(humi,1), round(temp,1)
    print(humi, temp)


if type(temp) is not float:
    temp = 0.0

if type(humi) is not float:
    humi = 0.0

ts = getInflxTimestamp()
write2influxapi(f'air,sensor_id=DHT22 temperature={temp},humidity={humi} {ts}')

ts = getOSMTimestamp()
postOSMvalues(tempID, temp, ts)
postOSMvalues(humiID, humi, ts)

postOpenhabValues(oh_tempID, temp, ts)
postOpenhabValues(oh_humiID, humi, ts)