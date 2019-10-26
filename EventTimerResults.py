import sqlite3
import time
import datetime
from dbHelper import DbHelper
from setup import Setup
from division import Division
from results import Results


def createresulttable ():
    db.setDatabaseFile(setup.databaseFile)
    db.connectToDatabase()
    db.createXCResultTable()
    db.closeDatabaseFile()


def calculateTimeOnCourse(self):
    return 60 / (self.startTime - self.finishTime)


# Global variables
epoch = datetime.datetime(1970,1,1,0,0,0)
file = "setup.json"
Connected = False

db = DbHelper()
setup = Setup(file)

# create the result table if needed
createresulttable()

div = Division()
alldivisions = div.getalldivisions(setup.databaseFile)

for division in alldivisions:
    div.setdivisionresults(division)
    print(f'\t{div.division} {div.optSpeed} {div.maxSpeed} {div.timeLimit} {div.distance}'
          f' {div.numOfFences} {div.numOfRiders} {div.optTimeSec} {div.minTimeSec}')

    divisionresults = db.getresultsfordivision(setup.databaseFile, div.division)

    for rider in divisionresults:
        result = Results()
        result.calculateresults(rider, div.optTimeSec, div.minTimeSec, div.timeLimit)
        print(f'\t{result.riderNum} {result.division} {result.startTime} {result.finishTime} {result.timeOnCourse}'
              f' {result.timeFaults} {result.speedFaults} {result.overTime} {result.totalFaults} {result.error}')
        # put results in database
