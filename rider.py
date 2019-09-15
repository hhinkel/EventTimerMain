import datetime
from dbHelper import DbHelper

class Rider:
    
    message = None
    number = None
    fence = None
    startTime = None
    finishTime = None

    def __init__(self, msg):
        Rider.message = msg.decode('utf-8')
        
    def parseMessage(self):
        print(Rider.message)
        dataList = Rider.message.split(',')
        print(dataList)
        Rider.number = int(dataList[0])
        Rider.fence = int(dataList[1])
        Rider.startTime = int(dataList[2])
        Rider.finishTime = int(dataList[3])

    def getNumber(self):
        return Rider.number
    
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

    def parseStartTime(self):
        if ((not startTime) or (startTime == 0)):
            return 0
        else:
            return datetime.datetime.utcfromtimestamp(Rider.startTime)

    def parseFinishTime(self):
        if ((not finishTime) or (finishTime == 0)):
            return 0
        else:
            return datetime.datetime.utcfromtimestamp(Rider.finishTime)

    def insertIntoXCTable(self, file):
        db = DbHelper()

        db.setDatabaseFile(file)
        db.openDatabaseFile()
        db.connectToDatabase()

        DbHelper.dbCursor.execute("INSERT INTO xcTable VALUES (?,?,?,?)",
        (Rider.number, Rider.fence, Rider.startTime, Rider.finishTime))
        DbHelper.dbConnection.commit()
        
        db.closeDatabaseFile()
