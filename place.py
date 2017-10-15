class Place(object):
    def __init__(self, place):
        self.id = int(place["id"])
        self.desc = place["desc"]
        self.north = int(place["north"])
        self.east = int(place["east"])
        self.south = int(place["south"])
        self.west = int(place["west"])
        if place["goal"] == "True":
            self.goal = True
        else:
            self.goal = False

    def isGoal(self):
        return self.goal

    def getDescription(self):
        return self.desc

    # returns dictonary of possible movement in {direction:placeID} format
    def getExits(self):
        options = {}
        if self.north and self.north != -1:
            options["north"] = self.north
        if self.east and self.east != -1:
            options["east"] = self.east
        if self.south and self.south != -1:
            options["south"] = self.south
        if self.west and self.west != -1:
            options["west"] = self.west
        return options

    # returns a dictionary containing the properties of Place - JSON serializable
    def export(self):
        return self.__dict__