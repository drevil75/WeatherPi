import time
import subprocess

while True:
    try:
        subprocess.Popen(["python3", 'get_bme280.py'])
        subprocess.Popen(["python3", 'get_hdc1080.py'])
        subprocess.Popen(["python3", 'get_mics6814.py'])
        subprocess.Popen(["python3", 'get_mq131.py'])
        subprocess.Popen(["python3", 'get_rain.py'])
        subprocess.Popen(["python3", 'get_scd30.py'])
        subprocess.Popen(["python3", 'get_smt50.py'])
        subprocess.Popen(["python3", 'get_soundlevel.py'])
        subprocess.Popen(["python3", 'get_sps30.py'])
        subprocess.Popen(["python3", 'get_tsl45315.py'])
        subprocess.Popen(["python3", 'get_veml6070.py'])
        subprocess.Popen(["python3", 'get_wind.py'])
        time.sleep(60)
    except:
        pass

    