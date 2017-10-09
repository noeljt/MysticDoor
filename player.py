from place import *

class Player:
    def __init__(self, start):
        self.name = "Default"
        self.location = start

    # Add possible exits
    def move(self, direction):
        options = self.location.getOptions()
        if direction in options:
            self.location = options[direction]
            return True
        else:
            return False

    def getLocation(self):
        return self.location

    def getName(self):
        return self.name