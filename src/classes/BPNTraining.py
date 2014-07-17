#! /usr/bin/python
from classes.BackPropagationNetwork import *
from classes.Dataset import *
from classes.LightDataset import *
from classes.Settings import *
import utils, hand
import numpy as np
import sys, math
import scipy.stats


class BPNTraining():
	
	settings = Settings()
	Dmin,Dmax = 50, 4000
	trainingInput, testingInput = [], []
	currentH, currentW = 0, 0
	target = []
	
	
	def __init__(self, training, positive, negative):
		for i in training:
			print("Loading {0}".format(i))
			file = self.settings.getTrainingFolder()+str(i).zfill(3)+".json"
			data = utils.loadJsonFromFile(file)
			self.trainingInput.append(self.normalizeLightInput2(data))

		for i in negative:
			print("Loading negative {0}".format(i))
			file = self.settings.getNegativeLightFolder()+str(i).zfill(3)+".json"
			data = utils.loadJsonFromFile(file)
			self.trainingInput.append(self.normalizeLightInput2(data))
			self.target.append(0)

		for i in positive:
			print("Loading positive {0}".format(i))
			file = self.settings.getPositiveLightFolder()+str(i).zfill(3)+".json"
			data = utils.loadJsonFromFile(file)
			self.trainingInput.append(self.normalizeLightInput2(data))
			self.target.append(1)
	
	
	def keepRange(self, value, max):
		if value < 0:
			return 0
		elif value > max:
			return max
		else: 
			return value

	def countWithinArea(self, data, h1, v1, h2,v2):
		# Return the percentage of actual data within a restricted area
		if self.currentW != 0 and self.currentH != 0:
			return np.sum(data[v1:v2, h1:h2], dtype=np.int32)/float(self.currentH*self.currentW)
		else:
			return 0

	def diviseInFour(self, input, data, recursion=False):
		h,w = data.shape
	
		input.append(self.countWithinArea(data, 0, 0, w/2, h/2)) # upper left
		input.append(self.countWithinArea(data, w/2, 0, w, h/2)) # upper right
		input.append(self.countWithinArea(data, 0, h/2, w/2, h)) # lower left
		input.append(self.countWithinArea(data, w/2, h/2, w, h)) # lower right
	
		if recursion:
			self.diviseInFour(input, data[0:h/2, 0:w/2]) # upper left
			self.diviseInFour(input, data[0:h/2, w/2:w]) # upper right
			self.diviseInFour(input, data[h/2:h, 0:w/2]) # lower left
			self.diviseInFour(input, data[h/2:h, w/2:w]) # lower right

	def getAverageDistance(self, data):
		centerV = int(self.currentH/2)
		centerH = int(self.currentW/2)
	
		#print("center is v:{0} and h:{1} and its value is {2}".format(centerV, centerH, data[centerV][centerH]))
	
		total = 0
		count = 0.0
		for i in range(self.currentW):
			for j in range(self.currentH):
				if data[j][i] == 1:
					total += math.sqrt(((i-centerV)**2) * ((j-centerH)**2))
					count += 1
		if count == 0.0:
			return 0
		else:
			return total/count


	def normalizeInput1(self, data):
		# Retrieve the depth map and convert it to a numpy array of floats
		depthMap = np.array(data["depth_map"]).astype(float)
	
	
		# Retrieve the position of the pointing hand
		if data["hand"]["type"]==LEFT_HAND:
			v,h,d = map(int, data["skeleton"]["hand"]["left"])
		elif data["hand"]["type"]==RIGHT_HAND:
			v,h,d = map(int, data["skeleton"]["hand"]["right"])
		else:
			v,h,d = (0,0,0)
	
		# Determine the bounding box around the pointing hand. Here fixed to the biggest one for hands at least as far as 500mm
		shift = 150
	
		# Determine the coordinates of the bounding box to extract
		x1 = keepRange(int(h-shift), 480)
		y1 = keepRange(int(v-shift), 640)
		x2 = keepRange(int(h+shift)+1, 480)
		y2 = keepRange(int(v+shift)+1, 640)
	
		# Extract the informations within the bounding box
		startH = shift-h+x1
		startV = shift-v+y1
		endH = shift+x2-h
		endV = shift+y2-v
	
		max = (2*shift)+1
		extracted = np.zeros(max*max).reshape(max, max)
		extracted[startV:endV, startH:endH] = depthMap[y1:y2, x1:x2]
	
		# Extract the hand from the background with a threshold
		start = d-200
		end = d+200
	
		x,y = extracted.shape
		for j in range(x):
			for k in range(y):
				if extracted[j][k]<start or extracted[j][k]>end:
					extracted[j][k] = 0
				else:
					extracted[j][k] = 1
	
	
		# Count the number of occurences by row and columns
		v1 = np.ravel(extracted.sum(axis=0))
		v2 = np.ravel(extracted.sum(axis=1))
	
		# Concatenate these values
		final = np.hstack((v1,v2))
	
	
		# Convert all values to a 0-1 range-restricted pool (with 1 for close points and 0 for far ones)
		#rangeRestricted = (Dmax-extracted)/(Dmax-Dmin)
	
		return final






	def normalizeInput2(self, data):
		# Retrieve the depth map and convert it to a numpy array of floats
		depthMap = np.array(data["depth_map"]).astype(float)
	
	
		# Retrieve the position of the pointing hand
		if data["hand"]["type"]==Dataset.LEFT_HAND:
			v,h,d = map(int, data["skeleton"]["hand"]["left"])
		elif data["hand"]["type"]==Dataset.RIGHT_HAND:
			v,h,d = map(int, data["skeleton"]["hand"]["right"])
		else:
			# Take arbitrarily the right hand
			v,h,d = map(int, data["skeleton"]["hand"]["right"])
	
		# Determine the bounding box around the pointing hand. Here fixed to the biggest one for hands at least as far as 500mm
		if d != 0:
			shift = int((1000.0/d)*90)
		else:
			shift = 1
	
		# Determine the coordinates of the bounding box to extract
		x1 = self.keepRange(int(h-shift), 480)
		y1 = self.keepRange(int(v-shift), 640)
		x2 = self.keepRange(int(h+shift)+1, 480)
		y2 = self.keepRange(int(v+shift)+1, 640)
	
		# Extract the informations within the bounding box
		startH = shift-h+x1
		startV = shift-v+y1
		endH = shift+x2-h
		endV = shift+y2-v
	
		max = (2*shift)+1
		extracted = np.zeros(max*max).reshape(max, max)
		extracted[startV:endV, startH:endH] = depthMap[y1:y2, x1:x2]
	
		# Extract the hand from the background with a threshold
		start = d-200
		end = d+200
		
		x,y = extracted.shape
		for j in range(x):
			for k in range(y):
				if extracted[j][k]<start or extracted[j][k]>end:
					extracted[j][k] = 0
				else:
					extracted[j][k] = 1
	
		# Remove all zeros columns and rows
		foo = np.rot90(extracted[~np.all(extracted == 0, axis=1)])
		binary = np.rot90(foo[~np.all(foo == 0, axis=1)], -1)
		
		# Hold the ratio
		self.currentH, self.currentW = binary.shape
		
		input = []
		if self.currentW != 0:
			input.append(self.currentH/float(self.currentW))
		else: input.append(0)
		

		# Hold the percentage of actual data within sub-areas
		input.append(self.countWithinArea(binary, 0, 0, self.currentW/2, self.currentH)) # left
		input.append(self.countWithinArea(binary, self.currentW/2, 0, self.currentW, self.currentH)) # right
		input.append(self.countWithinArea(binary, 0, 0, self.currentW, self.currentH/2)) # up
		input.append(self.countWithinArea(binary, 0, self.currentH/2, self.currentW, self.currentH)) # down

		# Hold the value for recursively divided areas
		self.diviseInFour(input, binary, True)

		# Hold the average distance between all actual data and the center
		input.append(self.getAverageDistance(binary))
		
		return input
	
	
	def normalizeLightInput2(self, data):
		# Retrieve the depth map and convert it to a numpy array of floats
		depthMap = np.array(data["depth_map"]).astype(float)
	
	
		# Retrieve the position of the pointing hand
		if data["hand"]==LightDataset.LEFT_HAND:
			v,h,d = map(int, data["skeleton"]["hand"]["left"])
		elif data["hand"]==LightDataset.RIGHT_HAND:
			v,h,d = map(int, data["skeleton"]["hand"]["right"])
		else:
			# Take arbitrarily the right hand
			v,h,d = map(int, data["skeleton"]["hand"]["right"])
	
		# Determine the bounding box around the pointing hand. Here fixed to the biggest one for hands at least as far as 500mm
		if d != 0:
			shift = int((1000.0/d)*90)
		else:
			shift = 1
	
		# Determine the coordinates of the bounding box to extract
		x1 = self.keepRange(int(h-shift), 480)
		y1 = self.keepRange(int(v-shift), 640)
		x2 = self.keepRange(int(h+shift)+1, 480)
		y2 = self.keepRange(int(v+shift)+1, 640)
	
		# Extract the informations within the bounding box
		startH = shift-h+x1
		startV = shift-v+y1
		endH = shift+x2-h
		endV = shift+y2-v
	
		max = (2*shift)+1
		extracted = np.zeros(max*max).reshape(max, max)
		extracted[startV:endV, startH:endH] = depthMap[y1:y2, x1:x2]
	
		# Extract the hand from the background with a threshold
		start = d-200
		end = d+200
		
		x,y = extracted.shape
		for j in range(x):
			for k in range(y):
				if extracted[j][k]<start or extracted[j][k]>end:
					extracted[j][k] = 0
				else:
					extracted[j][k] = 1
	
		# Remove all zeros columns and rows
		foo = np.rot90(extracted[~np.all(extracted == 0, axis=1)])
		binary = np.rot90(foo[~np.all(foo == 0, axis=1)], -1)
		
		# Hold the ratio
		self.currentH, self.currentW = binary.shape
		
		input = []
		if self.currentW != 0:
			input.append(self.currentH/float(self.currentW))
		else: input.append(0)
		

		# Hold the percentage of actual data within sub-areas
		input.append(self.countWithinArea(binary, 0, 0, self.currentW/2, self.currentH)) # left
		input.append(self.countWithinArea(binary, self.currentW/2, 0, self.currentW, self.currentH)) # right
		input.append(self.countWithinArea(binary, 0, 0, self.currentW, self.currentH/2)) # up
		input.append(self.countWithinArea(binary, 0, self.currentH/2, self.currentW, self.currentH)) # down

		# Hold the value for recursively divided areas
		self.diviseInFour(input, binary, True)

		# Hold the average distance between all actual data and the center
		input.append(self.getAverageDistance(binary))
		
		# Hold the 7 first central moments
		for i in range(1, 8):
			moment = scipy.stats.moment(binary, i)
			input.append(np.average(moment))
		
		return input
	
	def run(self):
		lvInput = np.array(self.trainingInput)
		#lvTarget = np.ones(len(self.trainingInput))
		lvTarget = np.array(self.target)

		lFuncs = [None, gaussian, sgm]

		bpn = BackPropagationNetwork((len(self.trainingInput[0]), 35, 1), lFuncs)

		lnMax = 100000
		lnErr = 1e-5
		errMax = 1e100
		for i in range(lnMax+1):
			err = bpn.trainEpoch(lvInput, lvTarget, momentum=0.7)
			print("Iteration {0}\tError: {1:0.6f}".format(i, err))
			if err <= lnErr:
				print("Minimum error reached at iteration {0}".format(i))
				break
			if err >= errMax:
				print("Will not converge past iteration {0}".format(i))
				break
		
		# Display output
		lvOutput = bpn.run(lvInput)
		for i in range(lvInput.shape[0]):
			print("Ouput {0}: {1}".format(i, lvOutput[i]))
		
		print ""
		print ""
		
		
		lvInput = np.array(self.testingInput)
		lvOutput = bpn.run(lvInput)
		for i in range(lvInput.shape[0]):
			print("Ouput {0}: {1}".format(i, lvOutput[i]))