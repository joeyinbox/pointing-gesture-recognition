#! /usr/bin/python
import os, sys



# Definition of the Settings class
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
	
	
	
	# Constructor of the Settings class
	# 
	# @param	None
	# @return	None
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
	
	
	# Returns the ressource folder path
	# 
	# @param	None
	# @return	string				Path of the ressource folder
	def getResourceFolder(self):
		return os.path.join(self.application_path, self._resource_folder)
	
	
	# Returns the dataset folder path
	# 
	# @param	None
	# @return	string				Path of the dataset folder
	def getDatasetFolder(self):
		return os.path.join(self.application_path, self._dataset_folder)
	
	
	# Returns the positive dataset folder path
	# 
	# @param	None
	# @return	string				Path of the positive dataset folder
	def getPositiveFolder(self):
		return os.path.join(self.application_path, self._positive_folder)
	
	
	# Returns the negative dataset folder path
	# 
	# @param	None
	# @return	string				Path of the negative dataset folder
	def getNegativeFolder(self):
		return os.path.join(self.application_path, self._negative_folder)
	
	
	# Returns the accuracy dataset folder path
	# 
	# @param	None
	# @return	string				Path of the accuracy dataset folder
	def getAccuracyFolder(self):
		return os.path.join(self.application_path, self._accuracy_folder)