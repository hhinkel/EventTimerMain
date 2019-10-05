import datetime
import sqlite3
from dbHelper import DbHelper

class Rider:
    
    message = None
    number = None
    division = None
    fence = None
    startTime = None
    finishTime = None
    edit = None

    def __init__(self, msg):
        Rider.message = msg.decode('utf-8')
        
    def parseMessage(self):
        print(Rider.message)
        dataList = Rider.message.split(',')
        print(dataList)
        Rider.number = int(dataList[0])
        Rider.division = dataList[1]
        Rider.fence = int(dataList[2])
        Rider.startTime = int(dataList[3])
        Rider.finishTime = int(dataList[4])
        Rider.edit = dataList[5]

    def getNumber(self):
        return Rider.number
    
    def getDivision(self):
        return Rider.division
    
    def getFence(self):
        if (not Rider.fence):
            return "ERROR 2"
        elif (Rider.fence == 0):
            return "Start"
        elif (Rider.fence == 99):
            return "Finish"
        else:
            return str(Rider.fence)

    def getStartTime(self):
        return Rider.startTime

    def getFinishTime(self):
        return Rider.finishTime
    
    def getEdit(self):
        return Rider.edit

    def parseStartTime(self):
        if ((not Rider.startTime) or (Rider.startTime == 0)):
            return 0
        else:
            return datetime.datetime.utcfromtimestamp(Rider.startTime)

    def parseFinishTime(self):
        if ((not Rider.finishTime) or (Rider.finishTime == 0)):
            return 0
        else:
            return datetime.datetime.utcfromtimestamp(Rider.finishTime)

    def updateTables(self, file):
        db = DbHelper()

        db.setDatabaseFile(file)
        db.openDatabaseFile()
        db.connectToDatabase()

        if(Rider.edit == 'null'):
            Rider.insertIntoXCTable(self)
        elif(Rider.edit == 'D' and Rider.fence == 0):
            Rider.removeFromXCTable(self)
            Rider.insertIntoXCErrorTable(self, 2, "Rider deleted at start")
        elif (Rider.edit == 'D' and Rider.fence == 99):
            Rider.fence= 0
            Rider.finishTime = 0
            Rider.updateRiderInXCTable(self)
            Rider.insertIntoXCErrorTable(self, 3, "Rider deleted at finish")
        elif(Rider.number == int(Rider.edit)):
            Rider.updateRiderInXCTable(self)
            errText = "Rider division edited to " + Rider.division
            Rider.insertIntoXCErrorTable(self, 4, errText)
        elif(int(Rider.edit) and Rider.fence == 0):
            number = Rider.number
            Rider.number = int(Rider.edit)
            Rider.removeFromXCTable(self)
            errText = "Rider number edited from " + str(Rider.number) + " to " + str(number)
            Rider.insertIntoXCErrorTable(self, 5, errText)
            Rider.number = number
            Rider.insertIntoXCTable(self)
        elif(int(Rider.edit) and Rider.fence == 99):
            number = Rider.number
            Rider.number = int(Rider.edit)
            Rider.removeFromXCTable(self)
            errText = "Rider number edited from " + str(Rider.number) + " to " + str(number) + ". Entry not removed from xcTable"
            Rider.insertIntoXCErrorTable(self, 6, errText)
        else:
            Rider.insertIntoXCErrorTable(self, 1, "Error in updateTables")

        db.closeDatabaseFile()

    def insertIntoXCTable(self):
        if(Rider.fence == 0):
            if(Rider.checkIfRiderExists(self) == False):
                DbHelper.dbCursor.execute("INSERT INTO xcTable VALUES (?,?,?,?,?,?,?)",
                 (Rider.number, Rider.division, Rider.fence, Rider.startTime, Rider.finishTime, 0, Rider.edit))
                DbHelper.dbConnection.commit()
            else:
                errText = "Rider number " + str(Rider.number) + " already exists in xcTable"
                Rider.insertIntoXCErrorTable(self, 7, errText)
        if(Rider.fence == 99):
            if(Rider.checkIfFinishExists(self) == False):
                DbHelper.dbCursor.execute("SELECT start_time FROM xcTable WHERE rider_num = ?", (Rider.number,))
                startTime = DbHelper.dbCursor.fetchone()[0]
                if(startTime > Rider.finishTime):
                    errText = " For rider number " + str(Rider.number) + " the start " + str(startTime) + " time is after the finish time " + str(Rider.finishTime) + "."
                    Rider.insertIntoXCErrorTable(self, 8, errText)
                else:
                    DbHelper.dbCursor.execute("UPDATE xcTable SET fence_num = ?, finish_time = ? WHERE rider_num = ?",
                     (Rider.fence, Rider.finishTime, Rider.number))
                DbHelper.dbConnection.commit()
            else:
                errText = "Rider number " + str(Rider.number) + " already has a finish time in xcTable. New Time " + str(Rider.finishTime)
                Rider.insertIntoXCErrorTable(self, 9, errText)
    
    def checkIfRiderExists(self):
        DbHelper.dbCursor.execute("SELECT rider_num FROM xcTable WHERE rider_num = ?", (Rider.number,))
        data = DbHelper.dbCursor.fetchall()
        if(len(data) == 0):
            return False
        elif (data[0] == 0):
            return False
        else:
            return True

    def checkIfFinishExists(self):
        DbHelper.dbCursor.execute("SELECT finish_time FROM xcTable WHERE rider_num = ?", (Rider.number,))
        data = DbHelper.dbCursor.fetchone()
        if(len(data) == 0):
            return False
        elif(data[0] == 0):
            return False
        else:
            return True
    
    def removeFromXCTable(self):
        DbHelper.dbCursor.execute("DELETE FROM xcTable WHERE rider_num = ?",
         (Rider.number,))
        DbHelper.dbConnection.commit()

    def updateRiderInXCTable(self):
        DbHelper.dbCursor.execute("UPDATE xcTable SET division = ? WHERE rider_num = ?",
         (Rider.division, Rider.number))
        DbHelper.dbConnection.commit()
        
    def insertIntoXCErrorTable (self, errNum, errText):
        DbHelper.dbCursor.execute("INSERT INTO xcErrorTable VALUES (?,?,?,?,?)",
         (Rider.number, Rider.division, Rider.fence, errNum, errText))
        DbHelper.dbConnection.commit()
