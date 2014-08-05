#! /usr/bin/python
import base64, cv2, json, os, re
import numpy as np


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
	
	return json.loads(data)


# Encode a frame to base64
def getBase64(frame):
	tmp = cv2.imencode('.png', frame)[1]
	return base64.encodestring(tmp)


# Return the number of files within a folder
def getFileNumberInFolder(folder):
	total = 0
	
	for root, dirs, files in os.walk(folder):
		for file in files:
			if re.match(r"(.+)\.json$", file):
				total += 1
	
	return total