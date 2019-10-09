from dbHelper import DbHelper
from rider import Rider

class Results:
    # 0.4 faults per second over optimum time or under speed fault time
    faultValue = 0.4

    def __init__(self):
        self.riderNum = None
        self.division = None
        self.startTime = None
        self.finishTime = None
        self.timeOnCourse = None
        self.timeFaults = None
        self.speedFaults = None
        self.overTime = None

    def getresultsfordivision(self, file, division):
        db = DbHelper()

        db.setDatabaseFile(file)
        db.connectToDatabase()

        DbHelper.dbCursor.execute("SELECT * FROM xcTable WHERE division = ?", (division[0],))
        rows = DbHelper.dbCursor.fetchall()

        db.closeDatabaseFile()

        return rows

    def calculateresults(self, riderdata, opttime, mintime, timelimit):
        rider = Rider()
        rider.setriderdata(riderdata)

        self.riderNum = rider.number
        self.division = rider.division
        # format the start and finish times here?
        self.startTime = rider.startTime
        self.finishTime = rider.finishTime
        self.timeOnCourse = rider.calculateTimeOnCourse()
        self.timeFaults = self.calculatetimefaults(opttime)
        self.speedFaults = self.calculatespeedfaults(mintime)
        self.overTime = self.determineifovertime(timelimit)

    def calculatetimefaults(self, opttime):
        if (self.timeOnCourse < opttime):
            return 0
        else:
            return (self.timeOnCourse - opttime) * self.faultValue

    def calculatespeedfaults(self, mintime):
        # need to check for division here as no speed above Training
        if (self.timeOnCourse > mintime):
            return 0
        else:
            return (mintime - self.timeOnCourse) * self.faultValue

    def determineifovertime(self, timelimit):
        if (self.timeOnCourse > timelimit):
            return True
        else:
            return False

