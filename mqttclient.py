from Adafruit_IO import *
import sys
import time
import random
IO_USERNAME=  "mnhat71t"
IO_KEY=    "aio_dUnx06UqejE8m373P0rbKRmxBvYG"

def connected(client):
    print('Connected to {0}'.format('Light'))
    client.subscribe('Light')
def disconnected(client):
    print("Disconnected")
    sys.exit(1)
def subscribe(client, userdata, mid, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print('Subscribed to {0} with QoS {1}'.format('Light', granted_qos[0]))
def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))


client = MQTTClient(IO_USERNAME, IO_KEY)

client.on_connect = connected
client.on_disconnect= disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()
#create data
while True:
    shine =0
    light= random.randint(0,255)
    if (light<127): 
        shine=1
    print("Publishing {0} to {1}.".format(shine,'Light'))
    client.publish('Light',shine)
    time.sleep(5)
#get data from server
client.loop_blocking()
