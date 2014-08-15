#! /usr/bin/python -W ignore::FutureWarning
from classes.BackPropagationNetwork import *
import numpy as np
import sys
from copy import deepcopy
import signal
import heapq


class BPNHandler:
	
	# Hold eventual results
	resultTestingScore, resultTrainingScore, resultInitialWeights, resultWeights, resultConfig, resultIteration = [], [], [], [], [], []
	
	
	def __init__(self, live=False, features=6, hiddenLayers=33, output=4):
		# Define the functions that will be used
		self.lFuncs = [None, gaussian, sgm]
		
		# Initialise the right network
		if live:
			self.bpnValidating = BackPropagationNetwork((features, hiddenLayers, output), self.lFuncs)
			self.bpnValidating.setWeights(self.getRestrainedWeights())
		else:
			self.bpnTesting = BackPropagationNetwork((features, hiddenLayers, output), self.lFuncs)
	
	
	def check(self, features):
		lvInput = np.array(features)
		lvOutput = self.bpnValidating.run(lvInput)
		
		# The output will be an array whose first element indicates if a pointing gesture is recognised
		# In case of a pointing gesture, the second value represent the kind of gesture recognised
		result = [False,0]
		
		# Possibility to get an unified result for several feature inputs
		for i in range(lvInput.shape[0]):
			# If a gesture is recognised:
			if lvOutput[i][np.argmax(lvOutput[i])] > 0.5:
				result = [True, i]
		
		return result
	
	
	def run(self, trainingInput, trainingTarget, testingInput, testingTarget, trainingRate=0.05, momentum=0.1, optimal=False):
		# store the original SIGINT handler to display the results if interrupted
		original_sigint = signal.getsignal(signal.SIGINT)
		signal.signal(signal.SIGINT, self.displayResults)
		
		# Get the inputs and outputs
		lvTrainingInputOriginal = np.array(trainingInput)
		lvTrainingTargetOriginal = np.array(trainingTarget)
		
		lvTestingInputOriginal = np.array(testingInput)
		lvTestingTargetOriginal = np.array(testingTarget)
		
		
		# For research purpose, the number of hidden layers will be dynamic
		ran = np.arange(33, 50)
		
		# Loop the number of hidden layers
		for hidden in ran:
			
			
			# For optimal research purpose, the trainingRate can be dynamic
			if optimal:
				rate = np.arange(trainingRate, 1, 0.05)
			else:
				rate = [trainingRate]
			
			# Loop the number of training rates
			for trainingRate in rate:
				
				
				# For optimal research purpose, the momentum can be dynamic
				if optimal:
					mom = np.arange(momentum, 1.0, 0.1)
				else:
					mom = [momentum]
			
				# Loop the number of momentums
				for momentum in mom:
					
					
					# For optimal research purpose, the network can be ran several times
					if optimal:
						repeatition = range(5)
					else:
						repeatition = [1]
					
					# Loop the number of repeatitions
					for repeat in repeatition:
						
					
						print("{0} hidden layers with a training rate of {1} and a momentum of {2}".format(hidden, trainingRate, momentum))
			        	
			        	
						# Make a copy of the inputs and the outputs
						lvTrainingInput = deepcopy(lvTrainingInputOriginal)
						lvTrainingTarget = deepcopy(lvTrainingTargetOriginal)
		            	
						lvTestingInput = deepcopy(lvTestingInputOriginal)
						lvTestingTarget = deepcopy(lvTestingTargetOriginal)
			        	
			        	
						# Create a new network instance
						bpn = BackPropagationNetwork((len(trainingInput[0]), hidden, len(trainingTarget[0])), self.lFuncs)
			        	
						# Set our goals
						lnMax = 100000
						lnErr = 0.002
						errMax = 1e100
						sameLimit = 25
			        	
						# Will hold the weights for the best score of the run
						bestScore = 9000.0
						bestScoreTraining = 9000.0
						bestWeights = []
						initialWeights = []
						bestIteration = 0
						previous = 9000.0
						same = 0
						
						# Get the initial weights
						initialWeights = bpn.getWeights()
			        	
						# Start training!
						for i in range(lnMax+1):
							err = bpn.trainEpoch(lvTrainingInput, lvTrainingTarget, trainingRate, momentum)
							
				    	
							# Get the result for the current weights against the testing dataset
							self.bpnTesting.setWeights(bpn.getWeights())
							testingResult = self.bpnTesting.run(lvTestingInput)
		            		
							# Process the error on the testing dataset
							output_delta = self.bpnTesting._layerOutput[self.bpnTesting.layerCount-1]-lvTestingTarget.T
							error = np.sum(output_delta**2)
				    		
							# Keep track of this result if it is the best
							if error < bestScore:
								bestScore = error
								bestScoreTraining = err
								bestWeights = bpn.getWeights()
								bestIteration = i
							
				    		
							# Display some informations or stop the current training if necessary
							if i%500 == 0:
								print("Iteration {0}\tError: {1:0.6f}  \t{2:0.6f}".format(i, err, error))
								
								# Check that the network is not stuck
								if error == previous:
									same += 1
								else:
									same = 0
									previous = error
								
								if same == sameLimit:
									print("Network stuck with {1:0.6f}  \t{2:0.6f}".format(i, err, error))
									break
								
							if error <= lnErr:
								print("Minimum error reached at iteration {0} with {1:0.6f}  \t{2:0.6f}".format(i, err, error))
								break
							if error >= errMax:
								print("Will not converge past iteration {0} with {1:0.6f}  \t{2:0.6f}".format(i, err, error))
								break
		            	
						# Display output
						print 
						print("Stopped at Iteration {0}\tError: {1:0.6f}  \t{2:0.6f}".format(i, err, error))
			        	
			        	
						# Keep this result if it is good
						self.addResult(bestScore, bestScoreTraining, initialWeights, bestIteration, bestWeights, [hidden, trainingRate, momentum])
			        	
						print "The best weights for a score of {0:0.6f} at iteration {1} while training was at  {2:0.6f}:".format(bestScore, bestIteration, bestScoreTraining)
						print
		
		# If all loops have finished, display the results (any interuption during the process will call this function anyways...)
		self.displayResults(None, None)
	
	
	def addResult(self, bestScore, bestScoreTraining, initialWeights, bestIteration, bestWeights, config):
		if len(self.resultTestingScore) < 30:
			self.resultTestingScore.append(bestScore)
			self.resultTrainingScore.append(bestScoreTraining)
			self.resultInitialWeights.append(initialWeights)
			self.resultIteration.append(bestIteration)
			self.resultWeights.append(bestWeights)
			self.resultConfig.append(config)
		else:
			# Retrieve the worst score
			largest = heapq.nlargest(1, ((k, i) for i, k in enumerate(self.resultTestingScore)))
			
			if bestScore < largest[0][0]:
				self.resultTestingScore[largest[0][1]] = bestScore
				self.resultTrainingScore[largest[0][1]] = bestScoreTraining
				self.resultInitialWeights[largest[0][1]] = initialWeights
				self.resultIteration[largest[0][1]] = bestIteration
				self.resultWeights[largest[0][1]] = bestWeights
				self.resultConfig[largest[0][1]] = config
	
	
	def displayResults(self, signum, frame):
		print
		print
		print
		
		# Retrieve the 20 best results
		best = heapq.nsmallest(20, ((k, i) for i, k in enumerate(self.resultTestingScore)))
		
		# Display their informations
		i = 1
		for b in best:
			print
			print "###############"
			print "#{0} Result:".format(i)
			i+=1
			
			print "{0} Hidden layers, \tTraining rate: {1}, \tMomentum: {2}".format(self.resultConfig[b[1]][0], self.resultConfig[b[1]][1], self.resultConfig[b[1]][2])
			print "The best weights were for a score of {0:0.6f} at iteration {1} while training was at {2:0.6f}:".format(b[0], self.resultIteration[b[1]], self.resultTrainingScore[b[1]])
			print self.resultWeights[b[1]]
			
			print
			print "Initial weights:"
			print self.resultInitialWeights[b[1]]
		sys.exit(1)
	
	
	def getRestrainedWeights(self):
		# 33 hidden layers
		# Training rate: 0.05
		# Momentum: 0.1
		# Testing score: 3.42
		# Training score: 2.05
		
		return [
			np.array([[ 1.28107127e+00, -2.50866358e-01, -7.70813717e-02, 5.86088803e-01, -1.81528220e-01, 6.14477582e-02, -6.58753889e-02],
		       [ -2.57184868e+00, 3.93576665e+00, -1.26149034e+01, -3.66179352e+00, 1.44670491e+01, -1.68015999e+00, 5.28767781e-01],
		       [ -1.58804629e+01, 1.48027346e+01, -1.82924751e+00, -1.69732124e-01, 5.50417229e+00, 1.73233814e-01, -6.40740890e-01],
		       [ -3.61044147e+00, 1.26173848e+01, -1.00906717e+00, -5.26160516e-01, 5.38728246e+00, -6.32077505e+00, -1.46789574e+00],
		       [ -1.06566239e+01, 7.48004769e+00, 3.02209524e+00, -7.12537910e+00, 3.99967808e+00, 7.50157561e+00, -1.00150469e+00],
		       [ -2.09922646e+00, 3.52940090e+00, 7.21157037e-01, 1.60264695e+00, -5.25117361e-01, 1.75696799e+00, -1.25458253e+00],
		       [ -3.26854147e+00, 7.79945128e-01, -1.36375334e+00, -3.82706408e-01, 1.56292518e+00, 2.67137349e+00, 2.56889944e-02],
		       [ -1.00159690e+01, 1.00300063e+01, -1.16777372e+01, -2.82209911e+00, 1.70516447e+01, 7.98057646e+00, -2.64156438e+00],
		       [  2.36183054e+00, -9.62613704e-01, -5.05346870e-01, 1.31643268e+00, -1.23409504e+00, -4.70267839e-01, 1.14960378e-02],
		       [  1.20585832e+01, -8.96346054e+00, -1.23770661e+00, -8.73966164e+00, 1.11322299e+01, -7.48222977e+00, 7.96615321e-01],
		       [ -2.58579721e+00, 2.35002335e+00, 9.47321990e-01, -2.18293524e+00, 1.27813101e+00, 4.77519482e-02, -1.71859841e-01],
		       [ -3.56463270e-01, 1.46427062e+00, -9.09139431e-01, 4.29077087e+00, -3.51564656e+00, -1.03932241e+00, 1.05852845e-01],
		       [  4.40008115e+00, -3.82056563e+00, -2.37201422e+00, 3.27211050e+00, -1.74829012e-01, -1.65964185e+00, 2.75989792e-02],
		       [  1.03059314e+01, -4.64676474e+00, 1.87951386e+01, -7.46122015e+00, -1.01158257e+00, -1.07306956e+01, -1.28636140e+00],
		       [ -6.40313670e+00, -1.45941740e+00, 2.81970954e-01, -3.56644567e+00, 7.42638874e+00, 4.11764870e+00, -2.57496756e-02],
		       [  2.81578406e+00, -3.58360064e+00, -4.02496662e+00, 4.93810315e+00, 1.40954656e+00, -1.63265823e+00, -2.19087243e-02],
		       [  5.80503233e+00, -5.22380287e+00, -8.11440894e+00, 1.21754251e+01, -9.36294441e+00, 8.60525453e-01, 1.13491105e+00],
		       [  1.17512410e+01, 9.06783871e+00, -1.09276788e+01, -2.78611222e+00, -3.09594025e+00, 2.48971850e+00, -1.59023658e+00],
		       [  1.59853145e+00, -2.32311956e-01, -9.79092458e-01, 2.04118346e+00, -1.68156918e+00, -4.44760258e-01, -2.69098720e-02],
		       [  6.93443813e+00, 4.18076176e+00, 2.61017565e+00, -1.24386117e+01, -2.32253719e+00, -1.66454745e+00, 8.43719060e-01],
		       [  4.18943835e-01, 8.35608641e-01, 5.39244875e-02, 1.23237457e+00, -1.76949588e-02, 2.66743070e-01, -6.38449300e-01],
		       [ -1.49621116e+00, 3.37301347e+00, 5.95924921e+00, -4.96747475e+00, 4.44052015e-01, -1.76747038e+00, -3.52037562e-01],
		       [ -3.22434630e+00, 6.67874117e+00, -5.17664076e+00, -1.11304366e+01, 1.90183538e+01, -2.23094012e-01, -1.39323168e+00],
		       [ -1.55751515e+01, 1.75240637e+01, 3.85824362e+00, -9.57409582e+00, -9.19110140e-01, 8.83590672e+00, -1.18697719e+00],
		       [ -2.30631789e+00, 1.32475113e+01, -3.28478274e+00, -1.17781935e+01, -8.72797667e+00, 1.29110542e+01, 1.83004201e-01],
		       [ -9.22389317e-01, 1.72115766e+00, 1.18939250e+00, 2.56190072e-01, 3.19309249e-01, 1.29253301e+00, -1.12629092e+00],
		       [  4.48912381e+00, -5.82776482e+00, 6.52989325e+00, -9.72006728e+00, 3.66653713e+00, -3.43649582e-01, 1.67782080e-01],
		       [  1.89822228e+00, 8.56472305e+00, -9.71179735e+00, 6.21868356e-02, 8.54414398e+00, -6.00472589e+00, -8.61155876e-01],
		       [  1.16744472e+00, -3.66208564e-02, -2.15082472e-01, 7.84952152e-01, -2.17937778e-01, -9.91810609e-02, -1.15014096e-01],
		       [ -3.25124494e+00, 3.15849002e+00, 1.19358255e+00, -9.52334872e-01, -1.72860434e+00, 1.86580622e+00, -7.53108850e-02],
		       [  5.46184082e+00, 4.82224700e-01, -8.92907469e+00, 1.39145578e+01, -8.26199805e+00, -5.51409988e+00, 8.19954542e-01],
		       [ -3.76993788e+00, 2.01337094e+00, -1.56563718e-01, -2.18172351e+00, 2.90395889e+00, 1.35559492e+00, -5.86605840e-02],
		       [  7.07957369e-01, 4.30642503e-01, 4.78243344e-01, 6.33275670e-01, 1.28536122e-01, 4.75192427e-01, -7.44735541e-01]]),
			np.array([[ -1.01326569, 8.65834074, -8.4516781 , -10.33925623, -4.33328595, -1.35420434, -3.38529544, -10.16567475, -1.20898885, 7.59767855, -1.32997937, 3.38869378, -3.12050049, -5.74235272, 2.43528416, -1.58423753, -5.33098533, -6.74410945, 0.2728549 , -8.32157272, -0.64044207, 3.19363571, 2.3853336 , 1.02658616, -10.32618872, -0.91112015, -1.88540577, -9.86088593, -0.82450014, -2.78470577, 9.74321016, -2.72405856, -0.9453964 , -0.52567052],
		       [ -0.58741152, -3.79000291, 1.67379945, 15.03201154, -6.16922758, -1.78571359, -1.28713933, 14.07333565, -0.71953874, 1.74636161, -1.29280794, 1.18421492, -4.11705402, -3.24345217, -3.01630562, -4.76140717, 6.98888052, 8.31870005, -0.36691053, 7.52916953, -0.02103025, -2.9806681 , -6.47592012, -3.02022041, 9.24081967, -1.1599826 , 3.94155488, 2.18291277, -0.60965018, -4.23805654, -2.05644823, -2.37515646, -0.13559931, -5.97921339],
		       [ -1.27145589, -9.1843648 , -8.38404279, -7.22023444, -6.4782502 , 0.13493784, 0.03677718, -3.00544361, -2.47687272, -7.79605029, -3.13682822, -2.95998567, 0.58728825, 13.69371806, -7.94813847, -0.71675731, -6.96679275, -6.5822005 , -2.58252759, -1.99551509, -1.22579929, -4.66759628, -6.73598451, -12.21085789, 5.06429733, -0.09836107, -7.61656971, 10.7874057 , -1.38898417, 0.8901211 , -0.7670809 , -3.94773808, -1.31162517, 12.3208654 ],
		       [ -0.12199234, -10.19219712, 8.06935235, 6.9182037 , 2.30406498, 0.24799988, -3.37224594, -3.10677015, -0.02090579, -8.85714068, 0.89119597, -3.21427397, 3.22807991, -12.88817591, -2.60296851, 3.22849161, -6.24018907, 12.64210081, -0.83880417, 1.36770577, -0.86057057, 1.3002273 , 8.33254584, 8.61110381, -5.88632128, -0.19032465, -10.66967749, -5.49616384, -0.38647148, 2.19894426, -6.6359804 , -0.13424704, -0.12125402, -8.02089844]])]
	
	