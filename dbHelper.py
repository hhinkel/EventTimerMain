import sqlite3

class DbHelper:
    
    riderDbFile = None
    dbConnection = None
    dbCursor = None
    
    def __init__(self):
        pass

    def setDatabaseFile(self, filename):
        DbHelper.riderDbFile = filename

    def connectToDatabase(self):
        try:
            DbHelper.dbConnection = sqlite3.connect(DbHelper.riderDbFile)
            DbHelper.dbCursor = DbHelper.dbConnection.cursor()
        except sqlite3.DatabaseError as error:
            print("Cannot connect to Database ",DbHelper.riderDbFile, " ", error.args[0])
    def openDatabaseFile(self):
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
            time_oncourse INTEGER,
            edit TEXT)''')
            
        except sqlite3.Error as error:
            print("Cannot create xcTable table:", error.args[0])

    def createXCErrorTable(self):
        try:
            DbHelper.dbCursor.execute('''CREATE TABLE IF NOT EXISTS xcErrorTable
            (rider_num INTEGER NOT NULL,
            division TEXT NOT NULL,
            fence_num INTEGER NOT NULL,
            error_num INTEGER NOT NULL,
            error_text TEXT)''')
        except sqlite3.Error as error:
            print("Cannot create xcErrorTable:", error.args[0])