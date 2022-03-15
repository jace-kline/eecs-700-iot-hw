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

def mk_state(attrs):
    return {
        "state": {
            "reported": attrs
        }
    }

def on_message(client, userdata, message):
    data = message.payload.decode()
    if message.topic == 'device/rpi400/data':
        print(f"Received message from topic '{message.topic}':\n\t{data}")
        topic = '$aws/things/rpi400/shadow/update'
        payload = json.dumps({
            "state": {
                "reported": json.loads(data)
            }
        })
        client.publish(topic, payload)
        print(f"Published device shadow update to topic '{topic}':\n\t{payload}\n")
    elif message.topic == '$aws/things/rpi400/shadow/update/documents':
        print(f"Received state update message from topic '$aws/things/rpi400/shadow/update/documents':\n{data}\n")

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
    client.loop_forever()

# if this script is executed directly (not imported), then run main()
if __name__ == "__main__":
    main()