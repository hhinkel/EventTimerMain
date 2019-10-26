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
        elif self.finishTime - self.startTime > 0:
            return (self.finishTime - self.startTime)
        else:
            return 0

    def calculatetimefaults(self, opttime):
        if self.timeOnCourse is None:
            return None
        elif self.timeOnCourse < opttime:
            return 0
        else:
            faults = (self.timeOnCourse - opttime) * self.faultValue
            return "{:3.2f}".format(faults)

    def calculatespeedfaults(self, minTime=None):
        if self.timeOnCourse is None:
            return None
        elif minTime is None:
            return 0
        elif self.timeOnCourse > minTime:
            return 0
        else:
            faults =  (minTime - self.timeOnCourse) * self.faultValue
            return "{:3.2f}".format(faults)

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
            return float(self.timeFaults) + float(self.speedFaults)

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

    def enterresultsintable(self):
        file = "setup.json"
        setup = Setup(file)

        db = DbHelper()
        db.setDatabaseFile(setup.databaseFile)
        db.connectToDatabase()

        db.dbCursor.execute("INSERT INTO xcResultTable VALUES (?,?,?,?,?,?,?,?,?,?)",
                            (self.riderNum, self.division, self.startTime, self.finishTime,  self.timeOnCourse,
                             self.timeFaults, self.speedFaults, self.overTime, self.totalFaults, self.error))
        db.dbConnection.commit()

        db.closeDatabaseFile()