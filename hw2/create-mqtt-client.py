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

def main():
    print(load_yaml("./mqtt-client-config.yml"))

if __name__ == "__main__":
    main()
