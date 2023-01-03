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


def read_dht22():
    # Sensortype DHT11=11, DHT22=22
    for i in range(5):
        humi, temp = Adafruit_DHT.read_retry(sensortype, sensorpin)
        time.sleep(0.5)
        humi, temp = round(humi,1), round(temp,1)
        print(humi, temp)


    if type(temp) is not float:
        temp = 0.0

    if type(humi) is not float:
        humi = 0.0

    ts = getInflxTimestamp()
    print(ts)
    write2influxapi(f'dht22,type=air  temperature={temp},humidity={humi} {ts}')

    ts = getOSMTimestamp()
    osm_data = [
    {"sensor": f"{tempID}","value": f"{temp}","createdAt": f"{ts}"},
    {"sensor": f"{humiID}","value": f"{humi}","createdAt": f"{ts}"}
    ]
    postOSMvalues(osm_data)

    postOpenhabValues(oh_tempID, temp, ts)
    postOpenhabValues(oh_humiID, humi, ts)

if __name__ == "__main__":
    read_dht22()