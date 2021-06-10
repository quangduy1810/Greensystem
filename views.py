from datetime import datetime
from flask import render_template, request, redirect, url_for, jsonify, make_response,session
from flask_mysqldb import MySQL
from Greensys import app,conn

import os
#import Process
import webbrowser
import json
import glob

mysql=MySQL(app)

cur = conn.cursor()
#giả lập##############

data=[{'id':1,'locate':"ai biet",'plant':"xoài",'temp':23,'lighttime':8,'humidity':2000}]
#####################

@app.route('/')
@app.route('/homepage')
def homepage():
    
    if 'UserData' in session:
        account=session['UserData']
    else:
        account=None
    return render_template(
        'homepage.html',
        notify=notify,
        account= account
        )

        
@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['name']
        print(request.form['name'])
        print(request.form['password'])
        cur.execute("SELECT * FROM PERSON WHERE Username = '"+ username + "'")
        acc = cur.fetchone()
        session['UserData']=acc
        if acc is None or acc[2] != request.form['password']:
            error = 'Username hoặc mật khẩu không đúng'
        else:
            
            return redirect(url_for('homepage'))
    print(error)
    return render_template('logIn.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        cur.execute("SELECT * FROM PERSON WHERE username = '"+ username +"'")
        acc = cur.fetchone()
        if acc is not None:
            error = 'Tài khoản đã tồn tại'
        else:
            
            password = request.form['password']
            email = request.form['email']
            phonenumber = request.form['phonenumber']
            address= request.form['address']
            cur.execute("INSERT INTO PERSON ( username, password, address) VALUES ('"+username+"','"+password+"','"+address+"')")
            cur.execute("SELECT * FROM PERSON WHERE id=(SELECT max(id) FROM PERSON);")
            data= cur.fetchone()
            session['UserData']=data
            mysql.connection.commit()
            return redirect(url_for('homepage'))
    return render_template('signUp.html')

@app.route('/plantdata')
def plantdata():
    cur.execute("SELECT * FROM LAND WHERE UserID = '"+ str(session['UserData'][0]) + "'")
    data=cur.fetchall()
    print (data)
    data2=[]
    for value in data:
        cur.execute("SELECT * FROM DEVICE_USED_IN_LAND WHERE LandID='"+ str(value[1])+"' ")
        data2.append(cur.fetchall())
    print (data2)
    return render_template('plantdata.html',data=data)

@app.route('/envicondi', methods=['GET'])
def envicondi():
    if request.method == 'GET':
        cur.execute("SELECT environment_log.id,LandName,measureValue,measureType,CurrentTime,UserID FROM environment_log,land WHERE USERID = '"+ str(session['UserData'][0]) +"' ")
        data=cur.fetchall()
        #data = [(),(),(),...]
        land = data[1][1]
        # print("Land:" + str(land))
        temperature = []
        humidity = []
        brightness = []
        current_time = []
        for value in data:
            #print(value)
            if str(value[3]) == 'Temperature':
                temperature.append(value[2])
            if str(value[3]) == 'Humidity':
                humidity.append(value[2])
            if str(value[3]) == 'Brightness':
                brightness.append(value[2])
            if str(value[4]) not in current_time:
                current_time.append(str(value[4]))
        
        # print("Temperature length: "+ str(len(temperature)))
        # print("Humidity length: "+ str(len(humidity)))
        # print("Brightness length: "+ str(len(brightness)))
        # print("Current_time length: "+ str(len(current_time)))

        # print("Temperature: "+ str(temperature))
        # print("Humidity: "+ str(humidity))
        # print("Brightness:"+ str(brightness))
        # print("CurrentTime"+ str(current_time))

        return render_template('envicondi.html',land=land, temperature=temperature, humidity=humidity, brightness=brightness,current_time=current_time)

def average_data(label,data,option):
    process_label = []
    process_data = []
    start = label[0]
    end = label[-1]
    index = 0
    if option == 'seconds':
        process_label = label
        process_data = data
    if option == 'minutes':
        while start <= end:
            
            next_minute = start
            if start.minute < 59:
                next_minute = start.replace(minute= start.minute + 1)
            elif start.hour < 23:
                next_minute = start.replace(hour= start.hour + 1, minute= 0)
            elif start.day < 31 and start.month in (1,3,5,7,8,10,12):
                next_minute = start.replace(day= start.day + 1, hour=0)
            elif start.day < 30 and start.month in (2,4,6,9,11):
                next_minute = start.replace(day= start.day +1, hour=0)
            elif start.month < 12:
                next_minute = start.replace(month= start.month + 1, day=1)
            else:
                next_minute = start.replace(year= start.year + 1, month=1)
            
            #print(next_minute)

            temp_data = []
            for i in range(0,len(label)):
                if label[i] >= start and label[i] <= next_minute:
                    temp_data.append(data[i])
            if temp_data != []:
                process_label.append(start)
                process_data.append(sum(temp_data) / len(temp_data))
            start = next_minute
            index += 1
    if option == 'hours':
        while start <= end:
            
            next_hour = start
            if start.hour < 23:
                next_hour = start.replace(hour= start.hour + 1, minute= 0)
            elif start.day < 31 and start.month in (1,3,5,7,8,10,12):
                next_hour = start.replace(day= start.day + 1, hour=0)
            elif start.day < 30 and start.month in (2,4,6,9,11):
                next_hour = start.replace(day= start.day +1, hour=0)
            elif start.month < 12:
                next_hour = start.replace(month= start.month + 1, day=1)
            else:
                next_hour = start.replace(year= start.year + 1, month=1)
            
            temp_data = []
            for i in range(index,len(label)):
                if label[i] >= start and label[i] <= end:
                    temp_data.append(data[i])
            if temp_data != []:
                process_label.append(start)
                process_data.append(sum(temp_data) / len(temp_data))
            start = next_hour
            index += 1    
    if option == 'days':
        while start <= end:

            next_day = start
            if start.day < 31 and start.month in (1,3,5,7,8,10,12):
                next_day = start.replace(day= start.day + 1, hour=0)
            elif start.day < 30 and start.month in (2,4,6,9,11):
                next_day = start.replace(day= start.day +1, hour=0)
            elif start.month < 12:
                next_day = start.replace(month= start.month + 1, day=1)
            else:
                next_day = start.replace(year= start.year + 1, month=1)
            
            temp_data = []
            for i in range(index,len(label)):
                if label[i] >= start and label[i] <= end:
                    temp_data.append(data[i])
            if temp_data != []:
                process_label.append(start)
                process_data.append(sum(temp_data) / len(temp_data))
            start = next_day
            index += 1    
    if option == 'months':
        while start <= end:
            next_month = start
            if start.month < 12:
                next_day = start.replace(month= start.month + 1, day=1)
            else:
                next_day = start.replace(year= start.year + 1, month=1)

            temp_data = []
            for i in range(index,len(label)):
                if label[i] >= start and label[i] <= end:
                    temp_data.append(data[i])
            if temp_data != []:
                process_label.append(start)
                process_data.append(sum(temp_data) / len(temp_data))
            start = next_month
            index += 1   
    if option == 'years':
        while start <= end:
            next_year = start.replace(year= start.year + 1)
            temp_data = []
            for i in range(index,len(label)):
                if label[i] >= start and label[i] <= end:
                    temp_data.append(data[i])
            if temp_data != []:
                process_label.append(start)
                process_data.append(sum(temp_data) / len(temp_data))
            start = next_year
            index += 1   
    return process_label,process_data

def process_data(label,data, start_time, end_time, option):
    #label is of datetime
    new_label = []
    new_data = []

    process_label = []
    process_data = []

    process_label,process_data = average_data(label,data,option)

    for i in range(0,len(process_label)):
        if start_time <= process_label[i] and end_time >= process_label[i]:
            new_label.append(process_label[i].strftime("%Y-%m-%d %H:%M"))
            new_data.append(process_data[i])        

    return new_label,new_data

@app.route('/envicondi2', methods=["POST"])
def envicondi2():
    #Data to be sent back
    temp_label = []
    temp_data = []

    humid_label = []
    humid_data = []

    brightness_label = []
    brightness_data = []

    #Get data from database
    cur.execute("SELECT environment_log.id,LandName,measureValue,measureType,CurrentTime,UserID FROM environment_log,land WHERE USERID = '"+ str(session['UserData'][0]) +"' ")
    data=cur.fetchall()
    #data = [(),(),(),...]
    temperature = [[],[]]
    humidity = [[],[]]
    brightness = [[],[]]
    for value in data:
        if str(value[3]) == 'Temperature':
            temperature[0].append(value[2])
            temperature[1].append(value[4])
        if str(value[3]) == 'Humidity':
            humidity[0].append(value[2])
            humidity[1].append(value[4])
        if str(value[3]) == 'Brightness':
            brightness[0].append(value[2])
            brightness[1].append(value[4])
    #
    #Testing purpose
    #print("temperature[[],[]] length :" + str(len(temperature[0])) + " , " + str(len(temperature[1])))

    #Process Temperature submit
    if (request.form.get('form_type') == 'Temperature' ):
        #They are all text data
        if (request.form.get('start_temp_date')):
            start_temp_date = request.form['start_temp_date']
            #print(start_temp_date)
            #print(type(start_temp_date))
            #Convert to datetime
            start_temp_date = datetime.strptime(start_temp_date, '%Y-%m-%d %H:%M')

        if (request.form.get('end_temp_date')):
            end_temp_date = request.form['end_temp_date']
            #Convert to datetime
            end_temp_date = datetime.strptime(end_temp_date, '%Y-%m-%d %H:%M')
        #Get Option data
        if (request.form.get('option_temp')):
            option_temp = request.form['option_temp']
        
        #Process data
        temp_label,temp_data = process_data(temperature[1],temperature[0],start_temp_date,end_temp_date,option_temp)
    
    #Process Humidity submit
    if (request.form.get('form_type') == 'Humidity'):
        if (request.form['start_humid_date']):
            start_humid_date = request.form['start_humid_date']
            #Convert to datetime
            start_humid_date = datetime.strptime(start_humid_date, '%Y-%m-%d %H:%M')
        if (request.form['end_humid_date']):
            end_humid_date = request.form['end_humid_date']
            #Convert to datetime
            end_humid_date = datetime.strptime(end_humid_date, '%Y-%m-%d %H:%M')
        if (request.form['option_humid']):
            option_humid = request.form['option_humid']
        
        #Process data
        humid_label,humid_data = process_data(humidity[1],humidity[0],start_humid_date,end_humid_date,option_humid)
    
    #Process Brightness submit
    if (request.form.get('form_type') == 'Brightness'):
        if (request.form['start_bright_date']):
            start_bright_date = request.form['start_bright_date']
            #Convert to datetime
            start_bright_date = datetime.strptime(start_bright_date, '%Y-%m-%d %H:%M')
        if (request.form['end_bright_date']):
            end_bright_date = request.form['end_bright_date']
            #Convert to datetime
            end_bright_date = datetime.strptime(end_bright_date, '%Y-%m-%d %H:%M')    
        if (request.form['option_bright']):
            option_bright = request.form['option_bright']

        #Process data
        brightness_label,brightness_data = process_data(brightness[1],brightness[0],start_bright_date,end_bright_date,option_bright)
    #return
    return jsonify({'temp_label': temp_label, 'temp_data': temp_data, 'humid_label': humid_label, 'humid_data': humid_data, 'brightness_label': brightness_label, 'brightness_data': brightness_data})


@app.route('/wateringhistory')
def wateringhistory():
    cur.execute(
        "SELECT LandName From LAND " + 
        "WHERE UserId=" + str(session["UserData"][0]) + ";"
        )

    lands = cur.fetchall()

    query = "SELECT Land.LandName, Device.Id, Device.DeviceType, State, RealTime " + \
            "FROM DEVICE_ACTED_IN_LAND JOIN LAND ON (Land.Id = device_acted_in_land.LandId) " + \
            "JOIN DEVICE ON (Device.Id = Device_acted_in_land.deviceId) " + \
            "WHERE Land.UserId = '" + str(session['UserData'][0]) + "'" 

    cur.execute(query)
    data=cur.fetchall()

    return render_template('wateringhistory.html',lands = lands ,data=data)


notification = {
    "temperature" : "None",
    "humidity": "None",
    "brightness": "None",
    "alert": "None",
    "date": "None",
}

@app.route('/api', methods=['GET','POST'])
def notify_api(): 
    notification["date"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    if request.method == 'POST':
        req = request.json

        print(req)

        notification["temperature"] = req["temperature"]
        notification["humidity"] = req['humidity']
        notification["brightness"] = req['brightness']
        notification["alert"] = req['alert']

        return jsonify(notification)
    else :
        return jsonify(notification)

@app.route('/getLandId', methods=['GET'])
def getLandId():
    if request.method == 'GET':
        # Gen cho land khác thì thay id ở đây
        return jsonify({'landId' : 1})



@app.route('/notify', methods=['GET'])
def notify():
    return render_template('notify.html')

#add function
@app.route('/logout')
def logout():
    session.pop('UserData', None)
    return redirect(url_for('homepage'))
@app.route('/delete<id><type>', methods=['GET'])
def delete(id,type):
    if type == 'l': #stand for land
        cur.execute("DELETE FROM LAND WHERE ID = '"+ str(id) + "' AND  UserID = '"+ str(session['UserData'][0]) + "'" );
        cur.execute("SELECT * FROM LAND WHERE UserID = '"+ str(session['UserData'][0]) + "'")
        data=cur.fetchall()
        return render_template('plantdata.html',data=data)
    else:
        return "this is" + type

@app.route('/edit<id><type>', methods=['GET','POST']) 
def edit(id,type):
    data=None
    if type=='f':
        cur.execute("SELECT * FROM LAND WHERE ID = '"+ str(id) + "'AND  UserID = '"+ str(session['UserData'][0]) + "'")
        data=cur.fetchone();
    if request.method == 'POST':
        location = request.form['location']
        ltemp=request.form['ltemp']
        utemp=request.form['utemp']
        lhumid= request.form['lhumidity']
        uhumid=request.form['uhumidity']
        lhtemp=request.form['lhtemp']
        uhtemp=request.form['uhtemp']
        lhhumid= request.form['lhhumidity']
        uhhumid=request.form['uhhumidity']
        if type == 'f': #fix
            cur.execute("UPDATE LAND SET landName= '" + location + 
            "',lowerTemperature='" + ltemp + 
            "',upperTemperature='" + utemp + 
            "',lowerHumidity='" + lhumid + 
            "',upperHumidity='" + uhumid + 
            "',lowerHazardousTemperature='" + lhtemp +
            "',upperHazardousTemperature='" + uhtemp + 
            "',lowerHazardousHumidity='" + lhhumid + 
            "',upperHazardousHumidity='" + uhhumid + 
                "'WHERE Id='" + str(id) +"'")
            
        else:
            cur.execute("INSERT INTO LAND (landName ,lowerTemperature,upperTemperature,lowerHumidity,upperHumidity,lowerHazardousTemperature,upperHazardousTemperature,lowerHazardousHumidity,upperHazardousHumidity) VALUES('" + location + "','" + ltemp + "','" + utemp + "','" + lhumid + "','" + uhumid + "','" + lhtemp +"','" + uhtemp + "','" + lhhumid + "','" + uhhumid +"')WHERE UserId='" + str(id) +"'")
        return redirect(url_for('plantdata'))
    return render_template('edit.html',data=data)
               