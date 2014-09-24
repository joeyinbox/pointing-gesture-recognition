#! /usr/bin/python
import base64, cv2, json, os, os.path, re
import numpy as np

from os import listdir
from os.path import isfile, join



# Definition of the Utils class
class Utils:
	
	# Write array values to a file
	# 
	# @param	data				Data to write
	# @param	filename			File to create or modify
	# @return	None
	def writeToFile(self, data, filename):
	    f = open(filename, 'w')
	    f.write(data)
	
	
	# Dump the content of an object to a json file
	# 
	# @param	data				Data to write
	# @param	filename			File to create or modify
	# @return	None
	def dumpJsonToFile(self, data, filename):
		# Checks if the file already exists
		if os.path.isfile(filename):
			if not os.access(filename, os.R_OK):
				print "Access denied for file {0}".format(filename)
			else:
				print "File {0} already exists...".format(filename)
		else:
			with open(filename, 'w') as output:
				json.dump(data, output)
	
	
	# Load the content of a json file to an array
	# 
	# @param	filename			File to read the data from
	# @return	string				JSON encoded string of the data
	def loadJsonFromFile(self, filename):
		json_data = open(filename)
		data = json.load(json_data)
		json_data.close()
		
		return json.loads(data)
	
	
	# Encode a frame to base64
	# 
	# @param	frame				Value to process
	# @return	string				Base64 encoded string of the parameter data
	def getBase64(self, frame):
		tmp = cv2.imencode('.png', frame)[1]
		return base64.encodestring(tmp)
	
	
	# Return the number of files within a folder (recursively)
	# 
	# @param	folder				Folder to evaluate
	# @return	numeric				Total of files within the given folder
	def getFileNumberInFolder(self, folder):
		total = 0
		
		for root, dirs, files in os.walk(folder):
			for file in files:
				if re.match(r"(.+)\.json$", file):
					total += 1
		
		return total
	
	
	# Return all files from a folder
	# 
	# @param	path				Path to process
	# @return	array				Array of the file paths contained in the given folder
	def getFileList(self, path):
		return [path+f for f in listdir(path) if isfile(join(path,f)) and f!=".DS_Store"]
	
	
	# Return the python code to initialise a numpy array
	# 
	# @param	data				Array to process
	# @param	name				Name of the Python variable
	# @return	None
	def getPythonInitCode(self, data, name):
		print "if {0}:\n\treturn np.array([".format(name)
		
		for i in range(len(data)):
			text = "	["
			for j in range(len(data[i])):
				text+= "{0}".format(str(data[i][j]))
				if j<len(data[i])-1:
					text += ","
			text += "]"
			if i<len(data)-1:
				text += ","
			print text
		
		print "])"
		
	
	# Return the depth value of a point from the depth map
	# 
	# @param	depthMap			Array of the depth map of the captured scene
	# @param	position			Coordinates of the point to get the depth from
	# @return	numeric				Depth of the given coordinates
	def getDepthFromMap(self, depthMap, position):
		if len(depthMap.shape)<=1 or len(position)!=2:
			return 0
			
		y = int(position[0])
		x = int(position[1])
	
		height, width = depthMap.shape
    
		if y<0 or y>=width or x<0 or x>=height:
			return 0
		else:
			return depthMap[x][y]
	
	
	# At 1m, the hand is surrounded with a shift of 90 pixels around its center of gravity
	# 
	# @param	depth				Depth of the hand
	# @return	numeric				Advised bound around the hand in relation with its depth
	def getHandBoundShift(self, depth):
		if depth == 0:
			return 90
		else:
			return int((1000/float(depth))*90)