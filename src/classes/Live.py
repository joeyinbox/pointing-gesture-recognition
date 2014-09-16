#!/usr/bin/python
from openni import *
import numpy as np
import skeleton, ui
import time
from threading import Timer

from classes.BPNHandler import *
from classes.FeatureExtractor import *
from classes.LiveDataset import *
from classes.Settings import *
from classes.Utils import *
from classes.Testing import *


class Live():
	
	utils = Utils()
	featureExtractor = FeatureExtractor()
	bpn = BPNHandler(True)
	testing = Testing()
	
	def __init__(self):
		# Retrieve all settings
		self.settings = Settings()
		
		# Get the context and initialise it
		self.context = Context()
		self.context.init()

		# Create the depth generator to get the depth map of the scene
		self.depth = DepthGenerator()
		self.depth.create(self.context)
		self.depth.set_resolution_preset(RES_VGA)
		self.depth.fps = 30

		# Create the user generator to detect skeletons
		self.user = UserGenerator()
		self.user.create(self.context)

		# Initialise the skeleton tracking
		skeleton.init(self.user)

		# Start generating
		self.context.start_generating_all()
		
		# Create a new dataset item
		self.data = LiveDataset()
		self.data.hand = self.settings.BOTH_HAND
		
		# Update the frame
		Timer(0.001, self.updateImage, ()).start()
		
	
		
	def updateImage(self):
		# Update to next frame
		self.context.wait_and_update_all()
		
		# Extract informations of each tracked user
		self.data = skeleton.track(self.user, self.depth, self.data)

		# Get the whole depth map
		self.data.depth_map = np.asarray(self.depth.get_tuple_depth_map()).reshape(480, 640)
		
		# Create dummy values
		recognition = False
		hand = None
		origin = [0,0,0]
		end = [0,0,0]
		
		
		if len(self.user.users) > 0 and len(self.data.skeleton["head"]) > 0:
			# Test the data against the neural network if possible
			if self.data.hand != self.settings.NO_HAND:
				result = self.bpn.check(self.featureExtractor.getFeatures(self.data))
				
				if result[0] != False:
					recognition = True
					hand = result[1]
					origin = [self.featureExtractor.eyePosition[result[1]][0], 
							  self.featureExtractor.eyePosition[result[1]][1], 
							  self.utils.getDepthFromMap(self.data.depth_map, self.featureExtractor.eyePosition[result[1]])]
					end = [self.featureExtractor.fingerTip[result[1]][0], 
						   self.featureExtractor.fingerTip[result[1]][1], 
						   self.utils.getDepthFromMap(self.data.depth_map, self.featureExtractor.fingerTip[result[1]])]
					
		
		# Output the result
		print '{{"pointing":{0},"hand":{1},"origin":{2},"end":{3}}}'.format(recognition, hand, origin, end)
		
		Timer(0.001, self.updateImage, ()).start()