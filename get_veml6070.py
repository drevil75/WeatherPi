import time
import board
import adafruit_veml6070
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *
from apis.send2buffer import writeBuffer


def read_sensor():
    print('---------read_veml6070--------')
    with board.I2C() as i2c:
        uv = adafruit_veml6070.VEML6070(i2c)
        # Alternative constructors with parameters
        # uv = adafruit_veml6070.VEML6070(i2c, 'VEML6070_1_T')
        # uv = adafruit_veml6070.VEML6070(i2c, 'VEML6070_HALF_T', True)

        # take 10 readings
        for j in range(4):
            uv_raw = uv.uv_raw
            risk_level = uv.get_index(uv_raw)
            time.sleep(1)

        print(f"veml6070 uv={uv_raw}, risk_level={risk_level}")

        ts = getInflxTimestamp()
        data = f'veml6070,type=uv uv={uv_raw} {ts}'
        writeBuffer('influx-veml6070', data)

        ts = getOSMTimestamp()
        osm_data = [
            {"sensor": f"{uvID}","value": f"{uv_raw}","createdAt": f"{ts}"}
        ]
        writeBuffer('osm-veml6070', json.dumps(osm_data))

        # writeBuffer('openhab-veml6070', f'{oh_uvID},{uv_raw},{ts}')
        postOpenhabValues(oh_uvID,uv_raw, ts)

while True:
  read_sensor()
  time.sleep(60)
      