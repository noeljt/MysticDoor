from flask import Flask
from flask_ask import Ask, statement, question, session
from place.py import *
from player.py import *
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
def get_data(player, places):
    # Generate dummy 3x3 grid
    places = []
    place = Place()
    place.setDescription("(0,0)")
    places.push(place)
    place = Place()
    place.setDescription("(1,0)")
    places.push(place)
    place = Place()
    place.setDescription("(2,0)")
    places.push(place)
    place = Place()
    place.setDescription("(2,1)")
    places.push(place)
    place = Place()
    place.setDescription("(1,1)")
    places.push(place)
    place = Place()
    place.setDescription("(0,1)")
    places.push(place)
    place = Place()
    place.setDescription("(0,2)")
    places.push(place)
    place = Place()
    place.setDescription("(1,2)")
    places.push(place)
    place = Place()
    place.setDescription("(2,2)")
    places.push(place)

    places[0].addExit("east", places[1])
    places[1].addExit("east", places[2])
    places[1].addExit("north", places[4])
    places[2].addExit("north", places[3])
    places[3].addExit("west", places[4])
    places[4].addExit("west", places[5])
    places[4].addExit("south", places[1])
    places[5].addExit("north", places[6])
    places[6].addExit("east", places[7])
    places[7].addExit("east", places[8])
    places[8].setGoal()

    # Start the player in the bottom left
    player = player(places[0])

    return (player, places)

# Alexa Logic

# App starts here
@ask.launch
def launchSkill():
    welcome_message = "Welcome to the Mystic Door 3 by 3 maze adventure. Would you like to check your status or move?"
    return question(welcome_message)


# Tells where the player is and their movement options
@ask.intent("StatusIntent")
def status():
    location = "You are located at %s." % (player.location.getDescription())
    options = player.location.getOptions()
    if options.length = 0:
        response = "You are trapped."
    elif options.length = 1:
        response = "Your only option is %s." % (options.keys()[0])
    else:
        response = "Your options are {}.".format(options.keys())

    return statement(reponse)


# User tries to move in a direction
@ask.intent("MoveIntent")
def move(direction):
    options = player.location.getOptions()
    if direction in options.keys():
        player.location = options[direction]
        result = "You moved %s to %s." % (direction, player.location.getDescription())
    else:
        result = "You can't move that direction."

    if player.location.isGoal():
        result += " You have reached the end of the maze."
        get_data(player, places)

    return statement(result)

if __name__ == '__main__':
    app.run(debug=True)
