import sys
import time
import paho.mqtt.client as paho_client
import yaml
import json
import ssl

def load_yaml(path):
    with open(path, 'r') as stream:
        return yaml.load(stream, yaml.Loader)

def create_mqtt_client(config_yml_path):

    def on_connect(client, obj, flags, rc):
        if rc == 0:
            print("MQTT connection successful")
        else:
            print("MQTT connection failed")
            client.disconnect()

    # load config YAML file
    config = load_yaml(config_yml_path)

    # set client params
    client = paho_client.Client(config['client_name'])
    client.tls_set(
        ca_certs=config['cafile'],
        certfile=config['certfile'],
        keyfile=config['keyfile'],
        tls_version=ssl.PROTOCOL_SSLv23
    )
    client.tls_insecure_set(True)
    client.on_connect = on_connect

    # attempt to connect to broker
    client.connect(config['broker_ip'], config['port'], 30)

    # subscribe to topics in 'subscriptions' list from config file
    if "subscriptions" in config.keys():
        for topic in config['subscriptions']:
            client.subscribe(topic)
            print(f"Subscribed to {topic}")

    return client

def on_message(client, data, message):
    print(f"Received message from topic '{message.topic}': {message.payload}")

def main():
    # read in client name as argument
    config_yml_path = sys.argv[1] if len(sys.argv) > 1 else None

    if config_yml_path is None:
        print("Supply MQTT client config YAML file as argument to this script")
        exit(1)

    # create Paho MQTT client from YAML config file
    client = create_mqtt_client(config_yml_path)

    # set callback function for receiving messages
    client.on_message = on_message

    # run a background thread to send & receive messages
    client.loop_start()
    
    while True:
        # request temp and humidity status
        client.publish("device/rpi400/request", "")
        print("Published data request ('device/rpi400/request')")

        # wait 10 seconds before requesting again
        time.sleep(10)

# if this script is executed directly (not imported), then run main()
if __name__ == "__main__":
    main()