#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# GPIO-Ports
Counter_Wind = 0
windspeed = 0.0
pin_wind = 4
bouncetime = 30
messungspeed = '50'

f = open(f'messung{messungspeed}.txt', mode='w', encoding='utf-8')
f.write(f'messungspeed={messungspeed}-------')


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
GPIO.add_event_detect(pin_wind, GPIO.FALLING, callback = isr_wind, bouncetime = bouncetime) 

# Endlosschleife wie oben
try:
    while True:
        # nix Sinnvolles tun
        t += 1
        # print(f"time {t}")
        if t == 10:
            print(f't10 ---------- {Counter_Wind}')
            f.write(f't10={Counter_Wind}')
            

        if t == 20:
            print(f't20 ---------- {Counter_Wind}')
            f.write(f't20={Counter_Wind}')

        if t == 30:
            print(f't30 ---------- {Counter_Wind}')
            f.write(f't30={Counter_Wind}')

        if t == 40:
            print(f't40 ---------- {Counter_Wind}')
            f.write(f't40={Counter_Wind}')

        if t == 50:
            print(f't50 ---------- {Counter_Wind}')
            f.write(f't50={Counter_Wind}')

        if t == 60:
            print(f't60 ---------- {Counter_Wind}')
            f.write(f't60={Counter_Wind}')

            if Counter_Wind > 0:
                windspeed = (Counter_Wind / 2) / 60.0 * 2.4 # Counter / 60 Seconds * 2.4m/s

            windspeed = 0
            Counter_Wind = 0
            t = 0
        time.sleep(1)


except KeyboardInterrupt:
    f.close
    GPIO.cleanup()

