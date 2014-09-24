#! /usr/bin/python
from classes.BPNHandler import *
from classes.Dataset import *
from classes.DatasetManager import *
from classes.FeatureExtractor import *
from classes.Settings import *
from classes.Utils import *
import numpy as np
import sys
import cv2



# Definition of the Training class
class Training():
	
	# Load required classes
	bpn = BPNHandler()
	datasetManager = DatasetManager()
	featureExtractor = FeatureExtractor()
	settings = Settings()
	utils = Utils()
	
	
	# Returns the array of the positive targets based on the parameter
	# 
	# @param	data				Data to evaluate
	# @param	positiveTarget		Array of the positive targets
	# @return	array				Array of the positive targets based on the parameter
	def getPositiveTargetArray(self, data, positiveTarget):
		output = []
		for i in range(len(data)):
			for j in range(len(data[i])):
				output.append(positiveTarget[i])
		
		return output
	
	
	# Returns the array of the negative targets based on the parameter
	# 
	# @param	data					Data to evaluate
	# @param	positiveTargetLength	Length of the array of positive targets
	# @return	array					Array of the negative targets based on the parameter
	def getNegativeTargetArray(self, data, positiveTargetLength):
		# Create the negative target thanks to the lenth of the positive one
		negativeTarget = np.zeros(positiveTargetLength).astype(int)
		
		output = []
		for i in range(len(data)):
			for j in range(len(data[i])):
				output.append(negativeTarget)
		
		return output
	
	
	# Train the network with the complete set of data
	# 
	# @param	None
	# @return	None
	def complete(self):
		positiveTraining = self.datasetManager.getPositiveCompleteMixed("training")
		negativeTraining = self.datasetManager.getMainNegative("training")
		positiveTesting = self.datasetManager.getPositiveCompleteMixed("testing")
		negativeTesting = self.datasetManager.getMainNegative("testing")
		positiveTarget = self.datasetManager.getCompleteMixedTarget()
		
		# run the network
		self.run(positiveTraining, negativeTraining, positiveTesting, negativeTesting, positiveTarget, True)
	
	
	# Train the network with the restrained set of data
	# 
	# @param	None
	# @return	None
	def restrained(self):
		positiveTraining = self.datasetManager.getPositiveRestrained("training")
		negativeTraining = self.datasetManager.getNegativeMainRestrained("training")
		positiveTesting = self.datasetManager.getPositiveRestrained("testing")
		negativeTesting = self.datasetManager.getNegativeMainRestrained("testing")
		positiveTarget = self.datasetManager.getRestrainedTarget()
		
		# run the network
		self.run(positiveTraining, negativeTraining, positiveTesting, negativeTesting, positiveTarget, True)
		
	
	# Train the network with pre-computed recent values to bypass loading
	# 
	# @param	None
	# @return	None
	def recentValues(self):
		trainingInput = self.datasetManager.getRecentValuesRestrained(trainingInput=True)
		trainingTarget = self.datasetManager.getRecentValuesRestrained(trainingTarget=True)
		testingInput = self.datasetManager.getRecentValuesRestrained(testingInput=True)
		testingTarget = self.datasetManager.getRecentValuesRestrained(testingTarget=True)
		
		# run the network
		self.bpn.run(trainingInput, trainingTarget, testingInput, testingTarget, learningRate=0.05, momentum=0.1, optimal=True)
		
	
	# Train the network with the complete set of data
	# 
	# @param	positiveTraining		Array of positive data from the training set
	# @param	negativeTraining		Array of negative data from the training set
	# @param	positiveTesting			Array of positive data from the testing set
	# @param	negativeTesting			Array of negative data from the testing set
	# @param	positiveTarget			Array of positive targets to reach
	# @param	getData					Flag to output the processed features in order to bypass loading the next time
	# @return	None
	def run(self, positiveTraining, negativeTraining, positiveTesting, negativeTesting, positiveTarget, getData=False):
		# Load all dataset files and gather them accordingly
		training = self.datasetManager.loadDataset(positiveTraining)
		training.extend(self.datasetManager.loadDataset(negativeTraining))
		
		testing = self.datasetManager.loadDataset(positiveTesting)
		testing.extend(self.datasetManager.loadDataset(negativeTesting))
		
		# Process all features
		print "Processing features..."
		trainingInput = []
		for data in training:
			trainingInput.extend(self.featureExtractor.getFeatures(data))
		
		testingInput = []
		for data in testing:
			testingInput.extend(self.featureExtractor.getFeatures(data))
		
		
		# Build the target arrays
		trainingTarget = self.getPositiveTargetArray(positiveTraining, positiveTarget)
		trainingTarget.extend(self.getNegativeTargetArray(negativeTraining, len(positiveTarget)))
		
		testingTarget = self.getPositiveTargetArray(positiveTesting, positiveTarget)
		testingTarget.extend(self.getNegativeTargetArray(negativeTesting, len(positiveTarget)))
		
		
		# Check if we need to print the data or run the network
		if getData:
			self.utils.getPythonInitCode(trainingInput, "trainingInput")
			self.utils.getPythonInitCode(trainingTarget, "trainingTarget")
			self.utils.getPythonInitCode(testingInput, "testingInput")
			self.utils.getPythonInitCode(testingTarget, "testingTarget")
			
		else:
			# Run the network
			self.bpn.run(trainingInput, trainingTarget, testingInput, testingTarget, learningRate=0.05, momentum=0.1, optimal=False)




 if __name__ == __main__:
	 app = Training()
	 app.recentValues()