# import smbus
# import time

# i2c_ch = 1
# i2c_address = 0x48
# reg_temp = 0x00
# reg_config = 0x01

# bus = smbus.SMBus(i2c_ch)

# while True:
#     val = bus.read_i2c_block_data(i2c_address, reg_temp, 2)
#     print(val)
#     time.sleep(500)

import sys
import time
import adafruit_dht
import board

pin = board.D4
dht = adafruit_dht.DHT11(pin)

while True:
    temp = dht.temperature
    hum = dht.humidity
    print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temp, hum))
    time.sleep(3)
