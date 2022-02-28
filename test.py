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
import Adafruit_DHT

dht_version = 11
gpio_pin = 4

while True:
    hum, temp = Adafruit_DHT.read_retry(dht_version, gpio_pin)
    print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
    time.sleep(1)
