#! /usr/bin/python

class LiveDataset:
	def __init__(self):
		print "Live dataset"
		self.hand = 0
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