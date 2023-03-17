#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *
from apis.send2buffer import writeBuffer
import configparser

config = configparser.ConfigParser()
cfgFile = './config.cfg'
config.read(cfgFile)
sections = config.sections()
pin_wind = int(config['wind']['sensorpin'])

# GPIO-Ports
Counter_Wind = 0
windspeed = 0.0

# Zaehlvariable
t = 0

# GPIO initialisieren
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_wind, GPIO.IN) # Pin 12

# internen Pullup-Widerstand aktivieren.
GPIO.setup(pin_wind, GPIO.IN, pull_up_down = GPIO.PUD_UP)  

# Callback fuer GPIO
def isr_wind(channel):  
    global Counter_Wind
    Counter_Wind += 1
    # print("Counter_Wind: %d" % Counter_Wind)

# Interrupts aktivieren
GPIO.add_event_detect(pin_wind, GPIO.FALLING, callback = isr_wind, bouncetime = 80) 

# Endlosschleife wie oben
try:
    while True:
        # nix Sinnvolles tun
        t += 1
        # print(f"time {t}")
        if t == 60:

            if Counter_Wind > 0:
                windspeed = ((Counter_Wind) / 60.0 * 2.4) * 1.18 # Counter / 60 Seconds * 2.4m/s (1.18 is anemometer factor - loss of wind force)

                if Counter_Wind > 0:
                    bouncetime = 100
                if Counter_Wind > 100:
                    bouncetime = 50
                if Counter_Wind > 500:
                    bouncetime = 30
                if Counter_Wind > 1000:
                    bouncetime = 20
                if Counter_Wind > 1500:
                    bouncetime = 10
                GPIO.remove_event_detect(pin_wind)
                GPIO.add_event_detect(pin_wind, GPIO.RISING, callback = isr_wind, bouncetime = bouncetime)

                ts = getInflxTimestamp()
                data = f'wind,type=anemometer  volume={windspeed} {ts}'
                writeBuffer('influx-wind', data)

                ts = getOSMTimestamp()
                osm_data = [
                    {"sensor": f"{windspeedID}","value": f"{windspeed}","createdAt": f"{ts}"}
                ]
                writeBuffer('osm-wind', osm_data)

                writeBuffer('openhab-wind', f'{oh_windspeedID},{windspeed},{ts}')

            windspeed = 0
            Counter_Wind = 0
            t = 0
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
