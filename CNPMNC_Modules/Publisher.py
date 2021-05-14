import sys
from random import randint
from Adafruit_IO import MQTTClient
import time

ADAFRUIT_IO_USERNAME = "mnhat81t"
ADAFRUIT_IO_KEY = "aio_oAlJ83vRGQomqFzkDZaB2w2PwpHT"

def connected(client):
    print("process connected successfully")

def disconnected(client):
    print("Disconnected. Byee!")

def generateFeedValue(client):
    while True:
        temperature = randint(0,42)
        client.publish('Temperature',temperature)

        humidity = randint(0,100)
        client.publish('Humidity', humidity)

        brightness = randint(0, 255)
        client.publish('Brightness', brightness)

        time.sleep(10)

def initialize_callbacks():
    client.on_connect = connected
    client.on_disconnect = disconnected

if __name__ == '__main__':
    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    initialize_callbacks()
    client.connect()
    client.loop_background()
    generateFeedValue(client)

