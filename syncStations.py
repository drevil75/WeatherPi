#---------Sensoren IDs----------------------
senseBoxID = '6005d07cca495d001be58ef1'
tempID = '6005d07cca495d001be58efc'
humiID = '6005d07cca495d001be58efb'
presID = '6005d07cca495d001be58efa'
pm10ID = '6005d07cca495d001be58ef7'
pm25ID = '6005d07cca495d001be58ef6'
soiltempID = '6005d07cca495d001be58ef4'
soilHumiID = '6005d07cca495d001be58ef5'
windspeedID = '6005d07cca495d001be58ef2'
brightID = '6005d07cca495d001be58ef9'
uvID = '6005d07cca495d001be58ef8'
rainID = '6005d43bca495d001be756cc'
soundID = '6005d07cca495d001be58ef3'
getURL = f'https://api.opensensemap.org/boxes/' + senseBoxID + '/sensors'
postURL = f'https://api.sensor.community/v1/push-sensor-data/'
luftID = 'esp8266-2464265'
openhab = 'wolke.fritz.box:38080'

import logging
import requests, json, datetime
from time import gmtime, strftime
timestamp = strftime("%Y%m%d_%H%M%S", gmtime())
print(str(timestamp) + "  syncStationsMirko.py")

logger = logging.getLogger(__name__)
logging.debug('--syncStations.py--')
#-----Regenmenge des aktuellen Monats abrufen-------------------------
def last_day_in_month(y,m):
    y = int(y)
    m = int(m)
    print(y, m)
    if m < 12:
        m += 1
    elif m == 12:
        y += 1
        m = 1
    print(y, m)
    ret = datetime.date(y,m,1) - datetime.timedelta(days=1)
    logging.info(f'last_day_in_month={ret}')
    return ret

#-----Aktuelles Datum auslesen - für Rain-Abfrage----
now = datetime.datetime.now()
date = now.date()
logging.info(f'now={now}')
logging.info(f'date={date}')

sYear = str(now.strftime("%Y"))
sMonth = str(now.strftime("%m"))
logging.info(f'sYear={sYear}')
logging.info(f'sMonth={sMonth}')

fromDate = sYear + "-" + sMonth + "-01T00:00:00.000Z"
toDate = str(last_day_in_month(sYear, sMonth)) + "T23:59:59.000Z"
getRainURL = f'https://api.opensensemap.org/boxes/' + senseBoxID + '/data/' + rainID + '?from-date=' + fromDate + '&to-date=' + toDate + '&format=json'
logging.info(f'getRainURL={getRainURL}')
#print(fromDate)
#print(toDate)

#------------Regenwerte von senseBox abrufen--------------
response = requests.get(getRainURL)
json_data = json.loads(response.text)
#print(json_data)
rainMonth = 0.0
rainDay = 0.0

for key in json_data:
    #print(key['value'])
    rainDay += float(key['value'])

rain = str(rainDay)
print(round(rainDay,1))   
#---------------------------------------------------------

#------------Daten von senseBox abrufen--------------
response = requests.get(getURL)
json_data = json.loads(response.text)
pairs = json_data["sensors"]

#------------durch die Sensoren iterieren-------------
for key in pairs:
    #print(key)
    if (key["_id"] == tempID): 
        temp = key["lastMeasurement"]["value"]
    if (key["_id"] == humiID): 
        humi = key["lastMeasurement"]["value"]
    if (key["_id"] == presID): 
        pres = key["lastMeasurement"]["value"]
    if (key["_id"] == pm10ID): 
        pm10 = key["lastMeasurement"]["value"]
    if (key["_id"] == pm25ID): 
        pm25 = key["lastMeasurement"]["value"]
    if (key["_id"] == soiltempID): 
        soiltemp = key["lastMeasurement"]["value"]
    if (key["_id"] == soilHumiID): 
        soilHumi = key["lastMeasurement"]["value"]
    if (key["_id"] == windspeedID): 
        windspeed = key["lastMeasurement"]["value"]
    if (key["_id"] == brightID): 
        bright = key["lastMeasurement"]["value"]
    if (key["_id"] == uvID): 
        uv = key["lastMeasurement"]["value"]
    #if (key["_id"] == rainID): 
    #    rain = key["lastMeasurement"]["value"]
    #    print("-----------")
    #    print(rain)
    #    print("-----------")
    if (key["_id"] == soundID): 
        sound = key["lastMeasurement"]["value"]

#-------------JSON-Objekt für Datenimport in luftdateninfo zusammenbauen---------------------------------------------

