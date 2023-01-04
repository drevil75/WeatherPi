#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *

# GPIO-Ports
Counter_Wind = 0
windspeed = 0.0
pin_wind = 20

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
    print("Counter_Wind: %d" % Counter_Wind)

# Interrupts aktivieren
GPIO.add_event_detect(pin_wind, GPIO.FALLING, callback = isr_wind, bouncetime = 50) 

# Endlosschleife wie oben
try:
    while True:
        # nix Sinnvolles tun
        t += 1
        # print(f"time {t}")
        if t == 60:

            if Counter_Wind > 0:
                windspeed = (Counter_Wind / 2) / 60.0 * 2.4 # Counter / 60 Seconds * 2.4m/s

                ts = getInflxTimestamp()
                write2influxapi(f'wind,type=anemometer  volume={windspeed} {ts}')

                ts = getOSMTimestamp()
                osm_data = [
                    {"sensor": f"{windspeedID}","value": f"{windspeed}","createdAt": f"{ts}"}
                ]
                postOSMvalues(osm_data)
                postOpenhabValues(oh_windspeedID, windspeed, ts)

            windspeed = 0
            Counter_Wind = 0
            t = 0
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
