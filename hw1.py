import sys
import time
import adafruit_dht
import board

# connected to the GPIO 4 pin
pin = board.D4

# initialize connection
dht = adafruit_dht.DHT11(pin)

while True:
    # get temperature, humidity
    temp = dht.temperature
    hum = dht.humidity

    # print temperature, humidity
    print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temp, hum))

    # wait 3 seconds before reading again
    time.sleep(3)
