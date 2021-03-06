from flask import Flask
from flask_ask import Ask, statement, question, session
from pymongo import MongoClient
from place import *
from player import *
from item import *
from website import *
from narrator import *
from generator import *
from game import *
import json
import requests
import time
import unidecode
import random

# Flask Logic

app = Flask(__name__)
ask = Ask(app, "/test")
app.register_blueprint(website)


@app.route('/')
def homepage():
    return "hi there, how ya doin?"


def demoData():  # demoData generates the data to start a demo game
    # This is where we will get data in JSON format from the database
    data = {}
    data["player"] = {"name": "Joe", "location": "0"}

    data["places"] = []
    # Formatting is thanks to PEP8 but this is temporary anyway
    data["places"].append({
        "id": "0",
        "desc": "a dark room with a single candle in the center",
        "items": ["0"]
    })
    # Generate two places
    data["places"].append({
        "id": "1",
        "desc": "a brightly lit hallway with two pictures hanging on the wall",
        "items": ["1", "2"]
    })
    # Generate one place
    data["places"].append({
        "id": "2",
        "desc": "a four door elevator you can feel moving"
    })
    # Generate two places
    data["places"].append({
        "id": "3",
        "desc": "a classroom with the number 6113 on the door" +
                " and a lone paper on the floor",
        "south": "4",
        "items": ["3"]
    })
    data["places"].append({
        "id": "4",
        "desc": "your house",
        "north": "3",
        "goal": "true"
    })

    # Generate filler places
    places = [Place(p) for p in data["places"]]
    g = Generator()
    places += [Place(p) for p in
               g.generateRooms(places, 2, 0, "east", 1, "south")]
    places += [Place(p) for p in
               g.generateRooms(places, 1,  1, "north", 2, "west")]
    places += [Place(p) for p in
               g.generateRooms(places, 2,  2, "south", 3, "east")]
    data["places"] = [p.export() for p in places]

    data["items"] = []
    data["items"].append({
        "id": "0",
        "name": "candle",
        "desc": "a lit red candle with the letters R, P , and I on it"
    })
    data["items"].append({
        "id": "1",
        "name": "picture",
        "desc": "a picture of a woman with the name" +
                " Shirley Ann Jackson engraved on the frame"
    })
    data["items"].append({
        "id": "2",
        "name": "picture",
        "desc": "a picture of a man with an engraving reading," +
                " Dr. William Weightman Walker"
    })
    data["items"].append({
        "id": "3",
        "name": "paper",
        "desc": "a paper with a graded quiz and your" +
                " name on it... you did not do well"
    })

    # Generate 5 new random items and add each one to a random place
    for i in range(5):
        # Ids 0-3 are taken so start at 4
        id = 4+i
        # Append new item to the item data
        data["items"].append(g.randItemData(id))
        # Choose a random place by id
        rand_place_id = random.randint(0, len(data["places"])-1)
        # Append new item id to the place items data
        data["places"][rand_place_id]["items"].append(id)

    return data


def demoData2():
    # This is where we will get data in JSON format from the database
    data = {}
    data["player"] = {"name": "Joe", "location": "0"}

    data["places"] = []
    # Formatting is thanks to PEP8 but this is temporary anyway
    data["places"].append({
        "id": "0",
        "desc": "a cubicle, at your desk, at your dead-end job",
        "items": ["0"]
    })
    # Generate two places
    data["places"].append({
        "id": "1",
        "desc": "an empty meeting room with paper scattered around",
        "items": ["1", "2"]
    })
    # Generate one place
    data["places"].append({
        "id": "2",
        "desc": "an empty break room, your coworkers left garbage everywhere"
    })
    # Generate two places
    data["places"].append({
        "id": "3",
        "desc": "the lobby, which to your surprise is also empty",
        "south": "4",
        "items": ["3"]
    })
    data["places"].append({
        "id": "4",
        "desc": "a dark room, where a loud noise startles you and" +
                " you wake up to your phone alarm labeled: final exams..." +
                " the nightmare has begun",
        "north": "3",
        "goal": "True"
    })

    # Generate filler places
    places = [Place(p) for p in data["places"]]
    g = Generator()
    places += [Place(p) for p in
               g.generateRooms(places, 2, 0, "east", 1, "south")]
    places += [Place(p) for p in
               g.generateRooms(places, 1,  1, "north", 2, "west")]
    places += [Place(p) for p in
               g.generateRooms(places, 2,  2, "south", 3, "east")]
    data["places"] = [p.export() for p in places]

    data["items"] = []
    data["items"].append({
        "id": "0",
        "name": "paper",
        "desc": "a paper awaiting your signature"
    })
    data["items"].append({
        "id": "1",
        "name": "doodle",
        "desc": "the result of a bored businessman at a meeeting"
    })
    data["items"].append({
        "id": "2",
        "name": "paper",
        "desc": "a paper with a meeting agenda on it"
    })
    data["items"].append({
        "id": "3",
        "name": "paper",
        "desc": "a paper on the front desk that reads: wake up"
    })

    # Generate 5 new random items and add each one to a random place
    for i in range(5):
        # Ids 0-3 are taken so start at 4
        id = 4+i
        # Append new item to the item data
        data["items"].append(g.randItemData(id))
        # Choose a random place by id
        rand_place_id = random.randint(0, len(data["places"])-1)
        # Append new item id to the place items data
        data["places"][rand_place_id]["items"].append(id)

    return data

