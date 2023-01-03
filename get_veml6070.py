#https://learn.adafruit.com/adafruit-veml6070-uv-light-sensor-breakout/python-circuitpython
#sudo pip3 install adafruit-circuitpython-veml6070

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# VEML6070 Driver Example Code

import time
import board
import adafruit_veml6070
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *

with board.I2C() as i2c:
    uv = adafruit_veml6070.VEML6070(i2c)
    # Alternative constructors with parameters
    # uv = adafruit_veml6070.VEML6070(i2c, 'VEML6070_1_T')
    # uv = adafruit_veml6070.VEML6070(i2c, 'VEML6070_HALF_T', True)

    # take 10 readings
    for j in range(4):
        uv_raw = uv.uv_raw
        risk_level = uv.get_index(uv_raw)
        print("Reading: {0} | Risk Level: {1}".format(uv_raw, risk_level))
        time.sleep(1)

    print(f"UV: {uv_raw}")
    ts = getInflxTimestamp()
    write2influxapi(f'veml6070,type=uv uv={uv_raw} {ts}')

    ts = getOSMTimestamp()
    osm_data = [
        {"sensor": f"{uvID}","value": f"{uv_raw}","createdAt": f"{ts}"}
    ]
    postOSMvalues(osm_data)

    postOpenhabValues(oh_uvID, uv_raw, ts)