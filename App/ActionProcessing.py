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



aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

def getPumpState():
    data = aio.data(Constants.PUMP_RELAY_FEED_ID)
    return data[0]

def getLightState():
    data = aio.data(Constants.LIGHT_RELAY_FEED_ID)
    return data[0]

def waterAction(client,status):
    if status > 1:
        return 'Wrong action'
    if status == 0:
        pumpAction = PumpAction(Constants.PUMP_DEVICE_ID, OFF, "")
    else:
        pumpAction = PumpAction(Constants.PUMP_DEVICE_ID, ON, "")

    timeout = 31
    pre = getPumpState().created_at
    client.publish(Constants.PUMP_RELAY_FEED_ID, pumpAction.serialize())
    while(timeout > 0):
        if pre != getPumpState().created_at:
            break
        timeout = timeout - 1  
        if timeout <= 0:
            return 'Timeout, check your connection'
        time.sleep(30)
        aio.publish(Constants.PUMP_RELAY_FEED_ID, pumpAction.serialize()) 
    pumpTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insertActionToDatabase(pumpAction, pumpTime)
    return 'Send success'

def lightAction(client,status):
    if status > 1:
        return 'Wrong action'
        
    lightAction = LightAction(Constants.LIGHT_RELAY_FEED_ID, status, "")

    timeout = 31
    pre = getLightState().created_at
    
    client.publish(Constants.LIGHT_RELAY_FEED_ID, lightAction.serialize())
    while(timeout > 0):
        if pre != getLightState().created_at:
            break
        timeout = timeout - 1  
        if timeout <= 0:
            return 'Timeout, check your connection'
        time.sleep(30)
        client.publish(Constants.LIGHT_RELAY_FEED_ID, lightAction.serialize())
    pumpTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insertActionToDatabase(lightAction, pumpTime)
    return 'Send success'

def buttonLight(client):
    lightAction(client,1)
    time.sleep(120)
    lightAction(client,0)
    return 'Light off'
    
def buttonPump(client):
    waterAction(client,1)
    time.sleep(120)
    waterAction(client,0)
    return 'Pump off'

