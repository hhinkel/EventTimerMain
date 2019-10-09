from dbHelper import DbHelper


class Division:

    def __init__(self):
        self.division = None
        self.optSpeed = None
        self.maxSpeed = None
        self.timeLimit = None
        self.distance = None
        self.numOfFences = None
        self.numOfRiders = None
        self.optTimeSec = None
        self.minTimeSec = None

    def getalldivisions(self, file):
        db = DbHelper()

        db.setDatabaseFile(file)
        db.connectToDatabase()

        DbHelper.dbCursor.execute("SELECT * FROM divisionTable")
        rows =  DbHelper.dbCursor.fetchall()
        db.closeDatabaseFile()
        return rows

    def getonedivision(self, file, division):
        db = DbHelper()

        db.setDatabaseFile(file)
        db.connectToDatabase()

        DbHelper.dbCursor.execute("SELECT division FROM divisionTable WHERE division = ?", (division,))
        row = DbHelper.dbCursor.fetchall()
        db.closeDatabaseFile()
        return row

    def setdivisionresults(self, div):
        self.division = div[0]
        self.optSpeed = div[1]
        self.maxSpeed = div[2]
        self.timeLimit = div[3]
        self.distance = div[4]
        self.numOfFences = div[4]
        self.numOfRiders = div[6]
        self.optTimeSec = (self.distance / self.optTime) * 60
        self.minTimeSec = (self.distance / self.maxSpeed) * 60
