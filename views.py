from datetime import datetime
from flask import render_template, request, redirect, url_for, jsonify, make_response,session
from flask_mysqldb import MySQL
from Greensys import app,conn
import os, sys
from Adafruit_IO import Client
#import Process
import webbrowser
import json
import glob
import constants
import time
import threading
mysql=MySQL(app)

cur = conn.cursor()
#giả lập##############

data=[{'id':1,'locate':"ai biet",'plant':"xoài",'temp':23,'lighttime':8,'humidity':2000}]
#####################

environment_condition = {
    "temperature" : -1,
    "humidity":  -1,
    "brightness": -1,
    "alert": "The Weather is Okay",
    "date": -1,
    "alertCode" : 0
     }

    
@app.route('/wateringhistory')
def wateringhistory():
    cur.execute(
        "SELECT LandName From LAND " + 
        "WHERE UserId=" + str(session["UserData"][0]) + ";")

    lands = cur.fetchall()

    query = "SELECT Land.LandName, Device.Id, Device.DeviceType, Data, RealTime " + \
            "FROM DEVICE_ACTED_IN_LAND JOIN LAND ON (Land.Id = device_acted_in_land.LandId) " + \
            "JOIN DEVICE ON (Device.Id = Device_acted_in_land.deviceId) " + \
            "WHERE Land.UserId = '" + str(session['UserData'][0]) + "'" + " ORDER BY RealTime DESC;"

    cur.execute(query)
    data=cur.fetchall()

    return render_template('wateringhistory.html',lands = lands ,data=data)

@app.route('/receiver', methods=['GET','POST'])
def environment_condition_process(): 
    environment_condition["date"] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    if request.method == 'POST':
        request_content = request.json

        print(request_content)

        cur.execute("INSERT INTO ENVIRONMENT_LOG(LandId,MeasureValue,MeasureType,CurrentTime) VALUE " +
            "(" + str(constants.LAND_ID) + "," + str(request_content["value"]) + "," + 
            "\"" +str(request_content["type"]) + "\"" + "," + "\""  + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\"" + ")")

        cur.execute("INSERT INTO DEVICE_ACTED_IN_LAND(DeviceId, LandId, RealTime, Data) VALUE " + "(" +
                str(request_content["device-id"]) + "," + str(constants.LAND_ID) + "," + 
                "\""+ datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\"" + "," + str(request_content["value"]) + ");")

        conn.commit()

        print(request_content)

        if request_content["type"] == "temperature":
            environment_condition["temperature"] = int(request_content["value"])
        if request_content["type"] == "brightness":
            environment_condition["brightness"] = int(request_content["value"])
        if request_content["type"] == "humidity":
            environment_condition["humidity"] = int(request_content["value"])
        

        if check_environment() and constants.mode["auto-watering"] == "on":
            print("Dispatched a task for processing action")
            task = threading.Thread(target=process_action,args=())
            task.start()
            print("Finished task. Bye bye.")
            task.join()

        return jsonify(environment_condition)
    return jsonify(environment_condition)


