#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *

# GPIO-Ports
Counter_Rain = 0
Counter_Wind = 0
windspeed = 0.0
pin_rain = 19
pin_wind = 20
volPerKlick = 0.2995357196345664 #0,29... mm Regen pro qm =

# Zaehlvariable
t = 0

# GPIO initialisieren
GPIO.setmode(GPIO.BCM)
# GPIO.setup(pin_rain, GPIO.IN) # Pin 11
# GPIO.setup(pin_wind, GPIO.IN) # Pin 12

# internen Pullup-Widerstand aktivieren.
GPIO.setup(pin_rain, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(pin_wind, GPIO.IN, pull_up_down = GPIO.PUD_UP)  


# Callback fuer GPIO
def isr_rain(channel):  
    global Counter_Rain
    Counter_Rain += 1
#    print("Counter_Rain: %d" % Counter_Rain)

# Callback fuer GPIO
def isr_wind(channel):  
    global Counter_Wind
    Counter_Wind += 1
#    print("Counter_Wind: %d" % Counter_Wind)

# Interrupts aktivieren
GPIO.add_event_detect(pin_rain, GPIO.FALLING, callback = isr_rain, bouncetime = 50) 
GPIO.add_event_detect(pin_wind, GPIO.FALLING, callback = isr_wind, bouncetime = 50) 

# Endlosschleife wie oben
try:
  while True:
    # nix Sinnvolles tun
    t += 1
    print(f"time {t}")
    if t == 60:
      rainvolume = Counter_Rain * volPerKlick
      windspeed = (Counter_Wind / 2) / 60.0 * 2.4 # Counter / 60 Seconds * 2.4m/s

      ts = getInflxTimestamp()
      write2influxapi(f'rain,type=gauge  volume={rainvolume} {ts}')
      write2influxapi(f'wind,type=anemometer  volume={windspeed} {ts}')

      ts = getOSMTimestamp()
      osm_data = [
      {"sensor": f"{rainID}","value": f"{rainvolume}","createdAt": f"{ts}"},
      {"sensor": f"{humiID}","value": f"{windspeed}","createdAt": f"{ts}"}
      ]
      postOSMvalues(osm_data)

      postOpenhabValues(oh_rainID, rainvolume, ts)
      postOpenhabValues(oh_windspeedID, windspeed, ts)

      Counter_Rain = 0
      Counter_Wind = 0
      t = 0
      time.sleep(1)

except KeyboardInterrupt:
  GPIO.cleanup()
