from flask import Flask
from flask_ask import Ask, statement, question, session
from place import *
from player import *
from website import *
from narrator import *
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
    data["player"] = {"name": "Joe", "location": "0", "items": ["0", "1", "2"]}

    data["places"] = []
    data["places"].append({"id": "0", "desc":"a nice lake", "east":"1"})
    data["places"].append({"id": "1", "desc":"(1,0)", "north":"4", "east":"2", "west":"0"})
    data["places"].append({"id": "2", "desc":"(2,0)", "north":"3", "west":"1"})
    data["places"].append({"id": "3", "desc":"(2,1)", "east":"1", "south":"2", "west":"4"})
    data["places"].append({"id": "4", "desc":"(1,1)", "east":"3", "south":"1", "west":"5"})
    data["places"].append({"id": "5", "desc":"(0,1)", "north":"6", "east":"4"})
    data["places"].append({"id": "6", "desc":"(0,2)", "east":"7", "south":"5"})
    data["places"].append({"id": "7", "desc":"(1,2)", "east":"8", "west":"6"})
    data["places"].append({"id": "8", "desc":"(2,2)", "west":"7", "goal":"True"})

    data["items"] = []
    data["items"].append({"id": "0", "name": "sandwich", "location": "5", "desc": "A delicious ham and cheese sandwich on white bread"})
    data["items"].append({"id": "1", "name": "sword", "location": "3", "desc": "A sword, pretty straightforward"})
    data["items"].append({"id": "2", "name": "potion", "location": "1", "desc": "A mysterious potion"})

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
def saveData(player, places):
    data = {}
    data["player"] = player.export()
    data["places"] = [p.export() for p in places]
    data["items"] = [i.export() for i in items]
    session.attributes["game"] = data

# Alexa Logic

# App starts here
@ask.launch
def launchSkill():
    welcome_message = "Welcome to the Mystic Door 3 by 3 maze adventure. Would you like to check your status or move?"
    session.attributes['game'] = getData()
    return question(welcome_message)


# Tells where the player is and their movement options
@ask.intent("StatusIntent")
def status():
    # Pull data froms session and convert to classes
    player, places, items, location = loadData()
    # Find current location
    #response = "You are located at %s." % (location.getDescription())
    response = Narrator.randRoomLeadin() + " " + location.getDescription() + ". "
    # Items in location
    if location.hasItems():
        roomItems = location.getItems()
        if len(roomItems) == 0:
            response += "There are no items in this place."
        elif len(roomItems) == 1:
            response += "There is %s in this place." % (items[roomItems[0]].getDescription())
        else:
            itemNames = [items(i).getDescription() for i in roomItems]
            itemNames.insert(-2, "and")
            response += "There is %s in this place." %(", ".join(itemNames))
    # Possible exits from location
    exits = location.getExits()
    if len(exits) == 0:
        response += "You are trapped."
    elif len(exits) == 1:
        response += "Your only option is %s." % (exits.keys()[0])
    else:
        exitsString = ", ".join(exits.keys())
        response += "Your options are %s." % (exitsString)

    response += " Would you like to move or check your status again?"
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
        result = Narrator.randMoveNarration() + " " + str(direction) + ". "
    else:
        result = "You can't move that direction. "

    # Check if location is the end
    if location.isGoal():
        result += " You have reached the end of the maze. Would you like to play again?"
    else:
        result += "Would you like to move or check your status?"

    # Save current game state
    saveData(player, places)

    return question(result)

@ask.intent("YesIntent")
def yes():
    session.attributes["game"] = getData()
    text = "A new game has been made. Would you like to move or check your status?"
    return question(text)

@ask.intent("NoIntent")
def no():
    return statement("Thank you for playing.")

if __name__ == '__main__':
    app.run(debug=True)
