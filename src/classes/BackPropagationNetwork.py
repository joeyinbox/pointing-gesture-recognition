#! /usr/bin/python
import numpy as np


# Transfer sigmoid function
def sgm(x, derivative=False):
	if not derivative:
		return 1 / (1+np.exp(-x))
	else:
		out = sgm(x)
		return out*(1.0-out)

def linear(x, derivative=False):
	if not derivative:
		return x
	else:
		return 1.0

def gaussian(x, derivative=False):
	if not derivative:
		return np.exp(-x**2)
	else:
		return -2*x*np.exp(-x**2)

def tanh(x, derivative=False):
	if not derivative:
		return np.tanh(x)
	else:
		return 1.0 - np.tanh(x)**2


class BackPropagationNetwork:
	
	layerCount = 0
	shape = None
	weights = []
	tFuncs = []
	
	def __init__(self, layerSize, layerFunctions=None):
		
		# Layer information
		self.layerCount = len(layerSize)-1
		self.shape = layerSize
		self.weights = []
		
		if layerFunctions is None:
			lFuncs = []
			for i in range(self.layerCount):
				if i == self.layerCount-1:
					lFuncs.append(linear)
				else:
					lFuncs.append(sgm)
		else:
			if len(layerSize) != len(layerFunctions):
				raise ValueError("Incompatible list of transfer functions")
			elif layerFunctions[0] is not None:
				raise ValueError("Input layer cannot have a transfer function")
			else:
				lFuncs = layerFunctions[1:]
		
		self.tFuncs = lFuncs
		
		# Data from last run
		self._layerInput = []
		self._layerOutput = []
		self._previousWeightDelta = []
		
		# Create the weight arrays by pairs of layer neighbours
		for (l1, l2) in zip(layerSize[:-1], layerSize[1:]):
			self.weights.append(np.random.normal(scale=0.1, size=(l2, l1+1)))
			self._previousWeightDelta.append(np.zeros((l2, l1+1)))
	
	def run(self, input):
		
		lnCases = input.shape[0]
		
		# Re-initialise previous intermediate value lists
		self._layerInput = []
		self._layerOutput = []
		
		# Run the network based on the input data
		for index in range(self.layerCount):
			# Determine the layer input to eventually get previous values
			if index == 0:
				layerInput = self.weights[0].dot(np.vstack([input.T, np.ones([1, lnCases])]))
			else:
				layerInput = self.weights[index].dot(np.vstack([self._layerOutput[-1], np.ones([1, lnCases])]))
			
			# Hold the intermediate values for the next iteration
			self._layerInput.append(layerInput)
			self._layerOutput.append(self.tFuncs[index](layerInput))
		
		# Return the last output
		return self._layerOutput[-1].T
	
	# Trains the network for one epoch
	def trainEpoch(self, input, target, trainingRate=0.2, momentum=0.5):
		
		delta = []
		lnCases = input.shape[0]
		
		# Run the network
		self.run(input)
		
		# Calculate the deltas from back to front
		for index in reversed(range(self.layerCount)):
			if index == self.layerCount-1:
				# Compare to the target values
				output_delta = self._layerOutput[index]-target.T
				error = np.sum(output_delta**2)
				delta.append(output_delta*self.tFuncs[index](self._layerInput[index], True))
			else:
				# Compare to the following layer's delta
				delta_pullback = self.weights[index+1].T.dot(delta[-1])
				delta.append(delta_pullback[:-1, :]*self.tFuncs[index](self._layerInput[index], True))
		
		# Compute weight deltas
		for index in range(self.layerCount):
			delta_index = self.layerCount-1-index
			
			if index == 0:
				layerOutput = np.vstack([input.T, np.ones([1, lnCases])])
			else:
				layerOutput = np.vstack([self._layerOutput[index-1], np.ones([1, self._layerOutput[index-1].shape[1]])])
			
			currentWeightDelta = np.sum(\
								 layerOutput[None, :, :].transpose(2, 0, 1)*delta[delta_index][None, :, :].transpose(2, 1, 0)\
								 , axis=0)
			
			weightDelta = trainingRate*currentWeightDelta + momentum*self._previousWeightDelta[index]
			
			self.weights[index] -= weightDelta
			self._previousWeightDelta[index] = weightDelta
		
		return error
	
	# Get the weights
	def getWeights(self):
		return self.weights
	
	def setWeights(self, weights):
		self.weights = weights