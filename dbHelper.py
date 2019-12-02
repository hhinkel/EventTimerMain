import sqlite3
from setup import Setup
from utils import Utils


class DbHelper:
    
    riderDbFile = None
    dbConnection = None
    dbCursor = None
    colNames = None

    def createdatabase(self, file):
        self.setDatabaseFile(file)
        self.connectToDatabase()
        self.createDivisionTable()
        self.createXCTable()
        self.createFenceTable()
        self.createXCErrorTable()
        self.closeDatabaseFile()

    def createresulttable(self, file):
        # Database needs to already be open
        self.createXCResultTable()

    def setDatabaseFile(self, filename):
        self.riderDbFile = filename

    def connectToDatabase(self):
        try:
            self.dbConnection = sqlite3.connect(self.riderDbFile)
            self.dbCursor = self.dbConnection.cursor()
        except sqlite3.DatabaseError as error:
            print("Cannot connect to Database ",self.riderDbFile, " ", error.args[0])

    def openDatabaseFileRead(self):
        try:
            self.dbConnection = open(self.riderDbFile)
        except FileNotFoundError:
            print("Cannot open or create database file " + self.riderDbFile)

    def openDatabaseFileAppend(self):
        try:
            self.dbConnection = open(self.riderDbFile,"a")
        except FileNotFoundError:
            print("Cannot open or create database file " + self.riderDbFile)

    def closeDatabaseFile(self):
        self.dbConnection.close()

    def createDivisionTable(self):
        try:
            self.dbCursor.execute('''CREATE TABLE IF NOT EXISTS xcDivisionTable 
            (division TEXT UNIQUE,
            optSpeed INTEGER NOT NULL,	        
            maxSpeed INTEGER,
            timeLimit INTEGER,
            distance INTEGER NOT NULL,
            optTime INTEGER,
            minTime INTEGER,
            numOfFences INTEGER NOT NULL,
            numOfRiders INTEGER)''')
            setup = Setup("setup.json")
            Utils.division_setup(self)
        except sqlite3.Error as error:
            print("Cannot create xcDivisionTable: ", error.args[0])

    def createXCTable(self):
        try:
            self.dbCursor.execute('''CREATE TABLE IF NOT EXISTS xcTable
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
            self.dbCursor.execute('''CREATE TABLE IF NOT EXISTS xcFenceTable
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
            self.dbCursor.execute('''CREATE TABLE IF NOT EXISTS xcErrorTable
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

    def getresultsfordivision(self, division):

        self.dbCursor.execute("SELECT * FROM xcTable WHERE division = ?", (division,))
        rows = self.dbCursor.fetchall()

        return rows

    def selectFromTable(self, query):
        self.dbCursor.execute(query)
        return self.dbCursor.fetchall()

    def counttablerows(self, tablename):
        try:
            self.dbCursor.execute("SELECT * FROM {tn}".format (tn=tablename))
            return len(self.dbCursor.fetchall())
        except sqlite3.OperationalError as error:
            return 0
        
    def enterresultsintable(self, results):
        for result in results:
            self.dbCursor.execute("INSERT INTO xcResultTable VALUES (?,?,?,?,?,?,?,?,?,?)",
            (result[0], result[1], result[2], result[3],  result[4], result[5],
            result[6], result[7], result[8], result[9]))
            self.dbConnection.commit()
