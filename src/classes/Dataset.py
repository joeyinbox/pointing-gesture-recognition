#! /usr/bin/python
import json, utils
from copy import deepcopy
from classes.Settings import *


class Dataset:
	TYPE_TRAINING = 0
	TYPE_TESTING_POSITIVE = 1
	TYPE_TESTING_NEGATIVE = 2
	
	LEFT_HAND = 0
	RIGHT_HAND = 1
	NO_HAND = 2
	
	def __init__(self):
		self.settings = Settings()
		
		self.camera_height = 1500
		self.user = {
			"arm_length": 0,
			"height": 0,
			"distance": 0,
			"angle": 0
		}
		self.target = {
			"distance": 0,
			"angle": 0,
			"height": 0
		}
		self.hand = {
			"type": Dataset.LEFT_HAND,
			"height": 0,
			"width": 0,
			"thickness": 0
		}
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
		self.finger = []
		self.depth_map = []
		self.image = ""
		self.type = Dataset.TYPE_TRAINING
	
	
	def to_JSON(self):
		# Update the depth map and the image to prepare them
		self.depth_map = utils.convertOpenNIDepthMapToArray(self.depth_map)
		self.image = utils.getBase64(self.image)
		
		obj = deepcopy(self)
		del obj.settings
		
		return json.dumps(obj, default=lambda o: o.__dict__, separators=(',', ':'))
	
	
	def save(self):
		print "Saving dataset informations..."
		
		# Save the dataset to the right folder
		if self.type == Dataset.TYPE_TRAINING:
			filename = self.settings.getTrainingFolder()
		elif self.type == Dataset.TYPE_TESTING_POSITIVE:
			filename = self.settings.getPositiveTestingFolder()
		elif self.type == Dataset.TYPE_TESTING_NEGATIVE:
			filename = self.settings.getNegativeTestingFolder()
		else:
			filename = ""
		
		# Retrieve the number of files saved so far
		# Be careful that due to the sample file, the counter does not need to be incremented. Otherwise, the files would replace each others
		filename += str(utils.getFileNumberInFolder(self.settings.getDatasetFolder())).zfill(3)+".json"
		utils.dumpJsonToFile(self.to_JSON(), filename)
		
		# Re-initialise the finger-tip position
		self.finger = []
	
	
	
	
	def toggleTraining(self, obj, value):
		if value == "True":
			self.type = Dataset.TYPE_TRAINING
			print "Training"
	
	def togglePositiveTesting(self, obj, value):
		if value == "True":
			self.type = Dataset.TYPE_TESTING_POSITIVE
			print "Positive testing"
	
	def toggleNegativeTesting(self, obj, value):
		if value == "True":
			self.type = Dataset.TYPE_TESTING_NEGATIVE
			print "Negative testing"
	
	
	def toggleLeftHand(self, obj, value):
		if value == "True":
			self.hand["type"] = Dataset.LEFT_HAND
			print "Left hand"
	
	def toggleRightHand(self, obj, value):
		if value == "True":
			self.hand["type"] = Dataset.RIGHT_HAND
			print "Right hand"
	
	def toggleNoHand(self, obj, value):
		if value == "True":
			self.hand["type"] = Dataset.NO_HAND
			print "No hand"
	
	
	def setCameraHeight(self, obj, value):
		self.camera_height = int(obj.value.value)
	
	def setUserArmLength(self, obj, value):
		self.user["arm_length"] = int(obj.value.value)
	
	def setUserHeight(self, obj, value):
		self.user["height"] = int(obj.value.value)
		
	def setUserDistance(self, obj, value):
		self.user["distance"] = int(obj.value.value)
	
	def setUserAngle(self, obj, value):
		self.user["angle"] = int(obj.value.value)
	
	def setTargetHeight(self, obj, value):
		self.target["height"] = int(obj.value.value)
		
	def setTargetDistance(self, obj, value):
		self.target["distance"] = int(obj.value.value)
	
	def setTargetAngle(self, obj, value):
		self.target["angle"] = int(obj.value.value)
	
	def setHandHeight(self, obj, value):
		self.hand["height"] = int(obj.value.value)
	
	def setHandWidth(self, obj, value):
		self.hand["width"] = int(obj.value.value)
		
	def setHandThickness(self, obj, value):
		self.hand["thickness"] = int(obj.value.value)