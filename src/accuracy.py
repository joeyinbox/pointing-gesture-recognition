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

from matplotlib.colors import ColorConverter






class Accuracy:
	bpn = BPNHandler(True)
	datasetManager = DatasetManager()
	featureExtractor = FeatureExtractor()
	settings = Settings()
	utils = Utils()
	validator = Validator()

	expectedRadius = 2000
	
	

	
	
	def measuredPointedDirection(self):
		dataset = self.datasetManager.loadDataset(self.datasetManager.getAccuracyComplete())
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
		dataset = self.datasetManager.loadDataset(self.datasetManager.getAccuracyComplete())
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
	
	
	def drawUnifiedTrajectories(self):
		# Load the dataset
		dataset = self.datasetManager.loadDataset(self.datasetManager.getAccuracyComplete())
		
		
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
			
			closest = self.validator.findIntersection(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
			
			if closest != None:
				
				
				x = [fingerTipCoordinates[0]-targetCoordinates[0], closest[0]-targetCoordinates[0]]
				y = [fingerTipCoordinates[1]-targetCoordinates[1], closest[1]-targetCoordinates[1]]
				z = [fingerTipCoordinates[2]-targetCoordinates[2], closest[2]-targetCoordinates[2]]
				
				# Draw the impact point
				ax.plot(x, y, z)
		
		# Draw the target point
		ax.scatter(0, 0, 0, c="#000000", marker="o", s=2000)
		
		plt.show()
	
	
	def drawImpacts(self):
		# Load the dataset
		dataset = self.datasetManager.loadDataset(self.datasetManager.getAccuracyComplete())
		
		
		# Create the scene
		fig = plt.figure()
		ax = fig.gca(projection='3d')
		ax.set_aspect("equal")
		
		ax.set_xlabel('X (horizontal in mm)')
		ax.set_ylabel('Y (vertical in mm)')
		ax.set_zlabel('Z (depth in mm)')
		
		
		colorConverter = ColorConverter()
		
		
		for data in dataset:
			
			result = self.featureExtractor.getFeatures(data)
			
			
			# Processed data
			fingerTipCoordinates = self.featureExtractor.fingerTip[0]
			eyeCoordinates = self.featureExtractor.eyePosition[0]
			targetCoordinates = data.target
			depthMap = data.depth_map
			
			fingerTipCoordinates.append(self.utils.getDepthFromMap(depthMap, fingerTipCoordinates))
			eyeCoordinates.append(self.utils.getDepthFromMap(depthMap, eyeCoordinates))
			
			closest = self.validator.findIntersection(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
			
			
			if closest != None:
				x = closest[0]-targetCoordinates[0]
				y = closest[1]-targetCoordinates[1]
				z = closest[2]-targetCoordinates[2]
				
				distance = self.validator.findIntersectionDistance(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
				
				red = 1-(distance/200)
				if red < 0:
					red = 0
				elif red > 1:
					red = 1
				
				blue = 0+(distance/200)
				if blue < 0:
					blue = 0
				elif blue > 1:
					blue = 1
				
				cc = colorConverter.to_rgba((red,0,blue), 0.4)
				
				# Draw the impact point
				ax.scatter(x, y, z, color=cc, marker="o", s=50)
		
		# Draw the target point
		ax.scatter(0, 0, 0, c="#000000", marker="o", color="#000000", s=100)
		
		plt.show()
	
	
	
	def drawImpacts2D(self, x=True, y=True, z=False):
		# Load the dataset
		dataset = self.datasetManager.loadDataset(self.datasetManager.getAccuracyComplete())
		
		plt.axis("equal")
		colorConverter = ColorConverter()
		
		for data in dataset:
			
			result = self.featureExtractor.getFeatures(data)
			
			
			# Processed data
			fingerTipCoordinates = self.featureExtractor.fingerTip[0]
			eyeCoordinates = self.featureExtractor.eyePosition[0]
			targetCoordinates = data.target
			depthMap = data.depth_map
			
			fingerTipCoordinates.append(self.utils.getDepthFromMap(depthMap, fingerTipCoordinates))
			eyeCoordinates.append(self.utils.getDepthFromMap(depthMap, eyeCoordinates))
			
			closest = self.validator.findIntersection(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
			
			
			if closest != None:
				x = closest[0]-targetCoordinates[0]
				y = closest[1]-targetCoordinates[1]
				z = closest[2]-targetCoordinates[2]
				
				distance = self.validator.findIntersectionDistance(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
				
				red = 1-(distance/200)
				if red < 0:
					red = 0
				elif red > 1:
					red = 1
				
				blue = 0+(distance/200)
				if blue < 0:
					blue = 0
				elif blue > 1:
					blue = 1
				
				cc = colorConverter.to_rgba((red,0,blue), 0.4)
				
				if not x:
					plt.scatter(y, z, color=cc, marker="o", s=50)
				elif not y:
					plt.scatter(x, z, color=cc, marker="o", s=50)
				else:
					plt.scatter(x, y, color=cc, marker="o", s=50)
		
		plt.show()




if __name__ == "__main__":
	accuracy = Accuracy()
	accuracy.drawImpacts2D()




