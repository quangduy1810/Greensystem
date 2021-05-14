from EnvironmentChecking import plantEnvironmentCheck
from datetime import *
from utils import *

def sendWaterAction(duration):
    action = WateringAction(duration)
    
    # Code for sending action to
    # the server

    print("Watering Tree in " + str(duration) + " seconds")


    return True



# This will be implemented more later
lastWaterActionTimeStamp = -1

def processAction(Land, currentEnvironment):
    if plantEnvironmentCheck(Land, currentEnvironment) is False:
        return

    temperature, humidity = currentEnvironment.temperature, currentEnvironment.humidity

    lowerBoundTemp, upperBoundTemp = Land.temperatureRange
    lowerBoundHumid, upperBoundHumid = Land.humidityRange

    if temperature < lowerBoundTemp and humidity > upperBoundHumid:
        sendWaterAction(30) # thirty second
    if temperature < lowerBoundTemp and humidity < lowerBoundHumid:
        sendWaterAction(0)
    if temperature > upperBoundTemp and humidity > upperBoundHumid:
        sendWaterAction(5)
    if temperature > upperBoundTemp and humidity < lowerBoundHumid:
        sendWaterAction(30)


    # There is more to implement in this file
    # Til this point the weather is fine

    return




