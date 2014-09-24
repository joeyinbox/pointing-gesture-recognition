#! /usr/bin/python
import json, utils
import numpy as np
from copy import deepcopy
from classes.Settings import *
from classes.Utils import Utils



# Definition of the Dataset class
class Dataset:
	TYPE_POSITIVE = 0
	TYPE_NEGATIVE = 1
	TYPE_ACCURACY = 2
	TYPE_HEATMAP = 3
	
	LEFT_HAND = 0
	RIGHT_HAND = 1
	NO_HAND = 2
	
	DISTANCE_550 = 0
	DISTANCE_750 = 4
	DISTANCE_1000 = 1
	DISTANCE_1250 = 5
	DISTANCE_1500 = 2
	DISTANCE_1750 = 6
	DISTANCE_2000 = 3
	
	
	# Constructor of the Dataset class
	# 
	# @param	camera_height		Value of the camera height while gathering informations
	# @param	hand				Identifier of the hand (Ø|1|2)
	# @param	skeleton			Skeletal joints of the detected subject
	# @param	depth_map			Depth map of the captured scene
	# @param	image				RGB image of the captured scene
	# @param	type				Identifier of the type of data (0|1|2|3)
	# @param	distance			Identifier of the type of distance chosen (0|1|2|3|4|5|6) or the actual distance between the fingertip and the target
	# @param	target				Coordinates of the target
	# @return	None
	def __init__(self, camera_height=None, hand=None, skeleton=None, depth_map=None, image=None, type=None, distance=None, target=None):
		self.settings = Settings()
		self.utils = Utils()
		
		# Initialise each attributes with respective parameters; otherwise with a default value
		if camera_height is None:
			camera_height = 1500
		self.camera_height = camera_height
		
		if hand is None:
			hand = self.settings.LEFT_HAND
		self.hand = hand
		
		if skeleton is None:
			skeleton = {
				"head": [],
				"shoulder": {
					"left": [],
					"right": [],
					"center": []
				},
				"elbow": {
					"left": [],
					"right": []
				},
				"hand": {
					"left": [],
					"right": []
				}
			}
		self.skeleton = skeleton
		
		if depth_map is None:
			depth_map = []
		self.depth_map = np.array(depth_map)
		
		if image is None:
			image = ""
		self.image = image
		
		if type is None:
			type = Dataset.TYPE_POSITIVE
		self.type = type
		
		if distance is None:
			distance = Dataset.DISTANCE_550
		self.distance = distance
		
		if target is None:
			target = []
		self.target = target
	
	
	
	# Returns a JSON encoded string of the dataset object
	# 
	# @param	None
	# @return	string				JSON encoded string of the dataset object
	def to_JSON(self):
		# Convert the depth map to a serializable state
		self.depth_map = self.depth_map.tolist()
		
		# Encode the RGB image in a base64 string
		self.image = self.utils.getBase64(self.image)
		
		# Get rid of extra attributes to clean the output
		obj = deepcopy(self)
		del obj.settings
		del obj.utils
		
		return json.dumps(obj, default=lambda o: o.__dict__, separators=(',', ':'))
	
	
	
	# Save the dataset informations as a file
	# 
	# @param	None
	# @return	None
	def save(self):
		print "Saving dataset informations..."
		
		# Save the dataset to the right folder
		if self.type == Dataset.TYPE_POSITIVE:
			filename = self.settings.getPositiveFolder()
		elif self.type == Dataset.TYPE_NEGATIVE:
			filename = self.settings.getNegativeFolder()
		elif self.type == Dataset.TYPE_ACCURACY:
			filename = self.settings.getAccuracyFolder()
		else:
			raise ValueError("Invalid type of dataset to save", self.type)
		
		# Retrieve the number of files saved so far
		# Be careful that due to the sample file, the counter does not need to be incremented. Otherwise, the files would replace each others
		filename += str(self.utils.getFileNumberInFolder(filename)).zfill(3)+".json"
		self.utils.dumpJsonToFile(self.to_JSON(), filename)
	
	
	# Toggle the type identifier of the dataset
	# 
	# @param	value				Identifier of the new type of the dataset
	# @return	None
	def toggleType(self, value):
		self.type = value
		print "type toggled to {0}".format(value)
	
	
	# Toggle the distance identifier of the dataset
	# 
	# @param	value				Identifier of the new distance of the dataset
	# @return	None
	def toggleDistance(self, value):
		self.distance = value
		print "distance toggled to {0}".format(value)
	
	
	# Update the distance of the dataset
	# 
	# @param	value				Distance value
	# @return	None
	def setDistance(self, value):
		self.distance = value
		print "distance changed to {0}".format(value)
	
	
	# Toggle the hand identifier of the dataset
	# 
	# @param	value				Identifier of the new hand of the dataset
	# @return	None
	def toggleHand(self, value):
		self.hand = value
		print "hand toggled"
	
	
	# Returns the actual distance
	# 
	# @param	None
	# @return	numeric				Actual distance value (translated if identifier)
	def getWishedDistance(self):
		if self.distance == Dataset.DISTANCE_550:
			return 550
		elif self.distance == Dataset.DISTANCE_750:
			return 750
		elif self.distance == Dataset.DISTANCE_1000:
			return 1000
		elif self.distance == Dataset.DISTANCE_1250:
			return 1250
		elif self.distance == Dataset.DISTANCE_1500:
			return 1500
		elif self.distance == Dataset.DISTANCE_1750:
			return 1750
		elif self.distance == Dataset.DISTANCE_2000:
			return 2000
		else:
			return self.distance