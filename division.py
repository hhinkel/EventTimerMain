from dbHelper import DbHelper


class Division:

    def __init__(self):
        self.division = None
        self.optSpeed = None
        self.maxSpeed = None
        self.distance = None
        self.numOfFences = None
        self.numOfRiders = None
        self.optTime = None
        self.minTime = None

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
        self.distance = div[3]
        self.numOfFences = div[4]
        self.numOfRiders = div[5]
        self.optTime = self.optSpeed * self.distance
        self.minTime = self.maxSpeed * self.distance
