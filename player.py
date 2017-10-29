class Player(object):
    def __init__(self, data):
        self.name = data["name"]
        self.location = int(data["location"])
        if "inv" in data:
            self.inv = [int(item) for item in data["inv"]]
        else:
            self.inv = []

    # Change old location ID to new location ID
    def move(self, location):
        self.location = location

    # Returns current location ID
    def getLocation(self):
        return self.location

    # Returns name (string)
    def getName(self):
        return self.name

    # Returns True if item (ID) is in inventory
    def hasItem(self, item):
        return item in self.inv

    # Adds item ID to inventory
    def addItem(self, item):
        self.inv.push(item)

    # Removes item ID from inventory
    def removeItem(self, item):
        self.inv.remove(item)

    # Returns the item matching item (ID)
    def getItem(self, item):
        return self.inv.pop(self.inv.index(item))

    # returns a dictionary of Player properties - JSON serializable
    def export(self):
        return self.__dict__