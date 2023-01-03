import requests, json, datetime
import configparser
from dotenv import dotenv_values

env = dotenv_values()  # alternative dotenv_values("../pathto/myown.env") , .env is default
OpenSenseMap_TOKEN = env['OpenSenseMap_TOKEN']

config = configparser.ConfigParser()
config.read('./config.cfg')
url = config['opensensemap']['url']
org = config['opensensemap']['org']
bucket = config['opensensemap']['bucket']
cachefile = config['opensensemap']['cachefile']
senseBoxID = config['opensensemap']['senseBoxID']
tempID = config['opensensemap']['tempID']
humiID = config['opensensemap']['humiID']
presID = config['opensensemap']['presID']
dense_pm05_ID = config['opensensemap']['dense_pm05_ID']
dense_pm1_ID = config['opensensemap']['dense_pm1_ID']
dense_pm4_ID = config['opensensemap']['dense_pm4_ID']
dense_pm10_ID = config['opensensemap']['dense_pm10_ID']
dense_pm25_ID = config['opensensemap']['dense_pm25_ID']
count_partical_pm05_ID = config['opensensemap']['count_partical_pm05_ID']
count_partical_pm1_ID = config['opensensemap']['count_partical_pm1_ID']
count_partical_pm4_ID = config['opensensemap']['count_partical_pm4_ID']
count_partical_pm10_ID = config['opensensemap']['count_partical_pm10_ID']
count_partical_pm25_ID = config['opensensemap']['count_partical_pm25_ID']
soiltempID = config['opensensemap']['soiltempID']
soilHumiID = config['opensensemap']['soilHumiID']
windspeedID = config['opensensemap']['windspeedID']
brightID = config['opensensemap']['brightID']
uvID = config['opensensemap']['uvID']
rainID = config['opensensemap']['rainID']
soundID = config['opensensemap']['soundID']


def getOSMTimestamp():
   now = datetime.datetime.now()
   ts = int(datetime.datetime.timestamp(now))
   ts = str(now).replace(' ','T').split('.')[0] + '.000Z'
   return ts


def postOSMvalues(sensorID, val, ts):
   url = url + f'{senseBoxID}/{sensorID}'
   headers = {'Authorization': f'{OpenSenseMap_TOKEN}', 'Content-Type': 'application/json'}

   payload = {"value": f"{val}", "createdAt": f"{ts}"}

   data = f'{sensorID}, {json.dumps(payload)}'
   
   try:
         r = requests.post(url, headers=headers, data=payload, timeout=10)
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
