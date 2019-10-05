import json

class Setup:
    user = None
    key = None
    server = None
    port = None
    topic = None
    databaseFile = None

    def __init__(self, file):
        with open(file) as jsonFile:
            data = json.load(jsonFile)
            self.user = data["user"]
            self.key = data["key"]
            self.server = data["server"]
            self.port = data["port"]
            self.topic = data["topic"]
            self.databaseFile = data["databaseFile"]
        