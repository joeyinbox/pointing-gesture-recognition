#! /usr/bin/python
import json, utils


class Dataset:
	def __init__(self):
		self.camera_height = 0
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
		self.image = ""
		
	def to_JSON(self):
		# Update the depth map and the image to prepare them
		self.depth_map = utils.convertOpenNIDepthMapToArray(self.depth_map)
		self.image = utils.getBase64(self.image)
		
		return json.dumps(self, default=lambda o: o.__dict__, separators=(',', ':'))