#-------------SDS011-Daten auf luftdaten.ino hochladen-----------------------------------
headers = {'content-type': 'application/json', 'X-Pin':'1',"X-Sensor": luftID}
SDS011data = {"software_version": "1", "sensordatavalues":[{"value_type":"P1","value":pm10},{"value_type":"P2","value":pm25}]}  
response = requests.post(postURL, json=SDS011data,headers=headers)
json_data = json.loads(response.text)
print(response.text)
print(response.status_code)

#-------------BME280-Daten auf luftdaten.ino hochladen-----------------------------------
headers = {'content-type': 'application/json', 'X-Pin':'11',"X-Sensor": luftID}
BME280data = {"software_version": "1", "sensordatavalues":[{"value_type":"temperature","value":temp},{"value_type":"humidity","value":humi},{"value_type":"pressure","value":pres}]} 
response = requests.post(postURL, json=BME280data,headers=headers)
json_data = json.loads(response.text)
print(response.text)
print(response.status_code)


#-------------Werte in openhab3 hochladen-----------------------------------
headers = {'content-type': 'text/plain','accept': '*/*'}

r = requests.post(f'http://{openhab}/rest/items/senseBox_Aussentemperatur', data=temp, headers=headers)
print(r.status_code)

r = requests.post(f'http://{openhab}/rest/items/senseBox_Luftfeuchtigkeit', data=humi, headers=headers)
print(r.status_code)

r = requests.post(f'http://{openhab}/rest/items/senseBox_Luftdruck', data=pres, headers=headers)
print(r.status_code)

r = requests.post(f'http://{openhab}/rest/items/senseBox_FeinstaubPM10', data=pm10, headers=headers)
print(r.status_code)

r = requests.post(f'http://{openhab}/rest/items/senseBox_FeinstaubPM25', data=pm25, headers=headers)
print(r.status_code)

r = requests.post(f'http://{openhab}/rest/items/senseBox_SoilTemp', data=soiltemp, headers=headers)
print(r.status_code)

r = requests.post(f'http://{openhab}/rest/items/senseBox_SoilHumi', data=soilHumi, headers=headers)
print(r.status_code)

r = requests.post(f'http://{openhab}/rest/items/senseBox_Windspeed', data=windspeed, headers=headers)
print(r.status_code)

r = requests.post(f'http://{openhab}/rest/items/senseBox_Beleuchtungsstarke', data=bright, headers=headers)
print(r.status_code)

r = requests.post(f'http://{openhab}/rest/items/senseBox_UV', data=uv, headers=headers)
print(r.status_code)

r = requests.post(f'http://{openhab}/rest/items/senseBox_Rain', data=rain, headers=headers)
print(r.status_code)

r = requests.post(f'http://{openhab}/rest/items/senseBox_Sound', data=sound, headers=headers)
print(r.status_code)


#-----die letzten 0-Werte des Regensensors löschen------
#-----bei der Summenbildung für den aktuellen Monat wird sonst das Abfragelimit von 10000 letzte Messwerte
#-----überschritten.
session = requests.Session()
url = 'https://api.opensensemap.org/users/sign-in'
headers = {'Authorization': '9b77bbfa86f928d759067b16fe98c50b78037d8c6345bf3d13e3490cdf1bfd1a','content-type': 'application/json'}
json_data = {"email": "drevil75@gmail.com", "password": "!1qayxsw2"}
r1 = session.post(url,json=json_data, headers=headers)
jData = json.loads(r1.text)
token = json.loads(r1.text)['token']


fromDate = '2021-07-01T00:00:00.000Z'
toDate = '2021-08-30T00:00:00.000Z'
#url = f'https://api.opensensemap.org/boxes/6005d07cca495d001be58ef1/data/6005d43bca495d001be756cc?from-date=' + fromDate + '&to-date=' + toDate + '&format=json'
url = f'https://api.opensensemap.org/boxes/6005d07cca495d001be58ef1/data/6005d43bca495d001be756cc?format=json'

r1 = session.get(url,headers=headers)
jData = json.loads(r1.text)
#print(jData)

url = 'https://api.opensensemap.org/boxes/6005d07cca495d001be58ef1/6005d43bca495d001be756cc/measurements'
headers = {'Authorization': f'Bearer {token}','content-type': 'application/json'}

for key in jData:
    if float(key['value']) == 0:
        createdAt = key['createdAt']
        json_data = {"timestamps": f"{createdAt}"}
        print(json_data, key['value'])
        r1 = session.delete(url,json=json_data,headers=headers)
        print(r1)
