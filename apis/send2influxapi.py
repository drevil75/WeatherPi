#pip install influxdb-client
import configparser
import datetime
import requests, json

config = configparser.ConfigParser()
cfgFile = './config.cfg'
config.read(cfgFile)
sections = config.sections()

cachefile = './cache.csv' #config['default']['cachefile']
status = 0

# You can generate a Token from the "Tokens Tab" in the UI
# url = config['influxdb']['url']
# token = config['influxdb']['token']
# org = config['influxdb']['org']
# bucket = config['influxdb']['bucket']
url = 'http://192.168.1.50:18086/api/v2/write?org=wolke&bucket=test&precision=s'
token = 'eydsJXziy1z2b1blt-7uqBHxW-s44mQxG10YyzNvJTMfsBLbvLMnKtTCbsKJjxZWcJkhq0uxIvuKpOCbPqcTEQ=='
headers = {'Authorization': f'Token {token}','Content-Type': 'text/plain; charset=utf-8','Accept': 'application/json'}

def write2api(keyname, value):

   now = datetime.datetime.now()
   ts = int(datetime.datetime.timestamp(now))
   now2 = str(now).replace(' ','T').split('.')[0] + '.000Z'
   

   data = f'airSensors,sensor_id=TLM0201 temperature=73.97038159354763,humidity=35.23103248356096,co=0.48445310567793615 {ts}\n \
         airSensors,sensor_id=TLM0202 temperature=75.30007505999716,humidity=35.651929918691714,co=0.5141876544505826 {ts}'


   # data = f'{keyname} value={value} {ts}'

   try:
      r = requests.post(url, data=data, headers=headers, timeout=5)
      print(r, r.text, r.status_code)
      if r.status_code == 204:
         err_code = 1
      else:   
         err_code = r.text
   except:
      err_code = 'timeout'
   
   if err_code != 1:
      txt = f'{value}, {keyname}, {now2}, {err_code}, 0\n'

      f = open(cachefile, mode='a', encoding='utf-8')
      f.write(txt)
      f.close()

write2api('aaaa','8.234')

import RPi.GPIO as GPIO
import spidev
from time import sleep

# Initialisiere Joystick auf Analogen PINS 0 & 1
joyX = 0
joyY = 1

spi = spidev.SpiDev()
spi.open(0,0)
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)

def readadc(adcnum):
# SPI-Daten auslesen
 r = spi.xfer2([1,8+adcnum <<4,0])
 adcout = ((r[1] &3) <<8)+r[2]
 return adcout

while True:
   x = readadc(joyX)
   y = readadc(joyY)
   print("X: " + str(x) + " Y: " + str(y))
   if(x > 1000):
      print("Joystick gedrueckt")
   sleep(0.1)