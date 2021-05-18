from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import views
import os

import App.Main as app

app = Flask(__name__, template_folder= "static")
app.config['MYSQL_HOST'] = 'sql6.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql6412254'
app.config['MYSQL_PASSWORD'] = 'qM4MyknmEg'
app.config['MYSQL_DB'] = 'sql6412254'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql=MySQL(app)

app.start()