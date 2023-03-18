import time
import os, subprocess

subprocess.Popen(['/usr/bin/python3', 'get_wind.py'])
subprocess.Popen(['/usr/bin/python3', 'get_rain.py'])
subprocess.Popen(['/usr/bin/python3', 'transferData.py'])
subprocess.Popen(['/usr/bin/python3', 'fan_controller.py'])

while True:
    try:
        os.system('/usr/bin/python3 get_bme280.py')
        # os.system('/usr/bin/python3 get_cjmcu811.py')
        os.system('/usr/bin/python3 get_hdc1080.py')
        os.system('/usr/bin/python3 get_mics6814.py')
        os.system('/usr/bin/python3 get_mq131.py')
        os.system('/usr/bin/python3 get_scd30.py')
        os.system('/usr/bin/python3 get_smt50.py')
        os.system('/usr/bin/python3 get_soundlevel.py')
        os.system('/usr/bin/python3 get_sps30.py')
        os.system('/usr/bin/python3 get_tsl45315.py')
        os.system('/usr/bin/python3 get_veml6070.py')
        os.system('/usr/bin/python3 get_wifi_signal_strength.py')
        
        time.sleep(60)
    except:
        pass

    