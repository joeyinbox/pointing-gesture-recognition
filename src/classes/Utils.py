#! /usr/bin/python
import base64, cv2, json, os, os.path, re
import numpy as np

from os import listdir
from os.path import isfile, join


class Utils:
	
	# Write array values to a file
	def writeToFile(self, data, filename):
	    f = open(filename, 'w')
	    f.write(data)
	
	# Dump the content of an object to a json file
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
	def loadJsonFromFile(self, filename):
		json_data = open(filename)
		data = json.load(json_data)
		json_data.close()
		
		return json.loads(data)
	
	
	# Encode a frame to base64
	def getBase64(self, frame):
		tmp = cv2.imencode('.png', frame)[1]
		return base64.encodestring(tmp)
	
	
	# Return the number of files within a folder
	def getFileNumberInFolder(self, folder):
		total = 0
		
		for root, dirs, files in os.walk(folder):
			for file in files:
				if re.match(r"(.+)\.json$", file):
					total += 1
		
		return total
	
	# Return all files from a folder
	def getFileList(self, path):
		return [path+f for f in listdir(path) if isfile(join(path,f)) and f!=".DS_Store"]
	
	# Return the python code to initialise a numpy array
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
	def getHandBoundShift(self, depth):
		if depth == 0:
			return 90
		else:
			return int((1000/float(depth))*90)