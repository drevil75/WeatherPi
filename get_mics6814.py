import RPi.GPIO as GPIO
import spidev
from time import sleep
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *

config = configparser.ConfigParser()
config.read('./config.cfg')
co_pin = int(config['mics6814']['co_pin'])
no2_pin = int(config['mics6814']['no2_pin'])
nh3_pin = int(config['mics6814']['nh3_pin'])
pin_voltage = float(config['mics6814']['pin_voltage'])

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

    # print(len(vals), min(vals), max(vals))
    return vals


def read_mics():
   print('---------read_mics6814--------')
   # Mappingliste für CO erstellen Sensor-Range 1-100ppm
   coMap = mapRange(vmin=1, vmax=100, steps=1024)

   # Mappingliste für NO2 erstellen Sensor-Range 0.05-10ppm
   no2Map = mapRange(vmin=0.05, vmax=10, steps=1024)

   # Mappingliste für NH3 erstellen Sensor-Range 1-500ppm
   nh3Map = mapRange(vmin=1, vmax=500, steps=1024)

   # first messurement
   readadc(co_pin)
   readadc(no2_pin)
   readadc(nh3_pin)
   time.sleep(2)
   # second messurement
   coPinVal = readadc(co_pin)
   no2PinVal = readadc(no2_pin)
   nh3PinVal = readadc(nh3_pin)

   print(coPinVal, no2PinVal, nh3PinVal)

   if type(coPinVal) == int:
      if coPinVal in range(0,1023):
         coVal = coMap[coPinVal]
      else:
         coVal = 0
   else:
      coVal = 0

   if type(no2PinVal) == int:
      if no2PinVal in range(0,1023):
         no2Val = no2Map[no2PinVal]
      else:
         no2Val = 0
   else:
      no2Val = 0

   if type(nh3PinVal) == int:
      if nh3PinVal in range(0,1023):
         nh3Val = nh3Map[nh3PinVal]
      else:
         nh3Val = 0
   else:
      nh3Val = 0

   

   ts = getInflxTimestamp()
   data = f'mics6814,type=air co={coVal},no2={no2Val},nh3={nh3Val} {ts}'
   write2influxapi(data)

   ts = getOSMTimestamp()
   # send a bunch of data to OSM (prevents response 429 too many requests)
   osm_data = [
      {"sensor": f"{coID}", "value": f"{coVal}", "createdAt": f"{ts}"},
      {"sensor": f"{no2ID}", "value": f"{no2Val}", "createdAt": f"{ts}"},
      {"sensor": f"{nh3ID}", "value": f"{nh3Val}", "createdAt": f"{ts}"}
      ]
   postOSMvalues(osm_data)

   postOpenhabValues(coID, coVal, ts)
   postOpenhabValues(no2ID, no2Val, ts)
   postOpenhabValues(nh3ID, nh3Val, ts)

if __name__ == "__main__":
    read_mics()