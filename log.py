
import random
import sys
import time
import pandas as pd

# Import Adafruit IO MQTT client.
from Adafruit_IO import Client

# Visit Adafruit io website
# username:mnhat71.t@gmail.com
# password:DADN12345
# then copy the adafruit io key and
# username to replace these two.
ADAFRUIT_IO_KEY = 'aio_hQyW35GKcRXnArhYbCLIsGrqF1Ep'

ADAFRUIT_IO_USERNAME = 'mnhat71t'

BRIGHTNESS_THRESHOLD = 127

# Define callback functions which will be called when certain events happen.
def connected(client):
    print('Connected to Adafruit IO!  Listening for DemoFeed changes...')
    
def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))


# Create an client instance.
client = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
# client.on_connect    = connected
# client.on_disconnect = disconnected
# client.on_message    = message

# Connect to the Adafruit IO server.
# client.connect()

# client.loop_background()

# Now get data from Feed
temperature = client.data("temperature")
temp = []
bright = []
humid = []
for t in temperature:
    temp += [t.value]
brightness = client.data("brightness")
for b in temperature:
    bright += [t.value]
humidity = client.data("humidity")
for h in temperature:
    humid += [t.value]

df = {"Temperature":temp[:2],"Humidity":humid[:2],"Brightness":bright[:2]}
log = pd.DataFrame(df)
log.to_csv("log.csv")
