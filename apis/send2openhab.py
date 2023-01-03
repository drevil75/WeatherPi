import requests, json, datetime
import configparser


config = configparser.ConfigParser()
config.read('./config.cfg')
host = config['openhab']['host']
cachefile = config['openhab']['cachefile']
oh_tempID = config['openhab']['tempID']
oh_humiID = config['openhab']['humiID']
oh_presID = config['openhab']['presID']
oh_dense_pm05_ID = config['openhab']['dense_pm05_ID']
oh_dense_pm1_ID = config['openhab']['dense_pm1_ID']
oh_dense_pm4_ID = config['openhab']['dense_pm4_ID']
oh_dense_pm10_ID = config['openhab']['dense_pm10_ID']
oh_dense_pm25_ID = config['openhab']['dense_pm25_ID']
oh_count_partical_pm05_ID = config['openhab']['count_partical_pm05_ID']
oh_count_partical_pm1_ID = config['openhab']['count_partical_pm1_ID']
oh_count_partical_pm4_ID = config['openhab']['count_partical_pm4_ID']
oh_count_partical_pm10_ID = config['openhab']['count_partical_pm10_ID']
oh_count_partical_pm25_ID = config['openhab']['count_partical_pm25_ID']
oh_soiltempID = config['openhab']['soiltempID']
oh_soilHumiID = config['openhab']['soilHumiID']
oh_windspeedID = config['openhab']['windspeedID']
oh_brightID = config['openhab']['brightID']
oh_uvID = config['openhab']['uvID']
oh_rainID = config['openhab']['rainID']
oh_soundID = config['openhab']['soundID']



def getOpenhabTimestamp():
   now = datetime.datetime.now(datetime.timezone.utc)
   ts = int(datetime.datetime.timestamp(now))
   ts = str(now).replace(' ','T').split('.')[0] + '.000Z'
   return ts


def postOpenhabValues(ItemName, val, ts):
    print('-------postOpenhabValues-------')
    print(f'ItemName={ItemName}, value={val}')

    url = f'http://{host}/rest/items/{ItemName}'
    headers = {'content-type': 'text/plain','accept': '*/*'}


    try:
        r = requests.post(url, headers=headers, data=str(val), timeout=10)
        print(f'rc={r.status_code}, rtext{r.text}')
        if r.status_code in [200, 201, 202, 203, 204]:
            err_code = 1
        else:   
            err_code = r.text
    except:
            err_code = 'timeout'
