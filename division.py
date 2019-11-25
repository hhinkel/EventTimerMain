import datetime
from setup import Setup
from dbHelper import DbHelper


class Division:

    def getalldivisions(self, file):
        db = DbHelper()

        db.setDatabaseFile(file)
        db.connectToDatabase()

        db.dbCursor.execute("SELECT * FROM xcDivisionTable ")
        rows =  db.dbCursor.fetchall()
        db.closeDatabaseFile()
        return rows

    def getonedivision(self, file, division):
        db = DbHelper()

        db.setDatabaseFile(file)
        db.connectToDatabase()

        db.dbCursor.execute("SELECT * FROM xcDivisionTable WHERE division = ?", (division,))
        row = db.dbCursor.fetchall()
        db.closeDatabaseFile()
        return row

    def setdivisionresults(self, div):
        self.division = div[0]
        self.optSpeed = div[1]
        self.maxSpeed = div[2]
        self.timeLimit = div[3]
        self.distance = div[4]
        self.numOfFences = div[5]
        self.numOfRiders = div[6]
        self.optTimeSec = int((self.distance / self.optSpeed) * 60)
        self.minTimeSec = int((self.distance / self.maxSpeed) * 60)

    def setupdivision(self):
        setup = Setup("setup.json")
        db = DbHelper()

        db.setDatabaseFile(setup.databaseFile)
        db.connectToDatabase()
        for division in setup.divisions:
            optTime = self.determinetime(division[1], division[4])
            minTime = self.determinetime(division[2], division[4])
            db.dbCursor.execute("INSERT INTO xcDivisionTable VALUES (?,?,?,?,?,?,?,?,?)",
             (division[0], int(division[1]), int(division[2]), int(division[3]), int(division[4]), optTime, minTime, int(division[5]), int(division[6])))
            db.dbConnection.commit()

    def determinetime(self, mpermin, distance):
        # formula from http://www.myhorsechat.com/2013/03/14/how-to-calculate-the-optimum-time-in-eventing/
        # convert meters per min to meters per second
        mpersec = int(mpermin) / 60

        # determine the number of seconds needed to cover the distance at the meters per second determined above
        totalsecs = int(distance) / mpersec

        return str(datetime.timedelta(seconds=totalsecs))

