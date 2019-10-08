import sqlite3
import time
import datetime
from dbHelper import DbHelper
from setup import Setup

# Global variables
epoch = datetime.datetime(1970,1,1,0,0,0)
file = "setup.json"
Connected = False

setup = Setup(file)

# setup and open the database
db = DbHelper()

db.setDatabaseFile(setup.databaseFile)
db.openDatabaseFile()
db.connectToDatabase()
db.createXCResultTable()


db.closeDatabaseFile()
