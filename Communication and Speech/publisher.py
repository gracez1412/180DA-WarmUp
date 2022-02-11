import paho.mqtt.client as mqtt
import numpy as np

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Exepcted Disconnect')

# the default message callback
# wont be used if only publishing, but can still exist
def on_message(client, userdata, message):
    print('Received message: ' + str(message.payload) + '" on topic "' + message.topic + '" with QoS ' + str(message.qos))

# 1. create a client instance
client = mqtt.Client()

# add additional client options (security, certifications, etc.)
# many default options should be good to start off
# add callbacks to client

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# connect to a broker using one of the connect functions
client.connect_async("test.mosquitto.org")
# client.connect("localhost", 1883, 60)

# call one of the loop*() functions to maintain network traffic flow wit the broker
client.loop_start()

# use subscribe() to subscrive to a topic and receive messages

# 5. use publish() to publish messages to the broker.
# payload must be a string, bytearray, int, float or None.
print('Publishing...')
for i in range(10):
    print(i)
    client.publish('team5', 'hi', qos=1)

# use disconnect() to disconnect from the broker
client.loop_stop()
client.disconnect()

