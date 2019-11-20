import sqlite3


class DbHelper:
    
    riderDbFile = None
    dbConnection = None
    dbCursor = None
    
    def createdatabase(self, file):
        self.setDatabaseFile(file)
        self.connectToDatabase()
        self.createXCTable()
        self.createFenceTable()
        self.createXCErrorTable()
        self.closeDatabaseFile()

    def setDatabaseFile(self, filename):
        DbHelper.riderDbFile = filename

    def connectToDatabase(self):
        try:
            DbHelper.dbConnection = sqlite3.connect(DbHelper.riderDbFile)
            DbHelper.dbCursor = DbHelper.dbConnection.cursor()
        except sqlite3.DatabaseError as error:
            print("Cannot connect to Database ",DbHelper.riderDbFile, " ", error.args[0])

    def openDatabaseFileRead(self):
        try:
            DbHelper.dbConnection = open(DbHelper.riderDbFile)
        except FileNotFoundError:
            print("Cannot open or create database file " + DbHelper.riderDbFile)

    def openDatabaseFileAppend(self):
        try:
            DbHelper.dbConnection = open(DbHelper.riderDbFile,"a")
        except FileNotFoundError:
            print("Cannot open or create database file " + DbHelper.riderDbFile)

    def closeDatabaseFile(self):
        DbHelper.dbConnection.close()

    def createXCTable(self):
        try:
            DbHelper.dbCursor.execute('''CREATE TABLE IF NOT EXISTS xcTable
            (rider_num INTEGER PRIMARY KEY,
            division TEXT NOT NULL,
            fence_num INTEGER NOT NULL,
            start_time INTEGER,
            finish_time INTEGER,
            edit TEXT)''')
            
        except sqlite3.Error as error:
            print("Cannot create xcTable table: ", error.args[0])

    def createFenceTable(self):
        try:
            DbHelper.dbCursor.execute('''CREATE TABLE IF NOT EXISTS xcFenceTable
            (rider_num INTEGER NOT NULL,
            division TEXT NOT NULL,
            fence_num INTEGER NOT NULL,
            score INTEGER,
            PRIMARY KEY(rider_num, division, fence_num),
            FOREIGN KEY(rider_num) REFERENCES xcTable(rider_num)
            )''')
        except sqlite3.Error as error:
            print("Cannot create xcFenceTable: ", error.args[0])

    def createXCErrorTable(self):
        try:
            DbHelper.dbCursor.execute('''CREATE TABLE IF NOT EXISTS xcErrorTable
            (rider_num INTEGER NOT NULL,
            division TEXT NOT NULL,
            fence_num INTEGER NOT NULL,
            error_num INTEGER NOT NULL,
            error_text TEXT)''')
        except sqlite3.Error as error:
            print("Cannot create xcErrorTable: ", error.args[0])

    def createXCResultTable(self):
        try:
            self.dbCursor.execute('''CREATE TABLE IF NOT EXISTS xcResultTable
            (rider_num INTEGER PRIMARY KEY,
            division TEXT NOT NULL,
            start_time INTEGER NOT NULL,
            finish_time INTEGER,
            time_oncourse INTEGER,
            time_faults INTEGER,
            speed_faults INTEGER,
            over_Time INTEGER,
            total_faults INTEGER,
            error INTEGER)''')
        except sqlite3.Error as error:
            print("Cannot create xcResultTable: ", error.args[0])

    def getresultsfordivision(self, file, division):
        self.setDatabaseFile(file)
        self.connectToDatabase()

        self.dbCursor.execute("SELECT * FROM xcTable WHERE division = ?", (division,))
        rows = DbHelper.dbCursor.fetchall()

        self.closeDatabaseFile()

        return rows

    def selectFromTable(self, query):
        cursor = self.dbCursor
        cursor.execute(query)
        return cursor.fetchall()