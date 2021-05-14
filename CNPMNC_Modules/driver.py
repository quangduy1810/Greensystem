from Adafruit_IO import MQTTClient
from ActionProcessing import *
from CustomEnvironmentUpdate import *
from utils import * 
import sys

ADAFRUIT_IO_USERNAME = "mnhat81t"
ADAFRUIT_IO_KEY = "aio_oAlJ83vRGQomqFzkDZaB2w2PwpHT"

CurrentEnvironment = Environment(-1, -1, -1)

Land = Land(    
        tempRange=(20,30),humidRange=(70,80),
        hazardHumidRange=(40,90),hazardTempRange=(15,45))


def message(client, feed_id, payload):
    if feed_id == "Temperature":
        CurrentEnvironment.temperature = int(payload)
    elif feed_id == "Humidity":
        CurrentEnvironment.humidity = int(payload)
    elif feed_id == "Brightness":
        CurrentEnvironment.brightness = int(payload)

    processAction(Land, CurrentEnvironment)

    print('Feed {0} received new value: {1}'.format(feed_id, payload))

def connected(client):
    print('Connected to Adafruit IO!  Listening for changes...')

    client.subscribe("Temperature")
    client.subscribe("Humidity")
    client.subscribe("Brightness")

def subscribe(client, userdata, mid, granted_qos):
    print('Subscribed to {0} with QoS {1}'.format("..", granted_qos[0]))

def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe 

client.connect()

client.loop_blocking()


