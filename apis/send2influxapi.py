#pip install influxdb-client

import datetime, time
import requests, json
import configparser
from dotenv import dotenv_values

env = dotenv_values()  # alternative dotenv_values("../pathto/myown.env") , .env is default
INFLUXDB_TOKEN = env['INFLUXDB_TOKEN']
INFLUXDB_USERNAME = env['INFLUXDB_USERNAME']
INFLUXDB_PASSWORD = env['INFLUXDB_PASSWORD']

config = configparser.ConfigParser()
config.read('./config.cfg')
url = config['influxdb']['url']
org = config['influxdb']['org']
bucket = config['influxdb']['bucket']
cachefile = config['influxdb']['cachefile']

headers = {'Authorization': f'Token {INFLUXDB_TOKEN}','Content-Type': 'text/plain; charset=utf-8','Accept': 'application/json'}
status = 0


def getInflxTimestamp(): # returns unix timestamp
   now = datetime.datetime.now(datetime.timezone.utc)
   ts = time.mktime(now.timetuple())
   return ts



def write2influxapi(data):

   # data = f'airSensors,sensor_id=TLM0201 temperature=73.97038159354763,humidity=35.23103248356096,co=0.48445310567793615 {ts}\n \
   #          airSensors,sensor_id=TLM0202 temperature=75.30007505999716,humidity=35.651929918691714,co=0.5141876544505826 {ts}'

   try:
      r = requests.post(url, data=data, headers=headers, timeout=10)
      print(r, r.text, r.status_code)
      if r.status_code in [200, 201, 202, 203, 204]:
         err_code = 1
      else:   
         err_code = r.text
   except:
      err_code = 'timeout'
   
   if err_code != 1:
      f = open(cachefile, mode='a', encoding='utf-8')
      f.write(f'{data}\n')
      f.close()
