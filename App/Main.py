from Adafruit_IO import MQTTClient
from ActionProcessing import *
from utils import * 
import json
import sys
import mysql.connector
import requests
import os
 
 ####

def init():
    global CurrentEnvironment 

    global Land 
    
    # Get request 


    request = requests.get(Constants.WEB_SERVER_GET_LAND_ID_URL)

    payload = request.json()

    Constants.LAND_ID = int(payload["landId"])

    conn = mysql.connector.connect(**Constants.connectionString)
    cursor = conn.cursor()

    cursor.execute(
    " SELECT * FROM Land " +
    " WHERE Land.Id = " + str(Constants.LAND_ID) +
    ";"
    )

    res = cursor.fetchall()[0]

    cursor.close()
    conn.close()

    print("Land records associated with landId are: " + str(res))

    CurrentEnvironment = Environment(-1, -1, -1)

    Land = Land(    
            tempRange=(res[4],res[5]),
            humidRange=(res[6],res[7]),
            hazardTempRange=(res[8],res[9]),
            hazardHumidRange=(res[10],res[11])
            )

def message(client, feed_id, payload):
    dct = json.loads(payload)

    measureValue = None
    measureType = "None"

    if dct["name"] == "TEMP-HUMID":
        measureValue = CurrentEnvironment.temperature = int(dct["data"].split("-")[0])
        measureType = "Temperature"
    elif dct["name"] == "SOIL":
        measureValue = CurrentEnvironment.humidity = int(dct["data"])
        measureType = "Humidity"
    elif dct["name"] == "LIGHT":
        measureValue = CurrentEnvironment.brightness = int(dct["data"])
        measureType = "Brightness"

    processAction(client, Land, CurrentEnvironment)

    conn = mysql.connector.connect(**Constants.connectionString)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO ENVIRONMENT_LOG(LandId,MeasureValue,MeasureType,CurrentTime) " +
        "VALUES (" + 
            str(Constants.LAND_ID) + "," +
            str(measureValue) + "," + 
            "\"" + str(measureType) + "\"" + "," +  
            "\"" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\"" +
        ");" 
    )

    conn.commit()
    cursor.close()
    conn.close()

    print('Feed {0} received new value: {1}'.format(feed_id, payload))

def connected(client):
    print('Connected to Adafruit IO!  Listening for changes...')

    client.subscribe(Constants.SOIL_SENSOR_FEED_ID)
    client.subscribe(Constants.TEMP_HUMID_SENSOR_FEED_ID)
    client.subscribe(Constants.LIGHT_SENSOR_FEED_ID)

def subscribe(client, userdata, mid, granted_qos):
    print('Subscribed to {0} with QoS {1}'.format("..", granted_qos[0]))

def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)


def connected_():
    client.subscribe(Constants.LIGHT_SENSOR_FEED_ID)

def start():
    init()

    client = MQTTClient(Constants.ADAFRUIT_IO_USERNAME,Constants.ADAFRUIT_IO_KEY)

    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    client.on_subscribe = subscribe 

    client.connect()

    client.loop_blocking()


start()