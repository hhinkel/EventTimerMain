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

    def getresultsfordivision(self, file, division):
        db = DbHelper()

        db.setDatabaseFile(file)
        db.connectToDatabase()

        DbHelper.dbCursor.execute("SELECT * FROM xcTable WHERE division = ?", (division[0],))
        rows = DbHelper.dbCursor.fetchall()

        db.closeDatabaseFile()

        return rows

    def calculateresults(self, riderdata, opttime, mintime):
        rider = Rider()
        rider.setriderdata(riderdata)




