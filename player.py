class Player(object):
    def __init__(self, data):
        self.name = data["name"]
        self.location = int(data["location"])
        self.prev_location = int(data["location"])
        if "items" in data:
            self.items = [int(item) for item in data["items"]]
        else:
            self.items = []

    # Change old location ID to new location ID
    def move(self, location):
        self.prev_location = self.location
        self.location = location

    # Returns current location ID
    def getLocation(self):
        return self.location

    #Returns the previous location ID
    def getPrevLocation(self):
        return self.prev_location

    # Returns name (string)
    def getName(self):
        return self.name

    # Returns True if item (ID) is in inventory
    def hasItem(self, item):
        return item in self.items

    # Adds item ID to inventory
    def addItem(self, item):
        self.items.append(item)

    # Removes item ID from inventory
    def removeItem(self, item):
        self.items.remove(item)

    # Returns the item matching item (ID)
    def getItem(self, item):
        return self.items.pop(self.items.index(item))

    def getItems(self):
        return self.items

    # returns a dictionary of Player properties - JSON serializable
    def export(self):
        return self.__dict__
