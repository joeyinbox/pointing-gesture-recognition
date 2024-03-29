#! /usr/bin/python -W ignore::FutureWarning
from classes.BackPropagationNetwork import *
import numpy as np
import sys
from copy import deepcopy
import signal
import heapq



# Definition of the BPNHandler class
class BPNHandler:
	
	# Hold eventual results
	resultTestingScore, resultTrainingScore, resultInitialWeights, resultWeights, resultConfig, resultIteration = [], [], [], [], [], []
	
	
	# Constructor of the BPNHandler class
	# 
	# @param	live				Flag to initialise the right network in case of a live utilisation
	# @param	features			Number of features that will be handled by the network
	# @param	hiddenLayers		Number of neurones in the hidden layer of the network
	# @param	output				Number of neurones in the output layer of the network
	# @return	None
	def __init__(self, live=False, features=6, hiddenLayers=20, output=12):
		# Define the functions that will be used
		self.lFuncs = [None, gaussian, sgm]
		
		# Initialise the right network
		if live:
			self.bpnValidating = BackPropagationNetwork((features, hiddenLayers, output), self.lFuncs)
			self.bpnValidating.setWeights(self.getWeights(best=True))
		else:
			self.bpnTesting = BackPropagationNetwork((features, hiddenLayers, output), self.lFuncs)
	
	
	# Check a set of feature values against the network to detect a pointing gesture
	# 
	# @param	features			Input values to input the network
	# @return	array				Recognition result and corresponding hand identifier
	def check(self, features):
		lvInput = np.array(features)
		lvOutput = self.bpnValidating.run(lvInput)
		
		# The output will be an array whose first element indicates if a pointing gesture is recognised
		# In case of a pointing gesture, the second value represent the left (0) or right (1) hand
		result = [False,0]
		
		# Possibility to get an unified result for several feature inputs
		for i in range(lvInput.shape[0]):
			# If a gesture is recognised:
			if lvOutput[i][np.argmax(lvOutput[i])] > 0.5:
				result = [True, i]
		
		return result
	
	
	# Train the network
	# 
	# @param	trainingInput		2D Array of input feature values from the training set
	# @param	trainingTarget		2D Array of targeted values from the training set
	# @param	testingInput		2D Array of input feature values from the testing set
	# @param	testingTarget		2D Array of targeted values from the testing set
	# @param	learningRate		Learning rate value to influence weights and bias changes
	# @param	momentum			Momentum value to update the next weights by adding a defined fraction of the previous one
	# @param	optimal				Flag to train the network by iteratively changing its configuration
	# @return	None
	def run(self, trainingInput, trainingTarget, testingInput, testingTarget, learningRate=0.05, momentum=0.1, optimal=False):
		# store the original SIGINT handler to display the results if interrupted
		original_sigint = signal.getsignal(signal.SIGINT)
		signal.signal(signal.SIGINT, self.displayResults)
		
		# Get the inputs and outputs
		lvTrainingInputOriginal = np.array(trainingInput)
		lvTrainingTargetOriginal = np.array(trainingTarget)
		
		lvTestingInputOriginal = np.array(testingInput)
		lvTestingTargetOriginal = np.array(testingTarget)
		
		
		# For research purpose, the number of hidden layers will be dynamic
		ran = np.arange(2, 50)
		
		# Loop the number of hidden layers
		for hidden in ran:
			
			
			# For optimal research purpose, the learningRate can be dynamic
			if optimal:
				rate = np.arange(learningRate, 0.1, 0.05)
			else:
				rate = [learningRate]
			
			# Loop the number of Learning rates
			for locallearningRate in rate:
				
				
				# For optimal research purpose, the momentum can be dynamic
				if optimal:
					mom = np.arange(momentum, 0.2, 0.1)
				else:
					mom = [momentum]
			
				# Loop the number of momentums
				for localMomentum in mom:
					
					
					# For optimal research purpose, the network can be ran several times
					if optimal:
						repeatition = range(3)
					else:
						repeatition = [1]
					
					# Loop the number of repeatitions
					for repeat in repeatition:
						
					
						print("{0} hidden layers with a Learning rate of {1} and a momentum of {2}".format(hidden, locallearningRate, localMomentum))
			        	
			        	
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
							err = bpn.trainEpoch(lvTrainingInput, lvTrainingTarget, locallearningRate, localMomentum)
							
				    	
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
								if "{0:0.6f}".format(error) == "{0:0.6f}".format(previous):
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
						print("\nStopped at Iteration {0}\tError: {1:0.6f}  \t{2:0.6f}".format(i, err, error))
			        	
			        	
						# Keep this result if it is good
						self.addResult(bestScore, bestScoreTraining, initialWeights, bestIteration, bestWeights, [hidden, locallearningRate, localMomentum])
			        	
						print "The best weights for a score of {0:0.6f} at iteration {1} while training was at {2:0.6f}\n".format(bestScore, bestIteration, bestScoreTraining)
		
		# If all loops have finished, display the results (any interuption during the process will call this function anyways...)
		self.displayResults(None, None)
	
	
	# Add a result to the result array in order to display the top later
	# 
	# @param	bestScore			Best score over the testing set
	# @param	bestScoreTraining	Best score over the training set
	# @param	initialWeights		Array of the initial weights as a mean to be able to reproduce the same training
	# @param	bestIteration		Number of epochs necessary to get such results
	# @param	bestWeights			Array of the best weights found
	# @param	config				Configuration of the training
	# @return	None
	def addResult(self, bestScore, bestScoreTraining, initialWeights, bestIteration, bestWeights, config):
		# Fill an array to get the top 30 scores
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
			
			# And eventually replace it by the new one
			if bestScore < largest[0][0]:
				self.resultTestingScore[largest[0][1]] = bestScore
				self.resultTrainingScore[largest[0][1]] = bestScoreTraining
				self.resultInitialWeights[largest[0][1]] = initialWeights
				self.resultIteration[largest[0][1]] = bestIteration
				self.resultWeights[largest[0][1]] = bestWeights
				self.resultConfig[largest[0][1]] = config
	
	
	# Constructor of the BPNHandler class
	# 
	# @param	signum				Parameter returned by the signal handler
	# @param	frame				Parameter returned by the signal handler
	# @return	None
	def displayResults(self, signum, frame):
		print "\n\n"
		
		# Retrieve the 30 best results
		best = heapq.nsmallest(30, ((k, i) for i, k in enumerate(self.resultTestingScore)))
		
		# Display their informations
		i = 1
		for b in best:
			print "\n###############"
			print "#{0} Result:".format(i)
			i+=1
			
			print "{0} Hidden layers, \tLearning rate: {1}, \tMomentum: {2}".format(self.resultConfig[b[1]][0], self.resultConfig[b[1]][1], self.resultConfig[b[1]][2])
			print "The best weights were for a score of {0:0.6f} at iteration {1} while training was at {2:0.6f}:".format(b[0], self.resultIteration[b[1]], self.resultTrainingScore[b[1]])
			print self.resultWeights[b[1]]
			
			print "\nInitial weights:"
			print self.resultInitialWeights[b[1]]
		sys.exit(1)
	
	
	# Return an array of the weights for a restrained training
	# 
	# @param	None
	# @return	array				Weights for a restrained training
	def getRestrainedWeights(self):
		# 6 features
		# 4 outputs
		# 33 hidden layers
		# Learning rate: 0.05
		# Momentum: 0.1
		# Testing score: 3.42
		# Training score: 2.05
		# Validating score: 85.6 %
		
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
	
	
	# Returns the weights chosen by this porject so far
	# 
	# @param	initial				Flag to retrieve the initial weights as a mean to re-train the network
	# @param	best				Flag to retrieve the best weights in order to detect pointing gestures
	# @return	array				Chosen weights
	def getWeights(self, initial=False, best=True):
		# 6 features
		# 12 outputs
		# 20 hidden layers
		# Learning rate: 0.05
		# Momentum: 0.1
		
		# Testing error: 9.973816
		# Training error: 3.018302
		# Epochs: 247500
		
		# Testing score: 88.10 %
		# Training score: 98.50 %
		# Validating score: 88.10 %
		
		
		
		
		# Initial weights:
		if initial:
			return [np.array([[  1.94275535e+00,  -4.48771954e+00,   1.44591605e+01,  -1.83353731e+01,   4.14439961e+00,   4.94640574e+00,  -6.63135804e-01],
		       [ -3.08975392e+00,   3.52361778e+00,   1.12590780e+00,  -8.34642790e+00,   9.94807296e+00,  -1.09870044e+00,  -7.19630709e-01],
		       [ -3.52007158e+00,  -8.78013729e+00,   1.60949420e+01,  -1.86416121e+01,   9.02333575e+00,   8.44489631e+00,  -4.56354486e-01],
		       [  4.50563019e+00,  -5.59981097e+00,  -1.11107938e+00,  -1.30175559e+00,   2.03276096e+00,   3.51130602e+00,  -6.44612499e-01],
		       [ -1.06866624e+01,  -1.85310731e+00,  -7.06767252e-01,   2.11320073e+00,   1.87226651e+00,   4.13448472e+00,   1.14037046e+00],
		       [ -2.81816710e+00,   1.97111443e+00,   1.22071803e+00,   4.76380131e+00,  -7.39127999e+00,   4.68082494e-01,   3.93130001e-01],
		       [  2.06012135e+00,   1.22746066e+00,   1.05220465e-01,  -2.20492106e+01,   1.38405201e+01,   8.43775748e+00,  -1.05722409e+00],
		       [ -1.65419892e+00,   1.13887609e+00,   2.22096435e-01,  -1.23847381e+00,  -2.41624900e+00,   3.76817827e+00,  -2.96081256e-02],
		       [  8.80448110e+00,   1.63266283e-01,   7.20371556e+00,  -1.06202419e+01,  -3.22025124e-01,  -7.51060461e+00,   7.65896914e-01],
		       [ -1.40922732e+01,   2.46846448e+01,   6.53083761e-01,  -1.31633655e+01,   1.58783027e+01,  -1.93910343e+00,  -2.90619092e+00],
		       [ -1.02762716e+01,   7.72032915e+00,  -4.30492245e+00,   5.59156286e+00,  -3.49042811e+00,   5.16267696e+00,  -9.18569499e-03],
		       [ -5.66017101e+00,  -3.55002070e+00,  -2.40665610e-01,   4.58894118e+00,   2.42072817e-01,   3.47957528e+00,   2.53847741e-01],
		       [  4.53283283e+00,  -6.24625271e+00,   3.52416317e+00,  -1.54748953e+01,   1.43911104e+01,   5.25707117e-01,  -2.76822709e-01],
		       [ -3.94198983e-01,   7.09714170e-01,   1.68391110e+00,  -8.10386572e-01,   1.18781080e-01,  -1.59543781e+00,  -4.46917748e-02],
		       [ -7.95337917e+00,   2.24504385e+00,  -1.41159609e+01,   9.65320604e+00,  -1.09598935e+01,   1.37261535e+01,   1.88371836e+00],
		       [  5.67904363e+00,   5.04170826e+00,  -9.68048339e+00,   3.33137642e+00,   3.71253643e+00,  -7.41085754e+00,  -8.03438361e-02],
		       [  2.04453579e+01,  -5.94390724e-01,   9.01018805e+00,  -3.12380110e+01,  -7.04299555e-01,  -2.98231531e+00,   1.49756355e+00],
		       [  2.52960326e+00,  -3.28118281e+00,  -1.00610025e+00,   2.62210259e+00,  -7.42515686e-01,  -1.49555462e-01,   9.42621401e-02],
		       [ -5.78807129e+00,   3.09206032e+00,  -1.63024315e+01,   8.10189205e+00,   8.31294896e+00,  -2.37228530e+00,   1.15811291e+00],
		       [ -8.67644629e+00,   1.70064997e+00,   3.79894191e+00,   3.65832610e-02,   1.59602413e+00,   2.90359216e+00,  -3.24913099e-01]]), 
			   np.array([[  4.94476706,   5.16164263,   3.63260249,  -3.06220831,  -3.23790996,  -6.52801598, -10.03647739,  -0.85634592,  -5.0326119 , -10.3537647 ,   6.2443775 ,  -6.04585586,   3.21005412,  -2.30748095,  10.34602853,  -6.26757922,   3.88319795,   1.086484  ,  -2.40679443,  -5.73817959, -11.34489966],
		       [ -3.12210612,   6.56635327,  11.75119457,  -3.86963874,  -8.56603441,  -4.9024078 ,   6.87693174,  -6.39555201,   7.80995827, -10.65223709, -11.4219511 ,  -4.07330897,   3.62628327,  -0.27601461,  -8.48621995,  -7.23646161, -14.18707067,  -6.62831487,  -4.5047404 ,  -9.04857288,  -0.15644641],
		       [  3.5523558 ,   1.66500086,  -9.07740015,  -3.03003066,  -2.2092553 ,  -7.85243466,  -0.71177951,  -6.25558937,  -3.91539065,  -2.88876839, -14.11578646,   3.59062775, -10.38860379,  -0.2671146 ,  -4.3141202 ,   1.34410173,  -3.23165652,  -4.11613272,   7.18932559,  -1.29990426,   2.09898304],
		       [  0.02399916, -12.62552157,   3.66504878,   7.54962238,   9.30669908,  -7.12258414,  -9.8329376 ,  -1.80996825,  -7.58930994,  -7.37754066,   4.24666858,   1.28454766,  -5.14952031,  -3.47778787,  -5.87097681,  -9.32677245,  -3.92562629, -12.27584925,  -6.1420822 ,  -4.65959389,   8.82457236],
		       [  1.71845801,  -1.13696708,  -9.40285813,  -4.20227645,  -9.20460107,  -3.99847175,  -7.93083019,   0.72179458,  -4.61192774,   6.88908494, -14.12609785,  -7.28949615,   5.19511861,  -0.09546833,  -8.08349794,  -6.55073632,  15.83523521,  -4.39261358,  -1.90742264,  -3.81422242,  -3.55511372],
		       [-12.50608156,   3.30466531,   3.3308886 ,  -1.55058198,   1.81155238,  -3.07694991,  -4.97480762,  -9.6576194 ,   6.66736853,   4.95848358,  -3.72945519,   4.22935352,   7.017729  ,  -2.28813737,  -1.86474403,   1.38275332,  -1.85309437,  -3.96410959,  -7.68492867,   2.60370331,  -8.53970646],
		       [ -4.52214808,  -2.02255687,   1.17169359,  10.31640433,  -1.70412579, -10.71503057, -11.00115011,   1.41053495,   3.67243004,  10.43032471,  -6.31381258,  -7.90753208,  -4.82406346,  -2.55218148,   7.3857748 ,  -0.67157228,  -4.66336646,  -1.07068407,  -3.60345116,  -0.69176139,  -2.0303409 ],
		       [  1.48925405,  -8.88234306,  -6.23985246,  -2.36962976,   4.56457454,  -0.04911692,  -8.26599644,  -2.26113297,  -4.63153649,   5.04293953,   4.79648727,   2.16204525, -10.36591461,  -1.56543142,   6.12045456,  11.90732406,  -7.48268783,  -3.99685365,  10.81119913,   1.88132603, -10.42285846],
		       [ -9.72652716,  -3.85255688,  -5.14056142,  -4.41720111,  -5.63185053,   0.26244855,   1.95831209,   0.94622297, -13.26131299, -10.13953184,  -4.60516718,  -6.88631482,  -5.75061926,  -2.44361803, -17.71555622,  -5.46658026,  -3.27829318,  -0.84941543,  -2.18629745,  -5.98450759,   7.85629056],
		       [  3.46696353,  -0.57516321,   8.18887976,  11.04829226,  -2.09314244,  -1.06396456,  -6.64930367,  -5.25670254,   1.3369223 ,  -6.93969804,   2.2305586 ,   4.9693846 ,  -0.52798492,  -1.10809493,  -7.01846302,   3.4995234 ,  -2.82506159,   2.84611319,   0.68016019,  -7.4535741 , -14.75422082],
		       [-11.68277964,  -9.07033723, -11.01763788,  -4.42343477,   3.95963048,   5.80195847,  13.91883614,  -5.90790763,  -4.4288797 ,  -9.29917754,  -2.14455031,  10.82436055, -13.11031231,  -1.31480161,   0.18031514,  -4.11808679,   0.03397454,   2.00660172,  -7.63583487,  10.16589733, -12.10995399],
		       [  3.17026441,  -6.88897933,  -6.20764596,  -3.45306085,  -4.64134281,   7.09948783,  -9.27909255,   0.29270625,   6.83234513,   7.05481567,   5.86392193,  -8.2602333 , -14.0897227 ,  -0.75578102,   9.95981483,  -2.51841251,   0.61959521,  -2.95608121,  -5.70581119,  -5.17077975,  -9.37362685]])]
		
		
		
		# Best weights:
		if best:
			return [np.array([[1.73521170e+00, -5.19216691e+00, 1.53239076e+01, -1.84002767e+01, 3.45816775e+00, 5.70603654e+00, -6.53448666e-01],
				[ -3.31621803e+00, 3.55899391e+00, 1.16623818e+00, -8.57392590e+00, 1.02423802e+01, -8.98492741e-01, -7.48695542e-01],
				[ -3.43008866e+00, -8.77027842e+00, 1.59120599e+01, -1.83238518e+01, 8.80206145e+00, 8.37859364e+00, -4.43140251e-01],
				[  4.50453354e+00, -5.46882263e+00, -1.18987649e+00, -1.44618586e+00, 2.24581893e+00, 3.49636797e+00, -6.70808555e-01],
				[ -1.06179698e+01, -1.76393218e+00, -5.63453816e-01, 2.25522467e+00, 1.98632962e+00, 4.20591723e+00, 9.83195273e-01],
				[ -2.66150395e+00, 1.50748671e+00, 1.15081534e+00, 5.12084511e+00, -7.69581070e+00, 6.01174163e-01, 4.40945625e-01],
				[  1.67905354e+00, 2.49861036e+00, 1.48699620e-02, -2.34692621e+01, 1.50332877e+01, 8.29841447e+00, -1.16550019e+00],
				[ -1.68283966e+00, 1.03477071e+00, 1.55221045e-01, -9.01699419e-01, -2.47012030e+00, 3.63134321e+00, -1.62197576e-02],
				[  8.96458521e+00, 2.55493213e-01, 7.05238251e+00, -1.06492080e+01, -1.90026295e-01, -7.79622980e+00, 7.86295534e-01],
				[ -1.43438026e+01, 2.47328910e+01, 6.67378626e-01, -1.33592771e+01, 1.62315292e+01, -1.78162615e+00, -2.93764192e+00],
				[ -1.05133836e+01, 7.84829356e+00, -4.41960068e+00, 5.77734334e+00, -3.57269648e+00, 5.27905514e+00, -8.20181421e-03],
				[ -5.49592496e+00, -3.67552372e+00, 9.91305565e-02, 4.18338478e+00, 1.34161897e-01, 3.71703095e+00, 2.28215855e-01],
				[  4.54856719e+00, -6.28934314e+00, 3.59946132e+00, -1.55238687e+01, 1.43620731e+01, 5.52577735e-01, -2.76023228e-01],
				[ -4.98543034e-01, 7.68665611e-01, 1.67489462e+00, -2.86611116e-01, -1.35227920e-01, -1.82108342e+00, -4.21197122e-02],
				[ -8.32978749e+00, 2.63368925e+00, -1.46403442e+01, 9.75633062e+00, -1.06998960e+01, 1.38769380e+01, 1.88327826e+00],
				[  5.45232244e+00, 5.27870358e+00, -9.76315297e+00, 3.39941425e+00, 3.65244168e+00, -7.33592091e+00, -8.29649022e-02],
				[  2.17121067e+01, -1.08780863e+00, 8.47287619e+00, -3.13986077e+01, -9.66220484e-01, -3.38241172e+00, 1.64421232e+00],
				[  2.21745251e+00, -3.28886205e+00, -1.04281336e+00, 2.91432340e+00, -1.01100278e+00, 1.40238281e-01, 1.05016051e-01],
				[ -5.71616249e+00, 3.32422638e+00, -1.67631171e+01, 8.10419341e+00, 8.60217144e+00, -2.55166434e+00, 1.16922940e+00],
				[ -8.75374864e+00, 1.56729385e+00, 3.99969396e+00, -3.11183452e-01, 1.81128256e+00, 3.14668157e+00, -3.50081776e-01]]), 
				np.array([[5.72493087e+00, 5.49060304e+00, 4.29635066e+00, -3.06947163e+00, -3.23794860e+00, -7.19182342e+00, -1.02199141e+01, -7.66198471e-01, -5.31382344e+00, -1.08113706e+01, 7.23572070e+00, -6.37591259e+00, 3.81972753e+00, -3.17857085e+00, 1.15498690e+01, -6.56646022e+00, 4.43852286e+00, 8.84547883e-01, -2.28257921e+00, -5.89285389e+00, -1.28831647e+01],
				[ -3.06140678e+00, 7.38490448e+00, 1.30257692e+01, -3.89698831e+00, -8.56627762e+00, -5.05729628e+00, 7.93660215e+00, -7.53796421e+00, 8.53210138e+00, -1.15900978e+01, -1.20138915e+01, -4.63119546e+00, 3.73467189e+00, 5.70085505e-01, -8.59606659e+00, -7.66149653e+00, -1.55827554e+01, -7.22940967e+00, -4.55989685e+00, -1.07001967e+01, -2.27786985e-01],
				[  3.34282323e+00, 1.76703582e+00, -9.73833597e+00, -3.05263638e+00, -2.20924665e+00, -8.62883325e+00, -7.69777189e-01, -7.18304356e+00, -3.97082734e+00, -3.34156047e+00, -1.53538803e+01, 3.63148490e+00, -1.20142129e+01, 4.48391121e-01, -4.55988912e+00, 1.66827966e+00, -3.23172612e+00, -4.71402513e+00, 7.78977328e+00, -1.53581294e+00, 2.33869267e+00],
				[  4.06686794e-01, -1.35599102e+01, 3.84390605e+00, 8.17715835e+00, 9.30519232e+00, -7.36453394e+00, -1.00491565e+01, -2.20962474e+00, -8.69414369e+00, -8.07876283e+00, 4.90490031e+00, 1.69713660e+00, -6.02203596e+00, -4.89284768e+00, -6.25895555e+00, -9.89425183e+00, -3.89376854e+00, -1.35995317e+01, -6.65025370e+00, -4.88445500e+00, 9.79745070e+00],
				[  1.63747159e+00, -1.36122224e+00, -1.01161022e+01, -4.20049106e+00, -9.20460107e+00, -4.37911552e+00, -9.62352995e+00, 1.15580023e+00, -5.05104910e+00, 7.27940704e+00, -1.48523839e+01, -7.63595644e+00, 5.98184470e+00, 1.83630646e-01, -8.19465608e+00, -6.40946603e+00, 1.72989077e+01, -4.44771041e+00, -1.90823497e+00, -4.03857875e+00, -4.03302546e+00],
				[ -1.42904512e+01, 3.54488299e+00, 3.92094008e+00, -1.59524282e+00, 1.81155207e+00, -3.22904660e+00, -5.64703923e+00, -1.03528211e+01, 6.48453810e+00, 5.04860269e+00, -4.19017761e+00, 4.79833062e+00, 7.83796697e+00, -2.78959216e+00, -1.86600119e+00, 1.44659657e+00, -1.95496565e+00, -4.43902299e+00, -8.36065949e+00, 2.97838450e+00, -9.16393364e+00],
				[ -4.77714666e+00, -1.56639783e+00, 1.19292347e+00, 1.07642138e+01, -1.70412581e+00, -1.18963045e+01, -1.10206619e+01, 2.06937654e+00, 4.36287790e+00, 1.17986123e+01, -6.95046078e+00, -7.84208092e+00, -5.28595982e+00, -4.06866746e+00, 7.95486220e+00, -8.70395770e-01, -4.87569700e+00, -1.19923580e+00, -4.12922021e+00, -4.90301929e-01, -2.39452268e+00],
				[  1.67664996e+00, -1.00423331e+01, -6.07563214e+00, -2.20485753e+00, 4.56456252e+00, -3.66951384e-01, -8.53328869e+00, -2.19270498e+00, -4.72430724e+00, 5.55818228e+00, 5.47132080e+00, 2.41998773e+00, -1.06175068e+01, -1.84887362e+00, 6.88405328e+00, 1.25580447e+01, -8.40656966e+00, -4.98741056e+00, 1.19121926e+01, 2.73418380e+00, -1.14210594e+01],
				[ -1.01466675e+01, -4.01419421e+00, -5.65156263e+00, -5.08952172e+00, -5.63673192e+00, 2.46846622e-01, 2.25902304e+00, 1.29197333e+00, -1.44727981e+01, -1.10617656e+01, -5.25671380e+00, -8.22073850e+00, -6.50306538e+00, -2.91099092e+00, -2.05796501e+01, -5.85992249e+00, -3.20940322e+00, -1.38569981e+00, -2.16324807e+00, -6.51827351e+00, 9.05836776e+00],
				[  3.25553997e+00, -1.10005396e+00, 9.14926007e+00, 1.17065925e+01, -2.10430728e+00, -8.21992550e-01, -6.64736094e+00, -6.28561216e+00, 1.45067735e+00, -7.00086858e+00, 2.92080721e+00, 5.36925444e+00, -7.90160567e-01, -1.72568110e+00, -7.04247309e+00, 3.66165848e+00, -2.82507440e+00, 3.45481249e+00, 6.77068115e-01, -8.11733804e+00, -1.52638539e+01],
				[ -1.23080404e+01, -1.06246430e+01, -1.11325614e+01, -4.98225002e+00, 3.95952114e+00, 7.16319973e+00, 1.56754483e+01, -6.56534931e+00, -5.08950529e+00, -9.88422800e+00, -2.53292746e+00, 1.24120679e+01, -1.37260202e+01, -1.47541201e+00, 6.15378453e-01, -4.10116278e+00, -1.45533855e-01, 1.72487042e+00, -8.15633289e+00, 1.12354719e+01, -1.37904204e+01],
				[  3.54670662e+00, -7.50752892e+00, -6.36631343e+00, -3.39381467e+00, -4.64134281e+00, 7.86806273e+00, -1.06608504e+01, 4.31849159e-03, 7.57836754e+00, 7.69403828e+00, 7.09915993e+00, -8.59828176e+00, -1.43742392e+01, -5.85363888e-01, 1.10039138e+01, -2.47805760e+00, 4.49122966e-01, -3.27669879e+00, -5.89958132e+00, -5.47870244e+00, -1.04608037e+01]])]
	
	