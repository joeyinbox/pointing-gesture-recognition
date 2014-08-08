#! /usr/bin/python
from classes.BPNHandler import *
import numpy as np
import sys
import cv2
from os import listdir
from os.path import isfile, join
import utils

class testBPN():
	
	# Load settings
	settings = Settings()
	
	def previous(self):

		# All positions with up, lateral and down declinasons 
		# ID:	complete1
		positive = np.array([
			[79, 117, 119, 196, 224, 247], # Back right up
			[80, 199, 225, 251], # Back right lateral
			[81, 201, 226, 253], # Back right down
			[1, 11, 37, 44, 48, 87, 122, 126, 136, 151], # Right up
			[2, 12, 38, 45, 49, 88, 123, 127, 137, 152], # Right lateral
			[3, 13, 50, 89, 124, 128, 138, 153], # Right down
			[58, 97, 166, 195, 219, 242], # Front right up
			[59, 60, 98, 167, 192, 221, 244], # Front right lateral
			[61, 99, 168, 194, 223, 245], # Front right down
			[21, 26, 69, 74, 107, 112, 141, 146, 171, 176], # Front up
			[22, 27, 70, 75, 108, 113, 142, 147, 172, 177], # Front lateral
			[23, 28, 71, 76, 109, 114, 143, 148, 173, 178], # Front down
			[16, 40, 53, 64, 102, 131, 161, 182, 215, 236], # Front left up
			[17, 41, 54, 65, 103, 132, 162, 183, 216, 239], # Front left lateral
			[8, 18, 42, 55, 66, 104, 133, 163, 185, 218, 241], # Front left down
			[6, 32, 156, 210, 233, 262], # Left up
			[7, 211, 232, 264], # Left lateral
			[34, 212, 235, 265], # Left down
			[83, 156, 204, 227, 256], # Back left up
			[84, 157, 206, 228, 258], # Back left lateral
			[85, 158, 208, 229, 260] # Back left down
		])
		positiveTarget = np.array([
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





		# Group all position disregarding up, lateral or down
		# ID:	complete2
		positive = np.array([
			[79, 117, 119, 196, 224, 247, 80, 199, 225, 251, 81, 201, 226, 253], # Back right
			[1, 11, 37, 44, 48, 87, 122, 126, 136, 151, 2, 12, 38, 45, 49, 88, 123, 127, 137, 152, 3, 13, 50, 89, 124, 128, 138, 153], # Right
			[58, 97, 166, 195, 219, 242, 59, 60, 98, 167, 192, 221, 244, 61, 99, 168, 194, 223, 245], # Front right
			[21, 26, 69, 74, 107, 112, 141, 146, 171, 176, 22, 27, 70, 75, 108, 113, 142, 147, 172, 177, 23, 28, 71, 76, 109, 114, 143, 148, 173, 178], # Front
			[16, 40, 53, 64, 102, 131, 161, 182, 215, 236, 17, 41, 54, 65, 103, 132, 162, 183, 216, 239, 8, 18, 42, 55, 66, 104, 133, 163, 185, 218, 241], # Front left
			[6, 32, 156, 210, 233, 262, 7, 211, 232, 264, 34, 212, 235, 265], # Left
			[83, 156, 204, 227, 256, 84, 157, 206, 228, 258, 85, 158, 208, 229, 260] # Back left
		])
		positiveTarget = np.array([
			[1,0,0,0,0,0,0],
			[0,1,0,0,0,0,0],
			[0,0,1,0,0,0,0],
			[0,0,0,1,0,0,0],
			[0,0,0,0,1,0,0],
			[0,0,0,0,0,1,0],
			[0,0,0,0,0,0,1]
		])







		# Few simple positions
		# ID:	restrained1
		positive = np.array([
			[1, 11, 37, 44, 48, 87, 122, 126, 136, 151, 2, 12, 38, 45, 49, 88, 123, 127, 137, 152, 3, 13, 50, 89, 124, 128, 138, 153], # Right
			[58, 97, 166, 195, 219, 242, 59, 60, 98, 167, 192, 221, 244, 61, 99, 168, 194, 223, 245], # Front right
			[16, 40, 53, 64, 102, 131, 161, 182, 215, 236, 17, 41, 54, 65, 103, 132, 162, 183, 216, 239, 8, 18, 42, 55, 66, 104, 133, 163, 185, 218, 241], # Front left
			[6, 32, 156, 210, 233, 262, 7, 211, 232, 264, 34, 212, 235, 265], # Left
		])
		positiveTarget = np.array([
			[1,0,0,0],
			[0,1,0,0],
			[0,0,1,0],
			[0,0,0,1]
		])






		# Few simple positions mixed
		# ID:	mixed1
		#positive = np.array([
		#	[1, 11, 37, 44, 48, 87, 122, 126, 136, 151, 2, 12, 38, 45, 49, 88, 123, 127, 137, 152, 3, 13, 50, 89, 124, 128, 138, 153, 58, 97, 166, 195, 219, 242, 59, 60, 98, 167, 192, 221, 244, 61, 99, 168, 194, 223, 245], # Right
		#	[16, 40, 53, 64, 102, 131, 161, 182, 215, 236, 17, 41, 54, 65, 103, 132, 162, 183, 216, 239, 8, 18, 42, 55, 66, 104, 133, 163, 185, 218, 241, 6, 32, 156, 210, 233, 262, 7, 211, 232, 264, 34, 212, 235, 265] # Left
		#])
		#positiveTarget = np.array([
		#	[1,0,],
		#	[0,1,]
		#])









		# Fewer simple positions
		# ID:	obvious1
		#positive = np.array([
		#	[2, 12, 38, 45, 49, 88, 123, 127, 137, 152], # Right lateral
		#	[7, 211, 232, 264] # Left lateral
		#])
		#positiveTarget = np.array([
		#	[1,0],
		#	[0,1]
		#])





		# Old dataset restrained1
		#negative = np.array([0,1,2,3,4,5,6,7,8,9,12,15,16,17,20,21,22,23,24,26,33,42,43])
		


	def getFileList(self, path):
		return [path+f for f in listdir(path) if isfile(join(path,f)) and f!=".DS_Store"]
	
	def count(self, array):
		total = 0
		for i in range(len(array)):
			total += len(array[i])
		return total
	
	
	
	def getPositiveFull(self, type="training"):
		
		folder = self.settings.getPositiveLightFolder()
		
		return np.array([
			self.getFileList("{0}{1}/back-right/up/".format(folder, type)),
			self.getFileList("{0}{1}/back-right/lateral/".format(folder, type)),
			self.getFileList("{0}{1}/back-right/down/".format(folder, type)),
			
			self.getFileList("{0}{1}/right/up/".format(folder, type)),
			self.getFileList("{0}{1}/right/lateral/".format(folder, type)),
			self.getFileList("{0}{1}/right/down/".format(folder, type)),
			
			self.getFileList("{0}{1}/front-right/up/".format(folder, type)),
			self.getFileList("{0}{1}/front-right/lateral/".format(folder, type)),
			self.getFileList("{0}{1}/front-right/down/".format(folder, type)),
			
			self.getFileList("{0}{1}/front/up/".format(folder, type)),
			self.getFileList("{0}{1}/front/lateral/".format(folder, type)),
			self.getFileList("{0}{1}/front/down/".format(folder, type)),
			
			self.getFileList("{0}{1}/front-left/up/".format(folder, type)),
			self.getFileList("{0}{1}/front-left/lateral/".format(folder, type)),
			self.getFileList("{0}{1}/front-left/down/".format(folder, type)),
			
			self.getFileList("{0}{1}/left/up/".format(folder, type)),
			self.getFileList("{0}{1}/left/lateral/".format(folder, type)),
			self.getFileList("{0}{1}/left/down/".format(folder, type)),
			
			self.getFileList("{0}{1}/back-left/up/".format(folder, type)),
			self.getFileList("{0}{1}/back-left/lateral/".format(folder, type)),
			self.getFileList("{0}{1}/back-left/down/".format(folder, type))
		])
	
	
	
	def getPositiveMixed(self, type="training"):
		
		folder = self.settings.getPositiveLightFolder()
		
		backRight = self.getFileList("{0}{1}/back-right/up/".format(folder, type))
		backRight.extend(self.getFileList("{0}{1}/back-right/lateral/".format(folder, type)))
		backRight.extend(self.getFileList("{0}{1}/back-right/down/".format(folder, type)))
		
		right = self.getFileList("{0}{1}/right/up/".format(folder, type))
		right.extend(self.getFileList("{0}{1}/right/lateral/".format(folder, type)))
		right.extend(self.getFileList("{0}{1}/right/down/".format(folder, type)))
		
		frontRight = self.getFileList("{0}{1}/front-right/up/".format(folder, type))
		frontRight.extend(self.getFileList("{0}{1}/front-right/lateral/".format(folder, type)))
		frontRight.extend(self.getFileList("{0}{1}/front-right/down/".format(folder, type)))
		
		front = self.getFileList("{0}{1}/front/up/".format(folder, type))
		front.extend(self.getFileList("{0}{1}/front/lateral/".format(folder, type)))
		front.extend(self.getFileList("{0}{1}/front/down/".format(folder, type)))
		
		frontLeft = self.getFileList("{0}{1}/front-left/up/".format(folder, type))
		frontLeft.extend(self.getFileList("{0}{1}/front-left/lateral/".format(folder, type)))
		frontLeft.extend(self.getFileList("{0}{1}/front-left/down/".format(folder, type)))
		
		left = self.getFileList("{0}{1}/left/up/".format(folder, type))
		left.extend(self.getFileList("{0}{1}/left/lateral/".format(folder, type)))
		left.extend(self.getFileList("{0}{1}/left/down/".format(folder, type)))
		
		backLeft = self.getFileList("{0}{1}/back-left/up/".format(folder, type))
		backLeft.extend(self.getFileList("{0}{1}/back-left/lateral/".format(folder, type)))
		backLeft.extend(self.getFileList("{0}{1}/back-left/down/".format(folder, type)))
		
		
		return np.array([
			backRight,
			right,
			frontRight,
			front,
			frontLeft,
			left,
			backLeft
		])
	
	
	def getPositiveRestrainedMixed(self, type="training"):
		
		folder = self.settings.getPositiveLightFolder()
		
		right = self.getFileList("{0}{1}/right/up/".format(folder, type))
		right.extend(self.getFileList("{0}{1}/right/lateral/".format(folder, type)))
		right.extend(self.getFileList("{0}{1}/right/down/".format(folder, type)))
		
		frontRight = self.getFileList("{0}{1}/front-right/up/".format(folder, type))
		frontRight.extend(self.getFileList("{0}{1}/front-right/lateral/".format(folder, type)))
		frontRight.extend(self.getFileList("{0}{1}/front-right/down/".format(folder, type)))
		
		frontLeft = self.getFileList("{0}{1}/front-left/up/".format(folder, type))
		frontLeft.extend(self.getFileList("{0}{1}/front-left/lateral/".format(folder, type)))
		frontLeft.extend(self.getFileList("{0}{1}/front-left/down/".format(folder, type)))
		
		left = self.getFileList("{0}{1}/left/up/".format(folder, type))
		left.extend(self.getFileList("{0}{1}/left/lateral/".format(folder, type)))
		left.extend(self.getFileList("{0}{1}/left/down/".format(folder, type)))
		
		
		return np.array([
			right,
			frontRight,
			frontLeft,
			left
		])
	
	
	
	def getNegativeFull(self, type="training"):
		
		folder = self.settings.getNegativeLightFolder()
		
		output = self.getFileList("{0}{1}/back-right/closed/".format(folder, type))
		output.extend(self.getFileList("{0}{1}/back-right/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/back-right/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/back-right/three/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/back-right/peace/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/back-right/rock/".format(folder, type)))
		
		output.extend(self.getFileList("{0}{1}/right/closed/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/right/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/right/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/right/three/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/right/peace/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/right/rock/".format(folder, type)))
		
		output.extend(self.getFileList("{0}{1}/front-right/closed/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-right/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-right/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-right/three/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-right/peace/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-right/rock/".format(folder, type)))
		
		output.extend(self.getFileList("{0}{1}/front/closed/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front/three/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front/peace/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front/rock/".format(folder, type)))
		
		output.extend(self.getFileList("{0}{1}/front-left/closed/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-left/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-left/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-left/three/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-left/peace/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-left/rock/".format(folder, type)))
		
		output.extend(self.getFileList("{0}{1}/left/closed/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/left/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/left/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/left/three/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/left/peace/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/left/rock/".format(folder, type)))
		
		output.extend(self.getFileList("{0}{1}/back-left/closed/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/back-left/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/back-left/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/back-left/three/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/back-left/peace/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/back-left/rock/".format(folder, type)))
		
		return np.array(output)
	
	def getNegativeRestrained(self, type="training"):
		
		folder = self.settings.getNegativeLightFolder()
		
		output = self.getFileList("{0}{1}/right/closed/".format(folder, type))
		output.extend(self.getFileList("{0}{1}/right/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/right/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/right/three/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/right/peace/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/right/rock/".format(folder, type)))
		
		output.extend(self.getFileList("{0}{1}/front-right/closed/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-right/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-right/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-right/three/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-right/peace/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-right/rock/".format(folder, type)))
		
		output.extend(self.getFileList("{0}{1}/front-left/closed/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-left/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-left/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-left/three/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-left/peace/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-left/rock/".format(folder, type)))
		
		output.extend(self.getFileList("{0}{1}/left/closed/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/left/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/left/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/left/three/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/left/peace/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/left/rock/".format(folder, type)))
		
		return np.array(output)
	
	def getNegativeMainRestrained(self, type="training"):
		
		folder = self.settings.getNegativeLightFolder()
		
		output = self.getFileList("{0}{1}/right/closed/".format(folder, type))
		output.extend(self.getFileList("{0}{1}/right/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/right/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/right/three/".format(folder, type)))
		
		output.extend(self.getFileList("{0}{1}/front-right/closed/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-right/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-right/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-right/three/".format(folder, type)))
		
		output.extend(self.getFileList("{0}{1}/front-left/closed/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-left/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-left/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/front-left/three/".format(folder, type)))
		
		output.extend(self.getFileList("{0}{1}/left/closed/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/left/opened/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/left/four/".format(folder, type)))
		output.extend(self.getFileList("{0}{1}/left/three/".format(folder, type)))
		
		return np.array(output)
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	def getFullTarget(self):
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
	
	def getRestrainedMixedTarget(self):
		return np.array([
			[1,0,0,0],
			[0,1,0,0],
			[0,0,1,0],
			[0,0,0,1]
		])
	
	# New dataset
	# ID:	complete3
	
	
	def test(self):
		print self.count(self.getPositiveFull())
		print len(self.getNegativeFull())
		
		print
		print self.count(self.getPositiveFull("testing"))
		print len(self.getNegativeFull("testing"))
		
		print
		print self.count(self.getPositiveFull("validating"))
		print len(self.getNegativeFull("validating"))
		
		
		
		sys.exit(1)
		
	
	
	def full(self):
		positiveTraining = self.getPositiveFull("training")
		negativeTraining = self.getNegativeFull("training")
		positiveTesting = self.getPositiveFull("testing")
		negativeTesting = self.getNegativeFull("testing")
		positiveTarget = self.getFullTarget()
		
		# run the network
		self.run(positiveTraining, negativeTraining, positiveTesting, negativeTesting, positiveTarget, True)
		
	
	def testFull(self):
		bpn = BPNHandler()
		bpn.loadNewDataFeatures()
		bpn.run()
		
	
	def restrained(self):
		positiveTraining = self.getPositiveRestrainedMixed("training")
		negativeTraining = self.getNegativeMainRestrained("training")
		positiveTesting = self.getPositiveRestrainedMixed("testing")
		negativeTesting = self.getNegativeMainRestrained("testing")
		positiveTarget = self.getRestrainedMixedTarget()
		
		# run the network
		self.run(positiveTraining, negativeTraining, positiveTesting, negativeTesting, positiveTarget, True)
		
		
	def testRestrained(self):
		bpn = BPNHandler()
		bpn.loadNewDataRestrainedMixedFeatures()
		bpn.run()
		
		
		
	def validateRestrained(self):
		bpn = BPNHandler(True, 6, 33, 4)
		
		positiveValidating = self.getPositiveRestrainedMixed("validating")
		negativeValidating = self.getNegativeMainRestrained("validating")
		
		data = bpn.loadPositive("validating", positiveValidating, [])
		
		print "positive"
		good = 0
		bad = 0
		for d in data:
			result = bpn.test(d, True)
			if result == "None":
				bad += 1
			else:
				good += 1
			#print result
		print
		print "{0} corrects and {1} bad --> {2:0.2f}%".format(good, bad, (good/float(good+bad)*100))
		print
		
		
		data = bpn.loadNegative("validating", negativeValidating, [])
		
		print "negative"
		good2 = 0
		bad2 = 0
		for d in data:
			result = bpn.test(d, True)
			if result != "None":
				bad2 += 1
			else:
				good2 += 1
			#print result
		print
		print "{0} corrects and {1} bad --> {2:0.2f}%".format(good2, bad2, (good2/float(good2+bad2)*100))
		print "Final score = {0:0.2f}%".format(((good+good2)/float(good+bad+good2+bad2))*100)
		
		
		
		
	def run(self, positiveTraining, negativeTraining, positiveTesting, negativeTesting, positiveTarget, getData=False):
		bpn = BPNHandler()
		bpn.loadPositive("training", positiveTraining, positiveTarget)
		bpn.loadNegative("training", negativeTraining, len(positiveTarget[0]))
		
		bpn.loadPositive("testing", positiveTesting, positiveTarget)
		bpn.loadNegative("testing", negativeTesting, len(positiveTarget[0]))
		
		if getData:
			bpn.getData()
		else:
			bpn.run()







test = testBPN()
test.restrained()