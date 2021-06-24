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

