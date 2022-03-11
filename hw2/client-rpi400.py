import sys
import adafruit_dht
import board
import paho.mqtt.client as paho_client
import yaml

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

def load_yaml(path):
    with open(path, 'r') as stream:
        return yaml.load(stream, yaml.Loader)

def create_mqtt_client(config_yml_path):
    config = load_yaml(config_yml_path)
    client = paho_client.Client(config['client_name'])
    client.tls_set(
        ca_certs=config['cafile'],
        certfile=config['certfile'],
        keyfile=config['keyfile']
    )

    client.connect(config['broker_ip'], config['port'])
    return client

def main():
    # read in client name as argument
    config_yml_path = sys.argv[1] if len(sys.argv) > 1 else None

    if config_yml_path is None:
        print("Supply MQTT client config YAML file as argument to this script")
        exit(1)

    # connected to the GPIO 4 pin
    pin = board.D4

    # initialize reader
    reader = DHT11Reader(pin)

    # create Paho MQTT client from YAML config file
    client = create_mqtt_client(config_yml_path)

    # subscribe to temperature and humidity request topics
    topics = ["temp/request", "humidity/request"]
    for topic in topics:
        client.subscribe(topic)
        print(f"Subscribed to '{topic}'")

    def on_message(client, data, message):
        if message.topic in topics:
            # read temp & humidity data
            temp, hum = reader.read()
            res = None
            if message.topic == 'temp/request':
                res = str(temp)
                client.publish("temp/status", str(temp))
            else:
                res = str(hum)
                client.publish("humidity/status", str(hum))
            print(f"Published message '{res}' to topic '{message.topic}'")

    # set callback function for receiving messages
    client.on_message = on_message

    # busy wait for requests
    client.loop_forever()

# if this script is executed directly (not imported), then run main()
if __name__ == "__main__":
    main()