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
        Rider.number = dataList[0]
        Rider.fence = dataList[1]
        Rider.startTime = dataList[2]
        Rider.finishTime = dataList[3]
        
