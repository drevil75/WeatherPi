import RPi.GPIO as GPIO
import spidev
from time import sleep

# Initialisierung der Analogen Pins
A0,A1,A2,A3,A4,A5,A6,A7 = 0,1,2,3,4,5,6,7
pin_voltage = 3.3

# SPI-Einstellungen
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 2000000

def readadc(adcnum):
# Auslesen der SPI-Werte
 r = spi.xfer2([1,8+adcnum <<4,0])
 adcout = ((r[1] &3) <<8)+r[2]
 return adcout

while True:
    # Einlese der Analogen Werte und kopie in eine andere Variable
    a = ((readadc(A0) / 1024) * pin_voltage) * 50
    # b = readadc(A1)
    # c = readadc(A2)
    # d = readadc(A3)
    # e = readadc(A4)
    # f = readadc(A5)
    # g = readadc(A6)
    # h = readadc(A7)

    # Ausgabe der Analogen Werte
    print("Channel A0: " + str(a))
    # print("Channel A1: " + str(b))
    # print("Channel A2: " + str(c))
    # print("Channel A3: " + str(d))
    # print("Channel A4: " + str(e))
    # print("Channel A5: " + str(f))
    # print("Channel A6: " + str(g))
    # print("Channel A7: " + str(h))
    #print "_______________________________________\n"
    sleep(0.5)

