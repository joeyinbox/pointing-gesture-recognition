#! /usr/bin/python
import json


# Write array values to a file
def writeToFile(data, filename):
    f = open(filename, 'w')
    f.write(data)


# Prompt the user for a float value
def promptFloat(question, default):
	try:
		if int(default) == 0:
			return float(raw_input(question+": "))
		else:
			return float(raw_input(question+" (default: %f): "%(default)))
	except: 
		return float(default)

# Prompt the user for an int value
def promptInt(question, default):
	try:
		if int(default) == 0:
			return int(raw_input(question+": "))
		else:
			return int(raw_input(question+" (default: %d): "%(default)))
	except: 
		return int(default)


# Dump the content of an object to a json file
def dumpJsonToFile(data, filename):
	with open(filename, 'w') as output:
		json.dump(data, output)

# Load the content of a json file to an object
def loadJsonFromFile(filename):
	json_data = open(filename)
	data = json.load(json_data)
	json_data.close()
	return data