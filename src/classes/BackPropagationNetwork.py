#! /usr/bin/python
import numpy as np



# Transfer sigmoid function
# 
# @param	x					Numeric value to transform
# @param	derivative			Flag to use an alternative formula
# @return	float				Transformed value to use as a mean to update weights
def sgm(x, derivative=False):
	if not derivative:
		return 1 / (1+np.exp(-x))
	else:
		out = sgm(x)
		return out*(1.0-out)


# Transfer linear function
# 
# @param	x					Numeric value to transform
# @param	derivative			Flag to use an alternative formula
# @return	float				Transformed value to use as a mean to update weights
def linear(x, derivative=False):
	if not derivative:
		return float(x)
	else:
		return 1.0


# Transfer gaussian function
# 
# @param	x					Numeric value to transform
# @param	derivative			Flag to use an alternative formula
# @return	float				Transformed value to use as a mean to update weights
def gaussian(x, derivative=False):
	if not derivative:
		return np.exp(-x**2)
	else:
		return -2*x*np.exp(-x**2)


# Transfer hyperbolic tangent function
# 
# @param	x					Numeric value to transform
# @param	derivative			Flag to use an alternative formula
# @return	float				Transformed value to use as a mean to update weights
def tanh(x, derivative=False):
	if not derivative:
		return np.tanh(x)
	else:
		return 1.0 - np.tanh(x)**2


# Definition of the BackPropagationNetwork class
class BackPropagationNetwork:
	
	layerCount = 0				# Number of layers used within the network
	shape = None				# Size of the layers used within the network
	weights = []				# Actual weights of the network
	tFuncs = []					# Array of transfer functions chosen for the network
	
	
	# Constructor of the BackPropagationNetwork class
	# 
	# @param	layerSize			Size of the layers used within the network
	# @param	layerFunctions		Array of transfer functions chosen for the network
	# @return	None
	def __init__(self, layerSize, layerFunctions=None):
		
		# Layer informations
		self.layerCount = len(layerSize)-1
		self.shape = layerSize
		self.weights = []
		
		# Attribute transfer functions to the layers accordingly
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
		
		# Will hold data informations from the last run
		self._layerInput = []
		self._layerOutput = []
		self._previousWeightDelta = []
		
		# Create the weight arrays by pairs of layer neighbours
		for (l1, l2) in zip(layerSize[:-1], layerSize[1:]):
			self.weights.append(np.random.normal(scale=0.1, size=(l2, l1+1)))
			self._previousWeightDelta.append(np.zeros((l2, l1+1)))
	
	
	# Run the network based on the input data
	# 
	# @param	input				Input features
	# @return	array				Last output
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
	# 
	# @param	input				Input features
	# @param	target				Target values to match as closely as possible
	# @param	learningRate		Learning rate value to influence weights and bias changes
	# @param	momentum			Momentum value to update the next weights by adding a defined fraction of the previous one
		# @return	float				Error value between the current output and the target
	def trainEpoch(self, input, target, learningRate=0.2, momentum=0.5):
		
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
			
			currentWeightDelta = np.sum(layerOutput[None, :, :].transpose(2, 0, 1)*delta[delta_index][None, :, :].transpose(2, 1, 0), axis=0)
			
			weightDelta = learningRate*currentWeightDelta + momentum*self._previousWeightDelta[index]
			
			self.weights[index] -= weightDelta
			self._previousWeightDelta[index] = weightDelta
		
		return error
	
	
	# Returns the current weights of the network
	# 
	# @return	array				Array of the actual weights
	def getWeights(self):
		return self.weights
	
	
	# Replace the current weights of the network by new ones
	# 
	# @param	weights				Array of weights to use within the network
	# @return	None
	def setWeights(self, weights):
		self.weights = weights