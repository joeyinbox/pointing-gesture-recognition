#! /usr/bin/python
import os, sys


class Settings:
		
	def __init__(self):
		# Determine if the application is a script file or an executable
		if getattr(sys, 'frozen', False):
			self.application_path = os.path.dirname(sys.executable)
		elif __file__:
			self.application_path = os.path.dirname(__file__)+"/../../"
		
		self._dataset_folder = "dataset/"
		self._training_folder = self._dataset_folder + "training/"
		self._positive_testing_folder = self._dataset_folder + "testing/positive/"
		self._negative_testing_folder = self._dataset_folder + "testing/negative/"
	
	
	def getDatasetFolder(self):
		return os.path.join(self.application_path, self._dataset_folder)
	
	def getTrainingFolder(self):
		return os.path.join(self.application_path, self._training_folder)
	
	def getPositiveTestingFolder(self):
		return os.path.join(self.application_path, self._positive_testing_folder)
	
	def getNegativeTestingFolder(self):
		return os.path.join(self.application_path, self._negative_testing_folder)