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


class Validating():
	
	# Load required classes
	bpn = BPNHandler(True)
	datasetManager = DatasetManager()
	featureExtractor = FeatureExtractor()
	settings = Settings()
	utils = Utils()
	
	
	def complete(self):
		positiveValidating = self.datasetManager.getPositiveCompleteMixed("validating")
		negativeValidating = self.datasetManager.getMainNegative("validating")
		
		# run the network
		self.run(positiveValidating, negativeValidating)
	
	
	def restrained(self):
		positiveValidating = self.datasetManager.getPositiveRestrainedMixed("testing")
		negativeValidating = self.datasetManager.getNegativeMainRestrained("testing")
		
		# run the network
		self.run(positiveValidating, negativeValidating)
	
	def accuracy(self):
		positiveValidating = self.datasetManager.getAccuracyRestrained()
		
		# run the network
		self.run(positiveValidating, [])
		
		
		
	
	
	def run(self, positiveValidating, negativeValidating, getData=False):
		# Load all dataset files
		positive = self.datasetManager.loadDataset(positiveValidating)
		negative = self.datasetManager.loadDataset(negativeValidating)
		
		# Process all features
		print "Processing features..."
		positiveInput = []
		for data in positive:
			positiveInput.extend(self.featureExtractor.getFeatures(data))

		
		negativeInput = []
		for data in negative:
			negativeInput.extend(self.featureExtractor.getFeatures(data))
		
		
		# Check if we need to print the data or run the network
		if getData:
			self.utils.getPythonInitCode(positiveInput, "positiveInput")
			self.utils.getPythonInitCode(negativeInput, "negativeInput")
			
		else:
			# Run the validation against the network
			
			if len(positiveInput)>0:
				print "Positive validation"
				
				goodPositive = 0
				badPositive = 0
				for positive in positiveInput:
					result = self.bpn.check([positive])
					
					if result[0] == False:
						badPositive += 1
					else:
						goodPositive += 1
				print
				print "{0} corrects and {1} bad --> {2:0.2f}%".format(goodPositive, badPositive, (goodPositive/float(goodPositive+badPositive)*100))
				print
			
			if len(negativeInput)>0:
				print "Negative validation"
				goodNegative = 0
				badNegative = 0
				for negative in negativeInput:
					result = self.bpn.check([negative])
					
					if result[0] == True:
						badNegative += 1
					else:
						goodNegative += 1
				print
				print "{0} corrects and {1} bad --> {2:0.2f}%".format(goodNegative, badNegative, (goodNegative/float(goodNegative+badNegative)*100))
				print "Final score = {0:0.2f}%".format(((goodPositive+goodNegative)/float(goodPositive+badPositive+goodNegative+badNegative))*100)
		
			if len(positiveInput)==0 and len(negativeInput)==0:
				print "No input to validate..."




test = Validating()
test.restrained()