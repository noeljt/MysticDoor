from flask import Flask
from flask_ask import Ask, statement, question, session
from place import *
from player import *
import json
import requests
import time
import unidecode

# Flask Logic

app = Flask(__name__)
ask = Ask(app, "/test")


@app.route('/')
def homepage():
    return "hi there, how ya doin?"

# Functions

# This is where we will load data from the XML file in the future
def get_data():
    data = {}
    data["player"] = {"name": "Joe", "location": "0"}
    data["places"] = []
    data["places"].append({"id": "0", "desc":"(0,0)", "north":"-1", "east":"1", "south":"-1", "west":"-1", "goal":"False"})
    data["places"].append({"id": "1", "desc":"(1,0)", "north":"4", "east":"2", "south":"-1", "west":"0", "goal":"False"})
    data["places"].append({"id": "2", "desc":"(2,0)", "north":"3", "east":"-1", "south":"-1", "west":"1", "goal":"False"})
    data["places"].append({"id": "3", "desc":"(2,1)", "north":"-1", "east":"1", "south":"2", "west":"4", "goal":"False"})
    data["places"].append({"id": "4", "desc":"(1,1)", "north":"-1", "east":"3", "south":"1", "west":"5", "goal":"False"})
    data["places"].append({"id": "5", "desc":"(0,1)", "north":"6", "east":"4", "south":"-1", "west":"-1", "goal":"False"})
    data["places"].append({"id": "6", "desc":"(0,2)", "north":"-1", "east":"7", "south":"5", "west":"-1", "goal":"False"})
    data["places"].append({"id": "7", "desc":"(1,2)", "north":"-1", "east":"8", "south":"-1", "west":"6", "goal":"False"})
    data["places"].append({"id": "8", "desc":"(2,2)", "north":"-1", "east":"-1", "south":"-1", "west":"7", "goal":"True"})
    return data

# Temporary - will be moved to class logic
def get_options(place):
    options = {}
    for key in place:
        if key == "north" or key == "east" or key == "south" or key == "west":
            if place[key] != "-1":
                options[key] = place[key]
    return options

# Alexa Logic

# App starts here
@ask.launch
def launchSkill():
    welcome_message = "Welcome to the Mystic Door 3 by 3 maze adventure. Would you like to check your status or move?"
    session.attributes['game'] = get_data()
    return question(welcome_message)


# Tells where the player is and their movement options
@ask.intent("StatusIntent")
def status():
    game = session.attributes['game']
    player = game["player"]
    places = game["places"]
    player_location = places[int(player["location"])]
    location = "You are located at %s." % (player_location["desc"])
    options = get_options(player_location)
    if len(options) == 0:
        response = "You are trapped."
    elif len(options) == 1:
        response = "Your only option is %s." % (options.keys()[0])
    else:
        option_string = ", ".join(options.keys())
        response = "Your options are %s." % (option_string)

    response += " Would you like to move or check your status again?"
    return question(response)


# User tries to move in a direction
@ask.intent("MoveIntent")
def move(direction):
    game = session.attributes["game"]
    player = game["player"]
    places = game["places"]
    player_location = places[int(player["location"])]
    options = get_options(player_location)
    if direction in options.keys():
        player["location"] = options[direction]
        player_location = places[int(player["location"])]
        result = "You moved %s to %s." % (direction, player_location["desc"])
    else:
        result = "You can't move that direction."

    if player_location["goal"] == "True":
        result += " You have reached the end of the maze. Would you like to play again?"
    else:
        result += "Would you like to move or check your status?"

    return question(result)

@ask.intent("YesIntent")
def yes():
    session.attributes["game"] = get_data()
    text = "A new game has been made. Would you like to move or check your status?"
    return question(text)

@ask.intent("NoIntent")
def no():
    return statement("Thank you for playing.")

if __name__ == '__main__':
    app.run(debug=True)
