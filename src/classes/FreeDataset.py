#! /usr/bin/python
import json, utils
from copy import deepcopy
from classes.Settings import *


class FreeDataset:
	TYPE_POSITIVE = 0
	TYPE_NEGATIVE = 1
	
	
	def __init__(self):
		
		print "Free dataset chosen"
		
		self.settings = Settings()
		
		self.camera_height = 1500
		self.hand = []
		self.depth_map = []
		self.image = ""
		self.type = LightDataset.TYPE_POSITIVE
		
	
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
		if self.type == LightDataset.TYPE_POSITIVE:
			filename = self.settings.getPositiveFreeFolder()
		elif self.type == LightDataset.TYPE_NEGATIVE:
			filename = self.settings.getNegativeFreeFolder()
		else:
			filename = ""
		
		# Retrieve the number of files saved so far
		# Be careful that due to the sample file, the counter does not need to be incremented. Otherwise, the files would replace each others
		filename += str(utils.getFileNumberInFolder(filename)).zfill(3)+".json"
		utils.dumpJsonToFile(self.to_JSON(), filename)
	
	
	
	
	def toggleType(self, value):
		self.type = value
		print "type toggled"