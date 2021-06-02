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

@app.route('/envicondi')
def envicondi():
    cur.execute("SELECT environment.id,LandName,Temperature,Humidity,Brightness,CurrentTime,UserID FROM environment,land WHERE USERID = '"+ str(session['UserData'][0]) +"' ")
    data=cur.fetchall()
    #data = [(),(),(),...]
    land = data[1][1]
    print("Land:" + str(land))
    temperature = []
    humidity = []
    brightness = []
    current_time = []
    for value in data:
        temperature.append(value[2])
        humidity.append(value[3])
        brightness.append(value[4])
        current_time.append(str(value[5]))
    
    print("Temperature: "+ str(temperature))
    print("Humidity: "+ str(humidity))
    print("Brightness:"+ str(brightness))
    print("CurrentTime"+ str(current_time))

    return render_template('envicondi.html',land=land, temperature=temperature, humidity=humidity, brightness=brightness,current_time=current_time)
@app.route('/wateringhistory')
def wateringhistory():
    cur.execute("SELECT * FROM LAND WHERE UserID = '"+ str(session['UserData'][0]) + "'")
    data=cur.fetchall()
    return render_template('wateringhistory.html',data=data)


notification = {
    "temperature" : "None",
    "humidity": "None",
    "brightness": "None",
    "alert": "None",
    "date": "None",
}

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
               