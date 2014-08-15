#! /usr/bin/python
from classes.Dataset import *
from classes.Settings import *
from classes.Utils import *

import numpy as np
import sys



class DatasetManager():
	
	# Load settings
	settings = Settings()
	utils = Utils()
	
	
	# Load all dataset files
	def loadDataset(self, dataset):
		data = []
		
		for i in dataset:
			for j in i:
				name = j.split("/")
				print("Loading {0}/{1}/{2}/{3}".format(name[-4], name[-3], name[-2], name[-1]))
				data.append(self.createDatasetFromRawData(self.utils.loadJsonFromFile(str(j))))
		return data
	
	# Create a new Dataset object from raw data
	def createDatasetFromRawData(self, data):
		return Dataset(
			camera_height = data.get("camera_height", 1500), 
			hand = data.get("hand", 0), 
			skeleton = data.get("skeleton", []), 
			depth_map = data.get("depth_map", []), 
			image = data.get("image", ""), 
			type = data.get("type", 0), 
			distance = data.get("distance", 0), 
			target = data.get("target", [0,0,0]))
	
	# Return all positive files from a specified type separately (training, testing or validating)
	def getPositiveComplete(self, type="training"):
		if type!="training" and type!="testing" and type!="validating":
			raise "Invalid type of dataset wanted", type
		
		folder = self.settings.getPositiveFolder()
		
		return np.array([
			self.utils.getFileList("{0}{1}/back-right/up/".format(folder, type)),
			self.utils.getFileList("{0}{1}/back-right/lateral/".format(folder, type)),
			self.utils.getFileList("{0}{1}/back-right/down/".format(folder, type)),
			
			self.utils.getFileList("{0}{1}/right/up/".format(folder, type)),
			self.utils.getFileList("{0}{1}/right/lateral/".format(folder, type)),
			self.utils.getFileList("{0}{1}/right/down/".format(folder, type)),
			
			self.utils.getFileList("{0}{1}/front-right/up/".format(folder, type)),
			self.utils.getFileList("{0}{1}/front-right/lateral/".format(folder, type)),
			self.utils.getFileList("{0}{1}/front-right/down/".format(folder, type)),
			
			self.utils.getFileList("{0}{1}/front/up/".format(folder, type)),
			self.utils.getFileList("{0}{1}/front/lateral/".format(folder, type)),
			self.utils.getFileList("{0}{1}/front/down/".format(folder, type)),
			
			self.utils.getFileList("{0}{1}/front-left/up/".format(folder, type)),
			self.utils.getFileList("{0}{1}/front-left/lateral/".format(folder, type)),
			self.utils.getFileList("{0}{1}/front-left/down/".format(folder, type)),
			
			self.utils.getFileList("{0}{1}/left/up/".format(folder, type)),
			self.utils.getFileList("{0}{1}/left/lateral/".format(folder, type)),
			self.utils.getFileList("{0}{1}/left/down/".format(folder, type)),
			
			self.utils.getFileList("{0}{1}/back-left/up/".format(folder, type)),
			self.utils.getFileList("{0}{1}/back-left/lateral/".format(folder, type)),
			self.utils.getFileList("{0}{1}/back-left/down/".format(folder, type))
		])
	#END_DEF getPositiveComplete
	
	
	# Return all positive files from a specified type by orientation (training, testing or validating)
	def getPositiveMixed(self, type="training"):
		if type!="training" and type!="testing" and type!="validating":
			raise "Invalid type of dataset wanted", type
		
		folder = self.settings.getPositiveFolder()
		
		backRight = self.utils.getFileList("{0}{1}/back-right/up/".format(folder, type))
		backRight.extend(self.utils.getFileList("{0}{1}/back-right/lateral/".format(folder, type)))
		backRight.extend(self.utils.getFileList("{0}{1}/back-right/down/".format(folder, type)))
		
		right = self.utils.getFileList("{0}{1}/right/up/".format(folder, type))
		right.extend(self.utils.getFileList("{0}{1}/right/lateral/".format(folder, type)))
		right.extend(self.utils.getFileList("{0}{1}/right/down/".format(folder, type)))
		
		frontRight = self.utils.getFileList("{0}{1}/front-right/up/".format(folder, type))
		frontRight.extend(self.utils.getFileList("{0}{1}/front-right/lateral/".format(folder, type)))
		frontRight.extend(self.utils.getFileList("{0}{1}/front-right/down/".format(folder, type)))
		
		front = self.utils.getFileList("{0}{1}/front/up/".format(folder, type))
		front.extend(self.utils.getFileList("{0}{1}/front/lateral/".format(folder, type)))
		front.extend(self.utils.getFileList("{0}{1}/front/down/".format(folder, type)))
		
		frontLeft = self.utils.getFileList("{0}{1}/front-left/up/".format(folder, type))
		frontLeft.extend(self.utils.getFileList("{0}{1}/front-left/lateral/".format(folder, type)))
		frontLeft.extend(self.utils.getFileList("{0}{1}/front-left/down/".format(folder, type)))
		
		left = self.utils.getFileList("{0}{1}/left/up/".format(folder, type))
		left.extend(self.utils.getFileList("{0}{1}/left/lateral/".format(folder, type)))
		left.extend(self.utils.getFileList("{0}{1}/left/down/".format(folder, type)))
		
		backLeft = self.utils.getFileList("{0}{1}/back-left/up/".format(folder, type))
		backLeft.extend(self.utils.getFileList("{0}{1}/back-left/lateral/".format(folder, type)))
		backLeft.extend(self.utils.getFileList("{0}{1}/back-left/down/".format(folder, type)))
		
		
		return np.array([
			backRight,
			right,
			frontRight,
			front,
			frontLeft,
			left,
			backLeft
		])
	#END_DEF getPositiveMixed
	
	
	# Return main positive files from a specified type by orientation (training, testing or validating)
	def getPositiveRestrainedMixed(self, type="training"):
		if type!="training" and type!="testing" and type!="validating":
			raise "Invalid type of dataset wanted", type
		
		folder = self.settings.getPositiveFolder()
		
		right = self.utils.getFileList("{0}{1}/right/up/".format(folder, type))
		right.extend(self.utils.getFileList("{0}{1}/right/lateral/".format(folder, type)))
		right.extend(self.utils.getFileList("{0}{1}/right/down/".format(folder, type)))
		
		frontRight = self.utils.getFileList("{0}{1}/front-right/up/".format(folder, type))
		frontRight.extend(self.utils.getFileList("{0}{1}/front-right/lateral/".format(folder, type)))
		frontRight.extend(self.utils.getFileList("{0}{1}/front-right/down/".format(folder, type)))
		
		frontLeft = self.utils.getFileList("{0}{1}/front-left/up/".format(folder, type))
		frontLeft.extend(self.utils.getFileList("{0}{1}/front-left/lateral/".format(folder, type)))
		frontLeft.extend(self.utils.getFileList("{0}{1}/front-left/down/".format(folder, type)))
		
		left = self.utils.getFileList("{0}{1}/left/up/".format(folder, type))
		left.extend(self.utils.getFileList("{0}{1}/left/lateral/".format(folder, type)))
		left.extend(self.utils.getFileList("{0}{1}/left/down/".format(folder, type)))
		
		
		return np.array([
			right,
			frontRight,
			frontLeft,
			left
		])
	#END_DEF getPositiveRestrainedMixed
	
	
	# Return all negative files from a specified type separately (training, testing or validating)
	def getNegativeComplete(self, type="training"):
		if type!="training" and type!="testing" and type!="validating":
			raise "Invalid type of dataset wanted", type
		
		folder = self.settings.getNegativeFolder()
		
		output = self.utils.getFileList("{0}{1}/back-right/closed/".format(folder, type))
		output.extend(self.utils.getFileList("{0}{1}/back-right/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/back-right/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/back-right/three/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/back-right/peace/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/back-right/rock/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/right/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/right/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/right/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/right/three/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/right/peace/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/right/rock/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/front-right/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/three/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/peace/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/rock/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/front/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front/three/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front/peace/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front/rock/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/front-left/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/three/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/peace/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/rock/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/left/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/three/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/peace/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/rock/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/back-left/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/back-left/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/back-left/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/back-left/three/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/back-left/peace/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/back-left/rock/".format(folder, type)))
		
		return np.array([output])
	#END_DEF getNegativeComplete
	
	
	# Return all main negative files from a specified type by orientation (training, testing or validating)
	def getNegativeRestrained(self, type="training"):
		if type!="training" and type!="testing" and type!="validating":
			raise "Invalid type of dataset wanted", type
		
		folder = self.settings.getNegativeFolder()
		
		output = self.utils.getFileList("{0}{1}/right/closed/".format(folder, type))
		output.extend(self.utils.getFileList("{0}{1}/right/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/right/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/right/three/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/right/peace/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/right/rock/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/front-right/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/three/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/peace/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/rock/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/front-left/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/three/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/peace/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/rock/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/left/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/three/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/peace/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/rock/".format(folder, type)))
		
		return np.array([output])
	#END_DEF getNegativeRestrained
	
	
	# Return only main negative files from a specified type by orientation (training, testing or validating)
	def getNegativeMainRestrained(self, type="training"):
		if type!="training" and type!="testing" and type!="validating":
			raise "Invalid type of dataset wanted", type
		
		folder = self.settings.getNegativeFolder()
		
		output = self.utils.getFileList("{0}{1}/right/closed/".format(folder, type))
		output.extend(self.utils.getFileList("{0}{1}/right/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/right/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/right/three/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/front-right/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/three/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/front-left/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/three/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/left/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/four/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/three/".format(folder, type)))
		
		return np.array([output])
	#END_DEF getNegativeMainRestrained
	
	
	def getCompleteTarget(self):
		return np.array([
			[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
		])
	#END_DEF getCompleteTarget
	
	
	def getMixedTarget(self):
		return np.array([
			[1,0,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,0,1]
		])
	#END_DEF getMixedTarget
	
	
	def getRestrainedMixedTarget(self):
		return np.array([
			[1,0,0,0],
			[0,1,0,0],
			[0,0,1,0],
			[0,0,0,1]
		])
	#END_DEF getRestrainedMixedTarget
	
	