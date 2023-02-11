
from scd30_i2c import SCD30
import datetime, time
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *

config = configparser.ConfigParser()
cfgFile = './config.cfg'
config.read(cfgFile)

scd30 = SCD30()
# scd30.set_measurement_interval(2)
# scd30.start_periodic_measurement()


def read_scd30():
    print('---------read_scd30--------')

    scd30.get_data_ready()
    m = scd30.read_measurement()

    if m is not None:
        print(f"CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
        time.sleep(2)

    ts = getInflxTimestamp()
    write2influxapi(f'scd30,type=air co2={m[0]},temperature={m[1]},humidity={m[2]} {ts}')

    ts = getOSMTimestamp()
    osm_data = [
        {"sensor": f"{co2ID}","value": f"{m[0]}","createdAt": f"{ts}"}
    ]
    postOSMvalues(osm_data)

    ts = getOpenhabTimestamp()
    postOpenhabValues(oh_presID, m[0], ts)

if __name__ == "__main__":
    read_scd30()