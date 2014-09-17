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


class Training():
	
	# Load required classes
	bpn = BPNHandler()
	datasetManager = DatasetManager()
	featureExtractor = FeatureExtractor()
	settings = Settings()
	utils = Utils()
	
	
	def getPositiveTargetArray(self, data, positiveTarget):
		output = []
		for i in range(len(data)):
			for j in range(len(data[i])):
				output.append(positiveTarget[i])
		
		return output
	
	def getNegativeTargetArray(self, data, positiveTargetLength):
		# Create the negative target thanks to the lenth of the positive one
		negativeTarget = np.zeros(positiveTargetLength).astype(int)
		
		output = []
		for i in range(len(data)):
			for j in range(len(data[i])):
				output.append(negativeTarget)
		
		return output
	
	
	def complete(self):
		positiveTraining = self.datasetManager.getPositiveCompleteMixed("training")
		negativeTraining = self.datasetManager.getMainNegative("training")
		positiveTesting = self.datasetManager.getPositiveCompleteMixed("testing")
		negativeTesting = self.datasetManager.getMainNegative("testing")
		positiveTarget = self.datasetManager.getCompleteMixedTarget()
		
		# run the network
		self.run(positiveTraining, negativeTraining, positiveTesting, negativeTesting, positiveTarget, True)
	
	
	def restrained(self):
		positiveTraining = self.datasetManager.getPositiveRestrained("training")
		negativeTraining = self.datasetManager.getNegativeMainRestrained("training")
		positiveTesting = self.datasetManager.getPositiveRestrained("testing")
		negativeTesting = self.datasetManager.getNegativeMainRestrained("testing")
		positiveTarget = self.datasetManager.getRestrainedTarget()
		
		# run the network
		self.run(positiveTraining, negativeTraining, positiveTesting, negativeTesting, positiveTarget, True)
		
	
	def recentValues(self):
		trainingInput = self.datasetManager.getRecentValuesRestrained(trainingInput=True)
		trainingTarget = self.datasetManager.getRecentValuesRestrained(trainingTarget=True)
		testingInput = self.datasetManager.getRecentValuesRestrained(testingInput=True)
		testingTarget = self.datasetManager.getRecentValuesRestrained(testingTarget=True)
		
		# run the network
		self.bpn.run(trainingInput, trainingTarget, testingInput, testingTarget, learningRate=0.05, momentum=0.1, optimal=True)
		
	
	
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