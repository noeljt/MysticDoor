class Item(object):
    def __init__(self, data):
        self.id = int(data["id"])
        self.name = data["name"]
        self.location = int(data["location"])
        self.description = data["desc"]

    def getID(self):
        return self.id

    def getLocation(self):
        return self.location

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    # returns a dictionary of Item properties - JSON serializable
    def export(self):
        return self.__dict__