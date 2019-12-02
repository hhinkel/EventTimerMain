import datetime
from setup import Setup
from dbHelper import DbHelper


class Division:

    def getalldivisions(self, db):
        db.dbCursor.execute("SELECT * FROM xcDivisionTable ")
        return db.dbCursor.fetchall()

    def getonedivision(self, db, division):
        db.dbCursor.execute("SELECT * FROM xcDivisionTable WHERE division = ?", (division,))
        row = db.dbCursor.fetchall()
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
