from django.test import TestCase
from datetime import datetime, timedelta
#from .models import MetricValueRegistration

#for mysql
'''
import MySQLdb

db = MySQLdb.connect(host='63.250.59.170',    # your host, usually localhost
                     user="bob_marley",         # your username
                     passwd='322223af09',  # your password
                     db="new_service_catalog",
                     port=3306)        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM app1_metricvalue")

# print all the first cell of all the rows
for row in cur.fetchall():
    print(row)

db.close()

'''
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^66

#for microsoft sql server
'''
import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:myserver.database.windows.net' 
database = 'mydb' 
username = 'myusername' 
password = 'mypassword' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM app1_metricvalue")

# print all the first cell of all the rows
for row in cur.fetchall():
    print(row)

db.close()

'''

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#for oracle


'''
now = now.replace(day = 26)
date_begin = now - timedelta(days=now.weekday(), weeks=0)
date_begin = date_begin.replace(hour=0, minute=0, second=0, microsecond=0)
print(date_begin)
# Create your tests here.
'''
