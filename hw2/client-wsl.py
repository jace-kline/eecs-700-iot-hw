import sys
import time
import paho.mqtt.client as paho_client
import yaml

def load_yaml(path):
    with open(path, 'r') as stream:
        return yaml.load(stream, yaml.Loader)

def create_mqtt_client(config_yml_path):
    config = load_yaml(config_yml_path)
    client = paho_client.Client(config['client_name'])
    client.tls_set(
        ca_certs=config['ca_certs'],
        certfile=config['certfile'],
        keyfile=config['keyfile']
    )

    client.connect(config['broker_ip'], config['port'])
    return client

def on_message(client, data, message):
    print(f"Received message from topic '{message.topic}': '{message.data}'")

def main():
    # read in client name as argument
    config_yml_path = sys.argv[1] if len(sys.argv) > 1 else None

    if config_yml_path is None:
        print("Supply MQTT client config YAML file as argument to this script")
        exit(1)

    # create Paho MQTT client from YAML config file
    client = create_mqtt_client(config_yml_path)

    # subscribe to temperature and humidity status topics
    topics = ["temp/status", "humidity/status"]
    for topic in topics:
        client.subscribe(topic)
        print(f"Subscribed to '{topic}'")
    

    # set callback function
    client.on_message = on_message

    while True:

        # request temp and humidity status from MQTT broker
        client.publish("temp/request", "")
        print("Published temperature request: 'temp/request'")
        client.publish("humidity/request", "")
        print("Published humidity request: 'humidity/request'")

        # wait 10 seconds before requesting again
        time.sleep(10)

# if this script is executed directly (not imported), then run main()
if __name__ == "__main__":
    main()