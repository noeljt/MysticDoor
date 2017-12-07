# game.py
# stores game data to save into mongoDB


class Game(object):
    def __init__(self, data):
        self.player = data["player"]
        self.places = data["places"]
        self.items = data["items"]
        self.title = data["title"]
        if "_id" in data:
            self._id = data["_id"]
        else:
            self._id = -1

    # returns a list of all items where the
    # index is the ID and the value is the item
    def getItems(self):
        return self.items

    # returns a list of all places, where the index
    # is the ID and the value is the place
    def getPlaces(self):
        return self.places

    # returns the player
    def getPlayer(self):
        return self.player

    # returns the title of the adventure
    def getTitle(self):
        return self.title

    # returns a JSON serializable representation of the class
    def export(self):
        return self.__dict__
