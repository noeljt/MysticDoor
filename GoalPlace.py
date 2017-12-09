
class GoalPlace extends Place{
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
       
        # If items aren't present, assign it to an empty list
        if "items" in place:
            self.items = [int(item) for item in place["items"]]
        else:
            self.items = []
# If goal isn't present in data, assign it as False
       if "goal" in place:
           self.goal = place["goal"]
       else:
           self.goal = False
           
def isGoal(self):
  return self.goal
}
