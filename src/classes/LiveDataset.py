#! /usr/bin/python

class LiveDataset:
	LEFT_HAND = 0
	RIGHT_HAND = 1
	BOTH_HAND = 2
	
	
	def __init__(self):
		print "Live dataset"
		self.hand = []
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
	
	def getData(self):
		return self
		
	def toggleHand(self, value):
		self.hand = value
		print "hand toggled to {0}".format(value)