class Player(object):
    def __init__(self, data):
        self.name = data["name"]
        self.location = int(data["location"])

    # Add possible exits
    def move(self, location):
        self.location = location

    def getLocation(self):
        return self.location

    def getName(self):
        return self.name

    # returns a dictionary of Player properties - JSON serializable
    def export(self):
        return self.__dict__