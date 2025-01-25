import RPi.GPIO as GPIO
import time, datetime
import configparser

config = configparser.ConfigParser()
config.read('./config.cfg')
fanpin = int(config['fan']['fanpin'])

GPIO.setmode(GPIO.BCM)
GPIO.setup(fanpin, GPIO.OUT)


while True:

    GPIO.output(fanpin, GPIO.HIGH)
    time.sleep(10)
    GPIO.output(fanpin, GPIO.LOW)
    time.sleep(3600)