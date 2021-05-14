from datetime import datetime
from flask import render_template, request, redirect, url_for, jsonify, make_response
from flask_mysqldb import MySQL
from Greensys import app
import os
#import Process
import webbrowser
import json
import glob
mysql=MySQL(app)
userData = {'id':None,'name':None,'land':None,''}
@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')
@app.route('/login')
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM account WHERE username = '"+ username + "'")
        acc = cur.fetchone()
        if acc is None or acc['password'] != request.form['password']:
            error = 'Username hoặc mật khẩu không đúng'
        else:
            userData['id'] = acc['id']
            userData['name'] = acc['name']

            cur.execute("SELECT * FROM farm WHERE owner_id = "+ str(userData['id']))
            acc = cur.fetchone()
            if acc is not None:
                userData['id'] = acc['id']
                acc = None
    return render_template('logIn.html')
@app.route('/signup',methods=['GET','POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE username = '"+ username +"'")
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
    return render_template('plantdata.html')
@app.route('/envicondi')
def envicondi():
    return render_template('envicondi.html')
@app.route('/wateringhistory')
def wateringhistory():
    return render_template('wateringhistory.html')
