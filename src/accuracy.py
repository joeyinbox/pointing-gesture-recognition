#! /usr/bin/python
import numpy as np
import sys

from classes.BPNHandler import *
from classes.DatasetManager import *
from classes.FeatureExtractor import *
from classes.Settings import *
from classes.Trigonometry import *
from classes.Utils import *

from mpl_toolkits.mplot3d import Axes3D, proj3d
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from itertools import product, combinations
from matplotlib.colors import ColorConverter



# Definition of the Accuracy class
class Accuracy:
	bpn = BPNHandler(True)
	datasetManager = DatasetManager()
	featureExtractor = FeatureExtractor()
	settings = Settings()
	trigonometry = Trigonometry()
	utils = Utils()
	
	expectedRadius = 2000
	
	direction = [
		"back-right",
		"right",
		"front-right",
		"front",
		"front-left",
		"left",
		"back-left"
	]
	
	
	# Evaluate the pointed direction and display the average distance and angle
	# 
	# @param	None
	# @return	None
	def processedPointedDirection(self):
		dataset = self.datasetManager.loadDataset(self.datasetManager.getAccuracyComplete())
		outputDistance = []
		outputAngle = []
		outputAngleCamera = []
		outputDistanceAt2m = []
		
		for data in dataset:
			features = self.featureExtractor.getFeatures(data)
			
			depthMap = data.depth_map
			targetCoordinates = data.target
			
			fingerTipCoordinates = self.featureExtractor.fingerTip[0]
			fingerTipCoordinates.append(self.utils.getDepthFromMap(depthMap, fingerTipCoordinates))
			
			eyeCoordinates = self.featureExtractor.eyePosition[0]
			eyeCoordinates.append(self.utils.getDepthFromMap(depthMap, eyeCoordinates))
			
			
			# Retrieve the distance between the actual target and the closest impact
			distance = self.trigonometry.findIntersectionDistance(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
			if distance == None:
				print "Missed..."
			else:
				outputDistance.append(distance)
				
				# Retrieve the distance between the target and the fingertip:
				targetDistance = float(data.distance)
				
				# Calculate the error angles
				angle = math.degrees(math.asin(distance/targetDistance))
				outputAngle.append(angle)
				
				angleCamera = math.degrees(math.asin(distance/targetCoordinates[2]))
				outputAngleCamera.append(angleCamera)
				
				distanceAt2m = math.asin(distance/targetDistance)*2000
				outputDistanceAt2m.append(distanceAt2m)
				
				print "--- Impact distance: {0:0.1f} mm\t Impact at 2m: {1:0.1f}\t Error angle (fingertip): {2:0.1f} deg\t Error angle (camera): {3:0.1f} deg".format(distance, distanceAt2m, angle, angleCamera)
				
		
		print "---\n--- Average impact distance of {0:0.1f} mm.".format(np.average(outputDistance))
		print "--- Average impact distance at 2 m of {0:0.1f} mm.".format(np.average(outputDistanceAt2m))
		print "--- Average eror angle of {0:0.1f} deg at the fingertip.".format(np.average(outputAngle))
		print "--- Average eror angle of {0:0.1f} deg at the camera.".format(np.average(outputAngleCamera))
	
	
	# Evaluate the pointed direction by category and display the average distance and angle
	# 
	# @param	None
	# @return	None
	def processedPointedDirectionByCategory(self):
		datasets = self.datasetManager.getAccuracyComplete()
		
		# Load all categories separately
		dataset = []
		for data in datasets:
			dataset.append(self.datasetManager.loadDataset([data]))
		
		
		for category in range(len(dataset)):
			outputDistance = []
			outputAngle = []
			outputAngleCamera = []
			outputDistanceAt2m = []
			
			print "\n--- {0}".format(self.direction[category])
		
			for data in dataset[category]:
				features = self.featureExtractor.getFeatures(data)
				
				depthMap = data.depth_map
				targetCoordinates = data.target
				
				fingerTipCoordinates = self.featureExtractor.fingerTip[0]
				fingerTipCoordinates.append(self.utils.getDepthFromMap(depthMap, fingerTipCoordinates))
				
				eyeCoordinates = self.featureExtractor.eyePosition[0]
				eyeCoordinates.append(self.utils.getDepthFromMap(depthMap, eyeCoordinates))
				
				
				# Retrieve the distance between the actual target and the closest impact
				distance = self.trigonometry.findIntersectionDistance(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
				if distance == None:
					print "Missed..."
				else:
					outputDistance.append(distance)
					
					# Retrieve the distance between the target and the fingertip:
					targetDistance = float(data.distance)
					
					# Calculate the error angles
					angle = math.degrees(math.asin(distance/targetDistance))
					outputAngle.append(angle)
					
					angleCamera = math.degrees(math.asin(distance/targetCoordinates[2]))
					outputAngleCamera.append(angleCamera)
					
					distanceAt2m = math.asin(distance/targetDistance)*2000
					outputDistanceAt2m.append(distanceAt2m)
					
					print "--- Impact distance: {0:0.1f} mm\t Impact at 2m: {1:0.1f}\t Error angle (fingertip): {2:0.1f} deg\t Error angle (camera): {3:0.1f} deg".format(distance, distanceAt2m, angle, angleCamera)
					
			
			print "---\n--- Average impact distance of {0:0.1f} mm.".format(np.average(outputDistance))
			print "--- Average impact distance at 2 m of {0:0.1f} mm.".format(np.average(outputDistanceAt2m))
			print "--- Average eror angle of {0:0.1f} deg at the fingertip.".format(np.average(outputAngle))
			print "--- Average eror angle of {0:0.1f} deg at the camera.".format(np.average(outputAngleCamera))
	
	
	# Draw a graphic with centered trajectories' origins
	# 
	# @param	None
	# @return	None
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
			
			closest = self.trigonometry.findIntersection(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
			
			if closest != None:
				x = [fingerTipCoordinates[0]-targetCoordinates[0], closest[0]-targetCoordinates[0]]
				y = [fingerTipCoordinates[1]-targetCoordinates[1], closest[1]-targetCoordinates[1]]
				z = [fingerTipCoordinates[2]-targetCoordinates[2], closest[2]-targetCoordinates[2]]
				
				# Draw the trajectory
				ax.plot(x, y, z)
		
		# Draw the target point
		ax.scatter(0, 0, 0, c="#000000", marker="o", s=2000)
		plt.show()
	
	
	# Draw a 3D graphic with the closests impacts
	# 
	# @param	None
	# @return	None
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
			
			closest = self.trigonometry.findIntersection(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
			
			
			if closest != None:
				x = closest[0]-targetCoordinates[0]
				y = closest[1]-targetCoordinates[1]
				z = closest[2]-targetCoordinates[2]
				
				distance = self.trigonometry.findIntersectionDistance(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
				
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
	
	
	# Draw a 2D graphic with the closests impacts
	# 
	# @param	x					Flag to display the horizontal axis
	# @param	y					Flag to display the vertical axis
	# @param	z					Flag to display the depth axis
	# @return	None
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
			
			closest = self.trigonometry.findIntersection(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
			
			
			if closest != None:
				x = closest[0]-targetCoordinates[0]
				y = closest[1]-targetCoordinates[1]
				z = closest[2]-targetCoordinates[2]
				
				distance = self.trigonometry.findIntersectionDistance(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
				
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


	# Draw a 3D heatmap from several recorded points
	# 
	# @param	points				Array of all recorded points
	# @param	blurred				Flag to add a blurry effect to all points
	# @return	numeric				Depth of the given coordinates
	def createHeatmap(self, points, blurred=False):
		# Create the scene
		fig = plt.figure()
		ax = fig.gca(projection='3d')
		ax.set_aspect("equal")
		
		# Create axes
		ax.set_xlabel('X (horizontal in mm)')
		ax.set_ylabel('Y (vertical in mm)')
		ax.set_zlabel('Z (depth in mm)')
		
		points = np.array(points)
		
		# Retrieve extrem values
		maxX, maxY, maxZ, tmp = points.max(axis=0)
		minX, minY, minZ, tmp = points.min(axis=0)
		
		# Retrieve middle values
		midX = minX+(maxX-minX)/2
		midY = minY+(maxY-minY)/2
		midZ = minZ+(maxZ-minZ)/2
		
		# Draw center axis
		ax.plot([minX, maxX], [midY, midY], [midZ, midZ])
		ax.plot([midX, midX], [minY, maxY], [midZ, midZ])
		ax.plot([midX, midX], [midY, midY], [minZ, maxZ])
		
		# Add points
		for point in points:
			print "[{0},{1},{2},{3}],".format(point[0], point[1], point[2], point[3])
			
			# Add a blurr effect to points if needed
			if blurred:
				for i in np.arange(0.1,1.01,0.1):
					if point[3] == True:
						c = (1,0,0, 0.3/i/10)
					else:
						c = (0,0,1, 0.3/i/10)
					ax.scatter(point[0], point[1], point[2], s=(50*i*(0.55))**2, color=c)
			else:
				if point[3] == True:
					c = (1,0,0, 0.3)
				else:
					c = (0,0,1, 0.3)
				ax.scatter(point[0], point[1], point[2], s=50, color=c)
		
		# Set the correct view
		#ax.view_init(azim=-128, elev=-163)
		ax.view_init(azim=-89, elev=-74)
		
		# Display the graph
		plt.show()
	
	
	# Draw a 2D heatmap from several recorded points
	# 
	# @param	points				Array of all recorded points
	# @param	view				Point of view to display the proper axes
	# @param	blurred				Flag to add a blurry effect to all points
	# @return	numeric				Depth of the given coordinates
	def showHeatmap(self, points, view, blurred=True):
		if view != "top" and view != "front":
			raise ValueError("Invalid view.. Please specify 'top' or 'front'.", view)
		
		# Create the scene
		if view=="top":
			ax = plt.subplot(111, aspect=0.3)
		else:
			ax = plt.subplot(111, aspect=1)
		
		points = np.array(points)
		
		# Retrieve extrem values
		maxX, maxY, maxZ, tmp = points.max(axis=0)
		minX, minY, minZ, tmp = points.min(axis=0)
		
		margin = 50
		
		ax.set_xlim([minX-margin, maxX+margin])
		if view=="top":
			ax.set_ylim([minZ-margin, maxZ+margin])
		else:
			ax.set_ylim([minY-margin, maxY+margin])
		
		# Retrieve middle values
		midX = minX+(maxX-minX)/2
		midY = minY+(maxY-minY)/2
		midZ = minZ+(maxZ-minZ)/2
		
		# Draw center axis
		if view=="top":
			ax.plot([minX+(midX/2), maxX-(midX/2)], [midZ, midZ])
			ax.plot([midX, midX], [minZ+(midZ/2), maxZ-(midZ/2)])
		else:
			ax.plot([minX+(midX/2), maxX-(midX/2)], [midY, midY])
			ax.plot([midX, midX], [minY+(midY/2), maxY-(midY/2)])
		
		# Add points
		for point in points:
			print "[{0},{1},{2},{3}],".format(point[0], point[1], point[2], point[3])
			
			# Add a blurr effect to points if needed
			if blurred:
				for i in np.arange(0.1,1.01,0.1):
					if point[3] == True:
						c = (1,0,0, 0.3/i/10)
					else:
						c = (0,0,1, 0.1/i/10)
					
					if view=="top":
						ax.scatter(point[0], point[2], s=(50*i*(0.55))**2, color=c)
					else:
						ax.scatter(point[0], point[1], s=(50*i*(0.55))**2, color=c)
			else:
				if point[3] == True:
					c = (1,0,0, 0.3)
				else:
					c = (0,0,1, 0.1)
				
				if view=="top":
					ax.scatter(point[0], point[2], s=50, color=c)
				else:
					ax.scatter(point[0], point[1], s=50, color=c)
		
		# Display the graph
		ax.invert_xaxis()
		ax.invert_yaxis()
		plt.show()
	
	
	
if __name__ == "__main__":
	accuracy = Accuracy()
	accuracy.processedPointedDirectionByCategory()