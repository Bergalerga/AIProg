from mnist_basics import *
from time import time
import theano
import numpy as np
import theano.tensor as T
import theano.tensor.nnet as Tann


class ANN():
    '''
    nb = # bits, nh = # hidden nodes (in the single hidden layer)
    lr = learning rate
    '''


    def __init__(self, number_of_training_images, ann_type = None, nb=784, nh=700, lr=0.001, custom = False, layer_list = None):
        '''
        Initializes by loading the images and building the neural network structure.
        '''
        self.images, self.labels = gen_x_flat_cases(number_of_training_images)
        self.lrate = lr
        if custom:
            self.build_custom_ann(layer_list, ann_type)
        if ann_type == "rlu":
            self.build_rectified_linear_ann(nb, nh)
        elif ann_type == "sigmoid":
            self.build_sigmoid_ann(nb, nh)
        elif ann_type == "ht":
            self.build_hyperbolic_tangent_ann(nb, nh)
        elif ann_type =="sigmoid2":
            self.build_sigmoid2_ann(nb, nh, 600)
        elif ann_type == "rlu2":
            self.build_rectified_linear2_ann(nb, nh, 700)

    def build_rectified_linear_ann(self, nb, nh):
        '''
        Builds a neural network, using rectified linear units as the activation function.
        '''
        print("Building rectified linear ann")
        w1 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nb,nh)))
        w2 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nh,10)))
        input = T.dvector('input')
        target = T.wvector('target')
        x1 = T.switch(T.dot(input,w1) > 0, T.dot(input,w1), 0)
        x2 = T.switch(T.dot(x1,w2) > 0, T.dot(x1,w2), 0)
        error = T.sum(pow((target - x2), 2))
        params = [w1, w2]
        gradients = T.grad(error, params)
        backprops = [(p, p - self.lrate*g) for p,g in zip(params,gradients)]

        self.trainer = theano.function(inputs=[input, target], outputs=error, updates=backprops, allow_input_downcast=True)
        self.predictor = theano.function(inputs=[input], outputs=x2, allow_input_downcast=True)

    def build_rectified_linear2_ann(self, nb, nh, nh2):
        '''
        Builds a neural network, using rectified linear units 2 as the activation function.
        '''
        print("Building rectified linear ann")
        w1 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nb,nh)))
        w2 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nh,nh2)))
        w3 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nh2, 10)))
        input = T.dvector('input')
        target = T.wvector('target')
        x1 = T.switch(T.dot(input,w1) > 0, T.dot(input,w1), 0)
        x2 = T.switch(T.dot(x1,w2) > 0, T.dot(x1,w2), 0)
        x3 = T.switch(T.dot(x2, w3) > 0, T.dot(x2, w3), 0)
        error = T.sum(pow((target - x3), 2))
        params = [w1, w2, w3]
        gradients = T.grad(error, params)
        backprops = [(p, p - self.lrate*g) for p,g in zip(params,gradients)]

        self.trainer = theano.function(inputs=[input, target], outputs=error, updates=backprops, allow_input_downcast=True)
        self.predictor = theano.function(inputs=[input], outputs=x3, allow_input_downcast=True)
    
    
    def build_sigmoid_ann(self,nb,nh):
        '''
        Builds a neural network, using sigmoids as the activation function.
        '''
        print("Building sigmoid ann")
        w1 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nb,nh)))
        w2 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nh,10)))
        input = T.dvector('input')
        target = T.wvector('target')
        x1 = Tann.sigmoid(T.dot(input,w1))
        x2 = Tann.sigmoid(T.dot(x1,w2))
        error = T.sum(pow((target - x2), 2))
        params = [w1, w2]
        gradients = T.grad(error, params)
        backprop_acts = [(p, p - self.lrate*g) for p,g in zip(params,gradients)]

        self.trainer = theano.function(inputs=[input, target], outputs=error, updates=backprop_acts, allow_input_downcast=True)
        self.predictor = theano.function(inputs=[input], outputs=x2, allow_input_downcast=True)

    def build_sigmoid2_ann(self, nb, nh, nh2):
        '''
        Builds a neural network, using sigmoids as the activation function.
        '''
        print("Building sigmoid 2 ann")
        w1 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nb,nh)))
        w2 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nh,nh2)))
        w3 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nh2,10)))
        input = T.dvector('input')
        target = T.wvector('target')
        x1 = Tann.sigmoid(T.dot(input,w1))
        x2 = Tann.sigmoid(T.dot(x1, w2))
        x3 = Tann.sigmoid(T.dot(x2, w3))
        error = T.sum(pow((target - x3), 2))
        params = [w1, w2, w3]
        gradients = T.grad(error, params)
        backprop_acts = [(p, p - self.lrate*g) for p,g in zip(params,gradients)]

        self.trainer = theano.function(inputs=[input, target], outputs=error, updates=backprop_acts, allow_input_downcast=True)
        self.predictor = theano.function(inputs=[input], outputs=x3, allow_input_downcast=True)

    def build_hyperbolic_tangent_ann(self,nb,nh):
        '''
        Builds a neural network, using hyperbolic tangent as the activation function.
        '''
        print("Building hyperbolic tangent ann")
        w1 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nb,nh)))
        w2 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nh,10)))
        input = T.dvector('input')
        target = T.wvector('target')
        x1 = T.tanh(T.dot(input,w1))
        x2 = T.tanh(T.dot(x1,w2))
        error = T.sum(pow((target - x2), 2))
        params = [w1, w2]
        gradients = T.grad(error, params)
        backprop_acts = [(p, p - self.lrate*g) for p,g in zip(params,gradients)]

        self.trainer = theano.function(inputs=[input, target], outputs=error, updates=backprop_acts, allow_input_downcast=True)
        self.predictor = theano.function(inputs=[input], outputs=[x2], allow_input_downcast=True)

    def do_training(self, epochs=1, test_interval=None, errors=[]):
        '''

        '''
        for i in range(epochs):
            print("epoch: ", i)
            error = 0
            for j in range(len(self.images)):
                if j % 1000 == 0:
                    print(str(float(round((j/len((self.images)) * 100)))) + "% complete")
                tar = [0] * 10
                tar[self.labels[j]] = 1
                error += self.trainer(self.images[j], tar)
            errors.append(error)
        return errors

    def do_testing(self,scatter=True, blind_test_images=None):
        '''

        '''
        if not blind_test_images:
            self.test_images, self.test_labels = gen_x_flat_cases(100, type="testing")
            self.preprosessing(self.test_images)
        else:
            self.test_images = blind_test_images
            self.test_labels = None
        hidden_activations = []
        for c in self.test_images:
            end = self.predictor(c)
            hidden_activations.append(end)
        self.check_result(hidden_activations)
        return self.test_labels, hidden_activations

    def blind_test(self, images):
        '''

        '''
        #Raw images is a list with sublist of raw_images
        self.preprosessing(images)
        raw_results = self.do_testing(blind_test_images=images)
        results = []
        for i in range(len(raw_results)):
            highest_value = int(np.where(raw_results[i] == max(raw_results[i]))[0][0])
            results.append(highest_value)
        #Returns a list with the classifications of the images
        return results

    def preprosessing(self, feature_sets):
        '''

        '''
        #Scales images to have values between 0.0 and 1.0 instead of 0 and 255
        for image in range(len(feature_sets)):
            for value in range(len(feature_sets[image])):
                feature_sets[image][value] = feature_sets[image][value]/float(255)

    def check_result(self, result):
        '''

        '''
        count = 0
        for i in range(len(self.test_labels)):
            b = int(self.test_labels[i]) == np.argmax(result[i])# == max(result[i]))[0][0])
            if b:
                count += 1
        print("statistics:", (count/float(len(self.test_labels))) * 100)

    def build_custom_ann(self, layer_list, ann_type, nb = 784):
        '''

        '''
        layer_list = [nb] + layer_list
        input = T.dvector('input')
        target = T.wvector('target')
        w_list = []
        b_list = []
        x_list = []
        
        gradients = T.grad(error, params)
        backprops = [(p, p - self.lrate*g) for p,g in zip(params,gradients)]

        self.trainer = theano.function(inputs=[input, target], outputs=error, updates=backprops, allow_input_downcast=True)
        self.predictor = theano.function(inputs=[input], outputs=x_list[-1], allow_input_downcast=True)


