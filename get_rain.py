#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# GPIO-Ports
Counter_17 = 0
Counter_18 = 0

# Zaehlvariable
Tic = 0

# GPIO initialisieren
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN) # Pin 11
GPIO.setup(18, GPIO.IN) # Pin 12

# internen Pullup-Widerstand aktivieren.
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)  

# Callback fuer GPIO 17
def isr17(channel):  
    global Counter_17
    Counter_17 = Counter_17 + 1
    print("Counter_17: %d" % Counter_17)

# Callback fuer GPIO 18
def isr18(channel):  
    global Counter_18
    Counter_18 = Counter_18 + 1
    print("Counter_18: %d" % Counter_18)

# Interrupts aktivieren
GPIO.add_event_detect(17, GPIO.FALLING, callback = isr17, bouncetime = 200) 
GPIO.add_event_detect(18, GPIO.FALLING, callback = isr18, bouncetime = 200) 

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