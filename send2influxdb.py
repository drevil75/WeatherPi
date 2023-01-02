#pip install influxdb-client
import configparser
from datetime import datetime

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

config = configparser.ConfigParser()
cfgFile = './config.cfg'
config.read(cfgFile)
sections = config.sections()

# You can generate a Token from the "Tokens Tab" in the UI
url = config['influxdb']['url']
token = config['influxdb']['token']
org = config['influxdb']['org']
bucket = config['influxdb']['bucket']

client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

def write2db(ts, keyname, value):

    #json_data = [{"measurement": f"{keyname}","time": f"{ts}","fields": {"value": value}}]
    json_data = [{"measurement": f"{keyname}","fields": {"value": value}}]
    write_api.write(bucket, org, json_data, time_precision='ms')

