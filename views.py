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
            name = request.form['name']
            password = request.form['password']
            email = request.form['email']
            phonenumber = request.form['phonenumber']
            address= request.form['address']
            cur.execute("INSERT INTO account (id, name, username, password, email) VALUES ('AUTO_INCREMENT PRIMARY KEY','"+name+"','"+username+"','"+password+"','"+email+"')")
            mysql.connection.commit()
            return redirect(url_for('/homepage'))
    return render_template('signUp.html')
@app.route('/plantdata')
def plantdata():
    cur.execute("SELECT * FROM LAND WHERE UserID = '"+ str(session['UserData'][0]) + "'")
    data=cur.fetchall()
    print (data);
    data2=[]
    for value in data:
        cur.execute("SELECT * FROM DEVICE_USED_IN_LAND WHERE LandID='"+ str(value[1])+"' ")
        data2.append(cur.fetchall())
    print (data2);
    return render_template('plantdata.html',data=data)
@app.route('/envicondi')
def envicondi():
    cur.execute("SELECT * FROM LAND WHERE UserID = '"+ str(session['UserData'][0]) + "'")
    data=cur.fetchall()
    return render_template('envicondi.html',data=data)
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
@app.route('/edit<data>', methods=['GET']) 
def edit(data):
    if session['UserData']== data:
        return render_template('plantdata.html',data=data)
    else:
        cur.execute("DELETE FROM LAND WHERE UserID = '"+ str(session['UserData'][0]) + "'");
        cur.execute("UPDATE Land SET " +  
            "lowerTemperature=" + str(data[4]) + "," +
            "upperTemperature=" + str(data[5]) + "," +
            "lowerHumidity=" + str(data[6]) + "," +
            "upperHumidity=" + str(data[7]) + "," +
            "WHERE Id=" + str() +"")           