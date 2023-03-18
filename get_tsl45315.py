import smbus
import time
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *
from apis.send2buffer import writeBuffer

def read_tsl45315():
   print('---------read_tsl45315--------')
   # Get I2C bus

   bus = smbus.SMBus(1)

   # TSL45315 address, 0x29(41)

   # Select Control register, 0x00(0), with Command register, 0x80(128)

   # 0x03(03) Normal operation

   bus.write_byte_data(0x29, 0x00 | 0x80, 0x03)

   # TSL45315 address, 0x29(41)

   # Select Configuration register, 0x01(1), with Command register, 0x80(128)

   # 0x00(00) Multiplier 1x, Tint : 400ms

   bus.write_byte_data(0x29, 0x01 | 0x80, 0x00)

   time.sleep(0.5)

   # TSL45315 address, 0x29(41)

   # Read data back from 0x04(4), with Command register, 0x80(128)

   # 2 bytes, LSB first

   data = bus.read_i2c_block_data(0x29, 0x04 | 0x80, 2)
   luminance = data[1] * 256 + data[0]

   print(f'tsl45315 lux={luminance}')

   ts = getInflxTimestamp()
   data = f'tsl45315,type=light luminance={luminance} {ts}'
   writeBuffer('influx-tsl45315', data)

   ts = getOSMTimestamp()
   osm_data = [
      {"sensor": f"{brightID}","value": f"{luminance}","createdAt": f"{ts}"}
   ]
   writeBuffer('osm-tsl45315', json.dumps(osm_data))

   # writeBuffer('openhab-tsl45315', f'{oh_brightID},{luminance},{ts}')
   postOpenhabValues(oh_brightID,luminance, ts)


if __name__ == "__main__":
   read_tsl45315()