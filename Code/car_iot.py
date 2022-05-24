from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

import time
import random
import json


ENDPOINT = "a3gjz7gfixx2gk-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID= "car1"
PATH_TO_ROOT_CA = "/workspaces/MQTT_AWS_IOT/Code/.certificate/ROOT-CA.crt"
PATH_TO_PRIVATE_KEY = "/workspaces/MQTT_AWS_IOT/Code/.certificate/private.key"
PATH_TO_CERTIFICATE = "/workspaces/MQTT_AWS_IOT/Code/.certificate/certificate.pem.crt"

TOPIC = "lab/telemetry"


def read_sensor():
    """
    Function for reading sensor data
    """
    print("Read Sensor Data")
    # Read sensor data
    sensor_data = random.randint(1, 120)
    print("Sensor Data: {}".format(sensor_data))
    return json.dumps({
        'trip_id': random.randint(1019312931, 300200320293),
        'engine_speed_mean': 1500 * random.random(),
        'fuel_level': random.randint(0, 100),
        'high_acceleration_event': random.randint(0, 12),
        'high_breaking_event': random.randint(0, 4),
        'odometer': 8.14 * random.random(),
        'oil_temp_mean': random.randint(12, 205),
        "speed": sensor_data
    })


def connect_aws_iot():
    """
    Function for sending data to AWS IoT

    Source: https://aws.amazon.com/premiumsupport/knowledge-center/iot-core-publish-mqtt-messages-python/
    """
    print("Send Data to AWS IoT")
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
                endpoint=ENDPOINT,
                cert_filepath=PATH_TO_CERTIFICATE,
                pri_key_filepath=PATH_TO_PRIVATE_KEY,
                client_bootstrap=client_bootstrap,
                ca_filepath=PATH_TO_ROOT_CA,
                client_id=CLIENT_ID,
                clean_session=False,
                keep_alive_secs=6)
    print("Connecting to {} with client ID '{}'...".format(
            ENDPOINT, CLIENT_ID))
    # Make the connect() call
    connect_future = mqtt_connection.connect()
    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")
    for i in range(1, 100):
        message = read_sensor()
        print(f"Publishing message {message}...")
        publish_future = mqtt_connection.publish(topic=TOPIC,
                                                 payload=message, 
                                                 qos=mqtt.QoS.AT_LEAST_ONCE)
        time.sleep(2)
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")


if __name__ == "__main__":
    connect_aws_iot()