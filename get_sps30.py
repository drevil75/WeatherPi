import sys
import json
from time import sleep
from classes.sps30 import SPS30
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *

pm_sensor = SPS30()
print(f"Firmware version: {pm_sensor.firmware_version()}")
print(f"Product type: {pm_sensor.product_type()}")
print(f"Serial number: {pm_sensor.serial_number()}")
states = pm_sensor.read_status_register()
print(f"Status register: {states}")
print(f"Auto cleaning interval: {pm_sensor.read_auto_cleaning_interval()}s")
print(f"Set auto cleaning interval: {pm_sensor.write_auto_cleaning_interval_days(2)}s")

pm_sensor.start_measurement()
sleep(10)
print(json.dumps(pm_sensor.get_measurement(), indent=2))
sleep(5)
print(json.dumps(pm_sensor.get_measurement(), indent=2))
sleep(5)
vals = pm_sensor.get_measurement()
pm_sensor.stop_measurement()

speed_status = states['speed_status']
laser_status = states['laser_status']
fan_status = states['fan_status']
dense_pm1 = vals['sensor_data']['mass_density']['pm1.0']
dense_pm25 = vals['sensor_data']['mass_density']['pm2.5']
dense_pm4 = vals['sensor_data']['mass_density']['pm4.0']
dense_pm10 = vals['sensor_data']['mass_density']['pm10']
c_pm05 = vals['sensor_data']['particle_count']['pm0.5']
c_pm1 = vals['sensor_data']['particle_count']['pm1.0']
c_pm25 = vals['sensor_data']['particle_count']['pm2.5']
c_pm4 = vals['sensor_data']['particle_count']['pm4.0']
c_pm10 = vals['sensor_data']['particle_count']['pm10']

print(speed_status, laser_status, fan_status)
print(dense_pm1, dense_pm10, dense_pm25, dense_pm4)
print(c_pm05, c_pm1, c_pm10, c_pm25, c_pm4)

ts = getInflxTimestamp()
data = f'particular_matter,sensor_id=sps30 dense_pm1={dense_pm1},dense_pm25={dense_pm25},dense_pm4={dense_pm4},dense_pm10={dense_pm10},cnt_particals_pm05={c_pm05},cnt_particals_pm1={c_pm1},cnt_particals_pm25={c_pm25},cnt_particals_pm4={c_pm4},cnt_particals_pm10={c_pm10} {ts}'

write2influxapi(data)

ts = getOSMTimestamp()
# postOSMvalues(dense_pm1_ID, dense_pm1, ts)
# postOSMvalues(dense_pm4_ID, dense_pm4, ts)
# postOSMvalues(dense_pm10_ID, dense_pm10, ts)
# postOSMvalues(dense_pm25_ID, dense_pm25, ts)


data = [
    {"sensor": f"{dense_pm1_ID}", "value": f"{dense_pm1}", "createdAt": f"{ts}"},
    {"sensor": f"{dense_pm4_ID}", "value": f"{dense_pm4}", "createdAt": f"{ts}"},
    {"sensor": f"{dense_pm10_ID}", "value": f"{dense_pm10}", "createdAt": f"{ts}"},
    {"sensor": f"{dense_pm25_ID}", "value": f"{dense_pm25}", "createdAt": f"{ts}"},
    {"sensor": f"{count_partical_pm05_ID}", "value": f"{c_pm05}", "createdAt": f"{ts}"},
    {"sensor": f"{count_partical_pm1_ID}", "value": f"{c_pm1}", "createdAt": f"{ts}"},
    {"sensor": f"{count_partical_pm4_ID}", "value": f"{c_pm4}", "createdAt": f"{ts}"},
    {"sensor": f"{count_partical_pm10_ID}", "value": f"{c_pm10}", "createdAt": f"{ts}"},
    {"sensor": f"{count_partical_pm25_ID}", "value": f"{c_pm25}", "createdAt": f"{ts}"}
    ]
print(data)
postOSMvalues(data)
# postOSMvalues(count_partical_pm05_ID, c_pm05, ts)
# postOSMvalues(count_partical_pm1_ID, c_pm1, ts)
# postOSMvalues(count_partical_pm4_ID, c_pm4, ts)
# postOSMvalues(count_partical_pm10_ID, c_pm10, ts)
# postOSMvalues(count_partical_pm25_ID, c_pm25, ts)

postOpenhabValues(oh_dense_pm1_ID, dense_pm1, ts)
postOpenhabValues(oh_dense_pm4_ID, dense_pm4, ts)
postOpenhabValues(oh_dense_pm10_ID, dense_pm10, ts)
postOpenhabValues(oh_dense_pm25_ID, dense_pm25, ts)

postOpenhabValues(oh_count_partical_pm05_ID, c_pm05, ts)
postOpenhabValues(oh_count_partical_pm1_ID, c_pm1, ts)
postOpenhabValues(oh_count_partical_pm4_ID, c_pm4, ts)
postOpenhabValues(oh_count_partical_pm10_ID, c_pm10, ts)
postOpenhabValues(oh_count_partical_pm25_ID, c_pm25, ts)