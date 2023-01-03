import time
from get_bme280 import *
from get_dht22 import *
from get_sound import *
from get_sps30 import *
from get_tsl45315 import *
from get_veml6070 import *


while True:
    try:
        read_bme280()
    except:
        pass
    try:
        read_dht22()
    except:
        pass
    try:
        read_sound()
    except:
        pass
    try:
        read_sps30()
    except:
        pass
    try:
        read_tsl45315()
    except:
        pass
    try:
        read_veml6070()
    except:
        pass
    # time.sleep(60)