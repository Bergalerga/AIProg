#!/usr/bin/env python
# -*- coding: utf-8 -*-

import theano
import theano.tensor as T
import theano.tensor.nnet as Tann
import numpy as np
#import matplotlib.pyplot as plt
import theano.tensor.nnet as Tann
import basics.mnist_basics as Mnist
#import grapher as graph
#import graphviz # Needed for the import of pydot
#import pydot # for printing out theano function graphs to a file

class ANN(object):
	'''

	'''


	def __init__(self):
		'''

		'''
		print("Theano")
		
	def blind_test(feature_sets):
		'''
		Takes a 2d-array as input, corresponding to the raw data images. Each element is an
		integer in range(0, 255).
		Returns a flat list of labels, corresponding to the number read by ANN.
		'''

	def train(training_set):
		'''

		'''
		pass

	def build_ann(self, nb = 784, nh = 2, learning_rate = 0.1):
		w1 = theano.shared(np.random.uniform(-.1,.1,size=(nb,nh)))
		w2 = theano.shared(np.random.uniform(-.1,.1,size=(nh,nb)))
		input = T.dvector('input')
		b1 = theano.shared(np.random.uniform(-.1,.1,size=nh))
		b2 = theano.shared(np.random.uniform(-.1,.1,size=nb))
		x1 = Tann.sigmoid(T.dot(input,w1) + b1)
		x2 = Tann.sigmoid(T.dot(x1,w2) + b2)
		error = T.sum((input - x2)**2)
		params = [w1,b1,w2,b2]
		gradients = T.grad(error,params)
		backprop_acts = [(p, p - learning_rate*g) for p,g in zip(params,gradients)]
		self.predictor = theano.function([input],[x2,x1])
		self.trainer = theano.function([input],error,updates=backprop_acts)

	def do_training(self, epochs = 1, test_interval = None, cases = None):
		errors = []
		if test_interval:
			self.avg_vector_distances = []
		for i in range(epochs):
			error = 0
			print("Start training")
			for c in cases[0]:
				#Vet ikke hva som skal inn i trainer funksjonen
				return
				error += self.trainer(c)
			errors.append(error)
			if test_interval:
				self.consider_interim_test(i,test_interval)	

	def do_testing(self,scatter=True):
		hidden_activations = []
		for c in self.cases:
			_, hact = self.predictor(c)
			hidden_activations.append(hact)
		if scatter: graph.simple_scatter(hidden_activations,radius=8)
		return hidden_activation

if __name__ == "__main__":
	cases = Mnist.load_all_flat_cases()
	#cases[0]: 2d list of all the test cases/images
	#cases[1]: 1d list of all the labels
	ann = ANN()
	ann.build_ann()
	ann.do_training(cases = cases)