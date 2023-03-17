import RPi.GPIO as GPIO
import spidev
from time import sleep
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *
from apis.send2buffer import writeBuffer

config = configparser.ConfigParser()
config.read('./config.cfg')
AnalogPin = int(config['mq131']['o3_pin'])
pin_voltage = float(config['mq131']['pin_voltage'])

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


def read_sensor():
   # Mappingliste für O3 erstellen Sensor-Range 10ppb-2ppm
   map = mapRange(vmin=1, vmax=100, steps=1024)

   # first messurement
   readadc(AnalogPin)
   time.sleep(2)
   # second messurement
   pinVal = readadc(AnalogPin)
   
   if type(pinVal) == int:
      if pinVal in range(0,1023):
         val = map[pinVal]
   else:
      val = 0

   

   ts = getInflxTimestamp()
   data = f'mq131,type=air o3={val} {ts}'
   writeBuffer('influx-mq131', data)

   ts = getOSMTimestamp()
   osm_data = [
      {"sensor": f"{coID}", "value": f"{val}", "createdAt": f"{ts}"}
      ]
   writeBuffer('osm-mq131', json.dumps(osm_data))

   writeBuffer('openhab-mq131', f'{o3ID},{val},{ts}')
   

if __name__ == "__main__":
    read_sensor()