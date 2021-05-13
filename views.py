from datetime import datetime
from flask import render_template, request, jsonify
from Greensys import app
import os
#import Process
import webbrowser
import json
import glob
@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')
@app.route('/login')
def login():
    return render_template('logIn.html')
@app.route('/signup')
def signup():
    return render_template('signUp.html')
@app.route('/plantdata.html')
def plantdata():
    return render_template('plantdata.html')
@app.route('/envicondi')
def envicondi():
    return render_template('envicondi.html')
@app.route('/wateringhistory')
def wateringhistory():
    return render_template('wateringhistory.html')
