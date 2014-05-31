#! /usr/bin/python
import utils, Dataset


def promptAllQuestions(data):
	print "All distances, depth and lengths are expressed in mm"
	print "Angles are expressed in degrees"
	print "Luminosity is expressed in lux\n"
	
	data.camera_height = utils.promptInt("Camera height", 1800)
	
	data = promptUserSpecs(data)
	data = promptUserPosition(data)
	
	data = promptHandSpecs(data)
	data = promptTargetPosition(data)
	return data

def promptUserPosition(data):
	data.user["distance"] = utils.promptInt("User distance", 0)
	data.user["angle"] = utils.promptInt("User angle", 0)
	return data

def promptUserSpecs(data):
	data.user["height"] = utils.promptInt("User height", 0)
	data.user["arm_length"] = utils.promptInt("Arm length", 0)
	return data

def promptHandSpecs(data):
	data.hand["height"] = utils.promptInt("Hand height", 0)
	data.hand["width"] = utils.promptInt("Hand width", 0)
	data.hand["thickness"] = utils.promptInt("Hand thickness", 0)
	return data

def promptTargetPosition(data):
	data.target["distance"] = utils.promptInt("Target distance", 0)
	data.target["angle"] = utils.promptInt("Target angle", 0)
	data.target["height"] = utils.promptInt("Target height", 0)
	return data