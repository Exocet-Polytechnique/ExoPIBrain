"""
ADXL345 (accelerometer)

I2C protocol:
    ADXL345 self-assigned address: 0x53
    to detect i2c devices (1 for 40-pin RP models, 0 for 26-pin RP models): $ i2cdetect -y 1

ADXL345 registers:
    0x2D - POWER_CTL - R/W - Power-saving features control. 
    0x32 - DATAX0 - R - X-Axis Data 0.
    0x33 - DATAX1 - R - X-Axis Data 1.
    0x34 - DATAY0 - R - Y-Axis Data 0.
    0x35 - DATAY1 - R - Y-Axis Data 1.
    0x36 - DATAZ0 - R - Z-Axis Data 0.
    0x37 - DATAZ1 - R - Z-Axis Data 1. 
"""

import smbus2
import time



bus = smbus2.SMBus(1) # 1 for 40-pin RP models, 0 for 26-pin RP models

ADXL345_ADDRESS = 0x53

ADXL345_REG_POWERCTRL = 0x2D
ADXL345_REG_DATA_FORMAT = 0x31
ADXL345_REG_XLSB = 0x32
ADXL345_REG_XMSB = 0x33
ADXL345_REG_YLSB = 0x34
ADXL345_REG_YMSB = 0x35
ADXL345_REG_ZLSB = 0x36
ADXL345_REG_ZMSB = 0x37



# Wake up the sensor (standby mode -> measurement mode)
bus.write_byte_data(ADXL345_ADDRESS, ADXL345_REG_POWERCTRL, 0b00001000)

# 
# bus.write_byte_data(ADXL345_ADDRESS, ADXL345_REG_DATA_FORMAT, 0x0B)

while True:

    # Read raw data (1 byte) from sensor registers
    # This method is not recommanded (it is better to use read_i2c_block_data() )
    x_lsb = bus.read_byte_data(ADXL345_ADDRESS, ADXL345_REG_XLSB)
    x_msb = bus.read_byte_data(ADXL345_ADDRESS, ADXL345_REG_XMSB)
    y_lsb = bus.read_byte_data(ADXL345_ADDRESS, ADXL345_REG_YLSB)
    y_msb = bus.read_byte_data(ADXL345_ADDRESS, ADXL345_REG_YMSB)
    z_lsb = bus.read_byte_data(ADXL345_ADDRESS, ADXL345_REG_ZLSB)
    z_msb = bus.read_byte_data(ADXL345_ADDRESS, ADXL345_REG_ZMSB)

    # Combine raw data bytes for each axis
    x = (x_msb << 8) + x_lsb
    y = (y_msb << 8) + y_lsb
    z = (z_msb << 8) + z_lsb

    # Convert to signed value (C2 by default)
    if (x & (1 << 16 - 1)):
        x = x - (1<<16)
    if (y & (1 << 16 - 1)):
        y = y - (1<<16)
    if (z & (1 << 16 - 1)):
        z = z - (1<<16)

    # Convert to units of g-force
    x = x * 0.004 
    y = y * 0.004
    z = z * 0.004

    # Convert to m/s
    x = x * 9.8
    y = y * 9.8
    z = z * 9.8

    print("")
    print(f"x = {x}")
    print(f"y = {y}")
    print(f"z = {z}")

    time.sleep(1)





