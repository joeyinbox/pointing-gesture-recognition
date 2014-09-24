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



# Definition of the Validating class
class Validating():
	
	# Load required classes
	bpn = BPNHandler(True)
	datasetManager = DatasetManager()
	featureExtractor = FeatureExtractor()
	settings = Settings()
	utils = Utils()
	
	
	# Evaluate the complete dataset
	# 
	# @param	type					Type of dataset to be evaluated
	# @return	None
	def complete(self, type):
		positiveValidating = self.datasetManager.getPositiveCompleteMixed(type)
		negativeValidating = self.datasetManager.getMainNegative(type)
		
		# run the network
		self.run(positiveValidating, negativeValidating)
	
	
	# Evaluate the restrained dataset
	# 
	# @param	type					Type of dataset to be evaluated
	# @return	None
	def restrained(self, type):
		positiveValidating = self.datasetManager.getPositiveRestrainedMixed(type)
		negativeValidating = self.datasetManager.getNegativeMainRestrained(type)
		
		# run the network
		self.run(positiveValidating, negativeValidating)
		
		
	# Evaluate the given informations
	# 
	# @param	positiveValidating		Array of all positive files to process
	# @param	negativeValidating		Array of all negative files to process
	# @param	getData					Flag to retrieve the data in order to bypass a future loading
	# @return	None
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
				count = 0
				for positive in positiveInput:
					result = self.bpn.check([positive])
					
					if result[0] == False:
						badPositive += 1
						print("{0} is erroneous".format(count))
					else:
						goodPositive += 1
					
					count += 1
				print
				print "{0} corrects and {1} bad --> {2:0.2f}%".format(goodPositive, badPositive, (goodPositive/float(goodPositive+badPositive)*100))
				print
			
			if len(negativeInput)>0:
				print "Negative validation"
				goodNegative = 0
				badNegative = 0
				count = 0
				for negative in negativeInput:
					result = self.bpn.check([negative])
					
					if result[0] == True:
						badNegative += 1
						print("{0} is erroneous".format(count))
					else:
						goodNegative += 1
					
					count += 1
				print
				print "{0} corrects and {1} bad --> {2:0.2f}%".format(goodNegative, badNegative, (goodNegative/float(goodNegative+badNegative)*100))
				print "Final score = {0:0.2f}%".format(((goodPositive+goodNegative)/float(goodPositive+badPositive+goodNegative+badNegative))*100)
		
			if len(positiveInput)==0 and len(negativeInput)==0:
				print "No input to validate..."



if __name__ == "__main__":
	app = Validating()
	app.restrained("training")
	app.complete("training")
	print "\n----------\t"
	
	app.restrained("testing")
	app.complete("testing")
	print "\n----------\t"
	
	app.restrained("validating")
	app.complete("validating")