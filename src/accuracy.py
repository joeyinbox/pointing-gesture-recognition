#! /usr/bin/python
import numpy as np
import sys

from classes.Settings import *
from classes.Validator import *
import utils

from mpl_toolkits.mplot3d import Axes3D, proj3d
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from itertools import product, combinations



class Accuracy:
	validator = Validator()
	settings = Settings()

	expectedRadius = 2000
	
	
	def getFullDatasetFiles(self):
		return np.array([
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.BACK_LEFT, self.settings.UP)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.BACK_LEFT, self.settings.LATERAL)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.BACK_LEFT, self.settings.DOWN)),
			
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.LEFT, self.settings.UP)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.LEFT, self.settings.LATERAL)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.LEFT, self.settings.DOWN)),
			
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.FRONT_LEFT, self.settings.UP)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.FRONT_LEFT, self.settings.LATERAL)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.FRONT_LEFT, self.settings.DOWN)),
			
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.FRONT, self.settings.UP)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.FRONT, self.settings.LATERAL)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.FRONT, self.settings.DOWN)),
			
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.FRONT_RIGHT, self.settings.UP)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.FRONT_RIGHT, self.settings.LATERAL)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.FRONT_RIGHT, self.settings.DOWN)),
			
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.RIGHT, self.settings.UP)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.RIGHT, self.settings.LATERAL)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.RIGHT, self.settings.DOWN)),
			
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.BACK_RIGHT, self.settings.UP)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.BACK_RIGHT, self.settings.LATERAL)),
			utils.getFileList(self.settings.getCompleteDatasetFolder(self.settings.BACK_RIGHT, self.settings.DOWN))
		])

	def loadFullDataset(self):
		dataset = self.getFullDatasetFiles()
		data = []
		
		for i in dataset:
			for j in i:
				name = j.split("/")
				print("Loading {0}/{1}/{2}".format(name[-3], name[-2], name[-1]))
				data.append(utils.loadJsonFromFile(str(j)))
		return data
	
	
	
	def pointedDirection(self):
		dataset = self.loadFullDataset()
		
		for data in dataset:
			fingerTipCoordinates = self.validator.retrieveCoordinates(data["fingerTip"]["height"], data["fingerTip"]["angle"], data["fingerTip"]["distance"])
			print data["fingerTip"]
			print fingerTipCoordinates
			
			eyeCoordinates = self.validator.retrieveCoordinates(data["eye"]["height"], data["eye"]["angle"], data["eye"]["distance"])
			print data["eye"]
			print eyeCoordinates
			
			targetCoordinates = self.validator.retrieveCoordinates(data["target"]["height"], data["target"]["angle"], data["target"]["distance"])
			print data["target"]
			print targetCoordinates
			
			distance = self.validator.findIntersectionDistance(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
			if distance == None:
				print "Missed..."
			else:
				print "The pointed direction intersects the target at a distance of {0:0.1f} mm.".format(distance)
	
			print 
			print
			print
	
	
	
	def draw(self):
		class Arrow3D(FancyArrowPatch):
		    def __init__(self, xs, ys, zs, *args, **kwargs):
		        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
		        self._verts3d = xs, ys, zs

		    def draw(self, renderer):
		        xs3d, ys3d, zs3d = self._verts3d
		        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
		        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
		        FancyArrowPatch.draw(self, renderer)
		
		
		# Load the dataset
		dataset = self.loadFullDataset()
		
		
		
		# Create the scene
		fig = plt.figure()
		ax = fig.gca(projection='3d')
		ax.set_aspect("equal")
		
		ax.set_xlabel('X (horizontal)')
		ax.set_ylabel('Y (vertical)')
		ax.set_zlabel('Z (depth)')
		
		
		for data in dataset:
			# Measured data
			fingerTipCoordinates = self.validator.retrieveCoordinates(data["fingerTip"]["height"], data["fingerTip"]["angle"], data["fingerTip"]["distance"])
			eyeCoordinates = self.validator.retrieveCoordinates(data["eye"]["height"], data["eye"]["angle"], data["eye"]["distance"])
			targetCoordinates = self.validator.retrieveCoordinates(data["target"]["height"], data["target"]["angle"], data["target"]["distance"])
			
			closest = self.validator.findIntersection(fingerTipCoordinates, eyeCoordinates, targetCoordinates, self.expectedRadius)
			
			if closest != None:
				
				# Draw points
				ax.scatter(fingerTipCoordinates[0],fingerTipCoordinates[1],fingerTipCoordinates[2], color="b", s=100)
				ax.scatter(eyeCoordinates[0],eyeCoordinates[1],eyeCoordinates[2], color="g", s=100)
				ax.scatter(targetCoordinates[0],targetCoordinates[1],targetCoordinates[2], color="r", s=100)
				
				# Draw closest point
				ax.scatter(closest[0],closest[1],closest[2], color="c", s=50)
		
				# Draw an arrow
				a = Arrow3D([eyeCoordinates[0],closest[0]],[eyeCoordinates[1],closest[1]],[eyeCoordinates[2],closest[2]], mutation_scale=20, lw=1, arrowstyle="-|>", color="k")
				ax.add_artist(a)
		
		
		plt.show()
		
		sys.exit(1)


if __name__ == "__main__":
	accuracy = Accuracy()
	accuracy.pointedDirection()




