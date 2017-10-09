class Place:
    def __init__(self, place):
        self.id = int(place["id"])
        self.description = place["data"]["description"]
        self.north = place["data"]["north"]
        self.east = place["data"]["east"]
        self.south = place["data"]["south"]
        self.west = place["data"]["west"]
        if place["data"]["goal"] == "True":
            self.goal = True
        else:
            self.goal = False

    # Add possible exits
    def addExit(self, direction, exit):
        if (direction == "north"):
            self.north = exit
        elif (direction == "east"):
            self.east = exit
        elif (direction == "south"):
            self.south = exit
        elif (direction == "west"):
            self.west = exit
        else:
            return False
        return True

    def setDescription(self, str):
        self.description = str

    def setGoal(self):
        self.goal = True

    def isGoal(self):
        return self.goal

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