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
pin_rain = int(config['rain']['sensorpin'])

# GPIO-Ports
Counter_Rain = 0
rainvolume = 0
volPerKlick = 0.2995357196345664 #0,29... mm Regen pro qm =

# Zaehlvariable
t = 0

# GPIO initialisieren
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_rain, GPIO.IN) # Pin 11

# internen Pullup-Widerstand aktivieren.
GPIO.setup(pin_rain, GPIO.IN, pull_up_down = GPIO.PUD_UP)


# Callback fuer GPIO
def isr_rain(channel):  
    global Counter_Rain
    Counter_Rain += 1
    # print("Counter_Rain: %d" % Counter_Rain)

# Interrupts aktivieren
GPIO.add_event_detect(pin_rain, GPIO.RISING, callback = isr_rain, bouncetime = 500) 

# Endlosschleife wie oben
try:
    while True:
        # nix Sinnvolles tun
        t += 1
        # print(f"time {t}")
        if t == 60:
            if Counter_Rain > 0:
                rainvolume = Counter_Rain * volPerKlick

                print(f'rain vol={rainvolume}')

                ts = getInflxTimestamp()
                data = f'rain,type=gauge  volume={rainvolume} {ts}'
                writeBuffer('influx-rain', data)

                ts = getOSMTimestamp()
                osm_data = [
                    {"sensor": f"{rainID}","value": f"{rainvolume}","createdAt": f"{ts}"}
                ]
                writeBuffer('osm-rain', json.dumps(osm_data))

                # writeBuffer('openhab-rain', f'{oh_rainID},{rainvolume},{ts}')
                postOpenhabValues(oh_rainID,rainvolume, ts)

            rainvolume = 0
            Counter_Rain = 0
            t = 0
        time.sleep(1)

except KeyboardInterrupt:
  GPIO.cleanup()
