from EnvironmentChecking import plantEnvironmentCheck
from utils import *
from Adafruit_IO import MQTTClient
import time
import datetime
import mysql.connector
import Constants as Constants

UNINITIALIZED   = -1
ON              =  1
OFF             =  0


class CurrentState:
    LIGHT_ON = UNINITIALIZED

def insertActionToDatabase(action, time):
    conn = mysql.connector.connect(**Constants.connectionString)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO DEVICE_ACTED_IN_LAND(DeviceId,LandId,RealTime,State) " +
        "VALUES (" + 
            str(action.deviceId) + "," +
            str(Constants.LAND_ID) + "," +
            "\"" + time + "\"" + "," +
            "\"" + str(action.status) + "\"" +   
        ");" 
    )

    conn.commit()
    cursor.close()
    conn.close()

def sendWaterAction(client, duration):    
    pumpOnAction = PumpAction(Constants.PUMP_DEVICE_ID, ON, "")
    pumpOffAction = PumpAction(Constants.PUMP_DEVICE_ID, OFF, "")

    pumpOnTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    client.publish(Constants.PUMP_RELAY_FEED_ID, pumpOnAction.serialize())
    
    print("Watering Tree in " + str(duration) + " seconds")
    time.sleep(duration)
    
    pumpOffTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    client.publish(Constants.PUMP_RELAY_FEED_ID, pumpOffAction.serialize())

    Constants.COOLDOWN_TIME = 60
    print("Cool Down Time is " + str(Constants.COOLDOWN_TIME))
    Constants.LAST_WATERING_TIMESTAMP = float(time.time())

    insertActionToDatabase(pumpOnAction, pumpOnTime)
    insertActionToDatabase(pumpOffAction, pumpOffTime)

    return True

def sendLightAction(client, status):
    lightAction = LightAction(Constants.LIGHT_DEVICE_ID, status, "")

    client.publish(Constants.LIGHT_RELAY_FEED_ID, LightAction(Constants.LIGHT_DEVICE_ID, status, "").serialize())
    
    print("Turn the Light " + ("ON" if status == 1 else "OFF"))
    
    insertActionToDatabase(lightAction, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    return True

def processAction(client, Land, currentEnvironment):
    if CurrentState.LIGHT_ON == UNINITIALIZED:
        sendLightAction(client, OFF)
        CurrentState.LIGHT_ON = OFF

    if plantEnvironmentCheck(Land, currentEnvironment) is False:
        return

    if float(time.time()) - Constants.LAST_WATERING_TIMESTAMP < Constants.COOLDOWN_TIME:
        return

    temperature, humidity = currentEnvironment.temperature, currentEnvironment.humidity

    lowerBoundTemp, upperBoundTemp = Land.temperatureRange
    lowerBoundHumid, upperBoundHumid = Land.humidityRange
    
    if currentEnvironment.brightness >= 100:
        sendLightAction(client, 0)
    else :
        sendLightAction(client, 1)

    if temperature < lowerBoundTemp and humidity > upperBoundHumid:
        sendWaterAction(client,20) # thirty second
    if temperature < lowerBoundTemp and humidity < lowerBoundHumid:
        sendWaterAction(client,10)
    if temperature > upperBoundTemp and humidity > upperBoundHumid:
        sendWaterAction(client,5)
    if temperature > upperBoundTemp and humidity < lowerBoundHumid:
        sendWaterAction(client,25)

    return




