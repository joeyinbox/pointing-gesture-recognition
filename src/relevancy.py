#! /usr/bin/python
from classes.Dataset import *
from classes.DatasetManager import *
from classes.Settings import *
from classes.Utils import *
import numpy as np



# Definition of the Relevancy class
class Relevancy():
	
	# Load required classes
	datasetManager = DatasetManager()
	settings = Settings()
	utils = Utils()
	
	repartition = [
		"training",
		"testing",
		"validating"
	]
	direction = [
		"back-right",
		"right",
		"front-right",
		"front",
		"front-left",
		"left",
		"back-left"
	]
	orientation = [
		"up",
		"lateral",
		"down"
	]
	negativeType = [
		"closed",
		"opened",
		"four",
		"three",
		"peace",
		"rock"
	]
	
	
	# Returns the repartition between positive and negative files
	# 
	# @param	None
	# @return	tuple				Tuple of the repartition for positive and negative files
	def getRepartition(self):
		# Get detailed counts
		positive = {}
		negative = {}
		
		for repartition in self.repartition:
			positive[repartition] = {}
			negative[repartition] = {}
		
			for direction in self.direction:
				positive[repartition][direction] = {}
				negative[repartition][direction] = {}
				
				for orientation in self.orientation:
					positive[repartition][direction][orientation] = self.getDetailedPositiveRepartition(repartition, direction, orientation)
				
				for negativeType in self.negativeType:
					negative[repartition][direction][negativeType] = self.getDetailedNegativeRepartition(repartition, direction, negativeType)
		
		return (positive, negative)
	
	
	# Returns the number of files in a given positive folder
	# 
	# @param	type				Type of dataset
	# @param	direction			Direction featured in the dataset
	# @param	orientation			Orientation featured in the dataset
	# @return	numeric				Number of files in a given positive folder
	def getDetailedPositiveRepartition(self, type, direction, orientation=""):
		return self.utils.getFileNumberInFolder(self.settings.getPositiveFolder()+type+"/"+direction+"/"+orientation+"/")
	
	
	# Returns the number of files in a given negative folder
	# 
	# @param	type				Type of dataset
	# @param	direction			Direction featured in the dataset
	# @param	orientation			Orientation featured in the dataset
	# @return	numeric				Number of files in a given negative folder
	def getDetailedNegativeRepartition(self, type, direction, orientation=""):
		return self.utils.getFileNumberInFolder(self.settings.getNegativeFolder()+type+"/"+direction+"/"+orientation+"/")
	
	
	# Display the general repartition
	# 
	# @param	None
	# @return	None
	def showRepartition(self):
		positive,negative = self.getRepartition()
		
		print "\n\nPositive repartition\n"
		positive = self.showPositiveRepartition(positive)
		
		print "\n\nNegative repartition\n"
		negative = self.showNegativeRepartition(negative)
		
		print "\n\nTotal repartition\n"
		self.showTotalRepartition(positive, negative)
		
		
	# Display and returns the positive repartition
	# 
	# @param	positive			Array of all positive file repartition
	# @return	dict				Informations about the repartition of the positive dataset
	def showPositiveRepartition(self, positive):
		totalPositive = 0
		
		totalTraining = 0
		totalTesting = 0
		totalValidating = 0
		
		for direction in self.direction:
			training = 0
			testing = 0
			validating = 0
			for orientation in self.orientation:
				if len(direction+orientation)<10:
					shift = "\t"
				else:
					shift = ""
				
				
				print("--- {0} {1}{2}\tTraining: {3} \t\tTesting: {4} \t\tValidating: {5}".format(direction, orientation, shift, positive["training"][direction][orientation], positive["testing"][direction][orientation], positive["validating"][direction][orientation]))
				training += positive["training"][direction][orientation]
				testing += positive["testing"][direction][orientation]
				validating += positive["validating"][direction][orientation]
			
			tmp = training+testing+validating
			totalTraining += training
			totalTesting += testing
			totalValidating += validating
			print("--- {0}\t\tTraining: {1} ({2:0.0f}%) \tTesting: {3} ({4:0.0f}%) \tValidating: {5} ({6:0.0f}%)\n---".format(direction,
																														 training,
																														 (training/float(tmp))*100,
																														 testing,
																														 (testing/float(tmp))*100,
																														 validating,
																														 (validating/float(tmp))*100))
		
		
		totalPositive = totalTraining+totalTesting+totalValidating
		print("--- Total: {0} \t\tTraining: {1} ({2:0.0f}%) \tTesting: {3} ({4:0.0f}%) \tValidating: {5} ({6:0.0f}%)".format(totalPositive,
																																totalTraining,
																																(totalTraining/float(totalPositive))*100,
																																totalTesting,
																																(totalTesting/float(totalPositive))*100,
																																totalValidating,
																																(totalValidating/float(totalPositive))*100))

		return {"total":totalPositive,"totalTraining":totalTraining,"totalTesting":totalTesting,"totalValidating":totalValidating}
		
	
	# Display and returns the negative repartition
	# 
	# @param	negative			Array of all negative file repartition
	# @return	dict				Informations about the repartition of the negative dataset
	def showNegativeRepartition(self, negative):
		totalNegative = 0
		
		totalTraining = 0
		totalTesting = 0
		totalValidating = 0
		
		for direction in self.direction:
			training = 0
			testing = 0
			validating = 0
			for negativeType in self.negativeType:
				if len(direction+negativeType)<11:
					shift = "\t"
				else:
					shift = ""
				
				
				print("--- {0} {1}{2}\tTraining: {3} \t\tTesting: {4} \t\tValidating: {5}".format(direction, negativeType, shift, negative["training"][direction][negativeType], negative["testing"][direction][negativeType], negative["validating"][direction][negativeType]))
				training += negative["training"][direction][negativeType]
				testing += negative["testing"][direction][negativeType]
				validating += negative["validating"][direction][negativeType]
			
			tmp = training+testing+validating
			totalTraining += training
			totalTesting += testing
			totalValidating += validating
			print("--- {0}\t\tTraining: {1} ({2:0.0f}%) \tTesting: {3} ({4:0.0f}%) \tValidating: {5} ({6:0.0f}%)\n---".format(direction,
																														 training,
																														 (training/float(tmp))*100,
																														 testing,
																														 (testing/float(tmp))*100,
																														 validating,
																														 (validating/float(tmp))*100))
		
		
		totalNegative = totalTraining+totalTesting+totalValidating
		print("--- Total: {0} \t\tTraining: {1} ({2:0.0f}%) \tTesting: {3} ({4:0.0f}%) \tValidating: {5} ({6:0.0f}%)".format(totalNegative,
																															 totalTraining,
																															 (totalTraining/float(totalNegative))*100,
																															 totalTesting,
																															 (totalTesting/float(totalNegative))*100,
																															 totalValidating,
																															 (totalValidating/float(totalNegative))*100))

		return {"total":totalNegative,"totalTraining":totalTraining,"totalTesting":totalTesting,"totalValidating":totalValidating}

	
	# Display the general repartition
	# 
	# @param	positive			Array of all positive file repartition informations
	# @param	negative			Array of all negative file repartition informations
	# @return	None
	def showTotalRepartition(self, positive, negative):
		total = positive["total"]+negative["total"]
		totalTraining = positive["totalTraining"]+negative["totalTraining"]
		totalTesting = positive["totalTesting"]+negative["totalTesting"]
		totalValidating = positive["totalValidating"]+negative["totalValidating"]
		
		
		print("--- Positive:\t{0} \tTraining: {1} ({2:0.0f}%) \tTesting: {3} ({4:0.0f}%) \tValidating: {5} ({6:0.0f}%)".format(positive["total"],
																															 positive["totalTraining"],
																															 (positive["totalTraining"]/float(positive["total"]))*100,
																															 positive["totalTesting"],
																															 (positive["totalTesting"]/float(positive["total"]))*100,
																															 positive["totalValidating"],
																															 (positive["totalValidating"]/float(positive["total"]))*100))
		
		print("--- Negative:\t{0} \tTraining: {1} ({2:0.0f}%) \tTesting: {3} ({4:0.0f}%) \tValidating: {5} ({6:0.0f}%)".format(negative["total"],
																															 negative["totalTraining"],
																															 (negative["totalTraining"]/float(negative["total"]))*100,
																															 negative["totalTesting"],
																															 (negative["totalTesting"]/float(negative["total"]))*100,
																															 negative["totalValidating"],
																															 (negative["totalValidating"]/float(negative["total"]))*100))
		
		print("--- Total:\t{0} \tTraining: {1} ({2:0.0f}%) \tTesting: {3} ({4:0.0f}%) \tValidating: {5} ({6:0.0f}%)".format(total,
																															 totalTraining,
																															 (totalTraining/float(total))*100,
																															 totalTesting,
																															 (totalTesting/float(total))*100,
																															 totalValidating,
																															 (totalValidating/float(total))*100))
		

if __name__ == "__main__":
	app = Relevancy()
	app.showRepartition()