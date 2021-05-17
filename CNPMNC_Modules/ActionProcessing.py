from EnvironmentChecking import plantEnvironmentCheck
from utils import *
from Adafruit_IO import MQTTClient
import time
import Constants



def sendWaterAction(client, duration):    
    client.publish(Constants.PUMP_RELAY_FEED_ID, PumpAction(Constants.PUMP_DEVICE_ID,status=1).serialize())
    print("Watering Tree in " + str(duration) + " seconds")
    time.sleep(duration)
    client.publish(Constants.PUMP_RELAY_FEED_ID, PumpAction(Constants.PUMP_DEVICE_ID, status=0).serialize())
    
    return True

def sendLightAction(client, status):

    return True

def processAction(client, Land, currentEnvironment):
    if plantEnvironmentCheck(Land, currentEnvironment) is False:
        return

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


    # There is more to implement in this file
    # Til this point the weather is fine

    return




