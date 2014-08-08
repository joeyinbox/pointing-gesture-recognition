#! /usr/bin/python
import os, sys


class Settings:
		
	def __init__(self):
		# Determine if the application is a script file or an executable
		if getattr(sys, 'frozen', False):
			self.application_path = os.path.dirname(sys.executable)
		elif __file__:
			self.application_path = os.path.dirname(__file__)+"/../../"
		
		self._resource_folder = "res/"
		
		self._dataset_folder = "dataset/full/"
		self._training_folder = self._dataset_folder + "training/"
		self._positive_testing_folder = self._dataset_folder + "testing/positive/"
		self._negative_testing_folder = self._dataset_folder + "testing/negative/"
		
		self._light_dataset_folder = "dataset/light/"
		self._positive_light_folder = self._light_dataset_folder + "positive/"
		self._negative_light_folder = self._light_dataset_folder + "negative/"
	
	
	def getResourceFolder(self):
		return os.path.join(self.application_path, self._resource_folder)
	
	def getDatasetFolder(self):
		return os.path.join(self.application_path, self._dataset_folder)
		
	
	def getTrainingFolder(self):
		return os.path.join(self.application_path, self._training_folder)
	
	def getPositiveTestingFolder(self):
		return os.path.join(self.application_path, self._positive_testing_folder)
	
	def getNegativeTestingFolder(self):
		return os.path.join(self.application_path, self._negative_testing_folder)
	
	
	
	def getLightDatasetFolder(self):
		return os.path.join(self.application_path, self._light_dataset_folder)
	
	def getPositiveLightFolder(self):
		return os.path.join(self.application_path, self._positive_light_folder)
	
	def getNegativeLightFolder(self):
		return os.path.join(self.application_path, self._negative_light_folder)