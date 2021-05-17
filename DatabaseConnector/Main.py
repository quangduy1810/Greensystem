import sys
import mysql.connector

import Constants

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
    password="enlk8.",  # Your Password  
    database="GreenSystem", # Your Database Name
    auth_plugin='mysql_native_password' 
)

# Initialize common variable for every other py files to use
Constants.db_cursor = conn.cursor()

Constants.db_cursor.execute("SELECT * FROM Land;")

res = Constants.db_cursor.fetchall()

print(res)