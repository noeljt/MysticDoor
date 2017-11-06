from random import choice
from place import *


class Generator(object):
    # Hopefully this stuff will load from DB in the future

    descriptions = ["a hallway", "a dark room", "a class room",
                    "a lecture hall", "a janitor's closet",
                    "a supply closet", "a staircase"]
    directions = ["north", "east", "south", "west"]
    opposite = {"north": "south", "east": "west",
                "south": "north", "west": "east"}

    def __init__(self, setting=""):
        # Type
        self.setting = setting

    def generateRooms(self, places, num, entrance, entranceDirection, exit=-1, exitDirection=""):
        # Tie entrance to first generated place
        direction = entranceDirection
        places[entrance].changeExit(direction, len(places))
        # Start generating rooms
        result = []
        for x in range(0, num):
            # Generate ID and description
            result.append({"id": str(x + len(places))})
            result[x]["desc"] = choice(Generator.descriptions)
            # First generated place needs to lead back to the entrance place
            direction = Generator.opposite[direction]
            if x == 0:
                result[x][direction] = str(places[entrance].getID())
            else:
                result[x][direction] = str(x + len(places) - 1)
            # Last generated place is handled out of loop
            if x == num - 1:
                pass
            else:
                while True:
                    newDirection = choice(Generator.directions)
                    if newDirection != direction:
                        direction = newDirection
                        result[x][direction] = str(x + len(places) + 1)
                        break
        # Deal with last generated place's exit
        if exit == -1:
            result[-1]["goal"] = "True"
        else:
            direction = Generator.opposite[exitDirection]
            # Avoid conflicts of direction with existing exits
            if direction not in result[-1]:
                result[-1][direction] = str(exit)
                places[exit].changeExit(Generator.opposite[direction],
                                        len(result) + len(places) - 1)
            else:
                result[-1][direction] = str(exit)
                places[exit].changeExit(Generator.opposite[direction],
                                        len(result) + len(places) - 1)
                # There was a conflict, reconnect exit to last place
                while True:
                    randDirection = choice(Generator.directions)
                    if randDirection != direction:
                        if Generator.opposite[randDirection] not in result[-2]:
                            del result[-2][Generator.opposite[direction]]
                            newID = str(len(result) - 1)
                            direction = randDirection
                            result[-2][Generator.opposite[direction]] = newID
                            result[-1][direction] = newID
                            break
        # Return JSON version of place objects
        return result
