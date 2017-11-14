class Item(object):
    def __init__(self, data):
        self.id = int(data["id"])
        self.name = data["name"]
        self.desc = data["desc"]
        self.action = data["action"]

    def getID(self):
        return self.id

    def getName(self):
        return self.name

    def getDescription(self):
        return self.desc

    def chooseAction(self):
        #choose random action
        return self.action[0]
    
    # returns a dictionary of Item properties - JSON serializable
    def export(self):
        return self.__dict__
