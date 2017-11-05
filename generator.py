from random import choice
from place import *

class Generator(object):
    # For now, these are here, but in the future we should load these from mongoDB
    # Also will need some way to differentiate between settings

    descriptions = ["a hallway", "a dark room", "a class room", "a lecture hall", "a janitor's closet", "a supply closet", "a staircase"]
    directions = ["north", "east", "south", "west"]
    opposite = {"north":"south", "east":"west", "south":"north", "west":"east"}

    def __init__(self, setting = ""):
        # Type
        self.setting = setting

    def generateRooms(self, places, num, entrance, exit = -1, exitDirection = ""):
        # Need to add the first generated place as a possible exit from the entrance place
        exits = places[entrance].getExits()
        if len(exits) < 4:
            # This is potentially very ineffecient...
            while True:
                direction = choice(Generator.directions)
                if not direction in exits:
                    places[entrance].changeExit(direction, len(places))
                    break
        # Start generating rooms
        result = []
        for x in range(0, num):
            # Create an object for each room to be generated and give an ID and random description
            result.append({"id":str(x + len(places))})
            result[x]["desc"] = choice(Generator.descriptions)
            # First generated place needs to lead back to the entrance place
            direction = Generator.opposite[direction]
            if x == 0:
                result[x][direction] = str(places[entrance].getID())
            else:
                result[x][direction] = str(x + len(places) - 1)
            # All except last generated place choose random direction to next place  
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
            # Make sure direction isn't already used from previous generated place
            if direction not in result[-1]:
                result[-1][direction] = str(exit)
                places[exit].changeExit(Generator.opposite[direction], len(result) + len(places) - 1)
            else:
                result[-1][direction] = str(exit)
                places[exit].changeExit(Generator.opposite[direction], len(result) + len(places) - 1)
                # Direction is already taken, re-connect last two generated places with new Generator.directions
                while True:
                    randomDirection = choice(Generator.directions)
                    if randomDirection != direction and Generator.opposite[randomDirection] not in result[-2]:
                        del result[-2][Generator.opposite[direction]]
                        direction = randomDirection
                        result[-2][Generator.opposite[direction]] = str(len(result) - 1)
                        result[-1][direction] = str(len(result) - 1)
                        break
        # Return JSON version of place objects
        return result




