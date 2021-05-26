from EnvironmentChecking import plantEnvironmentCheck
from utils import *
from Adafruit_IO import MQTTClient
import time
import Constants as Constants

def sendWaterAction(client, duration):    
    client.publish(Constants.PUMP_RELAY_FEED_ID, PumpAction(Constants.PUMP_DEVICE_ID,1).serialize())
    print("Watering Tree in " + str(duration) + " seconds")
    time.sleep(duration)
    client.publish(Constants.PUMP_RELAY_FEED_ID, PumpAction(Constants.PUMP_DEVICE_ID,0).serialize())

    Constants.COOLDOWN_TIME = 100
    Constants.LAST_WATERING_TIMESTAMP = time.time()

    return True

def sendLightAction(client, status):
    client.publish(Constants.LIGHT_RELAY_FEED_ID, LightAction(Constants.LIGHT_DEVICE_ID, status).serialize())
    print("Turn the Light " + ("ON" if status == 1 else "OFF"))
    return True

def processAction(client, Land, currentEnvironment):
    if plantEnvironmentCheck(Land, currentEnvironment) is False:
        return

    # if time.time() - Constants.LAST_WATERING_TIMESTAMP < Constants.COOLDOWN_TIME:
    #     return

    temperature, humidity = currentEnvironment.temperature, currentEnvironment.humidity

    lowerBoundTemp, upperBoundTemp = Land.temperatureRange
    lowerBoundHumid, upperBoundHumid = Land.humidityRange

    if temperature < lowerBoundTemp and humidity > upperBoundHumid:
        sendWaterAction(client,20) # thirty second
    if temperature < lowerBoundTemp and humidity < lowerBoundHumid:
        sendWaterAction(client,10)
    if temperature > upperBoundTemp and humidity > upperBoundHumid:
        sendWaterAction(client,5)
    if temperature > upperBoundTemp and humidity < lowerBoundHumid:
        sendWaterAction(client,30)

    if currentEnvironment.brightness >= 100:
        sendLightAction(client, 0)
    else :
        sendLightAction(client, 1)

    return