def start():
    '''

    '''
    number_of_training_images = 6000
    number_of_testing_images = 1000
    custom = input("Custom layers: Y/N")
    print("---------")
    if custom == "N" or custom == "n":
        ann_type = input("Options: sigmoid, sigmoid2, rlu, ht, rlu2: ")
        image_recog = ANN(number_of_training_images, ann_type)
        image_recog.preprosessing(image_recog.images)
    else:
        layerlist = input("Enter layer list: ")
        layerlist = layerlist.split()
        for x in range(len(layerlist)):
            layerlist[x] = int(layerlist[x])
        image_recog = ANN(number_of_training_images, custom = True, layer_list = layerlist)
        image_recog.preprosessing(image_recog.images)

    errors = []
    print("Successfully loaded the images and built the neural network")
    print("----------")
    while True:
        num = input(" 1: Train \n 2: Test \n 3: Blind test \n 4: Restart \n")
        if int(num) == 1:
            errors = image_recog.do_training(epochs=1, errors=errors)
        elif int(num) == 2:
            test_labels, result = image_recog.do_testing(number_of_testing_images)
        elif int(num) == 3:
            results = image_recog.blind_test(images)
        elif int(num) == 4:
            start()
        else:
            errors = image_recog.do_training(epochs=int(action), errors=errors)

if __name__ == "__main__":
    start()
    
