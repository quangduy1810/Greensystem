
import random
import sys
import time

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# Visit Adafruit io website
# username:mnhat71.t@gmail.com
# password:DADN12345
# then copy the adafruit io key and
# username to replace these two.
ADAFRUIT_IO_KEY = 'aio_AkKJ67VoIx3F8f6YGyJNUwKPoiSN'

ADAFRUIT_IO_USERNAME = 'mnhat71t'

BRIGHTNESS_THRESHOLD = 127

# Define callback functions which will be called when certain events happen.
def connected(client):
    print('Connected to Adafruit IO!  Listening for DemoFeed changes...')
    client.subscribe('temperature')
    client.subscribe('humidity')
    client.subscribe('brightness')
    client.subscribe('light')

def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

client.loop_background()

# Now send new values every 10 seconds.
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
while True:
    temperature = random.randint(26, 42)
    humidity = random.randint(45, 100)
    brightness = random.randint(0, 255)
    
    print('Publishing {0} to temperature.'.format(temperature))
    print('Publishing {0} to humidity.'.format(humidity))
    print('Publishing {0} to brightness.'.format(brightness))
    
    client.publish('temperature', temperature)
    client.publish('humidity', humidity)
    client.publish('brightness', brightness)

    if brightness < BRIGHTNESS_THRESHOLD:
        client.publish('light', 'OFF')
    else :
        client.publish('light', 'ON')

    time.sleep(10)

