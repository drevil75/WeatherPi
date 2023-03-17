import board
import busio
from adafruit_bme280 import basic as adafruit_bme280
import datetime, time
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *
from apis.send2buffer import writeBuffer

# Objekte erstellen
i2c     = busio.I2C(board.SCL, board.SDA)
bme280  = adafruit_bme280.Adafruit_BME280_I2C(i2c,address=0x76)

seehoehe = 200
fac      = pow(1.0-seehoehe/44330.0, 5.255)


def read_bme280():
  print('---------read_bme280--------')

  temperature,pressure,humidity = bme280.temperature, (bme280.pressure/fac), bme280.humidity

  print("Temperature : ", round(temperature,2), "C")
  print("Pressure : ", round(pressure), "hPa")
  print("Humidity : ", round(humidity,2), "%")

  ts = getInflxTimestamp()
  data = f'bme280,type=air temperature={temperature},humidity={humidity},pressure={pressure} {ts}'
  writeBuffer('influx-bme280', data)

  ts = getOSMTimestamp()
  osm_data = [
    {"sensor": f"{presID}","value": f"{pressure}","createdAt": f"{ts}"}
  ]
  writeBuffer('osm-bme280', json.dumps(osm_data))

  ts = getOpenhabTimestamp()
  writeBuffer('openhab-bme280', f'{oh_presID},{pressure},{ts}')

if __name__ == "__main__":
  read_bme280()