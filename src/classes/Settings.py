#! /usr/bin/python
import os, sys


class Settings:
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
		
		self._dataset_folder = "dataset/full/"
		
		self._light_dataset_folder = "dataset/light/"
		self._positive_light_folder = self._light_dataset_folder + "positive/"
		self._negative_light_folder = self._light_dataset_folder + "negative/"
	
	
	def getResourceFolder(self):
		return os.path.join(self.application_path, self._resource_folder)
	
	def getDatasetFolder(self):
		return os.path.join(self.application_path, self._dataset_folder)
	
	
	def getCompleteDatasetFolder(self, orientation, direction):
		if orientation == Settings.BACK_RIGHT:
			orientation = "back-right/"
		elif orientation == Settings.RIGHT:
			orientation = "right/"
		elif orientation == Settings.FRONT_RIGHT:
			orientation = "front-right/"
		elif orientation == Settings.FRONT:
			orientation = "front/"
		elif orientation == Settings.FRONT_LEFT:
			orientation = "front-left/"
		elif orientation == Settings.LEFT:
			orientation = "left/"
		elif orientation == Settings.BACK_LEFT:
			orientation = "back-left/"
		else:
			raise "Invalid orientation id", orientation
		
		
		if direction == Settings.UP:
			direction = "up/"
		elif direction == Settings.LATERAL:
			direction = "lateral/"
		elif direction == Settings.DOWN:
			direction = "down/"
		else:
			raise "Invalid direction id", direction
		
		
		return self.getDatasetFolder()+orientation+direction
	
	
	
	def getLightDatasetFolder(self):
		return os.path.join(self.application_path, self._light_dataset_folder)
	
	def getPositiveLightFolder(self):
		return os.path.join(self.application_path, self._positive_light_folder)
	
	def getNegativeLightFolder(self):
		return os.path.join(self.application_path, self._negative_light_folder)