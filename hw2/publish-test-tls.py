import sys
import time
import adafruit_dht
import board
import paho.mqtt.client as paho_client

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
    # read in client name as argument
    client_name = sys.argv[1] if len(sys.argv) > 1 else None

    if client_name is None:
        print("Supply MQTT client name as argument to this script")
        exit(1)

    # connected to the GPIO 4 pin
    pin = board.D4

    # initialize reader
    reader = DHT11Reader(pin)

    # specify MQTT broker IP address
    brokerIP = "192.168.86.82"
    port = 8883

    client = paho_client.Client(f"client-{client_name}")
    client.tls_set(
        ca_certs="/etc/mosquitto/certs/ca.crt",
        certfile=f"/etc/mosquitto/certs/client-{client_name}.crt",
        keyfile=f"/etc/mosquitto/certs/client-{client_name}.key"
    )

    client.on_connect = lambda: print("Connected to MQTT broker")
    client.on_disconnect = lambda: print("Disconnected from MQTT broker")

    client.connect(brokerIP, port)

    while True:
        # read temp & humidity data
        temp, hum = reader.read()

        # publish temp and humidity status to MQTT broker
        client.publish("temp/status", str(temp))
        client.publish("humidity/status", str(hum))
        print("Published data to MQTT broker")

        # print temp & humidity to terminal
        print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temp, hum))

        # wait 5 seconds before reading again
        time.sleep(5)

# if this script is executed directly (not imported), then run main()
if __name__ == "__main__":
    main()