import RPi.GPIO as GPIO
import spidev
from time import sleep
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *

config = configparser.ConfigParser()
config.read('./config.cfg')
AnalogPin = int(config['sound']['sensorpin'])
pin_voltage = float(config['sound']['pin_voltage'])

# Initialisierung der Analogen Pins
# A0,A1,A2,A3,A4,A5,A6,A7 = 0,1,2,3,4,5,6,7
# pin_voltage = 3.3

# SPI-Einstellungen
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 2000000

def readadc(adcnum):
# Auslesen der SPI-Werte
 r = spi.xfer2([1,8+adcnum <<4,0])
 adcout = ((r[1] &3) <<8)+r[2]
 return adcout

val = ((readadc(AnalogPin) / 1024) * pin_voltage) * 50

ts = getInflxTimestamp()
write2influxapi(f'dfrobot,type=sound  volume={val} {ts}')

ts = getOSMTimestamp()
osm_data = [
   {"sensor": f"{soundID}","value": f"{val}","createdAt": f"{ts}"}
]
postOSMvalues(osm_data)

postOpenhabValues(oh_soundID, val, ts)

print("Channel A0: " + str(val))
