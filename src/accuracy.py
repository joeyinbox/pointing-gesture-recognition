#! /usr/bin/python
import numpy as np
import sys

from classes.Settings import *
from classes.Validator import *
import utils


validator = Validator()
settings = Settings()


expectedRadius = 200






folder = settings.getCompleteDatasetFolder(settings.FRONT_RIGHT, settings.DOWN)


positive = np.array([
	utils.getFileList(folder)
])


for i in positive:
	for j in i:
		name = j.split("/")
		print("Loading {0}/{1}/{2}".format(name[-3], name[-2], name[-1]))
		data = utils.loadJsonFromFile(str(j))
		
		fingerTipCoordinates = validator.retrieveCoordinates(data["fingerTip"]["height"], data["fingerTip"]["angle"], data["fingerTip"]["distance"])
		print data["fingerTip"]
		print fingerTipCoordinates
		
		eyeCoordinates = validator.retrieveCoordinates(data["eye"]["height"], data["eye"]["angle"], data["eye"]["distance"])
		print data["eye"]
		print eyeCoordinates
		
		targetCoordinates = validator.retrieveCoordinates(data["target"]["height"], data["target"]["angle"], data["target"]["distance"])
		print data["target"]
		print targetCoordinates
		
		distance = validator.findIntersectionDistance(fingerTipCoordinates, eyeCoordinates, targetCoordinates, expectedRadius)
		if distance == None:
			print "Missed..."
		else:
			print "The pointed direction intersects the target at a distance of {0:0.1f} mm.".format(distance)














