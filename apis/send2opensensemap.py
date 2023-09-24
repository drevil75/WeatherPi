import requests, json, datetime
import configparser
from dotenv import dotenv_values

env = dotenv_values()  # alternative dotenv_values("../pathto/myown.env") , .env is default
OpenSenseMap_TOKEN = env['OpenSenseMap_TOKEN']

config = configparser.ConfigParser()
config.read('./config.cfg')
osm_url = config['opensensemap']['url']
cachefile = config['default']['cachedir'] + config['opensensemap']['cachefile']
senseBoxID = config['opensensemap']['senseBoxID']
tempID = config['opensensemap']['tempID']
humiID = config['opensensemap']['humiID']
presID = config['opensensemap']['presID']
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
co2ID = config['opensensemap']['co2ID']
coID = config['opensensemap']['coID']
nh3ID = config['opensensemap']['nh3ID']
no2ID = config['opensensemap']['no2ID']
o3ID = config['opensensemap']['o3ID']
co2ppmID = config['opensensemap']['co2ppmID']
co2ppbID = config['opensensemap']['co2ppbID']
co2tempID = config['opensensemap']['co2tempID']
wifiID = config['opensensemap']['wifiID']

def getOSMTimestamp():
   now = datetime.datetime.now(datetime.timezone.utc)
   ts = int(datetime.datetime.timestamp(now))
   ts = str(now).replace(' ','T').split('.')[0] + '.000Z'
   return ts


def postOSMvalues(payload):
   print('-------postOSMvalues-------')

   url = osm_url + f'{senseBoxID}/data'
   headers = {'Authorization': f'{OpenSenseMap_TOKEN}', 'Content-Type': 'application/json'}
   print(url)
   
   try:
      r = requests.post(url, headers=headers, json=payload, timeout=60)
      print(f'rc={r.status_code}')
      if r.status_code in [200, 201, 202, 203, 204]:
         err_code = 'ok'
      else:   
         err_code = r.text
         print(f'rc={r.status_code} headers={r.headers}')
   except:
      err_code = 'timeout'
      print('exception raised')

   return err_code