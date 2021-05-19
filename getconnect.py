from Adafruit_IO import *
import sys

ADAFRUIT_IO_USERNAME = "mnhat71t"
ADAFRUIT_IO_KEY = "aio_QDXp42hzVzSjY4zOATNmbhVjcgqc"

def connected(aio):
    print('Connected to {0}'.format('humidity'))
    aio.subscribe('temperature')
def disconnected(aio):
    print("Disconnected")
    sys.exit(1)
def subscribe(aio, userdata, mid, granted_qos):
    # This method is called when the aio subscribes to a new feed.
    print('Subscribed to {0} with QoS {1}'.format('humidity', granted_qos[0]))
def message(aio, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))

class Connection: 
    def getconnectClient():
        aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
        return aio 

    def getconnectMQTTClient():
        aio = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
        
        aio.on_connect = connected
        aio.on_disconnect= disconnected
        aio.on_message = message
        aio.on_subscribe = subscribe

        
        aio.connect()       
        aio.loop_background()


        return aio 