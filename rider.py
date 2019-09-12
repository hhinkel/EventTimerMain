class Rider:
    
    message = None

    def __init__(self, msg):
        print("created")
        Rider.message = msg
        self.number = None
        self.fence = None
        self.startTime = None
        self.finishTime = None

    def parseMessage(self, msg):
        print(Rider.message.split(','))
