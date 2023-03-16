import RPi.GPIO as GPIO
import spidev
from time import sleep
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *
from apis.send2buffer import writeBuffer

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

def mapRange(vmin, vmax, steps):

    step = (vmax - vmin) / (steps - 1) # steps - 1 because vmin is fixed the first value
    vals = [0,vmin]
    for i in range(1023): # begin with 0
        vmin += step
        vals.append(vmin)

    print(len(vals), min(vals), max(vals))
    return vals


def read_sound():
   print('---------read_sound--------')
   # Mappingliste für Sound-Level-Meter erstellen - Range 20-130dBA
   map = mapRange(vmin=20, vmax=130, steps=1024)
   
   # first messurement
   readadc(AnalogPin)
   time.sleep(2)
   # second messurement
   soundPinVal = readadc(AnalogPin)
   
   if type(soundPinVal) == int:
      if soundPinVal in range(0,1023):
         val = map[soundPinVal]
      else:
         val = 0
   else:
      val = 0

   ts = getInflxTimestamp()
   data = f'dfrobot,type=sound  volume={val} {ts}'
   writeBuffer('influx-sound', data)

   ts = getOSMTimestamp()
   osm_data = [
      {"sensor": f"{soundID}","value": f"{val}","createdAt": f"{ts}"}
   ]
   writeBuffer('osm-sound', osm_data)

   writeBuffer('openhab-sound', f'{oh_soundID},{val},{ts}')


if __name__ == "__main__":
  read_sound()