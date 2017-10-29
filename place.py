class Place(object):
    def __init__(self, place):
        self.id = int(place["id"])
        self.desc = place["desc"]
        if "north" in place:
            self.north = int(place["north"])
        if "east" in place:
            self.east = int(place["east"])
        if "south" in place:
            self.south = int(place["south"])
        if "west" in place:
            self.west = int(place["west"])
        if "goal" in place:
            self.goal = True
        else:
            self.goal = False
        if "items" in place:
            self.items = [int(item) for item in place["items"]]
        else:
            self.items = []

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
        if self.north:
            options["north"] = self.north
        if self.east:
            options["east"] = self.east
        if self.south:
            options["south"] = self.south
        if self.west:
            options["west"] = self.west
        return options

    # returns a dictionary containing the properties of Place - JSON serializable
    def export(self):
        return self.__dict__