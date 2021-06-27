import sys, os
from random import randint
from Adafruit_IO import MQTTClient
import json
import time

"""
*   change directory to /publisher/ then run the file
"""

def connected(client):
    print("process connected successfully")

def disconnected(client):
    print("Disconnected. Byee!")

def generateFeedValue(client):
    import constants

    client.loop_background()

    while True:
        temperature = randint(15,40)
        payload = {
            "id":"7",
            "name":"TEMP-HUMID",
            "data": str(temperature) + "-0",
            "unit":"*C-%"
            }
        client.publish(constants.TEMP_HUMID_SENSOR_FEED_ID,json.dumps(payload))

        print(json.dumps(payload))
        
        humidity = randint(70,90)
        payload = {
                "id":"9",
                "name":"SOIL",
                "data": str(humidity),
                "unit":"%"
            }

        client.publish(constants.SOIL_SENSOR_FEED_ID, json.dumps(payload))

        print(json.dumps(payload))
        
        brightness = randint(50, 150)
        payload = {
                "id":"13",
                "name":"LIGHT",
                "data": str(brightness),
                "unit":""
            }

        client.publish(constants.LIGHT_SENSOR_FEED_ID, json.dumps(payload))

        print(json.dumps(payload))

        time.sleep(40) # 1 request per 2/3 minute

def initialize_callbacks():
    client.on_connect = connected
    client.on_disconnect = disconnected

if __name__ == '__main__':
    sys.path.append(os.path.abspath('..'))
    print(sys.path)

    import constants
    client = MQTTClient(constants.ADAFRUIT_IO_USERNAME, constants.ADAFRUIT_IO_KEY)
    client.loop_background()
    initialize_callbacks()
    client.connect()
    generateFeedValue(client)


