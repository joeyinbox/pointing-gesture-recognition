#! /usr/bin/python
import json, utils
from copy import deepcopy
from classes.Settings import *


class Dataset:
	LEFT_HAND = 0
	RIGHT_HAND = 1
	
	
	def __init__(self):
		self.settings = Settings()
		
		self.camera_height = 1500
		self.target = {
			"distance": 0,
			"angle": 0,
			"height": 0
		}
		self.fingerTip = {
			"distance": 0,
			"angle": 0,
			"height": 0,
			"position" : [0,0]
		}
		self.eye = {
			"distance": 0,
			"angle": 0,
			"height": 0,
			"position" : [0,0]
		}
		self.hand = Dataset.LEFT_HAND
		self.orientation = self.settings.BACK_RIGHT
		self.direction = self.settings.UP
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
		filename = self.settings.getCompleteDatasetFolder(self.orientation, self.direction)
		
		# Retrieve the number of files saved so far
		# Be careful that due to the sample file, the counter does not need to be incremented. Otherwise, the files would replace each others
		filename += str(utils.getFileNumberInFolder(self.settings.getDatasetFolder())).zfill(3)+".json"
		utils.dumpJsonToFile(self.to_JSON(), filename)
		
		# Re-initialise finger-tip and eye positions
		self.fingerTip["position"] = [0,0]
		self.eye["position"] = [0,0]
	
	def validateValue(self, obj):
		if obj.value.value == "":
			return 0
		else:
			return int(obj.value.value)
	
	
	def toggleHand(self, value):
		self.hand = value
		print "hand toggled to {0}".format(value)
	
	def toggleOrientation(self, value):
		self.orientation = value
		print "orientation toggled to {0}".format(value)
	
	def toggleDirection(self, value):
		self.direction = value
		print "direction toggled to {0}".format(value)
	
	
	
	def setTargetHeight(self, obj, value):
		self.target["height"] = self.validateValue(obj)
		
	def setTargetDistance(self, obj, value):
		self.target["distance"] = self.validateValue(obj)
	
	def setTargetAngle(self, obj, value):
		self.target["angle"] = self.validateValue(obj)
	
	
	
	def setEyeHeight(self, obj, value):
		self.eye["height"] = self.validateValue(obj)
		
	def setEyeDistance(self, obj, value):
		self.eye["distance"] = self.validateValue(obj)
	
	def setEyeAngle(self, obj, value):
		self.eye["angle"] = self.validateValue(obj)
	
	def setEyePosition(self, value):
		self.eye["position"] = value
	
	
	
	def setFingerTipHeight(self, obj, value):
		self.fingerTip["height"] = self.validateValue(obj)
		
	def setFingerTipDistance(self, obj, value):
		self.fingerTip["distance"] = self.validateValue(obj)
	
	def setFingerTipAngle(self, obj, value):
		self.fingerTip["angle"] = self.validateValue(obj)
	
	def setFingerTipPosition(self, value):
		self.fingerTip["position"] = value
	
	
	
	def setCameraHeight(self, obj, value):
		self.camera_height = self.validateValue(obj)