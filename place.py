class Place(object):
    def __init__(self, place):
        self.id = int(place["id"])
        self.desc = place["desc"]
        # If the direction isn't present in data, assign it a value of -1
        if "north" in place:
            self.north = int(place["north"])
        else:
            self.north = -1
        if "east" in place:
            self.east = int(place["east"])
        else:
            self.east = -1
        if "south" in place:
            self.south = int(place["south"])
        else:
            self.south = -1
        if "west" in place:
            self.west = int(place["west"])
        else:
            self.west = -1
        # If goal isn't present in data, assign it as False
        if "goal" in place:
            self.goal = place["goal"]
        else:
            self.goal = False
        # If items aren't present, assign it to an empty list
        if "items" in place:
            self.items = [int(item) for item in place["items"]]
        else:
            self.items = []

    def changeExit(self, direction, ID):
        if direction == "north":
            self.north = ID
        elif direction == "east":
            self.east = ID
        elif direction == "south":
            self.south = ID
        else:
            self.west = ID

    def getID(self):
        return self.id

    def hasItems(self):
        if len(self.items) == 0:
            return False
        return True

    def addItem(self, item):
        self.items.append(item)

    def removeItem(self, item):
        self.items.remove(item)

    def getItem(self, item):
        return self.items.pop(self.items.index(item))

    def getItems(self):
        return self.items

    def isGoal(self):
        return self.goal

    def getDescription(self):
        return self.desc

    # returns dictonary of possible movement in {direction:placeID} format
    def getExits(self):
        options = {}
        if self.north != -1:
            options["north"] = self.north
        if self.east != -1:
            options["east"] = self.east
        if self.south != -1:
            options["south"] = self.south
        if self.west != -1:
            options["west"] = self.west
        return options

    # returns a JSON serializable dictionary
    def export(self):
        return self.__dict__
