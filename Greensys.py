from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import views
import os
# import cx_Oracle
# cx_Oracle.init_oracle_client(lib_dir=r"D:\coder\oracle\instantclient_19_11")
# def querydb():
#     con = cx_Oracle.connect('username/password@x.x.x.x:1521/Servicename')    
#     pn = request.form['phonenumber']
#     cur = con.cursor()
#     sql = """select to_char(DTCREAT,'yyyy-mm-dd hh24:mi:ss') ..... and numero = :numero"""
#     cur.execute(sql, numero = pn)
#     title = [i[0] for i in cur.description]
#     print(title)
#     results = []
#     for result in cur.fetchall():
#          results.append(result)
#     return render_template('query.html', results= results)
mysql = MySQL()
app = Flask(__name__, template_folder= "static")

app.config['MYSQL_HOST'] = 'sql6.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql6412254'
app.config['MYSQL_PASSWORD'] = 'qM4MyknmEg'
app.config['MYSQL_DB'] = 'sql6412254'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql=MySQL(app)
