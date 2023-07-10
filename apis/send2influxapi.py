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
cachefile = config['default']['cachedir'] + config['influxdb']['cachefile']

headers = {'Authorization': f'Token {INFLUXDB_TOKEN}','Content-Type': 'text/plain; charset=utf-8','Accept': 'application/json'}
status = 0


def getInflxTimestamp(): # returns unix timestamp
   now = datetime.datetime.now(datetime.timezone.utc)
   ts = int(time.mktime(now.timetuple()))
   return ts

def write2influxapi(data):
   print('-------write2influxapi-------')
   print(f'data={data}')

   # data = f'airSensors,sensor_id=TLM0201 temperature=73.97038159354763,humidity=35.23103248356096,co=0.48445310567793615 {ts}\n \
   #          airSensors,sensor_id=TLM0202 temperature=75.30007505999716,humidity=35.651929918691714,co=0.5141876544505826 {ts}'

   try:
      r = requests.post(url, data=data, headers=headers, timeout=10)
      print(f'rc={r.status_code}')
      if r.status_code in [200, 201, 202, 203, 204]:
         err_code = 'ok'
      else:   
         err_code = r.text
   except:
      err_code = 'timeout'
   
   return err_code

def getInflxMonthlyRain():
   data = "import \"date\" \nmonth = date.truncate(t: now(), unit: 1mo)\nfrom(bucket: \"WeatherPi\")\n  |> range(start: month)\n  |> filter(fn: (r) => r[\"_measurement\"] == \"rain\")\n  |> filter(fn: (r) => r[\"_field\"] == \"volume\")\n  |> aggregateWindow(every: 1mo, fn: sum, createEmpty: false)\n  |> yield(name: \"sum\")"

   try:
      r = requests.post(url, data=data, headers=headers, timeout=10)
      print(f'rc={r.status_code}')

      if r.status_code in [200, 201, 202, 203, 204]:
         err_code = 'ok'
      else:   
         err_code = r.text
   except:
      err_code = 'timeout'

   if "volume,rain,gauge" in r.text:
      print(r.text)

      lines = r.text.split('\n')
      for line in lines:
         if "volume,rain,gauge" in line:
            rainvolume = round(float(line.split(',')[6]),1)
            value = rainvolume

   return value
