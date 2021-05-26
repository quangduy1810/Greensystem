from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import views
import os
import mysql.connector
import sys

""" 
*   Initialize The Database. You can move this section
*   out of this file but remember to initialize database before
*   invoking call into the function of the file.
*   And remember the Constants file and mysql dependency as well.
"""

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",   #  
    user="root",    # Your Username
    password="nhoxso33",  # Your Password  
    database="greensystem", # Your Database Name
    auth_plugin='mysql_native_password'

)
print("success")
# Initialize common variable for every other py files to use

app = Flask(__name__, template_folder= "static")
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nhoxso33'
app.config['MYSQL_DB'] = 'greensystem'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql=MySQL(app)

