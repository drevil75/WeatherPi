
from scd30_i2c import SCD30
import datetime, time
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *
from apis.send2buffer import writeBuffer

config = configparser.ConfigParser()
cfgFile = './config.cfg'
config.read(cfgFile)

scd30 = SCD30()
# scd30.set_measurement_interval(2)
# scd30.start_periodic_measurement()


def read_sensor():
    print('---------read_scd30--------')

    scd30.get_data_ready()
    m = scd30.read_measurement()

    if m is not None:
        print(f"scd30 CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
        time.sleep(2)

    ts = getInflxTimestamp()
    data = f'scd30,type=air co2={m[0]},temperature={m[1]},humidity={m[2]} {ts}'
    writeBuffer('influx-scd30', data)

    ts = getOSMTimestamp()
    osm_data = [
        {"sensor": f"{co2ID}","value": f"{m[0]}","createdAt": f"{ts}"}
    ]
    writeBuffer('osm-scd30', json.dumps(osm_data))

    ts = getOpenhabTimestamp()
    # writeBuffer('openhab-scd30', f'{oh_presID},{m[0]},{ts}')
    postOpenhabValues(oh_presID,m[0], ts)

while True:
  read_sensor()
  time.sleep(60)
