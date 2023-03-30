import subprocess
from time import sleep
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *
from apis.send2buffer import writeBuffer



def read_sensor():
    result = subprocess.run(['/usr/sbin/iwconfig', 'wlan0'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    signal = result.split('Signal level=')[1].split(' dBm')[0].strip()
    print(f'wifi-signal={signal} dBm')

    ts = getInflxTimestamp()
    data = f'raspberry,type=wifi signal={signal} {ts}'
    writeBuffer('influx-wifi', data)


    ts = getOSMTimestamp()
    osm_data = [
        {"sensor": f"{wifiID}","value": f"{signal}","createdAt": f"{ts}"}
    ]
    writeBuffer('osm-wifi', json.dumps(osm_data))


while True:
  read_sensor()
  time.sleep(60)
