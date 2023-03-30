# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_ccs811
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *
from apis.send2buffer import writeBuffer

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
ccs811 = adafruit_ccs811.CCS811(i2c)


def read_sensor():
    print('---------read_cjmcu811--------')
    
    # Wait for the sensor to be ready
    while not ccs811.data_ready:
        pass

    co2ppm = round(ccs811.eco2,2)
    co2ppb = round(ccs811.tvoc,2)
    co2temp = round(ccs811.temperature,2)

    print(f'cjmcu811 co2ppm={co2ppm}, co2ppb={co2ppb}, co2temp={co2temp}')

    ts = getInflxTimestamp()
    data = f'cjmcu811,type=air co2ppm={co2ppm},co2ppb={co2ppb},co2temp={co2temp} {ts}'
    writeBuffer('influx-cjmcu811', data)

    ts = getOSMTimestamp()
    osm_data = [
        {"sensor": f"{co2ppmID}","value": f"{co2ppm}","createdAt": f"{ts}"},
        {"sensor": f"{co2ppbID}","value": f"{co2ppb}","createdAt": f"{ts}"},
        {"sensor": f"{co2tempID}","value": f"{co2temp}","createdAt": f"{ts}"}
    ]
    writeBuffer('osm-cjmcu811', json.dumps(osm_data))

    ts = getOpenhabTimestamp()
    data = f'{oh_co2ppmID},{co2ppm},{ts}\n'
    data += f'{oh_co2ppbID},{co2ppb},{ts}\n'
    data += f'{oh_co2tempID},{co2temp},{ts}\n'
    # writeBuffer('openhab-cjmcu811', data)
    postOpenhabValues(oh_co2ppmID,co2ppm, ts)
    postOpenhabValues(oh_co2ppbID,co2ppb, ts)
    postOpenhabValues(oh_co2tempID,co2temp, ts)

 
while True:
  read_sensor()
  time.sleep(60)