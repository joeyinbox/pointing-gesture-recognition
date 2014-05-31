#! /usr/bin/python
import numpy as np


# At 1m, the hand is surrounded with a shift of 75 pixels around its center of gravity
def getHandBoundShift(depth):
	if depth == 0:
		return 75
	else:
		return int((1000/float(depth))*75)

# Return the depth value of a point from the depth map
def getDepthFromMap(depthMap, position):
	x = int(position[0])
	y = int(position[1])
    
	if x<0 or x>=depthMap.width or y<0 or y>=depthMap.height:
		return 0
	else:
		return depthMap[x, y]

# Extract depth data from a specifed area
def extractDepthFromArea(depthMap, position, shift):
	result = np.zeros(shape=(2*shift+1, 2*shift+1))
    
	i = 0
	for x in range(int(position[0])-shift, int(position[0])+shift):
		j = 0
		for y in range(int(position[1])-shift, int(position[1])+shift):
			if x>=0 and x<depthMap.width and y>=0 and y<depthMap.height:
				result[i, j] = convertDepthToRange(depthMap[x, y])
			j += 1
		i += 1
    
	return result

# Convert depth data to a value within the range 1-0 (with 1 for smallest values from 500 to 4000 mm)
def convertDepthToRange(depth):
	maxDepth = 4000
	minDepth = 500
    
	if depth>=minDepth and depth<=maxDepth:
		return round((maxDepth-float(depth))/(maxDepth-minDepth), 3)
	return 0