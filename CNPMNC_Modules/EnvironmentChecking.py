from utils import *

def temperatureAlert():
    print("Temperature is too high. Check your plant right now!!")

def humidityAlert():
    print("Humidity is too high. Check your plant right now!!")

# Return True if the current environment is good,
# False otherwise.
def plantEnvironmentCheck(Land, environmentInfo):
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

