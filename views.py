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

mysql=MySQL(app)

cur = conn.cursor()
#giả lập##############

data=[{'id':1,'locate':"ai biet",'plant':"xoài",'temp':23,'lighttime':8,'humidity':2000}]
#####################

notification = {
    "temperature" :"None",
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