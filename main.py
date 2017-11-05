from flask import Flask
from flask_ask import Ask, statement, question, session
from place import *
from player import *
from item import *
from website import *
from narrator import *
from generator import *
import json
import requests
import time
import unidecode

# Flask Logic

app = Flask(__name__)
ask = Ask(app, "/test")
app.register_blueprint(website)


@app.route('/')
def homepage():
    return "hi there, how ya doin?"

# Functions

# This is where we will get data in JSON format from the database
def getData():
    data = {}
    data["player"] = {"name": "Joe", "location": "0"}

    data["places"] = []
    data["places"].append({"id": "0", "desc":"a nice lake", "east":"1"})
    data["places"].append({"id": "1", "desc":"a room with a potion on the floor", "north":"4", "east":"2", "west":"0", "items":["2"]})
    data["places"].append({"id": "2", "desc":"a dirt path", "north":"3", "west":"1"})
    data["places"].append({"id": "3", "desc":"a grassy scene with a sword in a stone", "east":"1", "south":"2", "west":"4", "items":["1"]})
    data["places"].append({"id": "4", "desc":"a volcanoe", "east":"3", "south":"1", "west":"5"})
    data["places"].append({"id": "5", "desc":"your dining room with a sandwhich and a laptop on the table", "north":"6", "east":"4", "items":["0", "3"]})
    data["places"].append({"id": "6", "desc":"siri's server room", "east":"7", "south":"5"})
    data["places"].append({"id": "7", "desc":"Amazon headquarters", "west":"6"})
    data["places"].append({"id": "8", "desc":"A bottomless abyss", "goal":"True"})

    # Some generated data
    places = [Place(p) for p in data["places"]]
    g = Generator()
    places += [Place(p) for p in g.generateRooms(places, 4, 7, 8, "south")]
    data["places"] = [p.export() for p in places]

    data["items"] = []
    data["items"].append({"id": "0", "name": "sandwich", "location": "5", "desc": "A delicious ham and cheese sandwich on white bread"})
    data["items"].append({"id": "1", "name": "sword", "location": "3", "desc": "A sword in a stone"})
    data["items"].append({"id": "2", "name": "potion", "location": "1", "desc": "A mysterious potion"})
    data["items"].append({"id": "3", "name": "laptop", "location": "5", "desc": "A beat up laptop"})

    return data

# Converts JSON session data into classes
def loadData():
    data = session.attributes["game"]
    player = Player(data["player"])
    places = [Place(p) for p in data["places"]]
    items = [Item(i) for i in data["items"]]
    location = places[player.getLocation()]
    return (player, places, items, location)

# Converts classes into JSON data and saves in session.attributes
def saveData(player, places, items):
    data = {}
    data["player"] = player.export()
    data["places"] = [p.export() for p in places]
    data["items"] = [i.export() for i in items]
    session.attributes["game"] = data

# Alexa Logic

# App starts here
@ask.launch
def launchSkill():
    welcome_message = "Welcome to the Mystic Door. "
    # Load game instance into session
    session.attributes['game'] = getData()
    # Pull data froms session and convert to classes
    player, places, items, location = loadData()
    # Tell current location
    welcome_message += "You are in %s. What would you like to do? " % (location.getDescription())
    return question(welcome_message)


# Tells where the player is and their movement options
@ask.intent("StatusIntent")
def status():
    # Pull data froms session and convert to classes
    player, places, items, location = loadData()
    # Find current location
    response = Narrator.randRoomLeadin() + " " + location.getDescription() + ". "
    # Items in location
    if location.hasItems():
        roomItems = location.getItems()
        if len(roomItems) == 0:
            response += "There are no items in this place. "
        elif len(roomItems) == 1:
            response += "There is %s in this place. " % (items[roomItems[0]].getDescription())
        else:
            itemNames = [items[i].getDescription() for i in roomItems]
            itemNames.insert(-2, "and")
            response += "There is %s in this place. " %(", ".join(itemNames))
    # Possible exits from location
    exits = location.getExits()
    if len(exits) == 0:
        response += "You are trapped. "
    elif len(exits) == 1:
        response += "Your only option is %s. " % (exits.keys()[0])
    else:
        exitsString = ", ".join(exits.keys())
        response += "Your options are %s. " % (exitsString)

    response += "What would you like to do next? "
    return question(response)


# User tries to move in a direction
@ask.intent("MoveIntent")
def move(direction):
    # Pull data froms session and convert to classes
    player, places, items, location = loadData()
    # Make sure movement is valid
    options = location.getExits()
    if direction in options.keys():
        player.move(options[direction])
        location = places[options[direction]]
        result = Narrator.randMoveNarration() + " " + str(direction) + " into " + location.getDescription() + ". "
    else:
        result = "You can't move that direction. "

    # Check if location is the end
    if location.isGoal():
        result += "You have reached the end of the maze. Would you like to play again? "
    else:
        result += "What would you like to do next? "

    # Save current game state
    saveData(player, places, items)

    return question(result)

@ask.intent("ExamineIntent")
def examine(choice):
    # Load session data into variables
    player, places, items, location = loadData()
    # For now we can only handle max four items
    letters = ["a", "b", "c", "d"]
    # Load items from location into options {letter:itemID}
    options = {}
    locationItems = location.getItems()
    for x in range(0, len(locationItems)):
        if x > 3:
            print "WARNING: Too many items in room %d" % (location.getID())
            break
        options[letters[x]] = locationItems[x]
    # If it's a valid choice, return item description
    if choice in options:
        response = items[options[choice]].getDescription() + ". "
    else:
        print choice
        if len(options) == 0:
            response = "You stare at your feet since there are no items in the room. "
        elif len(options) == 1:
            response = "There is only one item in the room, it is %s. " % (items[options["a"]].getDescription())
        else:            
            response = "Which item would you like to examine? Your options are "
            # Create a list of options and turn it into poor english
            temp = []
            for option in options:
                temp.append(option)
                temp.append(items[options[option]].getDescription())
            temp[-2] = "or"
            response += ", ".join(temp)
            response += ". "
            return question(response)
    response += "What would you like to do next? "
    return question(response)


@ask.intent("YesIntent")
def yes():
    session.attributes["game"] = getData()
    text = "A new game has been made. Would you like to move or check your status? "
    return question(text)

@ask.intent("NoIntent")
def no():
    return statement("Thank you for playing. ")

if __name__ == '__main__':
    app.run(debug=True)
