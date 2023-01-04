#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *

# GPIO-Ports
Counter_Rain = 0
pin_rain = 19
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
#    print("Counter_Rain: %d" % Counter_Rain)

# Interrupts aktivieren
GPIO.add_event_detect(pin_rain, GPIO.FALLING, callback = isr_rain, bouncetime = 50) 

# Endlosschleife wie oben
try:
  while True:
    # nix Sinnvolles tun
    t += 1
    print(f"time {t}")
    if t == 60:
      rainvolume = Counter_Rain * volPerKlick

      ts = getInflxTimestamp()
      write2influxapi(f'rain,type=gauge  volume={rainvolume} {ts}')

      ts = getOSMTimestamp()
      osm_data = [
      {"sensor": f"{rainID}","value": f"{rainvolume}","createdAt": f"{ts}"}
      ]
      postOSMvalues(osm_data)
      postOpenhabValues(oh_rainID, rainvolume, ts)

      Counter_Rain = 0
      t = 0
    time.sleep(1)

except KeyboardInterrupt:
  GPIO.cleanup()
