#! /usr/bin/python
import numpy as np


# At 1m, the hand is surrounded with a shift of 90 pixels around its center of gravity
def getHandBoundShift(depth):
	if depth == 0:
		return 90
	else:
		return int((1000/float(depth))*90)

# Return the depth value of a point from the depth map
def getDepthFromMap(depthMap, position):
	x = int(position[0])
	y = int(position[1])
	
	height, width = depthMap.shape
    
	if y<0 or y>=width or x<0 or x>=height:
		return 0
	else:
		return depthMap[x][y]