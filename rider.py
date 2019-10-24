import datetime
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
        if msg:
            self.message = msg.decode('utf-8')
        
    def parseMessage(self):
        print(self.message)
        dataList = self.message.split(',')
        print(dataList)
        self.number = int(dataList[0])
        self.division = dataList[1]
        self.fence = int(dataList[2])
        self.startTime = int(dataList[3])
        self.finishTime = int(dataList[4])
        self.edit = dataList[5]

    def setriderdata(self, riderdata):
        self.number = riderdata[0]
        self.division = riderdata[1]
        self.fence = riderdata[2]
        self.startTime = riderdata[3]
        self.finishTime = riderdata[4]
        self.edit = riderdata[5]

    def getNumber(self):
        return self.number
    
    def getDivision(self):
        return self.division
    
    def getFence(self):
        if not self.fence:
            return "ERROR 2"
        elif self.fence == 0:
            return "Start"
        elif self.fence == 99:
            return "Finish"
        else:
            return str(self.fence)

    def getStartTime(self):
        return self.startTime

    def getFinishTime(self):
        return self.finishTime
    
    def getEdit(self):
        return self.edit

    def parseStartTime(self):
        if (not self.startTime) or (self.startTime == 0):
            return 0
        else:
            return datetime.datetime.utcfromtimestamp(self.startTime)

    def parseFinishTime(self):
        if (not self.finishTime) or (self.finishTime == 0):
            return 0
        else:
            return datetime.datetime.utcfromtimestamp(self.finishTime)

    def updateTables(self, file):
        db = DbHelper()

        db.setDatabaseFile(file)
        # db.openDatabaseFileAppend()
        db.connectToDatabase()

        if self.edit == 'null':
            self.insertIntoXCTable()
        elif self.edit == 'D' and self.fence == 0:
            self.removeFromXCTable()
            self.insertIntoXCErrorTable(2, "Rider deleted at start")
        elif self.edit == 'D' and self.fence == 99:
            self.fence= 0
            self.finishTime = 0
            self.updateRiderInXCTable()
            self.insertIntoXCErrorTable(3, "Rider deleted at finish")
        elif self.number == int(self.edit):
            self.updateRiderInXCTable()
            errText = "Rider division edited to " + self.division
            self.insertIntoXCErrorTable(4, errText)
        elif int(self.edit) and self.fence == 0:
            number = self.number
            self.number = int(self.edit)
            self.removeFromXCTable()
            errText = "Rider number edited from " + str(self.number) + " to " + str(number)
            self.insertIntoXCErrorTable(5, errText)
            self.number = number
            self.insertIntoXCTable()
        elif int(self.edit) and self.fence == 99:
            number = self.number
            self.number = int(self.edit)
            self.removeFromXCTable()
            errText = "Rider number edited from " + str(self.number) + " to " + str(number) + ". Entry not removed from xcTable"
            self.insertIntoXCErrorTable(6, errText)
        else:
            self.insertIntoXCErrorTable(1, "Error in updateTables")

        db.closeDatabaseFile()

    def insertIntoXCTable(self):
        if self.fence == 0:
            if self.checkIfRiderExists() is False:
                DbHelper.dbCursor.execute("INSERT INTO xcTable VALUES (?,?,?,?,?,?,?)",
                 (self.number, self.division, self.fence, self.startTime, self.finishTime, 0, self.edit))
                DbHelper.dbCursor.execute("INSERT INTO xcFenceTable VALUES (?,?,?,?)",
                 (self.number, self.division, self.fence, self.startTime))
                DbHelper.dbConnection.commit()
            else:
                errText = "Rider number " + str(self.number) + " already exists in xcTable"
                self.insertIntoXCErrorTable(7, errText)
        if self.fence == 99:
            if self.checkIfFinishExists() is None:
                errText = "Rider number " + str(self.number) + " does not have an entry in the xcTable."
                self.insertIntoXCErrorTable(8, errText)
            elif self.checkIfFinishExists() is False:
                DbHelper.dbCursor.execute("SELECT start_time FROM xcTable WHERE rider_num = ?", (self.number,))
                startTime = DbHelper.dbCursor.fetchone()[0]
                if(startTime > self.finishTime):
                    errText = " For rider number " + str(self.number) + " the start " + str(startTime) + " time is after the finish time " + str(self.finishTime) + "."
                    self.insertIntoXCErrorTable(9, errText)
                else:
                    timeOnCourse = self.finishTime - startTime
                    DbHelper.dbCursor.execute("UPDATE xcTable SET fence_num = ?, finish_time = ?, time_oncourse = ? WHERE rider_num = ?",
                     (self.fence, self.finishTime, timeOnCourse, self.number))
                    DbHelper.dbCursor.execute("INSERT INTO xcFenceTable VALUES (?,?,?,?)",
                     (self.number, self.division, self.fence, self.finishTime))
                    DbHelper.dbConnection.commit()
            else:
                errText = "Rider number " + str(self.number) + " already has a finish time in xcTable. New Time " + str(self.finishTime)
                self.insertIntoXCErrorTable(10, errText)
    
    def checkIfRiderExists(self):
        DbHelper.dbCursor.execute("SELECT rider_num FROM xcTable WHERE rider_num = ?", (self.number,))
        data = DbHelper.dbCursor.fetchall()
        if len(data) == 0:
            return False
        elif data[0] == 0:
            return False
        else:
            return True

    def checkIfFinishExists(self):
        DbHelper.dbCursor.execute("SELECT finish_time FROM xcTable WHERE rider_num = ?", (self.number,))
        data = DbHelper.dbCursor.fetchone()
        if data is None:
            return None
        elif data[0] == 0:
            return False
        else:
            return True
    
    def removeFromXCTable(self):
        DbHelper.dbCursor.execute("DELETE FROM xcTable WHERE rider_num = ?",
         (self.number,))
        DbHelper.dbConnection.commit()

    def updateRiderInXCTable(self):
        DbHelper.dbCursor.execute("UPDATE xcTable SET division = ? WHERE rider_num = ?",
         (self.division, self.number))
        DbHelper.dbConnection.commit()
        
    def insertIntoXCErrorTable (self, errNum, errText):
        DbHelper.dbCursor.execute("INSERT INTO xcErrorTable VALUES (?,?,?,?,?)",
         (self.number, self.division, self.fence, errNum, errText))
        DbHelper.dbConnection.commit()

    def calculateTimeOnCourse(self):
        return 60 / (self.startTime - self.finishTime)

