import sqlite3
import time
import datetime
from dbHelper import DbHelper
from setup import Setup
from division import Division
from results import Results

# Global variables
epoch = datetime.datetime(1970,1,1,0,0,0)
file = "setup.json"
Connected = False

setup = Setup(file)

# create the result table if needed
db = DbHelper()

db.setDatabaseFile(setup.databaseFile)
db.connectToDatabase()
db.createXCResultTable()
db.closeDatabaseFile()

div = Division()
alldivisions = div.getalldivisions(setup.databaseFile)

for division in alldivisions:
    div.setdivisionresults(division)
    res = Results()

    divisionresults = res.getresultsfordivision(setup.databaseFile, div.division)

    for result in divisionresults:
        res.calculateresults(result, div.optTime, div.minTime)


