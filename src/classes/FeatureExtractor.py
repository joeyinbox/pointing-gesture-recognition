#! /usr/bin/python -W ignore::FutureWarning
from classes.Dataset import *
from classes.LiveDataset import *
from classes.Settings import *
from classes.Testing import *
import numpy as np
import sys, math
import scipy.stats, scipy.ndimage
import cv2
from copy import deepcopy
import signal
import heapq


class FeatureExtractor():
	
	# Load settings
	settings = Settings()
	
	# Compatibility with testing mode
	testing = Testing()
	
	# Hold all input feature data
	trainingInput, testingInput, validatingInput = [], [], []
	
	# Hold all target data
	trainingTarget, testingTarget = [], []
	
	# Hold eventual results
	resultTestingScore, resultTrainingScore, resultInitialWeights, resultWeights, resultConfig, resultIteration = [], [], [], [], [], []
	
	# Hold informations about the current input
	currentH, currentW = 0, 0
	currentBinary, currentExtracted = [], []
	
	# Hold the transformations applied to the current input
	cropTop, cropLeft, cropBottom, cropRight = 0, 0, 0, 0
	emptyTop, emptyLeft, emptyBottom, emptyRight = 0, 0, 0, 0
	rotationAngle = 0
	tar = 0
	
	# The current fingertip and eye (if any)
	fingerTip = [[0,0], [0,0]]
	eyePosition = [[0,0], [0,0]]
	orientation = ["", ""]
	
	
	bpnValidating = None
	
	def __init__(self):
		# Vectorize threshold functions to speed the process
		self.thresholdBinary = np.vectorize(self.thresholdBinary)
		self.thresholdExtracted = np.vectorize(self.thresholdExtracted)
	
	def thresholdBinary(self, x, start, end):
	    return 0 if x<start or x>end or x==0 else 1
	
	def thresholdExtracted(self, x, start, end):
	    return np.NaN if x<start or x>end or x==0 else x
	
	
	def findNearestValue(self, data, index, orientation=-1, shift=0):
		# Returns the index of the nearest value around the index parameter
		tmp = index+(orientation*shift)
		if tmp>=len(data) or tmp<0:
			return None
		elif data[tmp] == 1:
			return tmp
		else:
			# Invert the orientation
			orientation *= -1
			
			# Increase the shift every two checks (except for the first one)
			if orientation == 1:
				shift += 1
			return self.findNearestValue(data, index, orientation, shift)
	
	
	def tarExtracted(self):
		# Determine the minimal non-zero value of the matrice
		try:
			#min = np.nanmin(self.currentExtracted)											# fmin identity seems buggy
			self.tar = np.min(self.currentExtracted[~np.isnan(self.currentExtracted)])			# use this hack instead
		except ValueError:
			self.tar = 0
		
		# Remove this value to all elements of the matrice
		self.currentExtracted = self.currentExtracted-np.array([self.tar])
		
		# For testing purpose
		self.testing.timerMarker("Tar the values of the extracted hand")
	
	
	def getEuclidianDistance(self, a, b):
		return np.linalg.norm(a-b)

	def getAvgEuclidianDistance(self):
		# The reference point is taken at the center of the matrix
		h, v = self.currentExtracted.shape
		ref_h = h/2
		ref_v = v/2
		
		# Then we determine all euclidian distances between relevant points and that reference point
		distances = []
		
		# If the reference point is not a number, it will be considered as 0
		if np.isnan(self.currentExtracted[ref_h, ref_v]):
			reference = 0.0
		else:
			reference = self.currentExtracted[ref_h, ref_v]
	
		for i in range(h):
			for j in range(v):
				if not np.isnan(self.currentExtracted[i,j]) and (i!=ref_h or j!=ref_v):
					distances.append(self.getEuclidianDistance(np.array([i, j, self.currentExtracted[i,j]]), np.array([ref_h, ref_v, reference])))
		
		return np.average(distances)
	
	def removeEmptyColumnsRows(self):
		# Re-initialise empty holders
		self.emptyTop, self.emptyLeft, self.emptyBottom, self.emptyRight = 0, 0, 0, 0
		
		# Verify the content of the matrices
		if self.currentExtracted.size==0 or self.currentBinary.size==0:
			return False
		
		
		# Count along columns and rows from both matrices to detect empty ones
		column = self.currentBinary.sum(axis=0).astype(int)
		row = self.currentBinary.sum(axis=1).astype(int)

		# Remove empty left columns
		i = 0
		while i<len(column) and column[i]==0:
			self.currentExtracted = self.currentExtracted[:,1:]
			self.currentBinary = self.currentBinary[:,1:]
			self.emptyLeft += 1
			i += 1

		# Remove empty right columns
		i = len(column)-1
		while i>=0 and column[i]==0:
			self.currentExtracted = self.currentExtracted[:,:-1]
			self.currentBinary = self.currentBinary[:,:-1]
			self.emptyRight += 1
			i -= 1

		# Remove empty top rows
		i = 0
		while i<len(row) and row[i]==0:
			self.currentExtracted = self.currentExtracted[1:,:]
			self.currentBinary = self.currentBinary[1:,:]
			self.emptyTop += 1
			i += 1

		# Remove empty bottom rows
		i = len(row)-1
		while i>=0 and row[i]==0:
			self.currentExtracted = self.currentExtracted[:-1,:]
			self.currentBinary = self.currentBinary[:-1,:]
			self.emptyBottom += 1
			i -= 1
		
		# For testing purpose
		self.testing.timerMarker("Remove all zeros columns and rows from both matrices")
		
	
	
	
	def rotate(self, hand, elbow):
		# The dataset can be oriented in 4 different ways that can be rotated back to form a vertical line between the hand and the elbow joints
		
		# First, determine the relative position of the hand
		if hand[0]-elbow[0]<0:
			# the hand is located in the lower part
			v = elbow[0]-hand[0]
			up = False
		else:
			# the hand is located in the upper part
			v = hand[0]-elbow[0]
			up = True
		
		if hand[1]-elbow[1]<0:
			# the hand is located in the right part
			h = elbow[1]-hand[1]
			left = False
		else:
			# the hand is located in the left part
			h = hand[1]-elbow[1]
			left = True
		
		
		# Check if the elbow is on top/bottom extrems to determine the rotation degree
		if hand[0]==elbow[0] and hand[1]==elbow[1]:
			self.rotationAngle = 0
		elif v>h:
			if not up:
				self.rotationAngle = 0
			else:
				self.rotationAngle = 2
		else:
			if left:
				self.rotationAngle = 1
			else:
				self.rotationAngle = -1
		
		
		# Apply rotation
		self.currentBinary = np.rot90(self.currentBinary, self.rotationAngle)
		self.currentExtracted = np.rot90(self.currentExtracted, self.rotationAngle)
		
		# For testing purpose
		self.testing.timerMarker("Matrice rotation")
	
	
	def getHistogram(self):
		hist, bin_edges = np.histogram(~np.isnan(self.currentExtracted), density=True)
		return hist
	
	def sift(self, input):
		data = np.copy(self.currentExtracted).astype(np.uint8)
		gray = cv2.cvtColor(data, cv2.COLOR_GRAY2BGR)

		sift = cv2.SIFT()
		kp = sift.detect(gray, None)
		
		for i in range(len(kp)):
			x = kp[i].pt[0]
			y = kp[i].pt[1]
			size = kp[i].size
			dir_in_degrees = kp[i].angle
			laplacian = kp[i].class_id
			hessian = round(kp[i].response)
			
			input.append(laplacian)
			input.append(hessian)
			
			print laplacian
			print hessian
			print dir_in_degrees
			print size
	
	def surf(self, input):
		data = np.copy(self.currentExtracted).astype(np.uint8)
		gray = cv2.cvtColor(data, cv2.COLOR_GRAself.cropRightBGR)
		
		surfDetector = cv2.FeatureDetector_create("SURF")
		surfDescriptorExtractor = cv2.DescriptorExtractor_create("SURF")
		kp = surfDetector.detect(gray)
		(kp, descriptors) = surfDescriptorExtractor.compute(gray, kp)
		
		for i in range(len(kp)):
			x = kp[i].pt[0]
			y = kp[i].pt[1]
			size = kp[i].size
			dir_in_degrees = kp[i].angle
			laplacian = kp[i].class_id
			hessian = round(kp[i].response)
			
			input.append(laplacian)
			input.append(hessian)
			
			print laplacian
			print hessian
			print dir_in_degrees
			print size
	
	
	def display(self, b):
		x,y = b.shape
		for i in range(x):
			text = ""
			for j in range(y):
				if np.isnan(b[i,j]) or int(b[i,j]) == 0:
					text += " "
				else:
					text += str(int(b[i,j]))
					text += ","
			print text
		print
	
	def displayHTML(self, b):
		
		old_min = float(np.min(b))
		old_max = float(np.max(b))
		
		old_range = float(old_max - old_min)
		new_min = 0
		new_range = 1 - float(new_min)
		
		def f(n, old_min, old_range, new_range, new_min):
		    return float((n - float(old_min)) / float(old_range) * float(new_range) + float(new_min))

		f = np.vectorize(f)
		b = f(b, old_min, old_range, new_range, new_min)
		
		
		
		x,y = b.shape
		for i in range(x):
			text = ""
			for j in range(y):
				if np.isnan(b[i,j]):
					text += "ctx.fillStyle='rgba(0,0,0,0)'; ".format()
					text += "ctx.fillRect({0},{1},2,2);\n".format(j*2,i*2)
				else:
					text += "ctx.fillStyle='rgba(0,0,0,{0:.2f})'; ".format(b[i,j])
					text += "ctx.fillRect({0},{1},2,2);\n".format(j*2,i*2)
			print text
		print
		
		sys.exit(1)
		
	
	
	
	
	def keepRange(self, value, max):
		if value < 0:
			return 0
		elif value > max:
			if max > 0:
				return max
			else:
				return 0
		else: 
			return value

	def countWithinArea(self, data, total, h1, v1, h2, v2):
		# Return the percentage of actual data within a restricted area
		if self.currentW>0 and self.currentH>0 and total>0 and data.size>0 and data.shape[0]>=v2 and data.shape[1]>=h2:
			return np.sum(data[v1:v2, h1:h2], dtype=np.int32)/float(total)*100
		else:
			return 0
	
	def diviseInSix(self):
		h,w = self.currentBinary.shape
		total = np.sum(self.currentBinary)
		
		output = []
	
		output.append(self.countWithinArea(self.currentBinary, total, 0, 0, w/2, h/3)) 			# upper left
		output.append(self.countWithinArea(self.currentBinary, total, 0, h/3, w/2, 2*(h/3))) 	# middle left
		output.append(self.countWithinArea(self.currentBinary, total, 0, 2*(h/3), w/2, h)) 		# lower left
		
		output.append(self.countWithinArea(self.currentBinary, total, w/2, 0, w, h/3)) 			# upper right
		output.append(self.countWithinArea(self.currentBinary, total, w/2, h/3, w, 2*(h/3))) 	# middle right
		output.append(self.countWithinArea(self.currentBinary, total, w/2, 2*(h/3), w, h)) 		# lower right
		
		return self.normalizeInput(output)
	
	def getUpperPercent(self):
		h,w = self.currentBinary.shape
		total = np.sum(self.currentBinary)
		
		output = []
	
		output.append(self.countWithinArea(self.currentBinary, total, 0, 0, w/3, h/3)) 			# left
		output.append(self.countWithinArea(self.currentBinary, total, w/3, 0, 2*(w/3), h/3)) 	# middle
		output.append(self.countWithinArea(self.currentBinary, total, 2*(w/3), 0, w, h/3)) 		# right
		
		return self.normalizeInput(output, 0, 30)
	
	
	def getElbowHandAlignment(self, depth, hand_v, hand_h, elbow_v, elbow_h, handId):
		# Allow to discriminate gestures pointing left/right up, lateral and down
		# Uses the disposition of the hand and the elbow
		
		# At 1m, a variation of 60 pixels indicates a position change
		if depth>0:
			threshold = (60/float(depth))*1000
		else:
			threshold = 60
		
		# Right, Left or Front?
		if hand_h > elbow_h+threshold:
			h = 1	# Left (from user point of view)
			self.orientation[handId] = "Left "
		elif hand_h+threshold < elbow_h:
			h = -1	# Right (from user point of view)
			self.orientation[handId] = "Right "
		else:
			h = 0	# Front
			self.orientation[handId] = "Front "
		
		
		# Up, Down or Lateral?
		if hand_v > elbow_v+threshold:
			v = -1	# down
			self.orientation[handId] += "down"
		elif hand_v+threshold < elbow_v:
			v = 1	# up
			self.orientation[handId] += "up"
		else:
			v = 0	# lateral
			self.orientation[handId] += "lateral"
		
		
		# For testing purpose
		self.testing.timerMarker("Get elbow / hand alignment")
		
		return [h,v]
		
		
	
	
	def getTipHandDepthDiff(self, depthMap, fingerTip, handId):
		if fingerTip[1]<0 or fingerTip[1]>=480 or fingerTip[0]<0 or fingerTip[0]>=640 or len(self.currentBinary)==0:
			return 0.0
		
		# Retrieve fingertip depth
		fingerTipDepth = depthMap[fingerTip[1]][fingerTip[0]]
		
		# Retrieve non-empty values of the last row to get the coordinates of the middle value
		index = np.nonzero(self.currentBinary[-1] == 1)
		h = self.findNearestValue(self.currentBinary[-1], index[0][0]+int((index[0][-1]-index[0][0])/2))
		
		# Retrieve lower part depth
		lowerDepth = self.currentExtracted[-1][h]+self.tar
		
		# Check difference
		threshold = 100
		
		if fingerTipDepth+threshold < lowerDepth:
			print "front {1}".format(self.orientation[handId])
		elif fingerTipDepth > lowerDepth+threshold:
			print "back {1}".format(self.orientation[handId])
		else:
			print "lateral {1}".format(self.orientation[handId])
		
		return self.normalizeInput([fingerTipDepth/lowerDepth], 0.9, 1.1)[0]
	
	def getTopHandSizeDiff(self):
		# Get the height of the hand
		height = len(self.currentBinary)
		
		# Count the average number of data in the top 8% part
		upperIndex = int(height*0.08)
		lowerIndex = int(height*0.75)
		
		
		
		lower = np.sum(self.currentBinary[upperIndex:upperIndex+1, :])
		upper = np.sum(self.currentBinary[lowerIndex:lowerIndex+1, :], dtype=np.int32)
		
		print "lower= {0}\t upper= {1} \t divised={2}".format(lower, upper, lower/float(upper))
		
		return lower/float(upper)
		
		
		
	
	
	def normalizeInput(self, input, old_min=0, old_max=100):
		# Normalize the data in a range from -1 to 1
		old_range = old_max-old_min
		new_min = -1
		new_range = 1-new_min
		
		if old_range==0:
			raise ValueError("Invalid range")
	
		return [float((n-old_min) / float(old_range) * new_range + new_min) for n in input]
	
	def getFeatures(self, data):
		result = []
		
		# Retrieve the position of the pointing hand
		if data.hand==self.settings.LEFT_HAND or data.hand==self.settings.BOTH_HAND:
			h,v,d = map(int, data.skeleton["hand"]["left"])
			h2,v2,d2 = map(int, data.skeleton["elbow"]["left"])
			result.append(self.processFeatures(h,v,d, h2,v2,d2, data.depth_map, data.skeleton["head"], 0))
		if data.hand==self.settings.RIGHT_HAND or data.hand==self.settings.BOTH_HAND:
			h,v,d = map(int, data.skeleton["hand"]["right"])
			h2,v2,d2 = map(int, data.skeleton["elbow"]["right"])
			result.append(self.processFeatures(h,v,d, h2,v2,d2, data.depth_map, data.skeleton["head"], len(result)))
		
		# Then, return the corresponding features
		return result
	
	def processFeatures(self, h,v,d, h2,v2,d2, depthMap, head, handId=0):
		# Assert the validaity of the values
		if depthMap.size==0 or len(depthMap.shape)<=1:
			return [-1.0,-1.0,-1.0,-1.0,-1.0,-1.0]
		
		
		# Determine the bounding box around the pointing hand regarding to the depth of the hand
		if d != 0:
			shift = int((1000.0/d)*90)
		else:
			shift = 1
		
		# For testing purpose
		self.testing.startTimer()
	
		# Determine the coordinates of the bounding box to extract
		self.cropTop = self.keepRange(int(v-shift), 480)
		self.cropLeft = self.keepRange(int(h-shift), 640)
		self.cropBottom = self.keepRange(int(v+shift)+1, 480)
		self.cropRight = self.keepRange(int(h+shift)+1, 640)
		
		# For testing purpose
		self.testing.timerMarker("Determine the coordinates of the bounding box to extract")
	
		# Extract the informations within the bounding box
		startV = shift-v+self.cropTop
		startH = shift-h+self.cropLeft
		endV = shift+self.cropBottom-v
		endH = shift+self.cropRight-h
		
	
		max = (2*shift)+1
		self.currentExtracted = np.zeros(max*max).reshape(max, max)
		self.currentExtracted[startV:endV, startH:endH] = depthMap[self.cropTop:self.cropBottom, self.cropLeft:self.cropRight]
		self.currentBinary = np.copy(self.currentExtracted)
		
		# For testing purpose
		self.testing.timerMarker("Extract the informations within the bounding box")
		
	
		# Extract the hand from the background with a threshold
		start = d-100
		end = d+100
		
		self.currentBinary = self.thresholdBinary(self.currentBinary, start, end)
		self.currentExtracted = self.thresholdExtracted(self.currentExtracted, start, end)
		
		# For testing purpose
		self.testing.timerMarker("Extract the hand from the background with a threshold")
		
		
		# Remove all zeros columns and rows from both matrices
		self.removeEmptyColumnsRows()
		
		
		# Initialize the input features
		input = []
		
		
		# Rotate the hand to form a vertical line between the hand and the elbow
		self.rotate([v,h], [v2,h2])
		self.tarExtracted()
		
		# Calculate the elbow/hand alignment
		alignment = self.getElbowHandAlignment(d, v, h, v2, h2, handId)
		
		# Retrieve eyes position
		self.eyePosition[handId] = self.getEyePosition(depthMap, head, alignment)
		
		# For testing purpose
		self.testing.timerMarker("Get eye position")
		
		# Retrieve the finger tip position
		self.fingerTip[handId] = self.getFingerTip()
		
		# For testing purpose
		self.testing.timerMarker("Get fingertip")
		
		
		# Hold the ratio
		self.currentH, self.currentW = self.currentBinary.shape
		
		
		# /------------------------------------\
		# |          Feature 1 to 6            |
		# |   Percent of data in sub-regions   |
		# \------------------------------------/
		
		
		
		
		# Hold the percentage of actual data within sub-areas
		input.extend(self.diviseInSix())
		
		# For testing purpose
		self.testing.timerMarker("Process hand histogram")
		self.testing.stopTimer()
		
		return input
	
	
	def getFingerTip(self):
		# Prevent empty calls
		if len(self.currentBinary)==0:
			return [0,0]
		
		# Retrieve non-empty values of the first row
		index = np.nonzero(self.currentBinary[0] == 1)
		output = []
		
		if len(index)<1 or len(index[0])<1:
			return [0,0]
		
		# Finger tip coordinates (once rotated!)
		v = 0
		h = self.findNearestValue(self.currentBinary[0], index[0][0]+int((index[0][-1]-index[0][0])/2))
		if h == None:
			return [0,0]
		
		
		# Revert rotation to get the real coordinates
		if self.rotationAngle == -1:
			v = len(self.currentBinary[0])-1-h
			h = 0
		elif self.rotationAngle == 2:
			h = len(self.currentBinary[0])-1-h
			v = len(self.currentBinary)
		elif self.rotationAngle == 1:
			v = h
			h = len(self.currentBinary)-1
		
		
		# Revert empty columns/rows and initial crop
		return [self.cropLeft+h+self.emptyLeft, self.cropTop+v+self.emptyTop]
		
		
		
	def getEyePosition(self, depthMap, head, elbowHand):
		# Assert the validaity of the values
		if depthMap.size==0 or len(depthMap.shape)<=1:
			return [0,0]
			
		# First extract a sub-area based on the depth
		h,v,d = map(int, head)
		
		
		# Determine the bounding box around the head regarding its depth
		if d != 0:
			shift = int((1000.0/d)*90)
			line = int((1000.0/d)*80)
		else:
			shift = 1
			line = 1
	
		# Determine the coordinates of the bounding box to extract
		cropTop = self.keepRange(int(v-shift), 480)
		cropLeft = self.keepRange(int(h-shift), 640)
		cropBottom = self.keepRange(int(v+shift)+1, 480)
		cropRight = self.keepRange(int(h+shift)+1, 640)
	
		# Extract the informations within the bounding box
		startV = shift-v+cropTop
		startH = shift-h+cropLeft
		endV = shift+cropBottom-v
		endH = shift+cropRight-h
		
	
		max = (2*shift)+1
		extracted = np.zeros(max*max).reshape(max, max)
		extracted[startV:endV, startH:endH] = depthMap[cropTop:cropBottom, cropLeft:cropRight]
		
	
		# Extract the head from the background with a threshold
		start = d-100
		end = d+100
		
		extracted = self.thresholdBinary(extracted, start, end)
		
		
		
		
		# Re-initialise empty holders
		emptyTop, emptyLeft, emptyBottom, emptyRight = 0, 0, 0, 0
		
		
		# Remove all zeros columns and rows from both matrices
		column = extracted.sum(axis=0).astype(int)
		row = extracted.sum(axis=1).astype(int)

		# Remove empty left columns
		i = 0
		while i<len(column) and column[i]==0:
			extracted = extracted[:,1:]
			emptyLeft += 1
			i += 1

		# Remove empty right columns
		i = len(column)-1
		while i>=0 and column[i]==0:
			extracted = extracted[:,:-1]
			emptyRight += 1
			i -= 1

		# Remove empty top rows
		i = 0
		while i<len(row) and row[i]==0:
			extracted = extracted[1:,:]
			emptyTop += 1
			i += 1
		
		
		
		
		
		# The eyes are assumed to look at the finger tip
		# Based on the alignment of the hand and the elbow, we can extrapolate their relative position
		
		# First, let's make sure the chosen line is accessible
		if len(extracted)<=line:
			return [0,0]
		else:
			
			proportion = 0.15
			total = np.sum(extracted[line])
			index = np.nonzero(extracted[line] == 1)
			
			if len(index[0])==0:
				return [0,0]
			else:
				# left side (from the user point of view)
				if elbowHand[0] == 1:
					h = index[0][0] + total-(total*proportion)
				# right side (from the user point of view)
				elif elbowHand[0] == -1:
					h = index[0][0] + (total*proportion)
				# center
				else:
					h = index[0][0] + (total*0.5)
				
				
				# Return the coordinates
				v = int(cropTop+emptyTop+line)
				h = int(cropLeft+emptyLeft+h)
				
				return [h, v]