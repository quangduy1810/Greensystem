from datetime import datetime
from flask import render_template, request, redirect, url_for, jsonify, make_response,session
from flask_mysqldb import MySQL
from Greensys import app,conn
from envirstate import *

import os
#import Process
import webbrowser
import json
import glob
import views
cur = conn.cursor()
@app.route('/')
@app.route('/homepage',methods=['GET','POST'])
def homepage():
    acclist=None
    adminaccount=None
    account=None
    account != None or adminaccount != None
    # if request.method=='POST':
    #     print(request.form['user'])
    #     cur.execute("SELECT * FROM PERSON WHERE username = '"+ request.form['user'] +"'")
    #     acc=cur.fetchone()
    #     session['UserData']=acc
    if 'UserData' in session:
        account=session['UserData']
        print(session['UserData'])
    if 'Admin' in session:
        adminaccount=session['Admin']
        cur.execute("SELECT Id,Username FROM PERSON WHERE role is Null")
        acclist=cur.fetchall()
        print(session['Admin'])
    return render_template(
        'homepage.html',
        account= account,
        adminaccount=adminaccount,
        acclist=acclist
        )

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        cur.execute("SELECT * FROM PERSON WHERE Username = '"+ username + "'")
        acc = cur.fetchone()
        if acc is None or acc[2] != request.form['password']:
            error = 'Username hoặc mật khẩu không đúng'
        else:
            if acc[6] is None:
                session['UserData']= acc
            else:
                session['Admin']=acc    
            return redirect(url_for('homepage'))
    print(error)
    return render_template('logIn.html',error=error)



@app.route('/manage',methods=['GET','POST'])
def manage():
    cur.execute("SELECT * FROM PERSON WHERE username = '"+ request.form['user'] +"'")
    acc=cur.fetchone()
    session['UserData']=acc
    return redirect(request.referrer)

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
            name= request.form['name']
            password = request.form['password']
            email = request.form['email']
            phonenumber = request.form['phonenumber']
            address= request.form['address']
            cur.execute("INSERT INTO PERSON ( username, password,name,address,phone) VALUES ('"+username+"','"+password+"','"+name+"','"+address+"','"+phonenumber+"')")
            conn.commit();
            cur.execute("SELECT * FROM PERSON WHERE id=(SELECT max(id) FROM PERSON);")
            data= cur.fetchone()
            session['UserData']=data
            
            return redirect(url_for('homepage'))
    return render_template('signUp.html',error=error)
@app.route('/plantdata')
def plantdata():
    cur.execute("SELECT * FROM LAND INNER JOIN plant on Land.PlantId=plant.id WHERE UserID = '"+ str(session['UserData'][0]) + "'")
    data=cur.fetchall()
    i=0
    device=[]
    for value in data:
        
        cur.execute("SELECT device.deviceType, device.Id, device_used_in_land.LandId FROM device INNER JOIN device_used_in_land ON device.ID = device_used_in_land.DeviceId where LandId='"+ str(value[0]) + "' ")
        device+=cur.fetchall()
        i+=1
    session['Plantdata']=data
    print(device)
    return render_template('plantdata.html',data=data,data2=device)


