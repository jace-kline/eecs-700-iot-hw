import sys
import time
import adafruit_dht
import board

# A wrapper class for reading the DHT11 sensor
# Tries to catch and handle occasional read errors
class DHT11Reader:
    def __init__(self, pin):
        self.pin = pin
        self.dht = adafruit_dht.DHT11(pin)
        self.temperature = 0
        self.humidity = 0
        self.errors_in_a_row = 0
        self.error_threshold = 5

    def read(self):
        try:
            # try to read temperature, humidity from sensor
            self.temperature = self.dht.temperature
            self.humidity = self.dht.humidity
            self.errors_in_a_row = 0
        
        except RuntimeError as e:
            # sometimes this error occurs, but it shouldn't be fatal
            # catch and continue execution
            if self.errors_in_a_row < self.error_threshold:
                self.errors_in_a_row += 1
                print(f"Exception handled. Message = '{str(e)}'")
            # any other errors must be re-raised
            else:
                raise

        return self.temperature, self.humidity

def main():
    # connected to the GPIO 4 pin
    pin = board.D4

    # initialize reader
    reader = DHT11Reader(pin)

    while True:
        # read temp & humidity data
        temp, hum = reader.read()

        # print temp & humidity
        print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temp, hum))

        # wait 1 second before reading again
        time.sleep(1)

# if this script is executed directly (not imported), then run main()
if __name__ == "__main__":
    main()
