from pymongo import MongoClient
from player import *
from place import *
from item import *

### Game class structure ###
# title: string object, represents the title of the adventure
# player: Player object, represents the player
# places: dictionary, key is the id of each place, value is the corresponding Place object
# items: dictionary, key is the id of each item, value is the corresponding Item object

### Game class currently only work with localhost
### The name of the database should be "MysticDoorRecords"
### The collection that holds the game records is called "records"

class Game(object):
	#on initialization, establishes a connection with the database and pulls the necessary information
	def __init__(self, file):
		client = MongoClient('localhost', 27017)
		db = client['MysticDoorRecords']
		records = db.records
		savefile = records.find_one({'filename' : file})
		self.filename = file
		self.title = savefile['title']
		self.player = Player(savefile['player'])
		self.places = {}
		places_list = savefile['places']
		for element in places_list:
			self.places[element['id']] = Place(element)
		self.items = {}
		items_list = savefile['items']
		for element in items_list:
			self.items[element['id']] = Item(element)

	#returns the item with the matching id
	def getItem(self, id):
		return self.items[id]

	#returns a dictionary of all items where the key is the id and the value is the item
	def getAllItems(self):
		return self.items

	#returns the place with the matching id
	def getPlace(self, id):
		return self.places[id]

	#returns a dictionary of all places, where the key is the id and the value is the place
	def getAllPlaces(self):
		return self.places

	#returns the player
	def getPlayer(self):
		return self.player

	#returns the title of the adventure
	def GetTitle(self):
		return self.title

	#stores the current state of the game in a record, replacing the old record
	#     if necessary, functionality can be expanded to allow for multiple
	#     files pertaining to the same adventure
	def save(self):
		client = MongoClient('localhost', 27017)
		db = client['MysticDoorRecords']
		records = db.records
		post = {}
		post['player'] = self.player.export()
		post['title'] = self.title
		post['places'] = []
		for k, v in self.places.items():
			post['places'].append(v.export())
		post['items'] = []
		for k, v in self.items.items():
			post['items'].append(v.export())
		post['filename'] = self.filename

		records.delete_one({'filename' : self.filename})
		records.insert_one(post)









