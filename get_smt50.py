import RPi.GPIO as GPIO
import spidev
from time import sleep
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *

config = configparser.ConfigParser()
config.read('./config.cfg')
AnalogPinTemp = int(config['smt50']['sensorpintemp'])
AnalogPinHumi = int(config['smt50']['sensorpinhumi'])
pin_voltage = float(config['smt50']['pin_voltage'])

# Initialisierung der Analogen Pins
# A0,A1,A2,A3,A4,A5,A6,A7 = 0,1,2,3,4,5,6,7
# pin_voltage = 3.3

# SPI-Einstellungen
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 2000000

def readadc(pin):
# Auslesen der SPI-Werte
 r = spi.xfer2([1,8+pin <<4,0])
 adcout = ((r[1] &3) <<8)+r[2]
 return adcout


def read_smt50():
   print('---------read_sound--------')
   voltage = readadc(AnalogPinTemp) * (pin_voltage / 1024.0)
   soilTemperature = (voltage - 0.48) * 100

   voltage = readadc(AnalogPinHumi) * (pin_voltage / 1024.0)
   soilMoisture = (voltage * 100) / 2.99

   ts = getInflxTimestamp()
   write2influxapi(f'sht50,type=soil  temperature={soilTemperature},humidity={soilMoisture} {ts}')

   ts = getOSMTimestamp()
   osm_data = [
      {"sensor": f"{soiltempID}", "value": f"{soilTemperature}", "createdAt": f"{ts}"},
      {"sensor": f"{soilHumiID}", "value": f"{soilMoisture}", "createdAt": f"{ts}"}
   ]
   postOSMvalues(osm_data)

   postOpenhabValues(oh_soiltempID, soilTemperature, ts)
   postOpenhabValues(oh_soilHumiID, soilMoisture, ts)


if __name__ == "__main__":
  read_smt50()

