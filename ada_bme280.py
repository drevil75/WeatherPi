#!/usr/bin/python3
import time
import board
import busio
# import adafruit_bme280
from adafruit_bme280 import basic as adafruit_bme280

# Objekte erstellen
i2c     = busio.I2C(board.SCL, board.SDA)
bme280  = adafruit_bme280.Adafruit_BME280_I2C(i2c,address=0x76)


seehoehe = 200
fac      = pow(1.0-seehoehe/44330.0, 5.255)
print("Temp: %3.1f°C %2d%%" % (bme280.temperature,bme280.humidity))
print("Druck: %4d hPa" % int(bme280.pressure/fac))
