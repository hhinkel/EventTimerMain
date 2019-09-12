class Rider:
    
    message = None
    number = None
    fence = None
    startTime = None
    finishTime = None

    def __init__(self, msg):
        print("created")
        Rider.message = msg
        
    def parseMessage(self, msg):
        dataString = msg[msg.find("\'")+1:msg.find("\'")]
        print(dataString)
        dataList = dataString.split(',')
        print(dataList)
        Rider.number = int(dataList[0])
        Rider.fence = int(dataList[1])
        Rider.startTime = long(dataList[2])
        Rider.finishTime = long(dataList[3])
        
