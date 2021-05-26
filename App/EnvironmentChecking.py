from utils import *
import requests
import mysql.connector
import datetime
import Constants
# Return True if the current environment is good,
# False otherwise.
def plantEnvironmentCheck(Land, environmentInfo):
    if environmentInfo.temperature == -1 or environmentInfo.brightness == -1 or environmentInfo.brightness == -1:
        return False

    lowerBoundTemperature, upperBoundTemperature = Land.hazardousTemperatureRange
    lowerBoundHumidity, upperBoundHumidity = Land.hazardousHumidityRange

    # Unpacking environment data
    currentHumidity, currentTemperature = environmentInfo.humidity, environmentInfo.temperature

    humdityFine, temperatureFine = False, False
    
    payload = {
        "temperature": str(currentHumidity),
        "humidity": str(currentTemperature),
        "brightness": str(environmentInfo.brightness),
        "alert" : "Weather is Normal.",
        "code" : 0
    }

    if currentHumidity > lowerBoundHumidity and currentHumidity < upperBoundHumidity:
        humdityFine = True
    else :  
        payload["alert"] = "Humidity is Hazardous!"
        payload["code"] = 1

    if currentTemperature > lowerBoundTemperature and currentTemperature < upperBoundTemperature:
        temperatureFine = True
    else : 
        payload["alert"] = "Temperature is Hazardous!"
        payload["code"] = 2
        

    if humdityFine and temperatureFine:
        payload["alert"] = "The Weather is Normal!"
        payload["code"] = 0


    conn = mysql.connector.connect(**Constants.connectionString)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO ENVIRONMENT(LandId,Humidity,Temperature,Brightness,CurrentTime) " +
        "VALUES (" + 
            str(Constants.LAND_ID) + "," +
            str(payload["humidity"]) + "," + 
            str(payload["temperature"]) + "," + 
            str(payload["brightness"]) + "," + 
            "\"" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\"" +
        ");" 
    )

    conn.commit()

    cursor.close()
    conn.close()
    

    url = "http://127.0.0.1:5000/api"

    requests.post(url,json=payload)

    return humdityFine and temperatureFine