# Connect to database and load one demo game if none are present
# Default is localhost:27017
client = MongoClient()
db = client.mysticDoor
games = db.games
if games.count() == 0:
    data = demoData2()
    game = Game({"title": "Quiz Day",
                 "player": data['player'],
                 "places": data['places'],
                 "items": data['items']})
    games.insert_one(game.export())
    print("Game added to database")
else:
    print("Game already in database")


# Functions


def getData(title):
    # Retrieve one game by title from the database
    game = games.find({"title": title})[0]
    return game


def saveData():
    game = session.attributes["game"]
    result = games.replace_one({"_id": game._id}, game)


def constructStatusString():
    # Tells where the player is and their movement options
    # Pull data froms session and convert to classes
    player, places, items, location = loadSessionData()
    # Items in location
    if location.hasItems():
        roomItems = location.getItems()
        if len(roomItems) == 1:
            response = "There is one item here. "
        else:
            response = "There are %d items here. " % (len(roomItems))
    else:
        response = "There are no items here. "
    response += constructExitsString()
    return response


def constructExitsString():
    player, places, items, location = loadSessionData()
    response = ""
    if location.isGoal():
        response += "This is the end. Would you like to play again? "
    else:
        # Possible exits from location
        response += constructPreviousString()
        exits = location.getExits()
        if len(exits) == 0:
            response += "There are no exits, you are trapped. "
        elif len(exits) == 1:
            response += "The only exit is %s. " % (exits.keys()[0])
        else:
            tempKeys = exits.keys()
            tempKeys.insert(-1, "and")
            exitsString = ", ".join(tempKeys)
            response += "There are exits to the %s. " % (exitsString)
        response += "What would you like to do next? "
    return response


def constructPreviousString():
    player, places, items, location = loadSessionData()
    response = ""
    if player.getPrevLocation() == player.getLocation():
        return response
    else:
        exits = location.getExits()
        if len(exits) == 0:
            return response
        else:
            for key in exits:
                if exits[key] == player.getPrevLocation():
                    response += "You came from the %s. " % (key)
                    return response
    return response


def loadSessionData():
    # Converts JSON session data into classes
    data = session.attributes["game"]
    player = Player(data["player"])
    places = [Place(p) for p in data["places"]]
    items = [Item(i) for i in data["items"]]
    location = places[player.getLocation()]
    return (player, places, items, location)


def saveSessionData(player, places, items):
    # Converts classes into JSON data and saves in session.attributes
    game = session.attributes["game"]
    game["player"] = player.export()
    game["places"] = [p.export() for p in places]
    game["items"] = [i.export() for i in items]

# Alexa Logic


@ask.launch
def launchSkill():
    # App starts here
    welcome_message = "Welcome to the Mystic Door. "
    # Load game instance into session
    session.attributes['game'] = getData("Quiz Day")
    # Pull data froms session and convert to classes
    player, places, items, location = loadSessionData()
    # Tell current location
    welcome_message += "You are in %s. " % (location.getDescription())
    welcome_message += "What would you like to do? "
    return question(welcome_message).reprompt(
        "You can move, check your status, or examine items.")


@ask.intent("StatusIntent")
def status():
    response = constructStatusString()
    return question(response).reprompt(
        "You can move, check your status, or examine items.")


@ask.intent("MoveIntent")
def move(direction):
    # User tries to move in a direction

    # Pull data froms session and convert to classes
    player, places, items, location = loadSessionData()
    # Make sure movement is valid
    options = location.getExits()
    if direction in options.keys():
        player.move(options[direction])
        location = places[options[direction]]
        result = Narrator.randMoveNarration() + " "
        result += str(direction) + " into " + location.getDescription() + ". "
    else:
        result = "You can't move that direction. "
    # Save current game state
    saveSessionData(player, places, items)

    # Read the exits of the new location
    result += constructExitsString()

    return question(result).reprompt(
        "You can move, check your status, or examine items.")


@ask.intent("ExamineIntent")
def examine(choice):
    # Load session data into variables
    player, places, items, location = loadSessionData()
    # For now we can only handle max four items
    letters = ["a", "B.", "C", "D"]
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
        if len(options) == 0:
            response = "You stare at your feet since"
            response += " there are no items here. "
        elif len(options) == 1:
            response = "There is only one item here"
            response += ", it is %s. " % (items[options["a"]].getDescription())
        else:
            response = "Which item would you like to examine? "
            response += " Your options are "
            # Create a list of options and turn it into poor english
            temp = []
            for option in options:
                temp.append(option)
                temp.append(items[options[option]].getName())
            temp.insert(-2, "or")
            response += ", ".join(temp)
            response += ". "
            return question(response)
    response += "What would you like to do next? "
    return question(response).reprompt(
        "You can move, check your status, or examine items.")


@ask.intent("PickupIntent")
def pickup():
    player, places, items, location = loadSessionData()
    locationItems = location.getItems()
    response = "There is no item to pick up here. "
    if len(locationItems) > 0:
        response = "You pick up a %s. " % items[locationItems[0]].getName()
    response += "What would you like to do next?"
    return question(response).reprompt(
        "You can move, check your status, or examine items.")


@ask.intent("YesIntent")
def yes():
    session.attributes["game"] = getData("Quiz Day")
    text = "A new game has been made. "
    text += "Would you like to move or check your status? "
    return question(text).reprompt(
        "You can move, check your status, or examine items.")


@ask.intent("NoIntent")
def no():
    saveData()
    return statement("Thank you for playing. ")


@ask.session_ended
def session_ended():
    saveData()


if __name__ == '__main__':
    app.run(debug=True)
