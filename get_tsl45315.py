#https://www.instructables.com/Raspberry-Pi-TSL45315-Ambient-Light-Sensor-Python-/

import smbus
import time
import sendvaluesapi

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

# Convert the data to lux

luminance = data[1] * 256 + data[0]

# Output data to screen

print("Ambient Light Luminance : %d lux" %luminance)
sendvaluesapi.write2api('luminance', luminance)
