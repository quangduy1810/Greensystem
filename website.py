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
@app.route('/envicondi')
def envicondi():
    data= {
        "temperature" : getTemperature().value,
        "humidity": getHumidity().value,
        "brightness": getBrightness().value
    }
    cur.execute("SELECT * FROM LAND WHERE UserID = '"+ str(session['UserData'][0]) + "'")
    data2=cur.fetchall()
    return render_template('envicondi.html',data=data,data2=data2)
@app.route('/wateringhistory')
def wateringhistory():
    cur.execute("SELECT * FROM LAND WHERE UserID = '"+ str(session['UserData'][0]) + "'")
    data=cur.fetchall()
    return render_template('wateringhistory.html',data=data)





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
        cur.execute("DELETE FROM LAND WHERE ID = '"+ str(id) + "' AND  UserID = '"+ str(session['UserData'][0]) + "'" );
        conn.commit()
        
    else:
        cur.execute("DELETE FROM device_used_in_land WHERE deviceid='"+ id +"' and landid='" + type +"'")
        conn.commit()
    return redirect(request.referrer)
@app.route('/add<dv_id><l_id>',methods=['GET'])
def add(dv_id,l_id):
    cur.execute("INSERT INTO device_used_in_land (DeviceId, LandId) VALUES ('"+ dv_id +"','" + l_id +"') ")
    conn.commit()
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
            return redirect(url_for('plantdata'))        
    elif request.method == 'POST' :
            location = request.form['location']
            plant=request.form['plant']
            cur.execute("SELECT * FROM Plant where plantname='"+ plant +"'")
            plant=cur.fetchone()
            print(plant)
            cur.execute("INSERT INTO LAND (UserId,landName,PlantID, lowerTemperature,upperTemperature,lowerHumidity,upperHumidity,lowerHazardousTemperature,upperHazardousTemperature,lowerHazardousHumidity,upperHazardousHumidity) VALUES('" + str(session['UserData'][0]) + "','"  + location + "','"+ str(plant[0]) +"','" + str(plant[2]) + "','" + str(plant[3]) + "','" + str(plant[4]) + "','" + str(plant[5]) + "','" + str(plant[6]) +"','" + str(plant[7]) + "','" + str(plant[8])+ "','" + str(plant[9]) +"') ")
            conn.commit()        
            return redirect(url_for('plantdata'))
    if data3 is None:
        cur.execute("SELECT Id,DeviceType FROM DEVICE WHERE UserID='"+ str(session['UserData'][0]) +"' ")
        data2=cur.fetchall()
    cur.execute("SELECT id,plantname from plant")
    data4 =cur.fetchall()
    
    return render_template('edit.html',data=data,data2=data2,data3=data3,data4=data4,data5=data5,title=title)
      