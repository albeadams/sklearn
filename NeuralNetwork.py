
import numpy as np


class NeuralNetwork(object):

	def __init__(self, *args, **kwards):
		pass

	def feedforward(self, a):
		# Return the output of the network for an input vector a
		for b, w in zip(self.biases, self.weights):
			a = sigmoid(np.dot(w,a) + b)
		return a