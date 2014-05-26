#! /usr/bin/python
import json


class Dataset:
	def __init__(self):
		self.camera_height = 0
		self.luminosity = 0
		self.user = {
			"arm_length": 0,
			"height": 0,
			"distance": 0,
			"angle": 0
		}
		self.target = {
			"distance": 0,
			"angle": 0,
			"height": 0
		}
		self.hand = {
			"height": 0,
			"width": 0,
			"thickness": 0
		}
		self.skeleton = {
			"head": {
		  		"x": 0,
				"y": 0,
				"z": 0
			},
			"shoulder": {
				"left": {
			  		"x": 0,
					"y": 0,
					"z": 0
				},
				"right": {
			  		"x": 0,
					"y": 0,
					"z": 0
				},
				"center": {
			  		"x": 0,
					"y": 0,
					"z": 0
				}
			},
			"elbow": {
				"left": {
			  		"x": 0,
					"y": 0,
					"z": 0
				},
				"right": {
			  		"x": 0,
					"y": 0,
					"z": 0
				}
			},
			"hand": {
				"left": {
			  		"x": 0,
					"y": 0,
					"z": 0
				},
				"right": {
			  		"x": 0,
					"y": 0,
					"z": 0
				}
			}
		}
		self.depth_map = []
		
	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)