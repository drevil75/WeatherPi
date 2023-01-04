#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# GPIO-Ports
Counter_Rain = 0
Counter_Wind = 0
pin_rain = 19
pin_wind = 20

# Zaehlvariable
Tic = 0

# GPIO initialisieren
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_rain, GPIO.IN) # Pin 11
GPIO.setup(pin_wind, GPIO.IN) # Pin 12

# internen Pullup-Widerstand aktivieren.
GPIO.setup(pin_rain, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(pin_wind, GPIO.IN, pull_up_down = GPIO.PUD_UP)  

# Callback fuer GPIO 17
def isr_rain(channel):  
    global Counter_Rain
    Counter_Rain += 1
    print("Counter_Rain: %d" % Counter_Rain)

# Callback fuer GPIO 18
def isr_wind(channel):  
    global Counter_Wind
    Counter_Wind += 1
    print("Counter_Wind: %d" % Counter_Wind)

# Interrupts aktivieren
GPIO.add_event_detect(pin_rain, GPIO.FALLING, callback = isr_rain, bouncetime = 200) 
GPIO.add_event_detect(pin_wind, GPIO.FALLING, callback = isr_wind, bouncetime = 200) 

# Endlosschleife wie oben
try:
  while True:
    # nix Sinnvolles tun
    Tic = Tic + 1
    print("Tic %d" % Tic)
    time.sleep(1)

except KeyboardInterrupt:
  GPIO.cleanup()
  print("\nBye")