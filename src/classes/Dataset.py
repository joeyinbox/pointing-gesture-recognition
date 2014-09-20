#! /usr/bin/python
import json, utils
import numpy as np
from copy import deepcopy
from classes.Settings import *
from classes.Utils import Utils


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
	
	
	def __init__(self, camera_height=None, hand=None, skeleton=None, depth_map=None, image=None, type=None, distance=None, target=None):
		self.settings = Settings()
		self.utils = Utils()
		
		
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
	
	def to_JSON(self):
		# Update the depth map and the image to prepare them
		self.depth_map = self.depth_map.tolist()
		self.image = self.utils.getBase64(self.image)
		
		obj = deepcopy(self)
		del obj.settings
		del obj.utils
		
		return json.dumps(obj, default=lambda o: o.__dict__, separators=(',', ':'))
	
	
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
	
	
	
	
	def toggleType(self, value):
		self.type = value
		print "type toggled to {0}".format(value)
		
	def toggleDistance(self, value):
		self.distance = value
		print "distance toggled to {0}".format(value)
		
	def setDistance(self, value):
		self.distance = value
		print "distance changed to {0}".format(value)
	
	def toggleHand(self, value):
		self.hand = value
		print "hand toggled"
	
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