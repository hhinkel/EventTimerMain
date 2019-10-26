import sqlite3
from rider import Rider
from dbHelper import DbHelper
from setup import Setup

class Results:
    # 0.4 faults per second over optimum time or under speed fault time
    faultValue = 0.4

    def calculateresults(self, riderdata, opttime, mintime, timelimit):
        rider = Rider()
        rider.setriderdata(riderdata)

        self.riderNum = rider.number
        self.division = rider.division
        # format the start and finish times here?
        self.startTime = rider.startTime
        self.finishTime = rider.finishTime
        self.timeOnCourse = self.calculateTimeOnCourse()
        self.timeFaults = self.calculatetimefaults(opttime)
        self.speedFaults = self.calculatespeedfaults(mintime)
        self.overTime = self.determineifovertime(timelimit)
        self.totalFaults = self.determinefaults()
        self.error = self.determineiferror()
        return rider

    def calculateTimeOnCourse(self):
        if self.finishTime is 0:
            return None
        elif self.startTime - self.finishTime > 0:
            return 60 / (self.startTime - self.finishTime)
        else:
            return 0

    def calculatetimefaults(self, opttime):
        if self.timeOnCourse is None:
            return None
        elif self.timeOnCourse < opttime:
            return 0
        else:
            return (self.timeOnCourse - opttime) * self.faultValue

    def calculatespeedfaults(self, minTime=None):
        if self.timeOnCourse is None:
            return None
        elif minTime is None:
            return 0
        elif self.timeOnCourse > minTime:
            return 0
        else:
            return (minTime - self.timeOnCourse) * self.faultValue

    def determineifovertime(self, timelimit):
        if self.timeOnCourse is None:
            return 1
        elif self.timeOnCourse > timelimit:
            return 1
        else:
            return 0

    def determinefaults(self):
        if self.timeFaults is None and self.speedFaults is None:
            return None
        elif self.timeFaults is None:
            return self.speedFaults
        elif self.speedFaults is None:
            return self.timeFaults
        else:
            return self.timeFaults + self.speedFaults

    def determineiferror(self):
        file = "setup.json"
        setup = Setup(file)

        db = DbHelper()
        db.setDatabaseFile(setup.databaseFile)
        db.connectToDatabase()

        db.dbCursor.execute("SELECT rider_num FROM xcErrorTable WHERE rider_num = ?", (self.riderNum,))
        number = db.dbCursor.fetchone()
        if number:
            return 1

        db.closeDatabaseFile()