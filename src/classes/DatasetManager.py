#! /usr/bin/python
from classes.Dataset import *
from classes.Settings import *
from classes.Utils import *

import numpy as np
import sys



# Definition of the DatasetManager class
class DatasetManager():
	
	# Load settings
	settings = Settings()
	utils = Utils()
	
	
	# Load all dataset files
	def loadDataset(self, dataset):
		data = []
		count = 0
		
		for i in dataset:
			for j in i:
				name = j.split("/")
				print("{4} Loading {0}/{1}/{2}/{3}".format(name[-4], name[-3], name[-2], name[-1], count))
				data.append(self.createDatasetFromRawData(self.utils.loadJsonFromFile(str(j))))
				count += 1
				
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
			raise ValueError("Invalid type of dataset wanted", type)
		
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
	def getPositiveCompleteMixed(self, type="training"):
		if type!="training" and type!="testing" and type!="validating":
			raise ValueError("Invalid type of dataset wanted", type)
		
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
	#END_DEF getPositiveCompleteMixed
	
	
	# Return main positive files from a specified type separately (training, testing or validating)
	def getPositiveRestrained(self, type="training"):
		if type!="training" and type!="testing" and type!="validating":
			raise ValueError("Invalid type of dataset wanted", type)
		
		folder = self.settings.getPositiveFolder()
		
		return np.array([
			self.utils.getFileList("{0}{1}/right/up/".format(folder, type)),
			self.utils.getFileList("{0}{1}/right/lateral/".format(folder, type)),
			self.utils.getFileList("{0}{1}/right/down/".format(folder, type)),
			
			self.utils.getFileList("{0}{1}/front-right/up/".format(folder, type)),
			self.utils.getFileList("{0}{1}/front-right/lateral/".format(folder, type)),
			self.utils.getFileList("{0}{1}/front-right/down/".format(folder, type)),
			
			self.utils.getFileList("{0}{1}/front-left/up/".format(folder, type)),
			self.utils.getFileList("{0}{1}/front-left/lateral/".format(folder, type)),
			self.utils.getFileList("{0}{1}/front-left/down/".format(folder, type)),
			
			self.utils.getFileList("{0}{1}/left/up/".format(folder, type)),
			self.utils.getFileList("{0}{1}/left/lateral/".format(folder, type)),
			self.utils.getFileList("{0}{1}/left/down/".format(folder, type))
		])
	#END_DEF getPositiveRestrained
	
	
	# Return main positive files from a specified type by orientation (training, testing or validating)
	def getPositiveRestrainedMixed(self, type="training"):
		if type!="training" and type!="testing" and type!="validating":
			raise ValueError("Invalid type of dataset wanted", type)
		
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
			raise ValueError("Invalid type of dataset wanted", type)
		
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
	
	
	# Return main negative files from a specified type separately (training, testing or validating)
	def getMainNegative(self, type="training"):
		if type!="training" and type!="testing" and type!="validating":
			raise ValueError("Invalid type of dataset wanted", type)
		
		folder = self.settings.getNegativeFolder()
		
		output = self.utils.getFileList("{0}{1}/back-right/closed/".format(folder, type))
		output.extend(self.utils.getFileList("{0}{1}/back-right/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/back-right/four/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/right/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/right/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/right/four/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/front-right/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-right/four/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/front/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front/four/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/front-left/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/front-left/four/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/left/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/left/four/".format(folder, type)))
		
		output.extend(self.utils.getFileList("{0}{1}/back-left/closed/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/back-left/opened/".format(folder, type)))
		output.extend(self.utils.getFileList("{0}{1}/back-left/four/".format(folder, type)))
		
		return np.array([output])
	#END_DEF getNegativeComplete
	
	
	# Return all main negative files from a specified type by orientation (training, testing or validating)
	def getNegativeRestrained(self, type="training"):
		if type!="training" and type!="testing" and type!="validating":
			raise ValueError("Invalid type of dataset wanted", type)
		
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
			raise ValueError("Invalid type of dataset wanted", type)
		
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
	
	
	def getCompleteMixedTarget(self):
		return np.array([
			[1,0,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,0,1]
		])
	#END_DEF getCompleteMixedTarget
	
	
	def getRestrainedTarget(self):
		return np.array([
			[1,0,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,0,1,0,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,0,1,0,0,0,0,0,0],
			[0,0,0,0,0,0,1,0,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,0,1,0,0,0],
			[0,0,0,0,0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,0,1]
		])
	#END_DEF getRestrainedTarget
	
	
	def getRestrainedMixedTarget(self):
		return np.array([
			[1,0,0,0],
			[0,1,0,0],
			[0,0,1,0],
			[0,0,0,1]
		])
	#END_DEF getRestrainedMixedTarget
	
	
	def getAccuracyComplete(self):
		folder = self.settings.getAccuracyFolder()
		
		return np.array([
			self.utils.getFileList("{0}back-right/".format(folder)),
			self.utils.getFileList("{0}right/".format(folder)),
			self.utils.getFileList("{0}front-right/".format(folder)),
			self.utils.getFileList("{0}front/".format(folder)),
			self.utils.getFileList("{0}front-left/".format(folder)),
			self.utils.getFileList("{0}left/".format(folder)),
			self.utils.getFileList("{0}back-left/".format(folder))
		])
	#END_DEF getAccuracyComplete
	
	
	def getAccuracyRestrained(self):
		folder = self.settings.getAccuracyFolder()
		
		return np.array([
			self.utils.getFileList("{0}right/".format(folder)),
			self.utils.getFileList("{0}front-right/".format(folder)),
			self.utils.getFileList("{0}front-left/".format(folder)),
			self.utils.getFileList("{0}left/".format(folder))
		])
	#END_DEF getAccuracyComplete
	
	
	def getRecentValuesRestrained(self, trainingInput=False, trainingTarget=False, testingInput=False, testingTarget=False):
		if trainingInput:
			return np.array([
			[-0.936381709742,-0.659045725646,-0.367793240557,-0.541749502982,-0.575546719682,-0.919483101392],
			[-0.929337539432,-0.762776025237,-0.44858044164,-0.605047318612,-0.458675078864,-0.795583596215],
			[-0.957753240518,-0.583293326932,-0.275084013442,-0.595775324052,-0.605376860298,-0.982717234758],
			[-0.995729537367,-0.591459074733,-0.281138790036,-0.71103202847,-0.555871886121,-0.864768683274],
			[-0.95975565936,-0.617678763924,-0.401365432986,-0.664390945023,-0.497664390945,-0.859144807761],
			[-0.699041267195,-0.302209253856,-0.852438516048,-1.0,-0.821592330138,-0.324718632764],
			[-0.953565505804,-0.653399668325,-0.300165837479,-0.599502487562,-0.56135986733,-0.932006633499],
			[-0.978039215686,-0.638431372549,-0.27137254902,-0.621176470588,-0.55137254902,-0.939607843137],
			[-0.868372943327,-0.586837294333,-0.352833638026,-0.620658135283,-0.604204753199,-0.967093235832],
			[-0.870759289176,-0.511039310716,-0.366720516963,-0.685514270328,-0.586429725363,-0.979536887453],
			[-0.851654215582,-0.628601921025,-0.640341515475,-0.677694770544,-0.579509071505,-0.62219850587],
			[-1.0,-0.733382570162,-0.498522895126,-0.710487444609,-0.525110782866,-0.532496307238],
			[-0.645982498011,-0.376292760541,-0.838504375497,-0.978520286396,-0.761336515513,-0.399363564041],
			[-0.897332662305,-0.53598389532,-0.559134373427,-0.68495218923,-0.622546552592,-0.700050327126],
			[-0.950629722922,-0.545591939547,-0.557682619647,-0.705793450882,-0.566750629723,-0.67355163728],
			[-1.0,-0.721428571429,-0.433928571429,-0.748214285714,-0.573214285714,-0.523214285714],
			[-1.0,-0.817629179331,-0.412360688956,-0.758865248227,-0.570415400203,-0.440729483283],
			[-1.0,-0.647660818713,-0.558479532164,-0.776315789474,-0.519005847953,-0.498538011696],
			[-0.985100788782,-0.605609114812,-0.555652936021,-0.711656441718,-0.524101665206,-0.617879053462],
			[-0.952301719357,-0.534109816972,-0.694952856351,-0.749306711037,-0.542983915696,-0.526344980588],
			[-0.93916755603,-0.569903948773,-0.704375667022,-0.744930629669,-0.513340448239,-0.528281750267],
			[-0.926236378877,-0.590108968986,-0.773679798826,-0.68231349539,-0.546521374686,-0.481139983236],
			[-0.928664636799,-0.587646802958,-0.707698999565,-0.688560243584,-0.552849064811,-0.534580252284],
			[-1.0,-0.57962529274,-0.559718969555,-0.759953161593,-0.55737704918,-0.543325526932],
			[-0.99889135255,-0.635254988914,-0.592017738359,-0.741685144124,-0.531042128603,-0.50110864745],
			[-0.735294117647,-0.43954248366,-0.62908496732,-1.0,-0.75,-0.446078431373],
			[-0.586060348491,-0.324266893328,-0.862303442414,-1.0,-0.891202719932,-0.336166595835],
			[-0.598117647059,-0.296,-0.848470588235,-1.0,-0.872,-0.385411764706],
			[-0.653196930946,-0.273657289003,-0.838363171355,-1.0,-0.884398976982,-0.350383631714],
			[-0.732954545455,-0.275568181818,-0.600852272727,-1.0,-0.938920454545,-0.451704545455],
			[-0.740296400847,-0.298517995766,-0.580804516584,-1.0,-0.90684544813,-0.473535638673],
			[-0.741988496302,-0.423171733772,-0.57107641742,-1.0,-0.806080525883,-0.457682826623],
			[-0.732615522656,-0.212202781516,-0.851054284432,-1.0,-0.850157021086,-0.35397039031],
			[-0.659983291562,-0.292397660819,-0.910609857978,-1.0,-0.835421888053,-0.301587301587],
			[-0.666168410563,-0.198804185351,-0.895366218236,-1.0,-0.873442949676,-0.366218236173],
			[-0.780721790772,-0.243490178164,-0.629054362723,-1.0,-0.929648241206,-0.417085427136],
			[-0.746951219512,-0.317073170732,-0.631097560976,-1.0,-0.899390243902,-0.405487804878],
			[-0.676133532636,-0.673143996014,-0.872446437469,-0.998006975585,-0.460886895864,-0.319382162431],
			[-0.718837863168,-0.629803186504,-0.855670103093,-1.0,-0.482661668229,-0.313027179007],
			[-0.987376725838,-0.63550295858,-0.299408284024,-0.632347140039,-0.455621301775,-0.989743589744],
			[-0.929987608426,-0.396530359356,-0.395291201983,-0.741635687732,-0.614002478315,-0.922552664188],
			[-0.963349131122,-0.375671406003,-0.429383886256,-0.742812006319,-0.574091627172,-0.914691943128],
			[-0.649754500818,-0.427168576105,-0.882160392799,-0.973813420622,-0.603927986907,-0.46317512275],
			[-0.99043062201,-0.474420316526,-0.277143908723,-0.748987854251,-0.542142068458,-0.966875230033],
			[-0.953656770456,-0.404055032585,-0.292541636495,-0.737871107893,-0.630702389573,-0.981173062998],
			[-0.983570646221,-0.625410733844,-0.654983570646,-0.703176341731,-0.510405257393,-0.522453450164],
			[-1.0,-0.624505928854,-0.518577075099,-0.698814229249,-0.517786561265,-0.640316205534],
			[-0.994455445545,-0.588118811881,-0.527920792079,-0.682376237624,-0.533465346535,-0.673663366337],
			[-0.983739837398,-0.576461478901,-0.543941153697,-0.665505226481,-0.559427022842,-0.670925280681],
			[-1.0,-0.540089801155,-0.667094291212,-0.72674791533,-0.447081462476,-0.618986529827],
			[-0.935821872954,-0.512770137525,-0.779960707269,-0.721021611002,-0.516699410609,-0.533726260642],
			[-0.968981793661,-0.581928523264,-0.741065407957,-0.770734996628,-0.545515846258,-0.391773432232],
			[-0.939513477975,-0.512163050625,-0.737015121631,-0.804076265615,-0.568704799474,-0.438527284681],
			[-1.0,-0.605914972274,-0.689463955638,-0.718299445471,-0.488354898336,-0.497966728281],
			[-1.0,-0.76402461093,-0.533840028954,-0.664133188563,-0.541078537821,-0.496923633731],
			[-0.71797485559,-0.365273530411,-0.718654434251,-1.0,-0.762147468569,-0.435949711179],
			[-0.724579124579,-0.39797979798,-0.676767676768,-1.0,-0.801346801347,-0.399326599327],
			[-0.707276507277,-0.318918918919,-0.95841995842,-1.0,-0.782120582121,-0.233264033264],
			[-0.663149667839,-0.345838218054,-0.981242672919,-1.0,-0.752246971473,-0.257522469715],
			[-0.709254402398,-0.301611090296,-0.793930310978,-1.0,-0.826901461221,-0.368302735107],
			[-0.707738542449,-0.30803906837,-0.784372652141,-0.999248685199,-0.812171299775,-0.388429752066],
			[-0.972034280559,-0.441587731168,-0.375732972485,-0.646368967073,-0.644564727109,-0.919711321606],
			[-0.989213483146,-0.510112359551,-0.407640449438,-0.611685393258,-0.48404494382,-0.997303370787],
			[-1.0,-0.55459057072,-0.302109181141,-0.699131513648,-0.539081885856,-0.905086848635],
			[-0.542331881955,-0.747460087083,-1.0,-0.894533139816,-0.44847605225,-0.367198838897],
			[-0.749037721324,-0.6805234796,-0.945342571209,-0.990762124711,-0.403387220939,-0.230946882217],
			[-0.73474369406,-0.615134255492,-0.925956061839,-0.989422294548,-0.443449959317,-0.291293734744],
			[-0.766074313409,-0.568336025848,-0.452019386107,-1.0,-0.506300484653,-0.707269789984],
			[-0.733897202342,-0.517891997398,-0.443721535459,-1.0,-0.540013012362,-0.76447625244],
			[-0.668161434978,-0.520819987188,-0.78731582319,-0.989750160154,-0.467008327995,-0.566944266496],
			[-0.664811379097,-0.552257266543,-0.814471243043,-0.978973407545,-0.460729746444,-0.528756957328],
			[-0.721952796638,-0.482056256062,-0.662463627546,-0.979308115099,-0.533785968316,-0.62043323634],
			[-0.821714285714,-0.569142857143,-0.491428571429,-0.738285714286,-0.465142857143,-0.914285714286],
			[-0.807884508606,-0.594669627984,-0.499167129373,-0.710161021655,-0.475846751805,-0.912270960577],
			[-0.758649093904,-0.50823723229,-0.496705107084,-1.0,-0.607907742998,-0.628500823723],
			[-0.754709418838,-0.563927855711,-0.47254509018,-1.0,-0.56873747495,-0.640080160321],
			[-0.752081406105,-0.507863089732,-0.540240518039,-1.0,-0.695652173913,-0.504162812211],
			[-1.0,-0.786018237082,-0.376899696049,-0.665653495441,-0.316717325228,-0.854711246201],
			[-1.0,-0.871024734982,-0.398115429918,-0.706124852768,-0.2308598351,-0.793875147232],
			[-1.0,-0.844298245614,-0.34649122807,-0.637061403509,-0.313596491228,-0.858552631579],
			[-1.0,-0.811246559182,-0.36846244593,-0.723161620134,-0.307904050334,-0.78922532442],
			[-1.0,-0.853451600463,-0.323563440031,-0.725414577709,-0.300424219051,-0.797146162746],
			[-1.0,-0.724315068493,-0.420376712329,-0.726883561644,-0.458047945205,-0.670376712329],
			[-0.999154334038,-0.736152219873,-0.3911205074,-0.731923890063,-0.523044397463,-0.618604651163],
			[-0.488704819277,-0.67093373494,-0.985692771084,-0.917168674699,-0.584337349398,-0.353162650602],
			[-0.471901462664,-0.729792147806,-0.994611239415,-0.886836027714,-0.555812163202,-0.361046959199],
			[-0.625502008032,-0.660642570281,-0.988955823293,-0.908634538153,-0.489959839357,-0.326305220884],
			[-0.637274549098,-0.673346693387,-0.976953907816,-0.902805611222,-0.507014028056,-0.302605210421],
			[-0.613787700744,-0.537015276146,-0.908343125734,-0.956130043087,-0.623188405797,-0.361535448492],
			[-0.550510783201,-0.558456299659,-0.799091940976,-0.895573212259,-0.77866061294,-0.417707150965],
			[-0.547984099943,-0.541169789892,-0.798977853492,-0.892106757524,-0.776263486655,-0.443498012493],
			[-0.595584988962,-0.58587196468,-0.94701986755,-0.97174392936,-0.594701986755,-0.305077262693],
			[-0.573131094258,-0.659804983749,-0.966413867822,-0.943661971831,-0.524377031419,-0.332611050921],
			[-0.828402366864,-0.650887573964,-0.414201183432,-0.800788954635,-0.497041420118,-0.808678500986],
			[-0.709642470206,-0.612134344529,-0.495124593716,-0.893824485374,-0.512459371614,-0.776814734561],
			[-0.683229813665,-0.610766045549,-0.511387163561,-0.846790890269,-0.527950310559,-0.819875776398],
			[-0.997345132743,-0.797345132743,-0.388495575221,-0.687610619469,-0.321238938053,-0.80796460177],
			[-1.0,-0.829411764706,-0.43025210084,-0.658823529412,-0.273109243697,-0.808403361345],
			[-0.748054474708,-0.639105058366,-0.559338521401,-0.876459143969,-0.530155642023,-0.646887159533],
			[-0.747417840376,-0.616901408451,-0.572769953052,-0.870422535211,-0.531455399061,-0.66103286385],
			[-0.729957805907,-0.548523206751,-0.541490857947,-0.995780590717,-0.582278481013,-0.601969057665],
			[-0.707495429616,-0.563985374771,-0.719378427788,-0.912248628885,-0.569469835466,-0.527422303473],
			[-0.708547407753,-0.552545539468,-0.692666978048,-0.944885567492,-0.597384399813,-0.503970107426],
			[-0.739276703112,-0.603027754415,-0.465096719933,-0.848612279226,-0.490328006728,-0.853658536585],
			[-0.719357565511,-0.612848689772,-0.472527472527,-0.918850380389,-0.474218089603,-0.802197802198],
			[-0.771799628942,-0.625231910946,-0.508348794063,-0.890538033395,-0.509276437848,-0.694805194805],
			[-0.7430523918,-0.616400911162,-0.529840546697,-0.914350797267,-0.507061503417,-0.689293849658],
			[-0.717616580311,-0.588082901554,-0.599740932642,-0.944300518135,-0.607512953368,-0.54274611399],
			[-0.998953427525,-0.896389324961,-0.462061747776,-0.592883307169,-0.318681318681,-0.731030873888],
			[-0.986516853933,-0.805842696629,-0.402247191011,-0.65393258427,-0.327640449438,-0.823820224719],
			[-1.0,-0.807531380753,-0.419246861925,-0.655230125523,-0.312133891213,-0.805857740586],
			[-0.998309382925,-0.816568047337,-0.411665257819,-0.645815722739,-0.331360946746,-0.796280642434],
			[-1.0,-0.774744027304,-0.449829351536,-0.759726962457,-0.303754266212,-0.711945392491],
			[-1.0,-0.847988077496,-0.49478390462,-0.746646795827,-0.415797317437,-0.49478390462],
			[-1.0,-0.602689486553,-0.408312958435,-0.622249388753,-0.366748166259,-1.0],
			[-1.0,-0.673043478261,-0.328695652174,-0.666086956522,-0.332173913043,-1.0],
			[-1.0,-0.81207133059,-0.462277091907,-0.761316872428,-0.407407407407,-0.556927297668],
			[-0.997737556561,-0.798642533937,-0.369909502262,-0.747737556561,-0.371040723982,-0.714932126697],
			[-0.620592383639,-0.705218617772,-0.796897038082,-0.612129760226,-0.658674188999,-0.606488011283],
			[-0.720541401274,-0.738057324841,-0.694267515924,-0.62101910828,-0.654458598726,-0.571656050955],
			[-0.485849056604,-0.439465408805,-0.805031446541,-0.959119496855,-0.838050314465,-0.47248427673],
			[-0.703495630462,-0.685393258427,-0.628589263421,-0.5911360799,-0.700998751561,-0.69038701623],
			[-0.715363881402,-0.592452830189,-0.573045822102,-0.622641509434,-0.771428571429,-0.725067385445],
			[-0.708626760563,-0.617077464789,-0.549295774648,-0.617957746479,-0.721830985915,-0.785211267606],
			[-0.72602739726,-0.53852739726,-0.564212328767,-0.815068493151,-0.702054794521,-0.654109589041],
			[-0.707794075352,-0.524302559678,-0.763589301122,-0.851020995111,-0.507046304285,-0.646246764452],
			[-0.743119266055,-0.564875491481,-0.893840104849,-0.799475753604,-0.533420707733,-0.465268676278],
			[-0.797108673978,-0.668494516451,-0.787637088734,-0.661515453639,-0.486041874377,-0.599202392822],
			[-0.660672400313,-0.508209538702,-0.695074276779,-0.851446442533,-0.558248631744,-0.72634870993],
			[-0.724568490635,-0.497612926919,-0.570326845391,-0.872199779655,-0.72970987881,-0.60558207859],
			[-0.786085150571,-0.666666666667,-0.758047767394,-0.616822429907,-0.595015576324,-0.577362409138],
			[-0.744095875925,-0.622841029256,-0.715192104336,-0.711667254142,-0.594642227705,-0.611561508636],
			[-0.749546279492,-0.601451905626,-0.666061705989,-0.701633393829,-0.588384754991,-0.692921960073],
			[-0.737506575487,-0.649658074698,-0.714886901631,-0.642819568648,-0.59863229879,-0.656496580747],
			[-0.753312014619,-0.583371402467,-0.789858382823,-0.698492462312,-0.601644586569,-0.573321151211],
			[-0.827202737382,-0.573139435415,-0.610778443114,-0.72626176219,-0.559452523524,-0.703165098375],
			[-0.732015376167,-0.522240527183,-0.457440966502,-0.948380010983,-0.702361339923,-0.637561779242],
			[-0.773913043478,-0.509316770186,-0.822360248447,-0.742857142857,-0.633540372671,-0.51801242236],
			[-0.683801295896,-0.663066954644,-0.696760259179,-0.58444924406,-0.726133909287,-0.645788336933],
			[-0.69450101833,-0.615362234507,-0.494908350305,-0.519930171661,-0.686936281641,-0.988361943555],
			[-0.718301435407,-0.602870813397,-0.794258373206,-0.672846889952,-0.56519138756,-0.646531100478],
			[-0.651766709238,-0.652618135377,-0.739463601533,-0.612601106854,-0.667943805875,-0.675606641124],
			[-0.610655737705,-0.568852459016,-0.669672131148,-0.618032786885,-0.722131147541,-0.810655737705],
			[-0.676595744681,-0.584526112186,-0.787234042553,-0.573694390716,-0.601547388781,-0.776402321083],
			[-0.830036221789,-0.548063527445,-0.406519921984,-0.755363611034,-0.67288938423,-0.787127333519],
			[-0.727125767863,-0.512447462011,-0.71225347559,-0.903653410928,-0.658583899127,-0.485935984481],
			[-0.801007556675,-0.496221662469,-0.48026868178,-0.703610411419,-0.617968094039,-0.900923593619],
			[-0.697257026752,-0.506942092787,-0.781239417541,-0.811039620725,-0.528614967829,-0.674906874365],
			[-0.688546255507,-0.483259911894,-0.511894273128,-0.874449339207,-0.774889867841,-0.666960352423],
			[-0.824320759694,-0.588499076761,-0.858084938011,-0.68451595885,-0.557372724875,-0.48720654181],
			[-0.70290878283,-0.523863315448,-0.670149675233,-0.865009884213,-0.60180739904,-0.636260943236],
			[-0.712434691745,-0.510971786834,-0.781818181818,-0.867920585162,-0.570741901776,-0.556112852665],
			[-0.828371278459,-0.50122591944,-0.359719789842,-0.802451838879,-0.586690017513,-0.921541155867],
			[-0.763518385004,-0.63590483057,-0.870944484499,-0.648882480173,-0.545782263879,-0.534967555876],
			[-0.747568208778,-0.564887307236,-0.488493475682,-0.732384341637,-0.64650059312,-0.820166073547],
			[-0.821613236815,-0.654084798345,-0.876938986556,-0.669596690796,-0.46639089969,-0.511375387797],
			[-0.762896825397,-0.660218253968,-0.962301587302,-0.753968253968,-0.470734126984,-0.389880952381],
			[-0.758560140474,-0.523266022827,-0.675153643547,-0.722563652327,-0.627743634767,-0.692712906058],
			[-0.818374558304,-0.490459363958,-0.536395759717,-0.819081272085,-0.591519434629,-0.744169611307],
			[-0.45049272642,-0.564992961051,-0.972313467855,-0.8385734397,-0.639605818864,-0.53402158611],
			[-0.628250591017,-0.640070921986,-0.586288416076,-0.707446808511,-0.628841607565,-0.809101654846],
			[-0.779750581272,-0.624603677869,-0.507080955401,-0.576833650391,-0.546396110759,-0.965335024308],
			[-0.66026289181,-0.619143916414,-0.661611054938,-0.74384900573,-0.584765756657,-0.730367374452],
			[-0.617343427392,-0.608396421198,-0.683413626979,-0.774948382657,-0.600137646249,-0.715760495526],
			[-0.612815269257,-0.61554192229,-0.646898432175,-0.760736196319,-0.638718473074,-0.725289706885],
			[-0.584295612009,-0.671285604311,-0.857582755966,-0.703618167821,-0.612009237875,-0.571208622017],
			[-0.956538917424,-0.534176214935,-0.465823785065,-0.625049387594,-0.495061240616,-0.923350454366],
			[-0.883592574009,-0.61866532865,-0.64743268105,-0.712995484195,-0.452416792106,-0.68489713999],
			[-0.839961358879,-0.51215585252,-0.550796973112,-0.743680566736,-0.513121880535,-0.840283368218],
			[-0.83833226973,-0.546054031057,-0.559242714316,-0.677089980855,-0.540097851521,-0.839183152521],
			[-0.846597206828,-0.581910884505,-0.566836621592,-0.713145643981,-0.519397029483,-0.772112613611],
			[-0.844496487119,-0.553161592506,-0.711475409836,-0.654332552693,-0.499297423888,-0.737236533958],
			[-0.90527607362,-0.499877300613,-0.463067484663,-0.696196319018,-0.530306748466,-0.90527607362],
			[-0.675305442429,-0.499814883377,-0.49574231766,-0.831914105887,-0.635690485006,-0.861532765642],
			[-0.7153784219,-0.549516908213,-0.426328502415,-0.807165861514,-0.618760064412,-0.882850241546],
			[-0.68115942029,-0.524200164069,-0.514902925896,-0.823352474706,-0.589280831282,-0.867104183757],
			[-0.717196922437,-0.698482012892,-0.650655021834,-0.957579538366,-0.658140985652,-0.317945518819],
			[-0.788389513109,-0.561048689139,-0.767415730337,-0.810486891386,-0.496629213483,-0.576029962547],
			[-0.81103074141,-0.521247739602,-0.509493670886,-0.726491862568,-0.624321880651,-0.807414104882],
			[-0.795004306632,-0.617571059432,-0.832902670112,-0.806488659202,-0.4556416882,-0.492391616423],
			[-0.635236830456,-0.693669765383,-0.700752545374,-0.72023019035,-0.628154050465,-0.621956617973],
			[-0.403155421282,-0.675058744545,-0.969788519637,-0.865726753944,-0.658945955018,-0.427324605572],
			[-0.650539784086,-0.664134346261,-0.71931227509,-0.709716113555,-0.628948420632,-0.627349060376],
			[-0.39218328841,-0.75,-1.0,-0.88679245283,-0.541778975741,-0.429245283019],
			[-0.609501738123,-0.725376593279,-0.811123986095,-0.687137891078,-0.581691772885,-0.58516801854],
			[-0.647305808258,-0.685094471659,-0.771868439468,-0.62211336599,-0.601119664101,-0.672498250525],
			[-0.815505397448,-0.524370297677,-0.719332679097,-0.722603859993,-0.525024533857,-0.693163231927],
			[-0.822703335284,-0.700994733762,-0.624341720304,-0.715623171445,-0.534815681685,-0.601521357519],
			[-0.72684160607,-0.617451786279,-0.607967119823,-0.791969649067,-0.583939298135,-0.671830540626],
			[-0.706504065041,-0.512195121951,-0.587804878049,-0.717886178862,-0.641463414634,-0.834146341463],
			[-0.813014827018,-0.530477759473,-0.668863261944,-0.707578253707,-0.550247116969,-0.72981878089],
			[-0.801541425819,-0.622350674374,-0.757225433526,-0.691714836224,-0.523121387283,-0.604046242775],
			[-0.638686131387,-0.590510948905,-0.637226277372,-0.739416058394,-0.64598540146,-0.748175182482],
			[-0.957792207792,-0.734415584416,-0.388311688312,-0.663636363636,-0.466233766234,-0.78961038961],
			[-0.602090819993,-0.576608951323,-0.906566481542,-0.802025481869,-0.648480888598,-0.464227376674],
			[-0.632227488152,-0.638862559242,-0.679620853081,-0.759241706161,-0.576303317536,-0.713744075829],
			[-0.678212290503,-0.645810055866,-0.719553072626,-0.778770949721,-0.579888268156,-0.597765363128],
			[-0.842851667305,-0.648907627443,-0.861249520889,-0.755461862783,-0.428133384438,-0.463395937141],
			[-0.830425963489,-0.588640973631,-0.74523326572,-0.783367139959,-0.530223123732,-0.522109533469],
			[-0.829075708314,-0.643288434742,-0.866233163028,-0.766836971667,-0.427775197399,-0.466790524849]
		])
		if trainingTarget:
			return np.array([
			[1,0,0,0,0,0,0,0,0,0,0,0],
			[1,0,0,0,0,0,0,0,0,0,0,0],
			[1,0,0,0,0,0,0,0,0,0,0,0],
			[1,0,0,0,0,0,0,0,0,0,0,0],
			[1,0,0,0,0,0,0,0,0,0,0,0],
			[1,0,0,0,0,0,0,0,0,0,0,0],
			[1,0,0,0,0,0,0,0,0,0,0,0],
			[1,0,0,0,0,0,0,0,0,0,0,0],
			[1,0,0,0,0,0,0,0,0,0,0,0],
			[1,0,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,0,1,0,0,0,0,0,0,0,0],
			[0,0,0,1,0,0,0,0,0,0,0,0],
			[0,0,0,1,0,0,0,0,0,0,0,0],
			[0,0,0,1,0,0,0,0,0,0,0,0],
			[0,0,0,1,0,0,0,0,0,0,0,0],
			[0,0,0,1,0,0,0,0,0,0,0,0],
			[0,0,0,1,0,0,0,0,0,0,0,0],
			[0,0,0,1,0,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,0,1,0,0,0,0,0,0],
			[0,0,0,0,0,1,0,0,0,0,0,0],
			[0,0,0,0,0,1,0,0,0,0,0,0],
			[0,0,0,0,0,1,0,0,0,0,0,0],
			[0,0,0,0,0,1,0,0,0,0,0,0],
			[0,0,0,0,0,1,0,0,0,0,0,0],
			[0,0,0,0,0,0,1,0,0,0,0,0],
			[0,0,0,0,0,0,1,0,0,0,0,0],
			[0,0,0,0,0,0,1,0,0,0,0,0],
			[0,0,0,0,0,0,1,0,0,0,0,0],
			[0,0,0,0,0,0,1,0,0,0,0,0],
			[0,0,0,0,0,0,1,0,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,0,1,0,0,0],
			[0,0,0,0,0,0,0,0,1,0,0,0],
			[0,0,0,0,0,0,0,0,1,0,0,0],
			[0,0,0,0,0,0,0,0,1,0,0,0],
			[0,0,0,0,0,0,0,0,1,0,0,0],
			[0,0,0,0,0,0,0,0,1,0,0,0],
			[0,0,0,0,0,0,0,0,1,0,0,0],
			[0,0,0,0,0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,0,1],
			[0,0,0,0,0,0,0,0,0,0,0,1],
			[0,0,0,0,0,0,0,0,0,0,0,1],
			[0,0,0,0,0,0,0,0,0,0,0,1],
			[0,0,0,0,0,0,0,0,0,0,0,1],
			[0,0,0,0,0,0,0,0,0,0,0,1],
			[0,0,0,0,0,0,0,0,0,0,0,1],
			[0,0,0,0,0,0,0,0,0,0,0,1],
			[0,0,0,0,0,0,0,0,0,0,0,1],
			[0,0,0,0,0,0,0,0,0,0,0,1],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0]
		])
		if testingInput:
			return np.array([
			[-0.938818565401,-0.64135021097,-0.35970464135,-0.567510548523,-0.566455696203,-0.926160337553],
			[-0.912997903564,-0.520964360587,-0.343815513627,-0.666666666667,-0.572327044025,-0.98322851153],
			[-1.0,-0.649509803922,-0.557598039216,-0.730392156863,-0.552696078431,-0.509803921569],
			[-0.685468451243,-0.225621414914,-0.877629063098,-1.0,-0.874760994264,-0.336520076482],
			[-0.974674384949,-0.60492040521,-0.306801736614,-0.596237337192,-0.523154848046,-0.994211287988],
			[-1.0,-0.647940074906,-0.553772070626,-0.71214553237,-0.559122525415,-0.527019796683],
			[-0.999355462456,-0.525620367386,-0.661617789236,-0.733161456655,-0.44698678698,-0.633258137286],
			[-0.637371338084,-0.369754552652,-0.98178939034,-1.0,-0.733966745843,-0.27711797308],
			[-1.0,-0.541154791155,-0.323095823096,-0.688574938575,-0.544226044226,-0.902948402948],
			[-0.687358916479,-0.541760722348,-0.698645598194,-0.98532731377,-0.51467268623,-0.57223476298],
			[-0.735056542811,-0.467528271405,-0.637479806139,-0.988368336026,-0.528917609047,-0.642649434572],
			[-1.0,-0.735019241341,-0.423859263332,-0.659153380979,-0.280923584387,-0.901044529962],
			[-0.670080862534,-0.678706199461,-0.995687331536,-0.949326145553,-0.415633423181,-0.290566037736],
			[-0.589359310603,-0.508430123642,-0.919820157362,-0.957287373548,-0.638066691645,-0.3870363432],
			[-0.730348258706,-0.603980099502,-0.540298507463,-0.884577114428,-0.580099502488,-0.660696517413],
			[-1.0,-0.881237113402,-0.427628865979,-0.659381443299,-0.294845360825,-0.736907216495],
			[-0.656462585034,-0.557823129252,-0.547619047619,-0.702947845805,-0.685941043084,-0.849206349206],
			[-0.718298223874,-0.56712102437,-0.567947129285,-0.832300702189,-0.721602643536,-0.592730276745],
			[-0.779670037254,-0.626397019691,-0.505055880788,-0.903139968068,-0.639169771155,-0.546567323044],
			[-0.676726342711,-0.587723785166,-0.609207161125,-0.667519181586,-0.585677749361,-0.873145780051],
			[-0.670368725011,-0.679253665038,-0.65348733896,-0.578853842737,-0.713904931142,-0.704131497112],
			[-0.668614357262,-0.603505843072,-0.75959933222,-0.668614357262,-0.613522537563,-0.686143572621],
			[-0.728090952155,-0.567977261961,-0.688299384178,-0.586925627665,-0.678825201326,-0.749881572714],
			[-0.854160868355,-0.685499582522,-0.929306985806,-0.665460617868,-0.388811578068,-0.476760367381],
			[-0.716760502382,-0.509311390212,-0.787353832828,-0.871372888696,-0.566478995236,-0.548722390645],
			[-0.849547920434,-0.642676311031,-0.745388788427,-0.668716094033,-0.531283905967,-0.562386980108],
			[-0.800229621125,-0.590508993494,-0.905855338691,-0.642556448527,-0.539226942212,-0.521622655951],
			[-0.629970246146,-0.665674871517,-0.840952123343,-0.703543413579,-0.559642953746,-0.600216391669],
			[-0.949804432855,-0.721642764016,-0.460886571056,-0.526727509778,-0.45371577575,-0.887222946545],
			[-0.767157894737,-0.603368421053,-0.512421052632,-0.585684210526,-0.558736842105,-0.972631578947],
			[-0.65325738697,-0.641865432538,-0.616945532218,-0.74510501958,-0.604841580634,-0.73798504806],
			[-0.799054787327,-0.773148958516,-0.61106248906,-0.804305968843,-0.512340276562,-0.500087519692],
			[-0.872549019608,-0.613590263692,-0.604800540906,-0.741717376606,-0.47937795808,-0.687964841109],
			[-0.698448732501,-0.500189178963,-0.515323496027,-0.824820279985,-0.623912220961,-0.837306091563],
			[-0.824848024316,-0.599544072948,-0.834346504559,-0.803191489362,-0.476063829787,-0.462006079027],
			[-0.640618101545,-0.695364238411,-0.712141280353,-0.709492273731,-0.600883002208,-0.641501103753],
			[-0.679154658982,-0.750240153698,-0.71469740634,-0.521613832853,-0.622478386167,-0.71181556196],
			[-0.676344597811,-0.738219895288,-0.710613993337,-0.630652070443,-0.621132793908,-0.623036649215],
			[-0.618996222342,-0.701025364274,-0.6956287102,-0.698866702644,-0.624392876417,-0.661090124123],
			[-0.847046773643,-0.527483782861,-0.689996585865,-0.778081256402,-0.483782861045,-0.673608740184],
			[-0.645112781955,-0.506165413534,-0.848421052632,-0.814135338346,-0.714285714286,-0.471879699248],
			[-0.720733427362,-0.534555712271,-0.590973201693,-0.825105782793,-0.622002820874,-0.706629055007]
		])
		if testingTarget:
			return np.array([
			[1,0,0,0,0,0,0,0,0,0,0,0],
			[1,0,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0,0],
			[0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,0,1,0,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,0,1,0,0,0,0,0,0],
			[0,0,0,0,0,0,1,0,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,0,1,0,0,0],
			[0,0,0,0,0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0,0,1],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0]
		])
		
	
	def getRecentValuesComplete(self, trainingInput=False, trainingTarget=False, testingInput=False, testingTarget=False):
		if trainingInput:
			return np.array([
			[-0.95,-0.637931034483,-0.43275862069,-0.434482758621,-0.570689655172,-0.974137931034],
			[-0.873665480427,-0.55871886121,-0.613879003559,-0.288256227758,-0.665480427046,-1.0],
			[-0.921052631579,-0.555263157895,-0.5,-0.471052631579,-0.565789473684,-0.986842105263],
			[-0.603174603175,-0.473544973545,-0.822751322751,-0.981481481481,-0.730158730159,-0.388888888889],
			[-0.853820598007,-0.546511627907,-0.714285714286,-0.737541528239,-0.637873754153,-0.509966777409],
			[-0.974343310935,-0.49664019548,-0.837507635919,-0.688454489921,-0.534514355528,-0.468540012217],
			[-0.95297029703,-0.457920792079,-0.804455445545,-0.70297029703,-0.533415841584,-0.548267326733],
			[-0.773353751914,-0.321592649311,-0.748851454824,-0.989280245023,-0.756508422665,-0.410413476263],
			[-0.721453287197,-0.295847750865,-0.825259515571,-0.996539792388,-0.759515570934,-0.401384083045],
			[-0.560147601476,-0.411070110701,-0.759409594096,-0.994095940959,-0.828782287823,-0.446494464945],
			[-0.723901098901,-0.39010989011,-0.700549450549,-1.0,-0.751373626374,-0.434065934066],
			[-0.588405797101,-0.349896480331,-0.852587991718,-1.0,-0.845962732919,-0.36314699793],
			[-0.548200248242,-0.342987174183,-0.944559371121,-1.0,-0.751758378155,-0.4124948283],
			[-0.554384644336,-0.375987956342,-0.954083552879,-1.0,-0.733534060971,-0.382009785472],
			[-0.936381709742,-0.659045725646,-0.367793240557,-0.541749502982,-0.575546719682,-0.919483101392],
			[-0.929337539432,-0.762776025237,-0.44858044164,-0.605047318612,-0.458675078864,-0.795583596215],
			[-0.957753240518,-0.583293326932,-0.275084013442,-0.595775324052,-0.605376860298,-0.982717234758],
			[-0.995729537367,-0.591459074733,-0.281138790036,-0.71103202847,-0.555871886121,-0.864768683274],
			[-0.95975565936,-0.617678763924,-0.401365432986,-0.664390945023,-0.497664390945,-0.859144807761],
			[-0.699041267195,-0.302209253856,-0.852438516048,-1.0,-0.821592330138,-0.324718632764],
			[-0.953565505804,-0.653399668325,-0.300165837479,-0.599502487562,-0.56135986733,-0.932006633499],
			[-0.978039215686,-0.638431372549,-0.27137254902,-0.621176470588,-0.55137254902,-0.939607843137],
			[-0.868372943327,-0.586837294333,-0.352833638026,-0.620658135283,-0.604204753199,-0.967093235832],
			[-0.870759289176,-0.511039310716,-0.366720516963,-0.685514270328,-0.586429725363,-0.979536887453],
			[-0.851654215582,-0.628601921025,-0.640341515475,-0.677694770544,-0.579509071505,-0.62219850587],
			[-1.0,-0.733382570162,-0.498522895126,-0.710487444609,-0.525110782866,-0.532496307238],
			[-0.645982498011,-0.376292760541,-0.838504375497,-0.978520286396,-0.761336515513,-0.399363564041],
			[-0.897332662305,-0.53598389532,-0.559134373427,-0.68495218923,-0.622546552592,-0.700050327126],
			[-0.950629722922,-0.545591939547,-0.557682619647,-0.705793450882,-0.566750629723,-0.67355163728],
			[-1.0,-0.721428571429,-0.433928571429,-0.748214285714,-0.573214285714,-0.523214285714],
			[-1.0,-0.817629179331,-0.412360688956,-0.758865248227,-0.570415400203,-0.440729483283],
			[-1.0,-0.647660818713,-0.558479532164,-0.776315789474,-0.519005847953,-0.498538011696],
			[-0.985100788782,-0.605609114812,-0.555652936021,-0.711656441718,-0.524101665206,-0.617879053462],
			[-0.952301719357,-0.534109816972,-0.694952856351,-0.749306711037,-0.542983915696,-0.526344980588],
			[-0.93916755603,-0.569903948773,-0.704375667022,-0.744930629669,-0.513340448239,-0.528281750267],
			[-0.926236378877,-0.590108968986,-0.773679798826,-0.68231349539,-0.546521374686,-0.481139983236],
			[-0.928664636799,-0.587646802958,-0.707698999565,-0.688560243584,-0.552849064811,-0.534580252284],
			[-1.0,-0.57962529274,-0.559718969555,-0.759953161593,-0.55737704918,-0.543325526932],
			[-0.99889135255,-0.635254988914,-0.592017738359,-0.741685144124,-0.531042128603,-0.50110864745],
			[-0.735294117647,-0.43954248366,-0.62908496732,-1.0,-0.75,-0.446078431373],
			[-0.586060348491,-0.324266893328,-0.862303442414,-1.0,-0.891202719932,-0.336166595835],
			[-0.598117647059,-0.296,-0.848470588235,-1.0,-0.872,-0.385411764706],
			[-0.653196930946,-0.273657289003,-0.838363171355,-1.0,-0.884398976982,-0.350383631714],
			[-0.732954545455,-0.275568181818,-0.600852272727,-1.0,-0.938920454545,-0.451704545455],
			[-0.740296400847,-0.298517995766,-0.580804516584,-1.0,-0.90684544813,-0.473535638673],
			[-0.741988496302,-0.423171733772,-0.57107641742,-1.0,-0.806080525883,-0.457682826623],
			[-0.732615522656,-0.212202781516,-0.851054284432,-1.0,-0.850157021086,-0.35397039031],
			[-0.659983291562,-0.292397660819,-0.910609857978,-1.0,-0.835421888053,-0.301587301587],
			[-0.666168410563,-0.198804185351,-0.895366218236,-1.0,-0.873442949676,-0.366218236173],
			[-0.780721790772,-0.243490178164,-0.629054362723,-1.0,-0.929648241206,-0.417085427136],
			[-0.746951219512,-0.317073170732,-0.631097560976,-1.0,-0.899390243902,-0.405487804878],
			[-0.676133532636,-0.673143996014,-0.872446437469,-0.998006975585,-0.460886895864,-0.319382162431],
			[-0.718837863168,-0.629803186504,-0.855670103093,-1.0,-0.482661668229,-0.313027179007],
			[-0.987376725838,-0.63550295858,-0.299408284024,-0.632347140039,-0.455621301775,-0.989743589744],
			[-0.929987608426,-0.396530359356,-0.395291201983,-0.741635687732,-0.614002478315,-0.922552664188],
			[-0.963349131122,-0.375671406003,-0.429383886256,-0.742812006319,-0.574091627172,-0.914691943128],
			[-0.649754500818,-0.427168576105,-0.882160392799,-0.973813420622,-0.603927986907,-0.46317512275],
			[-0.99043062201,-0.474420316526,-0.277143908723,-0.748987854251,-0.542142068458,-0.966875230033],
			[-0.953656770456,-0.404055032585,-0.292541636495,-0.737871107893,-0.630702389573,-0.981173062998],
			[-0.983570646221,-0.625410733844,-0.654983570646,-0.703176341731,-0.510405257393,-0.522453450164],
			[-1.0,-0.624505928854,-0.518577075099,-0.698814229249,-0.517786561265,-0.640316205534],
			[-0.994455445545,-0.588118811881,-0.527920792079,-0.682376237624,-0.533465346535,-0.673663366337],
			[-0.983739837398,-0.576461478901,-0.543941153697,-0.665505226481,-0.559427022842,-0.670925280681],
			[-1.0,-0.540089801155,-0.667094291212,-0.72674791533,-0.447081462476,-0.618986529827],
			[-0.935821872954,-0.512770137525,-0.779960707269,-0.721021611002,-0.516699410609,-0.533726260642],
			[-0.968981793661,-0.581928523264,-0.741065407957,-0.770734996628,-0.545515846258,-0.391773432232],
			[-0.939513477975,-0.512163050625,-0.737015121631,-0.804076265615,-0.568704799474,-0.438527284681],
			[-1.0,-0.605914972274,-0.689463955638,-0.718299445471,-0.488354898336,-0.497966728281],
			[-1.0,-0.76402461093,-0.533840028954,-0.664133188563,-0.541078537821,-0.496923633731],
			[-0.71797485559,-0.365273530411,-0.718654434251,-1.0,-0.762147468569,-0.435949711179],
			[-0.724579124579,-0.39797979798,-0.676767676768,-1.0,-0.801346801347,-0.399326599327],
			[-0.707276507277,-0.318918918919,-0.95841995842,-1.0,-0.782120582121,-0.233264033264],
			[-0.663149667839,-0.345838218054,-0.981242672919,-1.0,-0.752246971473,-0.257522469715],
			[-0.709254402398,-0.301611090296,-0.793930310978,-1.0,-0.826901461221,-0.368302735107],
			[-0.707738542449,-0.30803906837,-0.784372652141,-0.999248685199,-0.812171299775,-0.388429752066],
			[-0.712649661635,-0.464862051015,-0.416970327954,-1.0,-0.629359708485,-0.776158250911],
			[-0.745169712794,-0.383812010444,-0.507049608355,-1.0,-0.58955613577,-0.774412532637],
			[-0.716091395236,-0.425376762275,-0.587749149246,-1.0,-0.542051531356,-0.728731161886],
			[-0.732770745429,-0.417721518987,-0.579934364744,-1.0,-0.523675574308,-0.745897796531],
			[-0.733281493002,-0.436236391913,-0.538880248834,-0.991446345257,-0.587091757387,-0.713063763608],
			[-0.74633770239,-0.42868157286,-0.479568234387,-0.999228989977,-0.624518118736,-0.72166538165],
			[-0.998337489609,-0.652535328346,-0.562759767249,-0.770573566085,-0.516209476309,-0.499584372402],
			[-0.996817820207,-0.689737470167,-0.575178997613,-0.721559268099,-0.52108194113,-0.495624502784],
			[-1.0,-0.621007038441,-0.691391445587,-0.75311315647,-0.453167298322,-0.48132106118],
			[-1.0,-0.618471687741,-0.748213304013,-0.76360637713,-0.407366684992,-0.462341946124],
			[-1.0,-0.574446161772,-0.824832560536,-0.711488923235,-0.379701184956,-0.5095311695],
			[-0.629326620516,-0.419131529264,-0.497797356828,-0.964128382631,-0.564505978603,-0.925110132159],
			[-0.721379310345,-0.432413793103,-0.544137931034,-1.0,-0.515172413793,-0.786896551724],
			[-0.746858168761,-0.466786355476,-0.89407540395,-0.855475763016,-0.520646319569,-0.516157989228],
			[-0.735558408216,-0.507916131793,-0.961489088575,-0.824561403509,-0.447154471545,-0.523320496363],
			[-0.674208144796,-0.529411764706,-0.589743589744,-0.923579688286,-0.540472599296,-0.742584213172],
			[-0.953063885267,-0.48457192525,-0.699261190787,-0.74098218166,-0.493263798349,-0.628857018688],
			[-0.907105994442,-0.464073044859,-0.80547836443,-0.719730051608,-0.483128225486,-0.620484319174],
			[-0.972034280559,-0.441587731168,-0.375732972485,-0.646368967073,-0.644564727109,-0.919711321606],
			[-0.989213483146,-0.510112359551,-0.407640449438,-0.611685393258,-0.48404494382,-0.997303370787],
			[-1.0,-0.55459057072,-0.302109181141,-0.699131513648,-0.539081885856,-0.905086848635],
			[-0.542331881955,-0.747460087083,-1.0,-0.894533139816,-0.44847605225,-0.367198838897],
			[-0.749037721324,-0.6805234796,-0.945342571209,-0.990762124711,-0.403387220939,-0.230946882217],
			[-0.73474369406,-0.615134255492,-0.925956061839,-0.989422294548,-0.443449959317,-0.291293734744],
			[-0.766074313409,-0.568336025848,-0.452019386107,-1.0,-0.506300484653,-0.707269789984],
			[-0.733897202342,-0.517891997398,-0.443721535459,-1.0,-0.540013012362,-0.76447625244],
			[-0.668161434978,-0.520819987188,-0.78731582319,-0.989750160154,-0.467008327995,-0.566944266496],
			[-0.664811379097,-0.552257266543,-0.814471243043,-0.978973407545,-0.460729746444,-0.528756957328],
			[-0.721952796638,-0.482056256062,-0.662463627546,-0.979308115099,-0.533785968316,-0.62043323634],
			[-0.821714285714,-0.569142857143,-0.491428571429,-0.738285714286,-0.465142857143,-0.914285714286],
			[-0.807884508606,-0.594669627984,-0.499167129373,-0.710161021655,-0.475846751805,-0.912270960577],
			[-0.758649093904,-0.50823723229,-0.496705107084,-1.0,-0.607907742998,-0.628500823723],
			[-0.754709418838,-0.563927855711,-0.47254509018,-1.0,-0.56873747495,-0.640080160321],
			[-0.752081406105,-0.507863089732,-0.540240518039,-1.0,-0.695652173913,-0.504162812211],
			[-1.0,-0.786018237082,-0.376899696049,-0.665653495441,-0.316717325228,-0.854711246201],
			[-1.0,-0.871024734982,-0.398115429918,-0.706124852768,-0.2308598351,-0.793875147232],
			[-1.0,-0.844298245614,-0.34649122807,-0.637061403509,-0.313596491228,-0.858552631579],
			[-1.0,-0.811246559182,-0.36846244593,-0.723161620134,-0.307904050334,-0.78922532442],
			[-1.0,-0.853451600463,-0.323563440031,-0.725414577709,-0.300424219051,-0.797146162746],
			[-1.0,-0.724315068493,-0.420376712329,-0.726883561644,-0.458047945205,-0.670376712329],
			[-0.999154334038,-0.736152219873,-0.3911205074,-0.731923890063,-0.523044397463,-0.618604651163],
			[-0.488704819277,-0.67093373494,-0.985692771084,-0.917168674699,-0.584337349398,-0.353162650602],
			[-0.471901462664,-0.729792147806,-0.994611239415,-0.886836027714,-0.555812163202,-0.361046959199],
			[-0.625502008032,-0.660642570281,-0.988955823293,-0.908634538153,-0.489959839357,-0.326305220884],
			[-0.637274549098,-0.673346693387,-0.976953907816,-0.902805611222,-0.507014028056,-0.302605210421],
			[-0.613787700744,-0.537015276146,-0.908343125734,-0.956130043087,-0.623188405797,-0.361535448492],
			[-0.550510783201,-0.558456299659,-0.799091940976,-0.895573212259,-0.77866061294,-0.417707150965],
			[-0.547984099943,-0.541169789892,-0.798977853492,-0.892106757524,-0.776263486655,-0.443498012493],
			[-0.595584988962,-0.58587196468,-0.94701986755,-0.97174392936,-0.594701986755,-0.305077262693],
			[-0.573131094258,-0.659804983749,-0.966413867822,-0.943661971831,-0.524377031419,-0.332611050921],
			[-0.828402366864,-0.650887573964,-0.414201183432,-0.800788954635,-0.497041420118,-0.808678500986],
			[-0.709642470206,-0.612134344529,-0.495124593716,-0.893824485374,-0.512459371614,-0.776814734561],
			[-0.683229813665,-0.610766045549,-0.511387163561,-0.846790890269,-0.527950310559,-0.819875776398],
			[-0.997345132743,-0.797345132743,-0.388495575221,-0.687610619469,-0.321238938053,-0.80796460177],
			[-1.0,-0.829411764706,-0.43025210084,-0.658823529412,-0.273109243697,-0.808403361345],
			[-0.748054474708,-0.639105058366,-0.559338521401,-0.876459143969,-0.530155642023,-0.646887159533],
			[-0.747417840376,-0.616901408451,-0.572769953052,-0.870422535211,-0.531455399061,-0.66103286385],
			[-0.729957805907,-0.548523206751,-0.541490857947,-0.995780590717,-0.582278481013,-0.601969057665],
			[-0.707495429616,-0.563985374771,-0.719378427788,-0.912248628885,-0.569469835466,-0.527422303473],
			[-0.708547407753,-0.552545539468,-0.692666978048,-0.944885567492,-0.597384399813,-0.503970107426],
			[-0.739276703112,-0.603027754415,-0.465096719933,-0.848612279226,-0.490328006728,-0.853658536585],
			[-0.719357565511,-0.612848689772,-0.472527472527,-0.918850380389,-0.474218089603,-0.802197802198],
			[-0.771799628942,-0.625231910946,-0.508348794063,-0.890538033395,-0.509276437848,-0.694805194805],
			[-0.7430523918,-0.616400911162,-0.529840546697,-0.914350797267,-0.507061503417,-0.689293849658],
			[-0.717616580311,-0.588082901554,-0.599740932642,-0.944300518135,-0.607512953368,-0.54274611399],
			[-0.998953427525,-0.896389324961,-0.462061747776,-0.592883307169,-0.318681318681,-0.731030873888],
			[-0.986516853933,-0.805842696629,-0.402247191011,-0.65393258427,-0.327640449438,-0.823820224719],
			[-1.0,-0.807531380753,-0.419246861925,-0.655230125523,-0.312133891213,-0.805857740586],
			[-0.998309382925,-0.816568047337,-0.411665257819,-0.645815722739,-0.331360946746,-0.796280642434],
			[-1.0,-0.774744027304,-0.449829351536,-0.759726962457,-0.303754266212,-0.711945392491],
			[-1.0,-0.847988077496,-0.49478390462,-0.746646795827,-0.415797317437,-0.49478390462],
			[-1.0,-0.602689486553,-0.408312958435,-0.622249388753,-0.366748166259,-1.0],
			[-1.0,-0.673043478261,-0.328695652174,-0.666086956522,-0.332173913043,-1.0],
			[-1.0,-0.81207133059,-0.462277091907,-0.761316872428,-0.407407407407,-0.556927297668],
			[-0.997737556561,-0.798642533937,-0.369909502262,-0.747737556561,-0.371040723982,-0.714932126697],
			[-1.0,-0.740097289785,-0.489923558026,-0.466296038916,-0.369006254343,-0.93467685893],
			[-1.0,-0.726586102719,-0.407854984894,-0.518126888218,-0.371601208459,-0.97583081571],
			[-1.0,-0.758985200846,-0.415081042988,-0.53206483439,-0.329105003524,-0.964763918252],
			[-0.99695585997,-0.68797564688,-0.502283105023,-0.51598173516,-0.324200913242,-0.972602739726],
			[-1.0,-0.898770788142,-0.418655097614,-0.722342733189,-0.276934201012,-0.683297180043],
			[-0.704834605598,-0.484308736217,-0.648854961832,-0.91518235793,-0.516539440204,-0.730279898219],
			[-0.710267229255,-0.625879043601,-0.582278481013,-0.801687763713,-0.57805907173,-0.701828410689],
			[-0.698149951315,-0.532619279455,-0.702044790652,-0.859785783836,-0.470301850049,-0.737098344693],
			[-0.713163064833,-0.595284872299,-0.628683693517,-0.929273084479,-0.449901768173,-0.683693516699],
			[-1.0,-0.842550422902,-0.483409238777,-0.545868575146,-0.348080676643,-0.780091086532],
			[-1.0,-0.826086956522,-0.52023988006,-0.544227886057,-0.265367316342,-0.844077961019],
			[-0.866206896552,-0.724137931034,-0.500689655172,-0.656551724138,-0.459310344828,-0.793103448276],
			[-1.0,-0.865220759101,-0.268783888459,-0.680867544539,-0.24244771495,-0.942680092951],
			[-1.0,-0.897374701671,-0.400954653938,-0.605011933174,-0.307875894988,-0.788782816229],
			[-1.0,-0.845252051583,-0.411488862837,-0.574443141852,-0.304806565064,-0.864009378664],
			[-0.998850574713,-0.796551724138,-0.364367816092,-0.681609195402,-0.289655172414,-0.868965517241],
			[-1.0,-0.800777453839,-0.397473275024,-0.67055393586,-0.339164237123,-0.792031098154],
			[-0.768688293371,-0.614950634697,-0.576868829337,-0.63610719323,-0.730606488011,-0.672778561354],
			[-0.940130963517,-0.534144059869,-0.455565949486,-0.408793264733,-0.661365762395,-1.0],
			[-0.6592,-0.6704,-0.7728,-0.584,-0.6288,-0.6848],
			[-0.788639365918,-0.513870541612,-0.799207397622,-0.449141347424,-0.686922060766,-0.762219286658],
			[-0.780336581045,-0.684676705049,-0.707705934455,-0.461470327724,-0.640389725421,-0.725420726306],
			[-0.768292682927,-0.662601626016,-0.596544715447,-0.525406504065,-0.676829268293,-0.770325203252],
			[-0.654794520548,-0.522191780822,-0.570410958904,-0.849863013699,-0.618630136986,-0.784109589041],
			[-0.898599066044,-0.766511007338,-0.455637091394,-0.602401601067,-0.47631754503,-0.800533689126],
			[-0.650017711654,-0.64576691463,-0.81863266029,-0.794544810485,-0.487070492384,-0.603967410556],
			[-0.563794983642,-0.616139585605,-0.6346782988,-0.672846237732,-0.693565976009,-0.818974918212],
			[-0.707558859975,-0.520859149112,-0.530772408096,-0.787691036762,-0.564642709624,-0.888475836431],
			[-0.826086956522,-0.652173913043,-0.718966603655,-0.649653434152,-0.542533081285,-0.610586011342],
			[-0.789960369881,-0.652575957728,-0.859973579921,-0.682959048877,-0.575957727873,-0.43857331572],
			[-0.763220205209,-0.730860299921,-0.833464877664,-0.662194159432,-0.49408050513,-0.516179952644],
			[-0.684147794994,-0.707985697259,-0.680572109654,-0.597139451728,-0.646007151371,-0.684147794994],
			[-0.746798029557,-0.580295566502,-0.512315270936,-0.670935960591,-0.637438423645,-0.852216748768],
			[-0.620592383639,-0.705218617772,-0.796897038082,-0.612129760226,-0.658674188999,-0.606488011283],
			[-0.720541401274,-0.738057324841,-0.694267515924,-0.62101910828,-0.654458598726,-0.571656050955],
			[-0.485849056604,-0.439465408805,-0.805031446541,-0.959119496855,-0.838050314465,-0.47248427673],
			[-0.703495630462,-0.685393258427,-0.628589263421,-0.5911360799,-0.700998751561,-0.69038701623],
			[-0.715363881402,-0.592452830189,-0.573045822102,-0.622641509434,-0.771428571429,-0.725067385445],
			[-0.708626760563,-0.617077464789,-0.549295774648,-0.617957746479,-0.721830985915,-0.785211267606],
			[-0.72602739726,-0.53852739726,-0.564212328767,-0.815068493151,-0.702054794521,-0.654109589041],
			[-0.707794075352,-0.524302559678,-0.763589301122,-0.851020995111,-0.507046304285,-0.646246764452],
			[-0.743119266055,-0.564875491481,-0.893840104849,-0.799475753604,-0.533420707733,-0.465268676278],
			[-0.797108673978,-0.668494516451,-0.787637088734,-0.661515453639,-0.486041874377,-0.599202392822],
			[-0.660672400313,-0.508209538702,-0.695074276779,-0.851446442533,-0.558248631744,-0.72634870993],
			[-0.724568490635,-0.497612926919,-0.570326845391,-0.872199779655,-0.72970987881,-0.60558207859],
			[-0.786085150571,-0.666666666667,-0.758047767394,-0.616822429907,-0.595015576324,-0.577362409138],
			[-0.744095875925,-0.622841029256,-0.715192104336,-0.711667254142,-0.594642227705,-0.611561508636],
			[-0.749546279492,-0.601451905626,-0.666061705989,-0.701633393829,-0.588384754991,-0.692921960073],
			[-0.737506575487,-0.649658074698,-0.714886901631,-0.642819568648,-0.59863229879,-0.656496580747],
			[-0.753312014619,-0.583371402467,-0.789858382823,-0.698492462312,-0.601644586569,-0.573321151211],
			[-0.827202737382,-0.573139435415,-0.610778443114,-0.72626176219,-0.559452523524,-0.703165098375],
			[-0.773913043478,-0.509316770186,-0.822360248447,-0.742857142857,-0.633540372671,-0.51801242236],
			[-0.683801295896,-0.663066954644,-0.696760259179,-0.58444924406,-0.726133909287,-0.645788336933],
			[-0.69450101833,-0.615362234507,-0.494908350305,-0.519930171661,-0.686936281641,-0.988361943555],
			[-0.718301435407,-0.602870813397,-0.794258373206,-0.672846889952,-0.56519138756,-0.646531100478],
			[-0.651766709238,-0.652618135377,-0.739463601533,-0.612601106854,-0.667943805875,-0.675606641124],
			[-0.610655737705,-0.568852459016,-0.669672131148,-0.618032786885,-0.722131147541,-0.810655737705],
			[-0.676595744681,-0.584526112186,-0.787234042553,-0.573694390716,-0.601547388781,-0.776402321083],
			[-0.830036221789,-0.548063527445,-0.406519921984,-0.755363611034,-0.67288938423,-0.787127333519],
			[-0.727125767863,-0.512447462011,-0.71225347559,-0.903653410928,-0.658583899127,-0.485935984481],
			[-0.801007556675,-0.496221662469,-0.48026868178,-0.703610411419,-0.617968094039,-0.900923593619],
			[-0.697257026752,-0.506942092787,-0.781239417541,-0.811039620725,-0.528614967829,-0.674906874365],
			[-0.688546255507,-0.483259911894,-0.511894273128,-0.874449339207,-0.774889867841,-0.666960352423],
			[-0.824320759694,-0.588499076761,-0.858084938011,-0.68451595885,-0.557372724875,-0.48720654181],
			[-0.70290878283,-0.523863315448,-0.670149675233,-0.865009884213,-0.60180739904,-0.636260943236],
			[-0.712434691745,-0.510971786834,-0.781818181818,-0.867920585162,-0.570741901776,-0.556112852665],
			[-0.828371278459,-0.50122591944,-0.359719789842,-0.802451838879,-0.586690017513,-0.921541155867],
			[-0.763518385004,-0.63590483057,-0.870944484499,-0.648882480173,-0.545782263879,-0.534967555876],
			[-0.747568208778,-0.564887307236,-0.488493475682,-0.732384341637,-0.64650059312,-0.820166073547],
			[-0.821613236815,-0.654084798345,-0.876938986556,-0.669596690796,-0.46639089969,-0.511375387797],
			[-0.762896825397,-0.660218253968,-0.962301587302,-0.753968253968,-0.470734126984,-0.389880952381],
			[-0.820368885325,-0.66639935846,-0.634322373697,-0.698476343224,-0.562149157979,-0.618283881315],
			[-0.4375,-0.590073529412,-0.989889705882,-0.809283088235,-0.650275735294,-0.522977941176],
			[-0.747113163972,-0.636258660508,-0.653579676674,-0.636258660508,-0.62817551963,-0.698614318707],
			[-0.809917355372,-0.607438016529,-0.642561983471,-0.715909090909,-0.556818181818,-0.667355371901],
			[-0.710023310023,-0.640093240093,-0.624242424242,-0.690442890443,-0.567365967366,-0.767832167832],
			[-0.693212447929,-0.50012251899,-0.528056848812,-0.88385199706,-0.77358490566,-0.621171281549],
			[-0.759959486833,-0.678595543552,-0.642808912897,-0.800472653612,-0.610735989196,-0.50742741391],
			[-0.824451410658,-0.546798029557,-0.596954769369,-0.76354679803,-0.69144648455,-0.576802507837],
			[-0.810051107325,-0.696337308348,-0.589011925043,-0.743185689949,-0.539608177172,-0.621805792164],
			[-0.725235849057,-0.615172955975,-0.815644654088,-0.80070754717,-0.559748427673,-0.483490566038],
			[-0.875106443372,-0.600908316775,-0.670167470905,-0.707067839909,-0.472040874255,-0.674709054783],
			[-0.864858199753,-0.502836004932,-0.649815043157,-0.682367447596,-0.523551171393,-0.776572133169],
			[-0.619258662369,-0.61361804996,-0.747784045125,-0.807010475423,-0.604754230459,-0.607574536664],
			[-0.45049272642,-0.564992961051,-0.972313467855,-0.8385734397,-0.639605818864,-0.53402158611],
			[-0.628250591017,-0.640070921986,-0.586288416076,-0.707446808511,-0.628841607565,-0.809101654846],
			[-0.779750581272,-0.624603677869,-0.507080955401,-0.576833650391,-0.546396110759,-0.965335024308],
			[-0.66026289181,-0.619143916414,-0.661611054938,-0.74384900573,-0.584765756657,-0.730367374452],
			[-0.617343427392,-0.608396421198,-0.683413626979,-0.774948382657,-0.600137646249,-0.715760495526],
			[-0.612815269257,-0.61554192229,-0.646898432175,-0.760736196319,-0.638718473074,-0.725289706885],
			[-0.584295612009,-0.671285604311,-0.857582755966,-0.703618167821,-0.612009237875,-0.571208622017],
			[-0.956538917424,-0.534176214935,-0.465823785065,-0.625049387594,-0.495061240616,-0.923350454366],
			[-0.883592574009,-0.61866532865,-0.64743268105,-0.712995484195,-0.452416792106,-0.68489713999],
			[-0.839961358879,-0.51215585252,-0.550796973112,-0.743680566736,-0.513121880535,-0.840283368218],
			[-0.83833226973,-0.546054031057,-0.559242714316,-0.677089980855,-0.540097851521,-0.839183152521],
			[-0.846597206828,-0.581910884505,-0.566836621592,-0.713145643981,-0.519397029483,-0.772112613611],
			[-0.844496487119,-0.553161592506,-0.711475409836,-0.654332552693,-0.499297423888,-0.737236533958],
			[-0.90527607362,-0.499877300613,-0.463067484663,-0.696196319018,-0.530306748466,-0.90527607362],
			[-0.675305442429,-0.499814883377,-0.49574231766,-0.831914105887,-0.635690485006,-0.861532765642],
			[-0.7153784219,-0.549516908213,-0.426328502415,-0.807165861514,-0.618760064412,-0.882850241546],
			[-0.68115942029,-0.524200164069,-0.514902925896,-0.823352474706,-0.589280831282,-0.867104183757],
			[-0.635236830456,-0.693669765383,-0.700752545374,-0.72023019035,-0.628154050465,-0.621956617973],
			[-0.403155421282,-0.675058744545,-0.969788519637,-0.865726753944,-0.658945955018,-0.427324605572],
			[-0.650539784086,-0.664134346261,-0.71931227509,-0.709716113555,-0.628948420632,-0.627349060376],
			[-0.39218328841,-0.75,-1.0,-0.88679245283,-0.541778975741,-0.429245283019],
			[-0.609501738123,-0.725376593279,-0.811123986095,-0.687137891078,-0.581691772885,-0.58516801854],
			[-0.647305808258,-0.685094471659,-0.771868439468,-0.62211336599,-0.601119664101,-0.672498250525],
			[-0.815505397448,-0.524370297677,-0.719332679097,-0.722603859993,-0.525024533857,-0.693163231927],
			[-0.822703335284,-0.700994733762,-0.624341720304,-0.715623171445,-0.534815681685,-0.601521357519],
			[-0.72684160607,-0.617451786279,-0.607967119823,-0.791969649067,-0.583939298135,-0.671830540626],
			[-0.706504065041,-0.512195121951,-0.587804878049,-0.717886178862,-0.641463414634,-0.834146341463],
			[-0.813014827018,-0.530477759473,-0.668863261944,-0.707578253707,-0.550247116969,-0.72981878089],
			[-0.801541425819,-0.622350674374,-0.757225433526,-0.691714836224,-0.523121387283,-0.604046242775],
			[-0.638686131387,-0.590510948905,-0.637226277372,-0.739416058394,-0.64598540146,-0.748175182482],
			[-0.957792207792,-0.734415584416,-0.388311688312,-0.663636363636,-0.466233766234,-0.78961038961],
			[-0.602090819993,-0.576608951323,-0.906566481542,-0.802025481869,-0.648480888598,-0.464227376674],
			[-0.632227488152,-0.638862559242,-0.679620853081,-0.759241706161,-0.576303317536,-0.713744075829],
			[-0.678212290503,-0.645810055866,-0.719553072626,-0.778770949721,-0.579888268156,-0.597765363128],
			[-0.844380403458,-0.697982708934,-0.643804034582,-0.610374639769,-0.460518731988,-0.742939481268],
			[-0.698606271777,-0.693379790941,-0.635888501742,-0.599303135889,-0.642857142857,-0.729965156794],
			[-1.0,-0.995498030388,-0.56555993247,-0.41924592009,-0.450759707372,-0.568936409679],
			[-0.619289340102,-0.568527918782,-0.610406091371,-0.809644670051,-0.752538071066,-0.639593908629],
			[-0.670571010249,-0.663250366032,-0.604685212299,-0.698389458272,-0.663250366032,-0.699853587116],
			[-0.475035663338,-0.60485021398,-0.848787446505,-0.764621968616,-0.554921540656,-0.751783166904],
			[-0.86344127975,-0.634802965275,-0.997658993367,-0.513850955911,-0.492001560671,-0.498244245025],
			[-0.863417982155,-0.632120796156,-0.432395332876,-0.655456417296,-0.497597803706,-0.919011667811],
			[-0.64367816092,-0.590804597701,-0.636781609195,-0.61724137931,-0.68275862069,-0.828735632184],
			[-0.808321645629,-0.520336605891,-0.629733520337,-0.670874240299,-0.575502571295,-0.79523141655],
			[-0.833157338965,-0.539598732841,-0.862724392819,-0.636747624076,-0.421330517423,-0.706441393875],
			[-0.661733615222,-0.696617336152,-0.950317124736,-0.720930232558,-0.549682875264,-0.420718816068],
			[-0.690246516613,-0.618435155413,-0.538049303323,-0.772775991426,-0.613076098607,-0.76741693462],
			[-0.637521713955,-0.602779386219,-0.666473653735,-0.742906774754,-0.639837869137,-0.7104806022],
			[-0.520181405896,-0.633560090703,-0.896598639456,-0.861224489796,-0.645351473923,-0.443083900227],
			[-0.696590909091,-0.622727272727,-0.635227272727,-0.773863636364,-0.603409090909,-0.668181818182]
		])
		if trainingTarget:
			return np.array([
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0]
		])
		if testingInput:
			return np.array([
			[-0.983146067416,-0.696629213483,-0.426966292135,-0.516853932584,-0.463483146067,-0.912921348315],
			[-0.848695652174,-0.514782608696,-0.653913043478,-0.754782608696,-0.674782608696,-0.553043478261],
			[-0.574432296047,-0.411269974769,-0.888982338099,-0.999158957107,-0.835155592935,-0.291000841043],
			[-0.938818565401,-0.64135021097,-0.35970464135,-0.567510548523,-0.566455696203,-0.926160337553],
			[-0.912997903564,-0.520964360587,-0.343815513627,-0.666666666667,-0.572327044025,-0.98322851153],
			[-1.0,-0.649509803922,-0.557598039216,-0.730392156863,-0.552696078431,-0.509803921569],
			[-0.685468451243,-0.225621414914,-0.877629063098,-1.0,-0.874760994264,-0.336520076482],
			[-0.974674384949,-0.60492040521,-0.306801736614,-0.596237337192,-0.523154848046,-0.994211287988],
			[-1.0,-0.647940074906,-0.553772070626,-0.71214553237,-0.559122525415,-0.527019796683],
			[-0.999355462456,-0.525620367386,-0.661617789236,-0.733161456655,-0.44698678698,-0.633258137286],
			[-0.637371338084,-0.369754552652,-0.98178939034,-1.0,-0.733966745843,-0.27711797308],
			[-0.752783964365,-0.462138084633,-0.380846325167,-1.0,-0.665924276169,-0.738307349666],
			[-0.708969465649,-0.572519083969,-0.605916030534,-0.899809160305,-0.532442748092,-0.68034351145],
			[-1.0,-0.541154791155,-0.323095823096,-0.688574938575,-0.544226044226,-0.902948402948],
			[-0.687358916479,-0.541760722348,-0.698645598194,-0.98532731377,-0.51467268623,-0.57223476298],
			[-0.735056542811,-0.467528271405,-0.637479806139,-0.988368336026,-0.528917609047,-0.642649434572],
			[-1.0,-0.735019241341,-0.423859263332,-0.659153380979,-0.280923584387,-0.901044529962],
			[-0.670080862534,-0.678706199461,-0.995687331536,-0.949326145553,-0.415633423181,-0.290566037736],
			[-0.589359310603,-0.508430123642,-0.919820157362,-0.957287373548,-0.638066691645,-0.3870363432],
			[-0.730348258706,-0.603980099502,-0.540298507463,-0.884577114428,-0.580099502488,-0.660696517413],
			[-1.0,-0.881237113402,-0.427628865979,-0.659381443299,-0.294845360825,-0.736907216495],
			[-1.0,-0.749606299213,-0.444094488189,-0.596850393701,-0.269291338583,-0.940157480315],
			[-0.637760702525,-0.427003293085,-0.714599341383,-0.945115257958,-0.495060373216,-0.780461031833],
			[-0.816753926702,-0.546247818499,-0.528795811518,-0.830715532286,-0.401396160558,-0.876090750436],
			[-0.615763546798,-0.673234811166,-0.686371100164,-0.632183908046,-0.706075533662,-0.686371100164],
			[-0.945794392523,-0.564485981308,-0.455140186916,-0.403738317757,-0.631775700935,-0.999065420561],
			[-0.625142857143,-0.497142857143,-0.481142857143,-0.856,-0.714285714286,-0.826285714286],
			[-0.766666666667,-0.584057971014,-0.559420289855,-0.676811594203,-0.686956521739,-0.726086956522],
			[-0.656462585034,-0.557823129252,-0.547619047619,-0.702947845805,-0.685941043084,-0.849206349206],
			[-0.718298223874,-0.56712102437,-0.567947129285,-0.832300702189,-0.721602643536,-0.592730276745],
			[-0.676726342711,-0.587723785166,-0.609207161125,-0.667519181586,-0.585677749361,-0.873145780051],
			[-0.670368725011,-0.679253665038,-0.65348733896,-0.578853842737,-0.713904931142,-0.704131497112],
			[-0.668614357262,-0.603505843072,-0.75959933222,-0.668614357262,-0.613522537563,-0.686143572621],
			[-0.728090952155,-0.567977261961,-0.688299384178,-0.586925627665,-0.678825201326,-0.749881572714],
			[-0.854160868355,-0.685499582522,-0.929306985806,-0.665460617868,-0.388811578068,-0.476760367381],
			[-0.716760502382,-0.509311390212,-0.787353832828,-0.871372888696,-0.566478995236,-0.548722390645],
			[-0.849547920434,-0.642676311031,-0.745388788427,-0.668716094033,-0.531283905967,-0.562386980108],
			[-0.800229621125,-0.590508993494,-0.905855338691,-0.642556448527,-0.539226942212,-0.521622655951],
			[-0.624161073826,-0.578859060403,-0.545302013423,-0.58389261745,-0.77432885906,-0.893456375839],
			[-0.648005854372,-0.63117453348,-0.859495060373,-0.674350530553,-0.571899012075,-0.615075009147],
			[-0.814881219184,-0.535634244733,-0.619901389511,-0.785298072613,-0.6620349619,-0.582250112057],
			[-0.649315068493,-0.606743940991,-0.757218124341,-0.80990516333,-0.589462592202,-0.587355110643],
			[-0.629970246146,-0.665674871517,-0.840952123343,-0.703543413579,-0.559642953746,-0.600216391669],
			[-0.949804432855,-0.721642764016,-0.460886571056,-0.526727509778,-0.45371577575,-0.887222946545],
			[-0.767157894737,-0.603368421053,-0.512421052632,-0.585684210526,-0.558736842105,-0.972631578947],
			[-0.65325738697,-0.641865432538,-0.616945532218,-0.74510501958,-0.604841580634,-0.73798504806],
			[-0.799054787327,-0.773148958516,-0.61106248906,-0.804305968843,-0.512340276562,-0.500087519692],
			[-0.872549019608,-0.613590263692,-0.604800540906,-0.741717376606,-0.47937795808,-0.687964841109],
			[-0.698448732501,-0.500189178963,-0.515323496027,-0.824820279985,-0.623912220961,-0.837306091563],
			[-0.640618101545,-0.695364238411,-0.712141280353,-0.709492273731,-0.600883002208,-0.641501103753],
			[-0.679154658982,-0.750240153698,-0.71469740634,-0.521613832853,-0.622478386167,-0.71181556196],
			[-0.676344597811,-0.738219895288,-0.710613993337,-0.630652070443,-0.621132793908,-0.623036649215],
			[-0.618996222342,-0.701025364274,-0.6956287102,-0.698866702644,-0.624392876417,-0.661090124123],
			[-0.847046773643,-0.527483782861,-0.689996585865,-0.778081256402,-0.483782861045,-0.673608740184],
			[-0.645112781955,-0.506165413534,-0.848421052632,-0.814135338346,-0.714285714286,-0.471879699248],
			[-0.720733427362,-0.534555712271,-0.590973201693,-0.825105782793,-0.622002820874,-0.706629055007],
			[-0.435543766578,-0.597877984085,-0.91299734748,-0.916180371353,-0.64774535809,-0.489655172414],
			[-0.549715909091,-0.615056818182,-0.761363636364,-0.785511363636,-0.615056818182,-0.673295454545],
			[-0.770454545455,-0.546590909091,-0.790909090909,-0.723863636364,-0.440909090909,-0.727272727273],
			[-0.707615341857,-0.677598665926,-0.755419677599,-0.755419677599,-0.510839355197,-0.593107281823]
		])
		if testingTarget:
			return np.array([
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[1,0,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,1],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0]
		])
		
	
	