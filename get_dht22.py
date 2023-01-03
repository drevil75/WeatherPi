
import board
import adafruit_dht
import RPi.GPIO as GPIO
import configparser
import datetime, time
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *

config = configparser.ConfigParser()
cfgFile = './config.cfg'
config.read(cfgFile)
sections = config.sections()

# sensortype = int(config['dht22']['sensortype'])
# sensorpin = int(config['dht22']['sensorpin'])
dhtDevice = adafruit_dht.DHT22(board.D27)

# GPIO.setmode(GPIO.BCM)
val_valid = False
c_loop = 0

def read_dht22():
    print('---------read_dht22--------')
    
    while val_valid == False and c_loop < 3:
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature # Fahrenheit = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            if type(temperature_c) == 'float':
                val_valid = True
                c_loop = 3
                temperature_c, humidity = round(temperature_c,2), round(humidity,2)

            print(temperature_c, humidity)

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            c_loop += 1
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error


    if type(temperature_c) is not float:
        temp = 0.0

    if type(humidity) is not float:
        humi = 0.0

    ts = getInflxTimestamp()
    print(ts)
    write2influxapi(f'dht22,type=air  temperature={temp},humidity={humi} {ts}')

    ts = getOSMTimestamp()
    osm_data = [
    {"sensor": f"{tempID}","value": f"{temp}","createdAt": f"{ts}"},
    {"sensor": f"{humiID}","value": f"{humi}","createdAt": f"{ts}"}
    ]
    postOSMvalues(osm_data)

    postOpenhabValues(oh_tempID, temp, ts)
    postOpenhabValues(oh_humiID, humi, ts)

if __name__ == "__main__":
    read_dht22()