@app.route('/api', methods=['GET','POST'])
def notify_api(): 
    
    res =   "The temperature is : " + notification["temperature"] + "\n" + \
            "The humidity is : " + notification["humidity"]  + "\n" + \
            "The brightness is :  " +  notification["brightness"] + "\n" + \
            str(notification["alert"])

    notification["date"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    if request.method == 'POST':
        req = request.json

        notification["temperature"] = req["temperature"]
        notification["humidity"] = req['humidity']
        notification["brightness"] = req['brightness']
        notification["alert"] = req['alert']

        return jsonify(res)
    else :

        return jsonify(notification)


@app.route('/envicondi', methods=['GET','POST'])
def envicondi():
    if request.method == 'GET':
        cur.execute("SELECT LandName FROM LAND WHERE USERID = '"+ str(session['UserData'][0]) +"' ")
        data=cur.fetchall()
        landName= []
        land= None
        for value in data:
            landName.append(value[0])
        return render_template('envicondi.html',landName=landName, land=land)
    else:
        cur.execute("SELECT LandName FROM LAND WHERE USERID = '"+ str(session['UserData'][0]) +"' ")
        data=cur.fetchall()
        landName= []
        for value in data:
            landName.append(value[0])


        cur.execute("SELECT environment_log.id,LandName,measureValue,measureType,CurrentTime,UserID FROM environment_log,land WHERE USERID = '"+ str(session['UserData'][0]) +"' ")
        data=cur.fetchall()
        #data = [(),(),(),...]
        land = None
        if data:
            land = request.form.get('option_land')

        # print("Land:" + str(land))
        temperature_label = []
        temperature_data = []
        humidity_label = []
        humidity_data = []
        brightness_label = []
        brightness_data = []
        current_time = []
        for value in data:
            if value[1] == land:
                if str(value[3]) == 'Temperature':
                    temperature_data.append(value[2])
                    temperature_label.append(str(value[4]))
                if str(value[3]) == 'Humidity':
                    humidity_data.append(value[2])
                    humidity_label.append(str(value[4]))
                if str(value[3]) == 'Brightness':
                    brightness_data.append(value[2])
                    brightness_label.append(str(value[4]))
                if str(value[4]) not in current_time:
                    current_time.append(str(value[4]))
        
        # print("Temperature length: "+ str(len(temperature_data)))
        # print("Humidity length: "+ str(len(humidity_data)))
        # print("Brightness length: "+ str(len(brightness_data)))
        # print("Current_time length: "+ str(len(current_time)))

        # print("Temperature: "+ str(temperature_data))
        # print("Humidity: "+ str(humidity_data))
        # print("Brightness:"+ str(brightness_data))
        # print("CurrentTime"+ str(current_time))

        return render_template('envicondi.html', landName=landName,land=land, temperature_label=temperature_label , temperature_data=temperature_data, humidity_label=humidity_label , humidity_data=humidity_data, brightness_label=brightness_label , brightness_data=brightness_data, current_time=current_time)

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

    start_temp_date = None
    end_temp_date = None
    start_humid_date = None
    end_humid_date = None
    start_bright_date = None
    end_bright_date = None

    #Get data from database
    cur.execute("SELECT environment_log.id,LandName,measureValue,measureType,CurrentTime,UserID FROM environment_log,land WHERE USERID = '"+ str(session['UserData'][0]) +"' ")
    data=cur.fetchall()
    #data = [(),(),(),...]
    temperature_data = [[],[]]
    humidity_data = [[],[]]
    brightness_data = [[],[]]
    for value in data:
        if str(value[3]) == 'Temperature':
            temperature_data[0].append(value[2])
            temperature_data[1].append(value[4])
        if str(value[3]) == 'Humidity':
            humidity_data[0].append(value[2])
            humidity_data[1].append(value[4])
        if str(value[3]) == 'Brightness':
            brightness_data[0].append(value[2])
            brightness_data[1].append(value[4])
    #
    #Testing purpose
    #print("temperature_data[[],[]] length :" + str(len(temperature_data[0])) + " , " + str(len(temperature_data[1])))

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
        if ( (start_temp_date == None) and ( end_temp_date != None) ):
            temp_label,temp_data = process_data(temperature_data[1],temperature_data[0],temperature_data[1][0],end_temp_date,option_temp)
        elif ( (start_temp_date != None) and (end_temp_date == None) ):
            temp_label,temp_data = process_data(temperature_data[1],temperature_data[0],start_temp_date,temperature_data[1][-1],option_temp)
        elif ( (start_temp_date == None) and (end_temp_date == None) ):
            temp_label,temp_data = process_data(temperature_data[1],temperature_data[0],temperature_data[1][0],temperature_data[1][-1],option_temp)
        else:
            temp_label,temp_data = process_data(temperature_data[1],temperature_data[0],start_temp_date,end_temp_date,option_temp)

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
        if ( (start_humid_date == None ) and ( end_humid_date != None) ):
            humid_label,humid_data = process_data(humidity_data[1],humidity_data[0],humidity_data[1][0],end_humid_date,option_humid)
        elif ( (start_humid_date != None) and (end_humid_date == None) ):
            humid_label,humid_data = process_data(humidity_data[1],humidity_data[0],start_humid_date,humidity_data[1][-1],option_humid)
        elif ( (start_humid_date == None) and (end_humid_date == None) ):
            humid_label,humid_data = process_data(humidity_data[1],humidity_data[0],humidity_data[1][0],humidity_data[1][-1],option_humid)
        else:
            humid_label,humid_data = process_data(humidity_data[1],humidity_data[0],start_humid_date,end_humid_date,option_humid)

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

        if ( (start_bright_date == None) and (end_bright_date != None) ):
            brightness_label,brightness_data = process_data(brightness_data[1],brightness_data[0],brightness_data[1][0],end_bright_date,option_bright)
        elif ( (start_bright_date != None) and (end_bright_date == None) ):
            brightness_label,brightness_data = process_data(brightness_data[1],brightness_data[0],start_bright_date,brightness_data[1][-1],option_bright)
        elif ( (start_bright_date == None) and (end_bright_date == None) ):
            brightness_label,brightness_data = process_data(brightness_data[1],brightness_data[0],brightness_data[1][0],brightness_data[1][-1],option_bright)
        else:
            brightness_label,brightness_data = process_data(brightness_data[1],brightness_data[0],start_bright_date,end_bright_date,option_bright)
        


        #return
    return jsonify({'temp_label': temp_label, 'temp_data': temp_data, 'humid_label': humid_label, 'humid_data': humid_data, 'brightness_label': brightness_label, 'brightness_data': brightness_data})





@app.route('/wateringhistory')
def wateringhistory():
    cur.execute("SELECT * FROM LAND WHERE UserID = '"+ str(session['UserData'][0]) + "'")
    data=cur.fetchall()
    return render_template('wateringhistory.html',data=data)

@app.route('/deletedevice<id>', methods=['GET'])
def deletedevice(id):
    cur.execute("DELETE FROM DEVICE WHERE Id = '"+ str(id) + "' AND  UserID = '"+ str(session['UserData'][0]) + "'" );
    conn.commit()

    #Log
    insert_log = (
        "INSERT INTO user_log (UserId, LandId, LogType, Descript, CurrentTime)"
        "VALUES (%s, %s, %s, %s, %s)"
    )
    data_log = (int(session['UserData'][0]) , -1 , 'Delete Device to User', 'Device id: ' + str(id), datetime.now())
    cur.execute(insert_log, data_log)     
    #

    return redirect(request.referrer)

@app.route('/adddevice<dv_id><deviceType>',methods=['GET'])
def adddevice(dv_id,deviceType):
    cur.execute("INSERT INTO device (Id, deviceType,UserId) VALUES ('"+ dv_id + ",'"+ deviceType +"',"+ str(session['UserData'][0]) +" ') ")
    conn.commit()

    #Log
    insert_log = (
        "INSERT INTO user_log (UserId, LandId, LogType, Descript, CurrentTime)"
        "VALUES (%s, %s, %s, %s, %s)"
    )
    data_log = (int(session['UserData'][0]) , -1 , 'Add Device to User', 'Device id: ' + str(dv_id) + ' deviceType: ' + str(deviceType), datetime.now())
    cur.execute(insert_log, data_log) 
    #

    return redirect(request.referrer)


@app.route('/planthistory')
def devicedata():
    cur.execute("SELECT plant_history.PlantId,plant_history.LandId, plantName ,StartTime,EndTime,Comment FROM (plant_history join plant on PlantId = plant.Id) join LAND on plant_history.LandId = land.Id where UserId ="+ str(session['UserData'][0]))
    data=cur.fetchall()

    return render_template('planthistory.html',data=data)


@app.route('/devicehistory')
def devicehistory():
    cur.execute("SELECT Id,LandId,deviceType,start_time,end_time FROM device_used_in_land join device on device_used_in_land.DeviceId = device.Id where UserId = '"+ str(session['UserData'][0]) + "'")
    data=cur.fetchall()

    return render_template('devicehistory.html',data=data)






#add function
@app.route('/logout')
def logout():
    if 'Admin' in session:
        session.pop('Admin', None)
    if 'UserData' in session:
        session.pop('UserData', None)
    return redirect(url_for('homepage'))
@app.route('/delete<id><type>', methods=['GET'])
def delete(id,type):
    if type == 'l': #stand for land

        #Log
        insert_log = (
            "INSERT INTO user_log (UserId, LandId, LogType, Descript, CurrentTime)"
            "VALUES (%s, %s, %s, %s, %s)"
        )
        data_log = (int(session['UserData'][0]) , int(id) , 'Delete Land', 'Land id: ' + str(type), datetime.now())
        cur.execute(insert_log, data_log)
        #

        cur.execute("DELETE FROM LAND WHERE ID = '"+ str(id) + "' AND  UserID = '"+ str(session['UserData'][0]) + "'" );
        conn.commit()
        
    else:

        #Log
        insert_log = (
            "INSERT INTO user_log (UserId, LandId, LogType, Descript, CurrentTime)"
            "VALUES (%s, %s, %s, %s, %s)"
        )
        data_log = (int(session['UserData'][0]) , int(id) , 'Delete Device from Land', 'Device id: ' + str(id) + ' Land id: ' + str(type), datetime.now())
        cur.execute(insert_log, data_log)
        #

        cur.execute("DELETE FROM device_used_in_land WHERE deviceid='"+ id +"' and landid='" + type +"'")
        conn.commit()
    return redirect(request.referrer)
@app.route('/add<dv_id><l_id>',methods=['GET'])
def add(dv_id,l_id):
    cur.execute("INSERT INTO device_used_in_land (DeviceId, LandId) VALUES ('"+ dv_id +"','" + l_id +"') ")
    conn.commit()

    #Log
    insert_log = (
        "INSERT INTO user_log (UserId, LandId, LogType, Descript, CurrentTime)"
        "VALUES (%s, %s, %s, %s, %s)"
    )
    data_log = (int(session['UserData'][0]) , int(l_id) , 'Add Device to Land', 'Device id: ' + str(dv_id) + ' Land id: ' + str(l_id), datetime.now())
    cur.execute(insert_log, data_log)
    #

    return redirect(request.referrer)
@app.route('/edit<id><type>', methods=['GET','POST']) 
def edit(id,type):
    
    data=None
    data2=None
    data3=None
    data4=None
    title="Thêm"
    data5=None
    if type=='f': #fix
        title="Chỉnh sửa"
        for value in session['Plantdata']:
            if value[0]== int(id):
                data=value

        cur.execute("SELECT device.Id, device.deviceType FROM person right join device On device.userid = person.id left join device_used_in_land on device_used_in_land.deviceid = Device.id and device_used_in_land.LandId='"+ id +"' where person.Id ='"+ str(session['UserData'][0]) +"' and device_used_in_land.DeviceId is Null")
        data2=cur.fetchall()
        
        cur.execute("SELECT  device.Id,device.deviceType FROM device INNER JOIN device_used_in_land ON device.ID = device_used_in_land.DeviceId WHERE device_used_in_land.LandId='"+ id + "'")
        data3=cur.fetchall()
        
        cur.execute("SELECT * FROM Plant where id='"+ str(data[3]) +"'")
        data5=cur.fetchone()
        #cur.execute("SELECT deviceid FROM ")
    if request.method == 'POST' and type=="f":
            location = request.form['location']
            plant=request.form['plant']
            ltemp=request.form['ltemp']
            utemp=request.form['utemp']
            lhumid= request.form['lhumidity']
            uhumid=request.form['uhumidity']
            lhtemp=request.form['lhtemp']
            uhtemp=request.form['uhtemp']
            lhhumid= request.form['lhhumidity']
            uhhumid=request.form['uhhumidity']
            if plant is not None:
                cur.execute("SELECT * FROM PLANT WHERE PlantName = '"+ plant + "'")
                data2= cur.fetchone()
            if data2 is None:
                    cur.execute("INSERT INTO PLANT (PlantName, lowerTemperature,upperTemperature,lowerHumidity,upperHumidity,lowerHazardousTemperature,upperHazardousTemperature,lowerHazardousHumidity,upperHazardousHumidity) VALUES ('"+plant+"','" + ltemp + "','" + utemp + "','" + lhumid + "','" + uhumid + "','" + lhtemp +"','" + uhtemp + "','" + lhhumid + "','" + uhhumid +"')")
                    conn.commit()
                    cur.execute("SELECT * FROM PLANT WHERE PlantName = '"+ plant + "'")
                    data2= cur.fetchone()
        
            cur.execute("UPDATE LAND SET landName= '" + location +
            "',plantid='" + str(data[3]) + 
            "',lowerTemperature='" + ltemp + 
            "',upperTemperature='" + utemp + 
            "',lowerHumidity='" + lhumid + 
            "',upperHumidity='" + uhumid + 
            "',lowerHazardousTemperature='" + lhtemp +
            "',upperHazardousTemperature='" + uhtemp + 
            "',lowerHazardousHumidity='" + lhhumid + 
            "',upperHazardousHumidity='" + uhhumid + 
                "'WHERE Id='" + str(id) +"'")
            conn.commit()

            #Log
            insert_log = (
            "INSERT INTO user_log (UserId, LandId, LogType, Descript, CurrentTime)"
            "VALUES (%s, %s, %s, %s, %s)"
            )
            data_log = (int(session['UserData'][0]) , int(id) , 'Update Land', 'plantid=' + str(data[3]) + ' lowerTemperature='+ltemp +' upperTemperature'+utemp +
            ' lowerHumidity='+lhumid +' upperHumidity='+uhumid +' lowerHazardousTemperature='+lhtemp +' upperHazardousTemperature='+uhtemp + ' lowerHazardousHumidity='+lhhumid +
            ' upperHazardousHumidity='+uhhumid, datetime.now())
            cur.execute(insert_log, data_log)
            #

            return redirect(url_for('plantdata'))        
    elif request.method == 'POST' :
            location = request.form['location']
            plant=request.form['plant']
            cur.execute("SELECT * FROM Plant where plantname='"+ plant +"'")
            plant=cur.fetchone()
            print(plant)
            cur.execute("INSERT INTO LAND (UserId,landName,PlantID, lowerTemperature,upperTemperature,lowerHumidity,upperHumidity,lowerHazardousTemperature,upperHazardousTemperature,lowerHazardousHumidity,upperHazardousHumidity) VALUES('" + str(session['UserData'][0]) + "','"  + location + "','"+ str(plant[0]) +"','" + str(plant[2]) + "','" + str(plant[3]) + "','" + str(plant[4]) + "','" + str(plant[5]) + "','" + str(plant[6]) +"','" + str(plant[7]) + "','" + str(plant[8])+ "','" + str(plant[9]) +"') ")
            
            #Log
            insert_log = (
            "INSERT INTO user_log (UserId, LandId, LogType, Descript, CurrentTime)"
            "VALUES (%s, %s, %s, %s, %s)"
            )
            data_log = (int(session['UserData'][0]) , int(id) , 'Add new Land', 'Location: '+location, datetime.now())
            cur.execute(insert_log, data_log)            
            #
            
            conn.commit()        
            return redirect(url_for('plantdata'))
    if data3 is None:
        cur.execute("SELECT Id,DeviceType FROM DEVICE WHERE UserID='"+ str(session['UserData'][0]) +"' ")
        data2=cur.fetchall()
    cur.execute("SELECT id,plantname from plant")
    data4 =cur.fetchall()
    
    
    return render_template('edit.html',data=data,data2=data2,data3=data3,data4=data4,data5=data5,title=title)
      
@app.route('/userhistory')
def userhistory():
    cur.execute("SELECT * FROM USER_LOG WHERE UserID = '"+ str(session['UserData'][0]) + "'")
    data=cur.fetchall()
    return render_template('userhistory.html',data=data)