#! /usr/bin/python
import os, sys


class Settings:
	LEFT_HAND = 0
	RIGHT_HAND = 1
	NO_HAND = 2
	BOTH_HAND = 3
	
	BACK_RIGHT = 0
	RIGHT = 1
	FRONT_RIGHT = 2
	FRONT = 3
	FRONT_LEFT = 4
	LEFT = 5
	BACK_LEFT = 6
	
	UP = 0
	LATERAL = 1
	DOWN = 2
	
		
	def __init__(self):
		# Determine if the application is a script file or an executable
		if getattr(sys, 'frozen', False):
			self.application_path = os.path.dirname(sys.executable)
		elif __file__:
			self.application_path = os.path.dirname(__file__)+"/../../"
		
		self._resource_folder = "res/"
		
		self._dataset_folder = "dataset/"
		self._positive_folder = self._dataset_folder + "positive/"
		self._negative_folder = self._dataset_folder + "negative/"
		self._accuracy_folder = self._dataset_folder + "accuracy/"
	
	
	def getResourceFolder(self):
		return os.path.join(self.application_path, self._resource_folder)
	
	
	
	def getDatasetFolder(self):
		return os.path.join(self.application_path, self._dataset_folder)
	
	def getPositiveFolder(self):
		return os.path.join(self.application_path, self._positive_folder)
	
	def getNegativeFolder(self):
		return os.path.join(self.application_path, self._negative_folder)
	
	def getAccuracyFolder(self):
		return os.path.join(self.application_path, self._accuracy_folder)