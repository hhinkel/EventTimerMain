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
        except ConnectionError:
            print("Cannot connect to Database " + DbHelper.riderDbFile)

    def openDatabaseFile(self):
        try:
            DbHelper.dbConnection = open(DbHelper.riderDbFile,"a")
        except FileNotFoundError:
            print("Cannot open or create database file " + DbHelper.riderDbFile)

    def closeDatabaseFile(self):
        DbHelper.dbConnection.close()

    def createXCTable(self):
        try:
            String CREATE_XC_TABLE = '''CREATE TABLE IF NOT EXISTS xcTable
            (rider_num INTEGER PRIMARY KEY,
            division TEXT NOT NULL,
            fence_num INTEGER NOT NULL,
            start_time INTEGER,
            finish_time INTEGER,
            edit INTEGER CHECK(edit <= 1))'''
            
            DbHelper.dbCursor.execute(CREATE_XC_TABLE)
            
            #DbHelper.dbCursor.execute('''CREATE TABLE IF NOT EXISTS xcTable 
            #(rider_num INTEGER PRIMARY KEY,
            #fence_num INTEGER NOT NULL,
            #start_time INTEGER,
            #finish_time INTEGER)''')
        except TypeError:
            print("Cannot create xcTable table")
