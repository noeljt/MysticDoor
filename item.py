class Item(object):
    def __init__(self, data, description):
        self.name = data["name"]
        self.location = int(data["location"])
        self.description = data["description"]

    def getLocation(self):
        return self.location

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    # returns a dictionary of Item properties - JSON serializable
    def export(self):
        return self.__dict__