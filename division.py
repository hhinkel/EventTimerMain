from dbHelper import DbHelper


class Division:

    def getalldivisions(self, file):
        db = DbHelper()

        db.setDatabaseFile(file)
        db.connectToDatabase()

        DbHelper.dbCursor.execute("SELECT * FROM xcDivisionTable ")
        rows =  DbHelper.dbCursor.fetchall()
        db.closeDatabaseFile()
        return rows

    def getonedivision(self, file, division):
        db = DbHelper()

        db.setDatabaseFile(file)
        db.connectToDatabase()

        DbHelper.dbCursor.execute("SELECT * FROM xcDivisionTable WHERE division = ?", (division,))
        row = DbHelper.dbCursor.fetchall()
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
