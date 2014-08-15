#! /usr/bin/python
import numpy as np
import sys

from classes.BPNHandler import *
from classes.DatasetManager import *
from classes.FeatureExtractor import *
from classes.Settings import *
from classes.Utils import *
from classes.Validator import *
from classes.Utils import *

from mpl_toolkits.mplot3d import Axes3D, proj3d
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from itertools import product, combinations



class Accuracy:
	bpn = BPNHandler(True)
	datasetManager = DatasetManager()
	featureExtractor = FeatureExtractor()
	settings = Settings()
	utils = Utils()
	validator = Validator()

	expectedRadius = 2000
	
	

	def getDatasetFiles(self):
		return np.array([
			self.utils.getFileList(self.settings.getAccuracyFolder())
		])
	
	
	def measuredPointedDirection(self):
		dataset = self.datasetManager.loadDataset(self.getDatasetFiles())
		output = []
		
		for data in dataset:
			fingerTipCoordinates = data.fingerTip
			eyeCoordinates = data.eye
			targetCoordinates = data.target
			
			distance = self.validator.findIntersectionDistance(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
			if distance == None:
				print "Missed..."
			else:
				print "The pointed direction intersects the target at a distance of {0:0.1f} mm.".format(distance)
				output.append(distance)
		
		print "Average distance of {0:0.1f} mm.".format(np.average(output))
	
	
	def processedPointedDirection(self):
		dataset = self.datasetManager.loadDataset(self.getDatasetFiles())
		output = []
		
		for data in dataset:
			features = self.featureExtractor.getFeatures(data)
			
			depthMap = data.depth_map
			targetCoordinates = data.target
			
			fingerTipCoordinates = self.featureExtractor.fingerTip[0]
			fingerTipCoordinates.append(self.utils.getDepthFromMap(depthMap, fingerTipCoordinates))
			
			eyeCoordinates = self.featureExtractor.eyePosition[0]
			eyeCoordinates.append(self.utils.getDepthFromMap(depthMap, eyeCoordinates))
			
			
			distance = self.validator.findIntersectionDistance(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
			if distance == None:
				print "Missed..."
			else:
				print "The pointed direction intersects the target at a distance of {0:0.1f} mm.".format(distance)
				output.append(distance)
		
		print "Average distance of {0:0.1f} mm.".format(np.average(output))
	
	
	def drawTrajectories(self):
		# Load the dataset
		dataset = self.datasetManager.loadDataset(self.getDatasetFiles())
		
		
		# Create the scene
		fig = plt.figure()
		ax = fig.gca(projection='3d')
		ax.set_aspect("equal")
		
		ax.set_xlabel('X (horizontal)')
		ax.set_ylabel('Y (vertical)')
		ax.set_zlabel('Z (depth)')
		
		
		for data in dataset:
			
			result = self.featureExtractor.getFeatures(data)
			
			
			# Processed data
			fingerTipCoordinates = self.featureExtractor.fingerTip[0]
			eyeCoordinates = self.featureExtractor.eyePosition[0]
			targetCoordinates = data.target
			depthMap = data.depth_map
			
			fingerTipCoordinates.append(self.utils.getDepthFromMap(depthMap, fingerTipCoordinates))
			eyeCoordinates.append(self.utils.getDepthFromMap(depthMap, eyeCoordinates))
			
			print fingerTipCoordinates
			print eyeCoordinates
			print targetCoordinates
			print
			
			closest = self.validator.findIntersection(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
			
			if closest != None:
				
				
				x = [fingerTipCoordinates[0]-targetCoordinates[0], closest[0]-targetCoordinates[0]]
				y = [fingerTipCoordinates[1]-targetCoordinates[1], closest[1]-targetCoordinates[1]]
				z = [fingerTipCoordinates[2]-targetCoordinates[2], closest[2]-targetCoordinates[2]]
				
				# Draw the impact point
				#ax.scatter(closest[0]-targetCoordinates[0], closest[1]-targetCoordinates[1], closest[2]-targetCoordinates[2], color="r", marker="^", s=100)
				ax.plot(x, y, z)
		
		# Draw the target point
		ax.scatter(0, 0, 0, c="#000000", marker="o", s=2000)
		
		plt.show()
		
		sys.exit(1)



if __name__ == "__main__":
	accuracy = Accuracy()
	accuracy.drawTrajectories()




