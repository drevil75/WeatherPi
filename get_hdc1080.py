
import sys
import json
from time import sleep
import SDL_Pi_HDC1080
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *
from apis.send2buffer import writeBuffer

def read_hdc1080():
    print('---------read_hdc1080--------')
    hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()
    vendor = hdc1080.readManufacturerID()
    devID = hdc1080.readDeviceID()
    sn = hdc1080.readSerialNumber()
    reg = hdc1080.readConfigRegister()
    hdc1080.turnHeaterOn() 
    hdc1080.readConfigRegister()
    hdc1080.setTemperatureResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_TEMPERATURE_RESOLUTION_11BIT)
    hdc1080.readConfigRegister()
    hdc1080.setTemperatureResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
    hdc1080.readConfigRegister()
    hdc1080.setHumidityResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_HUMIDITY_RESOLUTION_8BIT)
    hdc1080.readConfigRegister()
    hdc1080.setHumidityResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_HUMIDITY_RESOLUTION_14BIT)
    hdc1080.readConfigRegister()
    hdc1080.turnHeaterOff() 
    hdc1080.readConfigRegister()
    hdc1080.readTemperature()
    temperature_c = hdc1080.readTemperature()
    sleep(2)
    hdc1080.readHumidity()
    humidity = hdc1080.readHumidity()
    print(f'temp={temperature_c}, humi={humidity}')

    ts = getInflxTimestamp()
    data = f'hdc1080,type=air  temperature={temperature_c},humidity={humidity} {ts}'
    writeBuffer('influx-hdc1080', data)

    ts = getOSMTimestamp()
    osm_data = [
    {"sensor": f"{tempID}","value": f"{temperature_c}","createdAt": f"{ts}"},
    {"sensor": f"{humiID}","value": f"{humidity}","createdAt": f"{ts}"}
    ]
    writeBuffer('osm-hdc1080', json.dumps(osm_data))

    data = f'{oh_tempID},{temperature_c},{ts}\n'
    data += f'{oh_humiID},{humidity},{ts}\n'
    writeBuffer('openhab-hdc1080', data)



if __name__ == "__main__":
    read_hdc1080()

