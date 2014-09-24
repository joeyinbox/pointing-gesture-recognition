#! /usr/bin/python
import numpy as np
from classes.BPNHandler import *
from classes.FeatureExtractor import *
from classes.Utils import *



# Definition of the UnitTesting class
class UnitTesting:
	
	featureExtractor = FeatureExtractor()
	utils = Utils()
	bpn = BPNHandler(True)
	
	currentPassed = 0
	currentFailed = 0
	currentTotal = 0
	passed = 0
	failed = 0
	total = 0
	
	
	# Check that the result parameter is conform to another expectation parameter
	# 
	# @param	expectation			Targeted result
	# @param	result				Actual result to test
	# @param	method				Name of the method currently tested
	# @param	test				Name of the current assertion
	# @return	None
	def check(self, expectation, result, method, test):
		self.currentTotal += 1
		self.total += 1
		
		if type(expectation).__module__ == np.__name__:
			# np.array_equiv, np.array_equal, np.testing.assert_allclose all fail with np.NaN values
			tmp = True
			if type(result).__module__ == np.__name__ and expectation.size==result.size:
				shape = expectation.shape
				
				# Only considers 2D arrays
				for i in range(shape[0]):
					if len(shape)>1:
						for j in range(shape[1]):
							if expectation[i][j]!=None and np.isnan(expectation[i][j]):
								if result[i][j]==None or  not np.isnan(expectation[i][j]):
									tmp = False
							# Handle float approximation
							elif (type(expectation[i][j])==float and ('%0.5f'%expectation[i][j])!=('%0.5f'%result[i][j])) or (expectation[i][j]!=result[i][j]):
							#elif expectation[i][j] != result[i][j]:
								tmp = False
					elif expectation[i]!=None and np.isnan(expectation[i]):
						if result[i]==None or  not np.isnan(expectation[i]):
							tmp = False
					elif expectation[i] != result[i]:
						tmp = False
			else:
				tmp = False
		elif type(expectation)==list:
			
			if type(result)==list and len(expectation)==len(result):
				tmp = True
				for i in range(len(expectation)):
					if expectation[i]!=result[i]:
						tmp = False
			else:
				tmp = False
		elif expectation!=None and np.isnan(expectation):
			if np.isnan(result):
				tmp = True
			else:
				tmp = False
		elif expectation==result:
			tmp = True
		else:
			tmp = False
		
		
		if tmp:
			self.currentPassed += 1
			self.passed += 1
			print "--- Success \t{0}: \t{1}".format(method, test)
		else:
			self.currentFailed += 1
			self.failed += 1
			print "--- Failure \t{0}: \t{1} \t{2} while expecting {3}".format(method, test, result, expectation)
	
	
	# Display the results of the unit-tests of a category
	# 
	# @param	None
	# @return	None
	def getResults(self):
		print "------------------------\n--- Unit Testing results:"
		if self.currentTotal>0:
			print("--- {0} passed ({1}%)".format(self.currentPassed, int((self.currentPassed/self.currentTotal)*100)))
			print("--- {0} failed ({1}%)".format(self.currentFailed, int((self.currentFailed/self.currentTotal)*100)))
			print("--- Total asserted: {0}".format(self.currentTotal))
		else:
			print "--- None yet..."
		print "------------------------"
		
		self.currentPassed = 0
		self.currentFailed = 0
		self.currentTotal = 0
	
	
	# Display the final results of the unit-tests
	# 
	# @param	None
	# @return	None
	def getFinalResults(self):
		print "\n------------------------\n--- Final Unit Testing results:"
		if self.total>0:
			print("--- {0} passed ({1}%)".format(self.passed, int((self.passed/self.total)*100)))
			print("--- {0} failed ({1}%)".format(self.failed, int((self.failed/self.total)*100)))
			print("--- Total asserted: {0}".format(self.total))
		else:
			print "--- None yet..."
		print "------------------------"
		
		self.passed = 0
		self.failed = 0
		self.total = 0
		
	
	# Assert the FeaturesExtractor class
	# 
	# @param	None
	# @return	None
	def assertFeatureExtractor(self):
		print "\n--- FeaturesExtractor ---"
		
		
		
		# Assert the thresholdBinary method
		# Expected outputs:	0|1
		self.check(0, self.featureExtractor.thresholdBinary(1, 2, 1), "thresholdBinary", "x<start")
		self.check(0, self.featureExtractor.thresholdBinary(2, 2, 1), "thresholdBinary", "x>end")
		self.check(0, self.featureExtractor.thresholdBinary(0, -1, 0), "thresholdBinary", "x==0")
		self.check(1, self.featureExtractor.thresholdBinary(1, 1, 1), "thresholdBinary", "x==start and x==end")
		self.check(1, self.featureExtractor.thresholdBinary(2, 1, 2), "thresholdBinary", "x>start and x==end")
		self.check(1, self.featureExtractor.thresholdBinary(2, 2, 3), "thresholdBinary", "x==start and x<end")
		self.check(1, self.featureExtractor.thresholdBinary(2, 1, 3), "thresholdBinary", "x>start and x<end")
		
		
		
		# Assert the thresholdExtracted method
		# Expected outputs:	np.NaN|(x>=start and x<=end and x!=0)
		self.check(np.NaN, self.featureExtractor.thresholdExtracted(1, 2, 1), "thresholdExtracted", "x<start")
		self.check(np.NaN, self.featureExtractor.thresholdExtracted(2, 2, 1), "thresholdExtracted", "x>end")
		self.check(np.NaN, self.featureExtractor.thresholdExtracted(0, -1, 0), "thresholdExtracted", "x==0")
		self.check(1, self.featureExtractor.thresholdExtracted(1, 1, 1), "thresholdExtracted", "x==start and x==end")
		self.check(2, self.featureExtractor.thresholdExtracted(2, 1, 2), "thresholdExtracted", "x>start and x==end")
		self.check(2, self.featureExtractor.thresholdExtracted(2, 2, 3), "thresholdExtracted", "x==start and x<end")
		self.check(2, self.featureExtractor.thresholdExtracted(2, 1, 3), "thresholdExtracted", "x>start and x<end")
		
		
		
		# Assert the thresholdExtracted method
		# Expected outputs:	None|(index of nearest value 1)
		self.check(None, self.featureExtractor.findNearestValue([], 0), "findNearestValue", "empty array")
		self.check(None, self.featureExtractor.findNearestValue([0], 1), "findNearestValue", "index out of bound")
		self.check(None, self.featureExtractor.findNearestValue([0], -1), "findNearestValue", "index out of bound")
		self.check(None, self.featureExtractor.findNearestValue([0,0], 1), "findNearestValue", "no 1 in small even array")
		self.check(None, self.featureExtractor.findNearestValue([0,0,0], 1), "findNearestValue", "no 1 in small odd array")
		self.check(None, self.featureExtractor.findNearestValue([0,0,0,0,0], 1), "findNearestValue", "no 1 in big even array")
		self.check(None, self.featureExtractor.findNearestValue([0,0,0,0,0,0], 1), "findNearestValue", "no 1 in big odd array")
		self.check(None, self.featureExtractor.findNearestValue([0,0,0,0,1], 1), "findNearestValue", "far initial index not in middle of odd array")
		self.check(0, self.featureExtractor.findNearestValue([1,0,0,0,0], 1), "findNearestValue", "close initial index not in middle of odd array")
		self.check(3, self.featureExtractor.findNearestValue([0,0,0,1], 1), "findNearestValue", "far initial index not in middle of even array")
		self.check(0, self.featureExtractor.findNearestValue([1,0,0,0], 1), "findNearestValue", "close initial index not in middle of even array")
		self.check(0, self.featureExtractor.findNearestValue([1,0,0], 1), "findNearestValue", "1 as first index in small array")
		self.check(1, self.featureExtractor.findNearestValue([0,1,0], 1), "findNearestValue", "1 as middle index in small array")
		self.check(2, self.featureExtractor.findNearestValue([0,0,1], 1), "findNearestValue", "1 as last index in small array")
		self.check(0, self.featureExtractor.findNearestValue([1,0,0,0,0], 2), "findNearestValue", "1 as first index in big array")
		self.check(2, self.featureExtractor.findNearestValue([0,0,1,0,0], 2), "findNearestValue", "1 as middle index in big array")
		self.check(4, self.featureExtractor.findNearestValue([0,0,0,0,1], 2), "findNearestValue", "1 as last index in big array")
		
		
		
		# Assert the tarExtracted method
		# Expected outputs:	(same array with reduced values based on the minimum)|(same array if only NaN values)
		self.featureExtractor.currentExtracted = np.array([])
		self.featureExtractor.tarExtracted()
		self.check(np.array([]), self.featureExtractor.currentExtracted, "tarExtracted", "empty array")
		
		self.featureExtractor.currentExtracted = np.array([np.NaN,np.NaN])
		self.featureExtractor.tarExtracted()
		self.check(np.array([np.NaN,np.NaN]), self.featureExtractor.currentExtracted, "tarExtracted", "array of NaN values")
		
		self.featureExtractor.currentExtracted = np.array([-1,0,np.NaN])
		self.featureExtractor.tarExtracted()
		self.check(np.array([0,1,np.NaN]), self.featureExtractor.currentExtracted, "tarExtracted", "negative minimal value")
		
		self.featureExtractor.currentExtracted = np.array([0,2,np.NaN])
		self.featureExtractor.tarExtracted()
		self.check(np.array([0,2,np.NaN]), self.featureExtractor.currentExtracted, "tarExtracted", "zero minimal value")
		
		self.featureExtractor.currentExtracted = np.array([1,3,np.NaN])
		self.featureExtractor.tarExtracted()
		self.check(np.array([0,2,np.NaN]), self.featureExtractor.currentExtracted, "tarExtracted", "positive minimal value")
		
		self.featureExtractor.currentExtracted = np.array([[np.NaN,np.NaN],[np.NaN,np.NaN]])
		self.featureExtractor.tarExtracted()
		self.check(np.array([[np.NaN,np.NaN],[np.NaN,np.NaN]]), self.featureExtractor.currentExtracted, "tarExtracted", "2D array of NaN values")
		
		self.featureExtractor.currentExtracted = np.array([[1,0,np.NaN],[-1,0,np.NaN]])
		self.featureExtractor.tarExtracted()
		self.check(np.array([[2,1,np.NaN],[0,1,np.NaN]]), self.featureExtractor.currentExtracted, "tarExtracted", "2D array with negative minimal value")
		
		self.featureExtractor.currentExtracted = np.array([[0,2,np.NaN],[1,2,np.NaN]])
		self.featureExtractor.tarExtracted()
		self.check(np.array([[0,2,np.NaN],[1,2,np.NaN]]), self.featureExtractor.currentExtracted, "tarExtracted", "2D array with zero minimal value")
		
		self.featureExtractor.currentExtracted = np.array([[1,2,np.NaN],[3,4,np.NaN]])
		self.featureExtractor.tarExtracted()
		self.check(np.array([[0,1,np.NaN],[2,3,np.NaN]]), self.featureExtractor.currentExtracted, "tarExtracted", "2D array with positive minimal value")
		
		
		
		# Assert the removeEmptyColumnsRows method
		# Expected outputs:	same arrays without empty rows and columns
		self.featureExtractor.currentExtracted = np.array([])
		self.featureExtractor.currentBinary = np.array([])
		self.featureExtractor.removeEmptyColumnsRows()
		self.check(np.array([]), self.featureExtractor.currentExtracted, "removeEmptyColumnsRows", "empty array: currentExtracted")
		self.check(np.array([]), self.featureExtractor.currentBinary, "removeEmptyColumnsRows", "empty array: currentBinary")
		
		self.featureExtractor.currentExtracted = np.array([[0,0],[0,0]])
		self.featureExtractor.currentBinary = np.array([[0,0],[0,0]])
		self.featureExtractor.removeEmptyColumnsRows()
		self.check(np.array([[]]), self.featureExtractor.currentExtracted, "removeEmptyColumnsRows", "array of 0: currentExtracted")
		self.check(np.array([[]]), self.featureExtractor.currentBinary, "removeEmptyColumnsRows", "array of 0: currentBinary")
		
		self.featureExtractor.currentExtracted = np.array([[1,2],[3,4]])
		self.featureExtractor.currentBinary = np.array([[1,2],[3,4]])
		self.featureExtractor.removeEmptyColumnsRows()
		self.check(np.array([[1,2],[3,4]]), self.featureExtractor.currentExtracted, "removeEmptyColumnsRows", "array of non-zero values: currentExtracted")
		self.check(np.array([[1,2],[3,4]]), self.featureExtractor.currentBinary, "removeEmptyColumnsRows", "array of non-zero values: currentBinary")
		
		self.featureExtractor.currentExtracted = np.array([[0,0],[1,2]])
		self.featureExtractor.currentBinary = np.array([[0,0],[1,2]])
		self.featureExtractor.removeEmptyColumnsRows()
		self.check(np.array([[1,2]]), self.featureExtractor.currentExtracted, "removeEmptyColumnsRows", "first row empty: currentExtracted")
		self.check(np.array([[1,2]]), self.featureExtractor.currentBinary, "removeEmptyColumnsRows", "first row empty: currentBinary")
		
		self.featureExtractor.currentExtracted = np.array([[1,2],[0,0]])
		self.featureExtractor.currentBinary = np.array([[1,2],[0,0]])
		self.featureExtractor.removeEmptyColumnsRows()
		self.check(np.array([[1,2]]), self.featureExtractor.currentExtracted, "removeEmptyColumnsRows", "last row empty: currentExtracted")
		self.check(np.array([[1,2]]), self.featureExtractor.currentBinary, "removeEmptyColumnsRows", "last row empty: currentBinary")
		
		self.featureExtractor.currentExtracted = np.array([[0,1],[0,2]])
		self.featureExtractor.currentBinary = np.array([[0,1],[0,2]])
		self.featureExtractor.removeEmptyColumnsRows()
		self.check(np.array([[1],[2]]), self.featureExtractor.currentExtracted, "removeEmptyColumnsRows", "first column empty: currentExtracted")
		self.check(np.array([[1],[2]]), self.featureExtractor.currentBinary, "removeEmptyColumnsRows", "first column empty: currentBinary")
		
		self.featureExtractor.currentExtracted = np.array([[1,0],[2,0]])
		self.featureExtractor.currentBinary = np.array([[1,0],[2,0]])
		self.featureExtractor.removeEmptyColumnsRows()
		self.check(np.array([[1],[2]]), self.featureExtractor.currentExtracted, "removeEmptyColumnsRows", "last column empty: currentExtracted")
		self.check(np.array([[1],[2]]), self.featureExtractor.currentBinary, "removeEmptyColumnsRows", "last column empty: currentBinary")
		
		
		
		# Assert the removeEmptyColumnsRows method
		# Expected outputs:	rotated matrice by the rotationAngle
		# Expected outputs:	(-1|0|1|2) for rotationAngle
		self.featureExtractor.currentExtracted = np.array([[1,2],[3,4]])
		self.featureExtractor.currentBinary = np.array([[1,2],[3,4]])
		
		self.featureExtractor.rotate([0,0],[0,0])
		self.check(np.array([[1,2],[3,4]]), self.featureExtractor.currentExtracted, "rotate", "elbow/hand on same position: currentExtracted")
		self.check(np.array([[1,2],[3,4]]), self.featureExtractor.currentBinary, "rotate", "elbow/hand on same position: currentBinary")
		self.check(0, self.featureExtractor.rotationAngle, "rotate", "elbow/hand on same position: rotationAngle")
		
		self.featureExtractor.rotate([1,1],[0,0])
		self.check(np.array([[2,4],[1,3]]), self.featureExtractor.currentExtracted, "rotate", "elbow up left: currentExtracted")
		self.check(np.array([[2,4],[1,3]]), self.featureExtractor.currentBinary, "rotate", "elbow up left: currentBinary")
		self.check(1, self.featureExtractor.rotationAngle, "rotate", "elbow up left: rotationAngle")
		
		self.featureExtractor.rotate([0,1],[0,0])
		self.check(np.array([[4,3],[2,1]]), self.featureExtractor.currentExtracted, "rotate", "elbow up: currentExtracted")
		self.check(np.array([[4,3],[2,1]]), self.featureExtractor.currentBinary, "rotate", "elbow up: currentBinary")
		self.check(1, self.featureExtractor.rotationAngle, "rotate", "elbow up: rotationAngle")
		
		self.featureExtractor.rotate([0,1],[1,0])
		self.check(np.array([[3,1],[4,2]]), self.featureExtractor.currentExtracted, "rotate", "elbow up right: currentExtracted")
		self.check(np.array([[3,1],[4,2]]), self.featureExtractor.currentBinary, "rotate", "elbow up right: currentBinary")
		self.check(1, self.featureExtractor.rotationAngle, "rotate", "elbow up right: rotationAngle")
		
		self.featureExtractor.rotate([0,0],[1,0])
		self.check(np.array([[3,1],[4,2]]), self.featureExtractor.currentExtracted, "rotate", "elbow right: currentExtracted")
		self.check(np.array([[3,1],[4,2]]), self.featureExtractor.currentBinary, "rotate", "elbow right: currentBinary")
		self.check(0, self.featureExtractor.rotationAngle, "rotate", "elbow right: rotationAngle")
		
		self.featureExtractor.rotate([0,0],[1,1])
		self.check(np.array([[4,3],[2,1]]), self.featureExtractor.currentExtracted, "rotate", "elbow down right: currentExtracted")
		self.check(np.array([[4,3],[2,1]]), self.featureExtractor.currentBinary, "rotate", "elbow down right: currentBinary")
		self.check(-1, self.featureExtractor.rotationAngle, "rotate", "elbow down right: rotationAngle")
		
		self.featureExtractor.rotate([0,0],[0,1])
		self.check(np.array([[2,4],[1,3]]), self.featureExtractor.currentExtracted, "rotate", "elbow down: currentExtracted")
		self.check(np.array([[2,4],[1,3]]), self.featureExtractor.currentBinary, "rotate", "elbow down: currentBinary")
		self.check(-1, self.featureExtractor.rotationAngle, "rotate", "elbow down: rotationAngle")
		
		self.featureExtractor.rotate([1,0],[0,1])
		self.check(np.array([[1,2],[3,4]]), self.featureExtractor.currentExtracted, "rotate", "elbow down left: currentExtracted")
		self.check(np.array([[1,2],[3,4]]), self.featureExtractor.currentBinary, "rotate", "elbow down left: currentBinary")
		self.check(-1, self.featureExtractor.rotationAngle, "rotate", "elbow down left: rotationAngle")
		
		self.featureExtractor.rotate([1,0],[0,0])
		self.check(np.array([[4,3],[2,1]]), self.featureExtractor.currentExtracted, "rotate", "elbow left: currentExtracted")
		self.check(np.array([[4,3],[2,1]]), self.featureExtractor.currentBinary, "rotate", "elbow left: currentBinary")
		self.check(2, self.featureExtractor.rotationAngle, "rotate", "elbow left: rotationAngle")
		
		
		
		# Assert the keepRange method
		# Expected outputs:	integer value between 0 and max
		self.check(0, self.featureExtractor.keepRange(-1, 2), "keepRange", "negative value")
		self.check(0, self.featureExtractor.keepRange(0, 2), "keepRange", "zero value")
		self.check(1, self.featureExtractor.keepRange(1, 2), "keepRange", "positive value < max")
		self.check(2, self.featureExtractor.keepRange(2, 2), "keepRange", "positive value == max")
		self.check(2, self.featureExtractor.keepRange(3, 2), "keepRange", "positive value > max")
		self.check(0, self.featureExtractor.keepRange(-1, 0), "keepRange", "negative value and max==0")
		self.check(0, self.featureExtractor.keepRange(0, 0), "keepRange", "zero value and max==0")
		self.check(0, self.featureExtractor.keepRange(1, 0), "keepRange", "positive value and max==0")
		self.check(0, self.featureExtractor.keepRange(-1, -1), "keepRange", "negative value and negative max")
		self.check(0, self.featureExtractor.keepRange(0, -1), "keepRange", "zero value and negative max")
		self.check(0, self.featureExtractor.keepRange(1, -1), "keepRange", "positive value and negative max")
		
		
		
		# Assert the keepRange method
		# Expected outputs:	(percentage of actual data within a restricted area)|(0 as a fallback)
		self.featureExtractor.currentW = 0
		self.featureExtractor.currentH = 0
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),1,0,0,1,1), "countWithinArea", "zero currentW and currentH")
		
		self.featureExtractor.currentW = 0
		self.featureExtractor.currentH = 1
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),1,0,0,1,1), "countWithinArea", "zero currentW")
		
		self.featureExtractor.currentW = 1
		self.featureExtractor.currentH = 0
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),1,0,0,1,1), "countWithinArea", "zero currentH")
		
		self.featureExtractor.currentW = -1
		self.featureExtractor.currentH = -1
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),1,0,0,1,1), "countWithinArea", "negative currentW and currentH")
		
		self.featureExtractor.currentW = -1
		self.featureExtractor.currentH = 1
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),1,0,0,1,1), "countWithinArea", "negative currentW")
		
		self.featureExtractor.currentW = 1
		self.featureExtractor.currentH = -1
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),1,0,0,1,1), "countWithinArea", "negative currentH")
		
		self.featureExtractor.currentW = 1
		self.featureExtractor.currentH = 1
		self.check(0, self.featureExtractor.countWithinArea(np.array([]),1,0,0,1,1), "countWithinArea", "empty array")
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),0,0,0,1,1), "countWithinArea", "zero total")
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),10, 0,0, 0,0), "countWithinArea", "v1==v2 and h1==h2")
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),10, 0,0, 1,0), "countWithinArea", "v1==v2 and h1<h2")
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),10, 1,0, 0,0), "countWithinArea", "v1==v2 and h1>h2")
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),10, 0,0, 0,1), "countWithinArea", "v1<v2 and h1==h2")
		self.check(10, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),10, 0,0, 1,1), "countWithinArea", "v1<v2 and h1<h2")
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),10, 1,0, 0,1), "countWithinArea", "v1<v2 and h1>h2")
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),10, 0,1, 0,0), "countWithinArea", "v1>v2 and h1==h2")
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),10, 0,1, 1,0), "countWithinArea", "v1>v2 and h1<h2")
		self.check(0, self.featureExtractor.countWithinArea(np.array([[1,2],[3,4]]),10, 1,1, 0,0), "countWithinArea", "v1>v2 and h1>h2")
		
		
		
		# Assert the getElbowHandAlignment method
		# Expected outputs:	[(-1|0|1),(-1|0|1)]
		self.check([0,0], self.featureExtractor.getElbowHandAlignment(-1, 0,0,0,0, 0), "getElbowHandAlignment", "negative depth")
		self.check([0,0], self.featureExtractor.getElbowHandAlignment(0, 0,0,0,0, 0), "getElbowHandAlignment", "zero depth")
		self.check([0,0], self.featureExtractor.getElbowHandAlignment(1, 0,0,0,0, 0), "getElbowHandAlignment", "positive depth")
		
		self.check([1,0-1], self.featureExtractor.getElbowHandAlignment(1000,  61,61, 0,0, 0), "getElbowHandAlignment", "left down")
		self.check([-1,0-1], self.featureExtractor.getElbowHandAlignment(1000, 61,0,  0,61, 0), "getElbowHandAlignment", "right down")
		self.check([0,0-1], self.featureExtractor.getElbowHandAlignment(1000,  61,1,  0,0, 0), "getElbowHandAlignment", "front down")
		
		self.check([1,1], self.featureExtractor.getElbowHandAlignment(1000,  0,61, 61,0, 0), "getElbowHandAlignment", "left up")
		self.check([-1,1], self.featureExtractor.getElbowHandAlignment(1000, 0,0,  61,61, 0), "getElbowHandAlignment", "right up")
		self.check([0,1], self.featureExtractor.getElbowHandAlignment(1000,  0,1,  61,0, 0),  "getElbowHandAlignment", "front up")
		
		self.check([1,0], self.featureExtractor.getElbowHandAlignment(1000,  0,61, 0,0, 0), "getElbowHandAlignment", "left lateral")
		self.check([-1,0], self.featureExtractor.getElbowHandAlignment(1000, 0,0,  0,61, 0), "getElbowHandAlignment", "right lateral")
		self.check([0,0], self.featureExtractor.getElbowHandAlignment(1000,  0,1,  0,0, 0), "getElbowHandAlignment", "front lateral")
		
		
		
		# Assert the normalizeInput method
		# Expected outputs:	[normalized values in the range -1 to 1]
		self.check([], self.featureExtractor.normalizeInput([]), "normalizeInput", "empty array")
		self.check([-1,-1,-1], self.featureExtractor.normalizeInput([0,0,0],0,2), "normalizeInput", "low range values")
		self.check([0,0,0], self.featureExtractor.normalizeInput([1,1,1],0,2), "normalizeInput", "middle range values")
		self.check([1,1,1], self.featureExtractor.normalizeInput([2,2,2],0,2), "normalizeInput", "top range values")
		
		
		
		# Assert the processFeatures method
		# Expected outputs:	[6 normalized features]
		self.check([-1,-1,-1,-1,-1,-1], self.featureExtractor.processFeatures(0,0,0, 0,0,0, np.array([]), [0,0,0]), "processFeatures", "empty array")
		self.check([-1,-1,-1,-1,-1,-1], self.featureExtractor.processFeatures(0,0,0, 0,0,0, np.array([0,0,0]), [0,0,0]), "processFeatures", "1 dimensional array")
		self.check([-1,-1,-1,-1,-1,-1], self.featureExtractor.processFeatures(0,0,0, 0,0,0, np.array([[0,0,0],[0,0,0],[0,0,0]]), [0,0,0]), "processFeatures", "zero array")
		
		
		
		# Assert the getFingerTip method
		# Expected outputs:	[v,h] non negative values
		self.featureExtractor.cropLeft = 0
		self.featureExtractor.emptyLeft = 0
		self.featureExtractor.cropTop = 0
		self.featureExtractor.emptyTop = 0
		self.featureExtractor.rotationAngle = 0
		self.featureExtractor.currentBinary = np.array([[]])
		self.check([0,0], self.featureExtractor.getFingerTip(), "getFingerTip", "empty array")
		
		self.featureExtractor.currentBinary = np.array([[0,0,0,0,0]])
		self.check([0,0], self.featureExtractor.getFingerTip(), "getFingerTip", "zero array")
		
		self.featureExtractor.rotationAngle = -1
		self.featureExtractor.currentBinary = np.array([[1,0,0,0,0]])
		self.check([0,4], self.featureExtractor.getFingerTip(), "getFingerTip", "rotationAngle=-1 and extrem left value")
		self.featureExtractor.currentBinary = np.array([[0,0,1,0,0]])                     
		self.check([0,2], self.featureExtractor.getFingerTip(), "getFingerTip", "rotationAngle=-1 and middle value")
		self.featureExtractor.currentBinary = np.array([[0,0,0,0,1]])                     
		self.check([0,0], self.featureExtractor.getFingerTip(), "getFingerTip", "rotationAngle=-1 and extrem right value")
		
		self.featureExtractor.rotationAngle = 0
		self.featureExtractor.currentBinary = np.array([[1,0,0,0,0]])
		self.check([0,0], self.featureExtractor.getFingerTip(), "getFingerTip", "rotationAngle=0 and extrem left value")
		self.featureExtractor.currentBinary = np.array([[0,0,1,0,0]])
		self.check([2,0], self.featureExtractor.getFingerTip(), "getFingerTip", "rotationAngle=0 and middle value")
		self.featureExtractor.currentBinary = np.array([[0,0,0,0,1]])
		self.check([4,0], self.featureExtractor.getFingerTip(), "getFingerTip", "rotationAngle=0 and extrem right value")
		
		self.featureExtractor.rotationAngle = 1
		self.featureExtractor.currentBinary = np.array([[1,0,0,0,0]])
		self.check([0,0], self.featureExtractor.getFingerTip(), "getFingerTip", "rotationAngle=1 and extrem left value")
		self.featureExtractor.currentBinary = np.array([[0,0,1,0,0]])
		self.check([0,2], self.featureExtractor.getFingerTip(), "getFingerTip", "rotationAngle=1 and middle value")
		self.featureExtractor.currentBinary = np.array([[0,0,0,0,1]])
		self.check([0,4], self.featureExtractor.getFingerTip(), "getFingerTip", "rotationAngle=1 and extrem right value")
		
		self.featureExtractor.rotationAngle = 2
		self.featureExtractor.currentBinary = np.array([[1,0,0,0,0]])
		self.check([4,1], self.featureExtractor.getFingerTip(), "getFingerTip", "rotationAngle=2 and extrem left value")
		self.featureExtractor.currentBinary = np.array([[0,0,1,0,0]])
		self.check([2,1], self.featureExtractor.getFingerTip(), "getFingerTip", "rotationAngle=2 and middle value")
		self.featureExtractor.currentBinary = np.array([[0,0,0,0,1]])
		self.check([0,1], self.featureExtractor.getFingerTip(), "getFingerTip", "rotationAngle=2 and extrem right value")
		
		
		
		# Assert the getEyePosition method
		# Expected outputs:	[v,h] non negative values
		self.check([0,0], self.featureExtractor.getEyePosition(np.array([[]]), [0,0,0], [0,0]), "getEyePosition", "empty array")
		self.check([0,0], self.featureExtractor.getEyePosition(np.array([0,0,0]), [0,0,0], [0,0]), "getEyePosition", "1 dimensional array")
		self.check([0,0], self.featureExtractor.getEyePosition(np.array([[0,0,0],[0,0,0],[0,0,0]]), [0,0,0], [0,0]), "getEyePosition", "zero array")
	
	
	# Assert the Utils class
	# 
	# @param	None
	# @return	None
	def assertUtils(self):
		print "\n--- Utils ---"
		
		
		
		# Assert the getDepthFromMap method
		# Expected outputs:	non negative integer
		self.check(0, self.utils.getDepthFromMap(np.array([]), [0,0]), "getDepthFromMap", "empty array")
		self.check(0, self.utils.getDepthFromMap(np.array([[0,0],[0,0]]), [-1,0]), "getDepthFromMap", "y index out of bond (negative)")
		self.check(0, self.utils.getDepthFromMap(np.array([[0,0],[0,0]]), [2,0]), "getDepthFromMap", "y index out of bond (>=len)")
		self.check(0, self.utils.getDepthFromMap(np.array([[0,0],[0,0]]), [0,-1]), "getDepthFromMap", "x index out of bond (negative)")
		self.check(0, self.utils.getDepthFromMap(np.array([[0,0],[0,0]]), [0,2]), "getDepthFromMap", "x index out of bond (>=len)")
		self.check(0, self.utils.getDepthFromMap(np.array([[0,0],[0,0]]), []), "getDepthFromMap", "empty position array")
		self.check(0, self.utils.getDepthFromMap(np.array([[0,0],[0,0]]), [1]), "getDepthFromMap", "unexpected position array")
		self.check(42, self.utils.getDepthFromMap(np.array([[0,0],[0,42]]), [1,1]), "getDepthFromMap", "correct value")
		
		
		
		# Assert the getHandBoundShift method
		# Expected outputs:	integer
		self.check(-90, self.utils.getHandBoundShift(-1000), "getHandBoundShift", "negative depth")
		self.check(90, self.utils.getHandBoundShift(0), "getHandBoundShift", "zero depth")
		self.check(90, self.utils.getHandBoundShift(1000), "getHandBoundShift", "positive depth")
	
	
	# Assert the BPNHandler class
	# 
	# @param	None
	# @return	None
	def assertBPNHandler(self):
		print "\n--- BPNHandler ---"
		
		
		
		# Assert the check method
		# Expected outputs:	[Boolean, (0|1)]
		self.check([False,0], self.bpn.check([[0,0,0,0,0,0]]), "check", "zero array")