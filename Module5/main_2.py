
from mnist_basics import *
from time import time
import theano
import numpy as np
import theano.tensor as T
import theano.tensor.nnet as Tann


class ImageRecog():

    # nb = # bits, nh = # hidden nodes (in the single hidden layer)
    # lr = learning rate

    def __init__(self, nr_of_training_images, nb=28*28, nh=700, lr=0.001, bulk_size=1):
        self.images, self.labels = gen_x_flat_cases(nr_of_training_images)
        self.test_images, self.test_labels = gen_x_flat_cases(nr_of_testing_images, type="testing")
        #self.images, self.labels = gen_flat_cases()
        self.lrate = lr
        self.bulk_size = bulk_size
        self.build_ann(nb, nh)

    def floatX(self, X):
        return np.asarray(X, dtype=theano.config.floatX)

    def build_ann(self,nb,nh):
        w1 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nb, nh)))
        w2 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nh, 10)))
        input = T.fmatrix()
        target = T.fmatrix()
        x1 = Tann.sigmoid(T.dot(input,w1))
        x2 = Tann.sigmoid(T.dot(x1,w2))
        error = T.sum(pow((target - x2), 2))
        params = [w1, w2]
        gradients = T.grad(error, params)
        backprops = self.backprop_acts(params, gradients)

        self.get_x1 = theano.function(inputs=[input, target], outputs=error, allow_input_downcast=True)
        self.trainer = theano.function(inputs=[input, target], outputs=error, updates=backprops, allow_input_downcast=True)
        self.predictor = theano.function(inputs=[input], outputs=x2, allow_input_downcast=True)

    def backprop_acts (self, params, gradients):
        updates = []
        for p, g in zip(params, gradients):
            updates.append((p, p - self.lrate * g))
        return updates

    def do_training(self, epochs=1, test_interval=None, errors=[]):
        starttime = time()
        #graph.start_interactive_mode()
        #if test_interval: self.avg_vector_distances = []
        for i in range(epochs):
            print("epoch: ", i)
            error = 0
            i = 0
            j = self.bulk_size
            while j < len(self.images):
                image_group = self.images[i:j]
                result_group = [[0 for i in range(10)] for i in range(self.bulk_size)]
                for k in range(self.bulk_size):
                    label_index = self.labels[i + k]
                    result_group[k][label_index] = 1
                i += self.bulk_size
                j += self.bulk_size
            #for j in range(len(self.images)):
                if j % (self.bulk_size * 100) == 0:
                    print("image nr: ", j)
                #tar = [0] * 10
                #tar[self.labels[j]] = 1
                #tar = theano.shared(tar)
                #hhh = self.get_x1(image_group, result_group)
                #print("hh")
                error += self.trainer(image_group, result_group)
            print(error)
            print("avg error pr image: " + str(error/j))
            errors.append(error)
        print("Training time: " + str((time()-starttime)) + " sec")
        return errors

    def do_testing(self, nr_of_testing_images=10000, scatter=True, blind_test_images=None):
        if blind_test_images is not None:
            self.test_images = blind_test_images
            self.test_labels = None

        hidden_activations = []
        i = 0
        j = self.bulk_size
        while j < len(self.test_images):
            image_group = self.test_images[i:j]
            i += self.bulk_size
            j += self.bulk_size
            end = self.predictor(image_group)
            for res in end:
                hidden_activations.append(res)
        '''
        for c in self.test_images:
            end = self.predictor(c)
            hidden_activations.append(end)
        '''
        self.check_result(hidden_activations)
        return self.test_labels, hidden_activations

    def blind_test(self, images):
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
        #Scales images to have values between 0.0 and 1.0 instead of 0 and 255
        for image in range(len(feature_sets)):
            for value in range(len(feature_sets[image])):
                feature_sets[image][value] = feature_sets[image][value]/float(255)

    def check_result(self, result):
        count = 0
        for i in range(len(result)):
            #print image_recog.labels[i]
            #print result[i]
            b = int(self.test_labels[i]) == np.argmax(result[i])# == max(result[i]))[0][0])
            #print b
            # print (test_labels[i])
            # print(result[i])
            # print(np.argmax(result[i]))
            # print(b)
            # print ("---")
            if b:
                count += 1
        print("statistics:", (count/float(len(self.test_labels))) * 100)


nr_of_training_images = 60000
nr_of_testing_images = 10000
image_recog = ImageRecog(nr_of_training_images, bulk_size=50)
image_recog.preprosessing(image_recog.images)
image_recog.preprosessing(image_recog.test_images)


errors = []

starttime = time()
while True:
    action = input("Press 1 to train, 2 to test, r to set learning rate: ")
    if action == "r":
        image_recog.lrate = float(input("Enter a new learning rate: "))
    elif int(action) == 1:
        errors = image_recog.do_training(epochs=1, errors=errors)
    elif int(action) == 2:
        test_labels, result = image_recog.do_testing(nr_of_testing_images=nr_of_testing_images)
    else:
        errors = image_recog.do_training(epochs=int(action), errors=errors)
    print("Total time elapsed: " + str((time() - starttime)/60) + " min")