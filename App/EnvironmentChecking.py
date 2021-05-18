from utils import *
import requests


def temperatureAlert():
    # TODO : Send Alert To Web Server
    url = "localhost:" + ""
    
    r = requests.post(url,data={"Alert":"Temperature"})
            
    print("Temperature is too high. Check your plant right now!!")

def humidityAlert():
    # TODO : Send Alert To Web Server
    url = "localhost:" ""

    requests.post(url, data={"Alert":"Humidity"})

    print("Humidity is too high. Check your plant right now!!")

# Return True if the current environment is good,
# False otherwise.
def plantEnvironmentCheck(Land, environmentInfo):
    if environmentInfo.temperature == -1 or environmentInfo.brightness == -1 or environmentInfo.brightness == -1:
        return False

    lowerBoundTemperature, upperBoundTemperature = Land.hazardousTemperatureRange
    lowerBoundHumidity, upperBoundHumidity = Land.hazardousHumidityRange

    # Unpacking environment data
    currentHumidity, currentTemperature = environmentInfo.humidity, environmentInfo.temperature
    # brightness = environmentInfo.brightness

    humdityFine, temperatureFine = False, False

    if currentHumidity > lowerBoundHumidity and currentHumidity < upperBoundHumidity:
        humdityFine = True
    else :  
        humidityAlert()

    if currentTemperature > lowerBoundTemperature and currentTemperature < upperBoundTemperature:
        temperatureFine = True
    else : 
        temperatureAlert()
        
    return humdityFine and temperatureFine

