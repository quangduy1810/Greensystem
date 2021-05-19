import Constants
import mysql.connector
from utils import *

def CustomEnvironmentUpdate(landId,tempRange,humidRange,hazTempRange, hazHumidRange):
    
    conn = mysql.connector.connect(**Constants.connectionString)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Land WHERE Id=" + str(landId)
        )

    res = cursor.fetchall()

    if len(res) == 0:
        print("There is no such Land that equals to the given landId")

    try:
        cursor.execute(
            "UPDATE Land SET " +  
            "lowerTemperature=" + str(tempRange[0]) + "," +
            "upperTemperature=" + str(tempRange[1]) + "," +
            "lowerHumidity=" + str(humidRange[0]) + "," +
            "upperHumidity=" + str(humidRange[1]) + "," +
            "lowerHazardousTemperature=" + str(hazTempRange[0]) + "," +
            "upperHazardousTemperature=" + str(hazTempRange[1]) + "," +
            "lowerHazardousHumidity=" + str(hazHumidRange[0]) + "," +
            "upperHazardousHumidity=" + str(hazHumidRange[1]) + " " +
            "WHERE Id=" + str(landId) +";"
        )
    except:
        raise "An exception associated with the database has occured."


    cursor.execute(
        "SELECT * FROM Land WHERE Id=" + str(landId)
        )
    
    print(cursor.fetchall())
    cursor.close()
    conn.close()



CustomEnvironmentUpdate(1, (20, 50), (40,80), (10, 60), (20,90))