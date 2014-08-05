#! /usr/bin/python
import json, utils
from copy import deepcopy
from classes.Settings import *


class LightDataset:
	TYPE_POSITIVE = 0
	TYPE_NEGATIVE = 1
	
	LEFT_HAND = 0
	RIGHT_HAND = 1
	NO_HAND = 2
	
	DISTANCE_550 = 0
	DISTANCE_1000 = 1
	DISTANCE_1500 = 2
	DISTANCE_2000 = 3
	
	
	def __init__(self):
		
		print "light dataset chosen"
		
		self.settings = Settings()
		
		self.camera_height = 1500
		self.hand = LightDataset.LEFT_HAND
		self.skeleton = {
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
		self.depth_map = []
		self.image = ""
		self.type = LightDataset.TYPE_POSITIVE
		self.distance = LightDataset.DISTANCE_550
		
	
	def to_JSON(self):
		# Update the depth map and the image to prepare them
		self.depth_map = self.depth_map.tolist()
		self.image = utils.getBase64(self.image)
		
		obj = deepcopy(self)
		del obj.settings
		
		return json.dumps(obj, default=lambda o: o.__dict__, separators=(',', ':'))
	
	
	def save(self):
		print "Saving dataset informations..."
		
		# Save the dataset to the right folder
		if self.type == LightDataset.TYPE_POSITIVE:
			filename = self.settings.getPositiveLightFolder()
		elif self.type == LightDataset.TYPE_NEGATIVE:
			filename = self.settings.getNegativeLightFolder()
		else:
			filename = ""
		
		# Retrieve the number of files saved so far
		# Be careful that due to the sample file, the counter does not need to be incremented. Otherwise, the files would replace each others
		filename += str(utils.getFileNumberInFolder(filename)).zfill(3)+".json"
		utils.dumpJsonToFile(self.to_JSON(), filename)
	
	
	
	
	def toggleType(self, value):
		self.type = value
		print "type toggled"
		
	def toggleDistance(self, value):
		self.distance = value
		print "distance toggled"
	
	def toggleHand(self, value):
		self.hand = value
		print "hand toggled"
	
	def getWishedDistance(self):
		if self.distance == LightDataset.DISTANCE_550:
			return 550
		elif self.distance == LightDataset.DISTANCE_1000:
			return 1000
		elif self.distance == LightDataset.DISTANCE_1500:
			return 1500
		elif self.distance == LightDataset.DISTANCE_2000:
			return 2000