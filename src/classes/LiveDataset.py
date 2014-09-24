#! /usr/bin/python

# Definition of the LiveDataset class
class LiveDataset:
	
	# Constructor of the LiveDataset class
	# 
	# @param	None
	# @return	None
	def __init__(self):
		self.hand = 3
		self.skeleton = {
			"head": [],
			"shoulder": {
				"left": [],
				"right": [],
				"center": []
			},
			"elbow": {
				"left": [],
				"right": []
			},
			"hand": {
				"left": [],
				"right": []
			}
		}
		self.depth_map = []
	
	
	# Returns the data of the current instance
	# 
	# @param	None
	# @return	object				Data of the current instance
	def getData(self):
		return self
	
	
	# Toggle the type of hand
	# 
	# @param	value				Identifier to update
	# @return	None
	def toggleHand(self, value):
		self.hand = value
		print "hand toggled to {0}".format(value)