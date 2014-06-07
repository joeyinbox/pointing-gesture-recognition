#! /usr/bin/python
import json, utils


class Dataset:
	TYPE_TRAINING = 0
	TYPE_TESTING_POSITIVE = 1
	TYPE_TESTING_NEGATIVE = 2
	
	def __init__(self):
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
		
		return json.dumps(self, default=lambda o: o.__dict__, separators=(',', ':'))
	
	
	def save(self):
		print "Saving dataset informations..."
		utils.dumpJsonToFile(self.to_JSON(), "../dataset/yay.json")
	
	
	
	
	def toggleTraining(self, obj, value):
		if value == True:
			self.type = Dataset.TYPE_TRAINING
	
	def togglePositiveTesting(self, obj, value):
		if value == True:
			self.type = Dataset.TYPE_TESTING_POSITIVE
	
	def toggleNegativeTesting(self, obj, value):
		if value == True:
			self.type = Dataset.TYPE_TESTING_NEGATIVE
	
	
	def setCameraHeight(self, obj, value):
		self.camera_height = obj.value
	
	def setUserArmLength(self, obj, value):
		self.user["arm_length"] = obj.value
	
	def setUserHeight(self, obj, value):
		self.user["height"] = obj.value
		
	def setUserDistance(self, obj, value):
		self.user["distance"] = obj.value
	
	def setUserAngle(self, obj, value):
		self.user["angle"] = obj.value
	
	def setTargetHeight(self, obj, value):
		self.target["height"] = obj.value
		
	def setTargetDistance(self, obj, value):
		self.target["distance"] = obj.value
	
	def setTargetAngle(self, obj, value):
		self.target["angle"] = obj.value
	
	def setHandHeight(self, obj, value):
		self.hand["height"] = obj.value
	
	def setHandWidth(self, obj, value):
		self.hand["width"] = obj.value
		
	def setHandThickness(self, obj, value):
		self.hand["thickness"] = obj.value