@app.route('/api',methods=['GET'])
def notify_api():
    environment_condition["date"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    if request.method == 'GET':
        return jsonify(environment_condition)

def check_environment():
    import constants as const
    cur.execute(
        "SELECT lowerHazardousTemperature, upperHazardousTemperature, lowerHazardousHumidity, upperHazardousHumidity " + \
        "FROM LAND WHERE Id=" + str(const.LAND_ID)             )   
    
    data = cur.fetchall()[0]; humidity_good = True; temperature_good = True

    print(data)

    if int(environment_condition["temperature"]) < int(data[0]) or int(environment_condition["temperature"]) > int(data[1]): 
        environment_condition["alert"] = "Weather is Hazardous"; temperature_good = False
    if int(environment_condition["humidity"]) < int(data[2]) or int(environment_condition["humidity"]) > int(data[3]):
        environment_condition["alert"] = "Weather is Hazardous"; humidity_good = False

    if humidity_good and temperature_good:
        environment_condition["alert"] = "The condition is normal."
        environment_condition["alertCode"] = 0
    else :
        environment_condition["alertCode"] = 1

    return humidity_good and temperature_good

def process_action():
    import constants as const
    import utils 

    cur.execute(
        "SELECT lowerTemperature, upperTemperature, lowerHumidity, upperHumidity " +\
        "cooldown, duration_case_one, duration_case_two, duration_case_three, "+ 
        "duration_case_five, duration_case_six, duration_case_seven, duration_case_eight, duration_case_nine "+
        "FROM LAND WHERE Id=" + str(const.LAND_ID))

    data = cur.fetchall()[0]

    durations = data[-9::] 

    cooldown_time = data[4]

    client = Client(const.ADAFRUIT_IO_USERNAME, const.ADAFRUIT_IO_KEY)

    if float(time.time()) - float(const.LAST_WATERING_TIMESTAMP)  >= cooldown_time:
        if environment_condition["temperature"] < data[0] and environment_condition["humidity"] > data[3]:
            send_water_action(client,durations[0]) # thirty second
        elif environment_condition["temperature"] < data[0] and environment_condition["humidity"] < data[2]:
            send_water_action(client,durations[1])
        elif environment_condition["temperature"] > data[1] and environment_condition["humidity"] > data[3]:
            send_water_action(client,durations[2])
        elif environment_condition["temperature"] > data[1] and environment_condition["humidity"] < data[2]:
            send_water_action(client,durations[3])
        elif environment_condition["temperature"] > data[1]:
            send_water_action(client,durations[4])
        elif environment_condition["temperature"] < data[0]:
            send_water_action(client, durations[5])
        elif environment_condition["humidity"] > data[3]:
            send_water_action(client, durations[6])
        elif environment_condition["humidity"] > data[2]:
            send_water_action(client, durations[7])
        else :
            send_water_action(client, durations[8])


    print("Cool down time is " + str(cooldown_time))

    if environment_condition["brightness"] > 100 :
        send_light_action(client, 1)
    if environment_condition["brightness"] < 100:
        send_light_action(client, 0)

def send_water_action(client,duration):
    import constants as const
    import utils
    print("Watering Tree In " + str(duration) + "seconds")

    const.LAST_WATERING_TIMESTAMP = time.time()

    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    client.send(const.PUMP_RELAY_FEED_ID, utils.PumpAction(const.PUMP_DEVICE_ID, 1, "").serialize())    
    time.sleep(duration)
    client.send(const.PUMP_RELAY_FEED_ID, utils.PumpAction(const.PUMP_DEVICE_ID, 0, "").serialize())
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cur.execute("INSERT INTO DEVICE_ACTED_IN_LAND(DeviceId, LandId, RealTime, Data) "  
        + "VALUES (" + str(const.PUMP_DEVICE_ID) + "," + str(const.LAND_ID) + "," + 
          "\"" +  str(start_time) + "\"" "," + str(1) + ")" + ";")

    # conn.commit()

    cur.execute("INSERT INTO DEVICE_ACTED_IN_LAND(DeviceId, LandId, RealTime, Data) "  
        + "VALUES (" + str(const.PUMP_DEVICE_ID) + "," + str(const.LAND_ID) + "," + 
           "\"" +  str(end_time) + "\"" + "," + str(0) + ")"  ";")
        
    conn.commit()

def toggle_pump_switch(client, status):
    import constants as const
    import utils

    if const.mode["pump"] == "on" and status == 1:
        print("the pump is already on.")
        return
    if const.mode["pump"] == "off" and status == 0:
        print("the pump is already off")
        return

    print("Turn the pump " + ("on" if status == 1 else "off"))
    client.send(const.PUMP_RELAY_FEED_ID, utils.PumpAction(const.PUMP_DEVICE_ID, status, "").serialize())

    cur.execute("INSERT INTO DEVICE_ACTED_IN_LAND(DeviceId, LandId, RealTime, Data) "  
        + "VALUES (" + str(const.PUMP_DEVICE_ID) + "," + str(const.LAND_ID) + "," + 
        "\"" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\"" + "," + str(status) +")" + ";" )

    conn.commit()

    const.mode["pump"] = "on" if status == 1 else "off"


def send_light_action(client,status):
    import constants as const
    import utils

    if const.mode["light"] == "on" and status == 1:
        print("the light is already on.")
        return
    if const.mode["light"] == "off" and status == 0:
        print("the light is already off")
        return


    print("Turn the light " + str(status))
    client.send(const.LIGHT_RELAY_FEED_ID, utils.LightAction(const.LIGHT_DEVICE_ID, status, "").serialize())

    cur.execute("INSERT INTO DEVICE_ACTED_IN_LAND(DeviceId, LandId, RealTime, Data) "  
        + "VALUES (" + str(const.LIGHT_DEVICE_ID) + "," + str(const.LAND_ID) + "," + 
        "\"" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\"" + "," + str(status) + ")" + ";" )

    conn.commit()

    const.mode["light"] = "on" if status == 1 else "off"

@app.route('/switch', methods=['POST'])
def switcher():
    import constants as const

    if request.method == 'POST':
        req = request.json

        if req["mode"] == "auto-watering":
            if int(req["data"]) == 1:  
                print("Turn on auto-watering")
                const.mode["auto-watering"] = "on" 
            elif int(req["data"]) == 0:
                print("Turn off auto-watering")
                const.mode["auto-watering"] = "off"
        else :
            client = Client(const.ADAFRUIT_IO_USERNAME, const.ADAFRUIT_IO_KEY)
            if req["mode"] == "pump":
                toggle_pump_switch(client, int(req["data"]))
            if req["mode"] == "light":
                send_light_action(client, int(req["data"]))

        return jsonify(const.mode)


@app.route('/notify', methods=['GET'])
def notify():
    return render_template('notify.html')