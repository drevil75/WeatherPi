import time
from get_bme280 import *
from get_dht22 import *
from get_sound import *
from get_sps30 import *
from get_tsl45315 import *
from get_veml6070 import *


while True:
    read_bme280()
    read_dht22()
    read_sound()
    read_sps30()
    read_tsl45315()
    read_veml6070()
    time.sleep(60)