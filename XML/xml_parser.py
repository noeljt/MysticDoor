import xml.etree.ElementTree as ET
import json
from xmljson import Cobra
from collections import OrderedDict
from json import dumps


def parsexml(file):
	tree = ET.parse(file)
	root = tree.getroot()
	r = []
	for room in root.findall('place'):
		t = {}
		t['id'] = room.get('id')
		t['desc'] = room.find('desc').text
		if room.find('goal').text == 'true':
			t['goal'] = True
		else:
			t['goal'] = False
		if room.find('north').text == None:
			t['north'] = "-1"
		else:
			t['north'] = room.find('north').text
		if room.find('east').text == None:
			t['east'] = "-1"
		else:
			t['east'] = room.find('east').text
		if room.find('south').text == None:
			t['south'] = "-1"
		else:
			t['south'] = room.find('south').text
		if room.find('west').text == None:
			t['west'] = "-1"
		else:
			t['west'] = room.find('west').text

		r.append(t)
	return r

def parseXmlToJson(file):
	c = Cobra()
	r = c.data(ET.parse(file).getroot())
	return r

results = parseXmlToJson("place_only.xml")
print(dumps(results))