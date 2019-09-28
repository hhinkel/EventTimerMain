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

    def insertIntoXCTable(self, file):
        db = DbHelper()

        db.setDatabaseFile(file)
        db.openDatabaseFile()
        db.connectToDatabase()

        if(Rider.fence == 0):
            DbHelper.dbCursor.execute("INSERT INTO xcTable VALUES (?,?,?,?,?,?)",
             (Rider.number, Rider.division, Rider.fence, Rider.startTime, Rider.finishTime, Rider.edit))
            DbHelper.dbConnection.commit()
        if(Rider.fence == 99):
            DbHelper.dbCursor.execute("UPDATE xcTable SET fence_num = ?, finish_time = ? WHERE rider_num = ?",
             (Rider.fence, Rider.finishTime, Rider.number))
            DbHelper.dbConnection.commit()

        db.closeDatabaseFile()
