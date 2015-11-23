from time import time
import theano
import numpy as np
import theano.tensor as T
import theano.tensor.nnet as Tann
import file_handler
import json


class ANN():
    '''
    nb = # bits, nh = # hidden nodes (in the single hidden layer)
    lr = learning rate
    '''


    def __init__(self, ann_type, nb=40, nh=700, lr=0.001, custom = False, layer_list = None):
        '''
        Initializes by loading the images and building the neural network structure.
        '''
        #self.images, self.labels = gen_flat_cases()
        self.lrate = lr
        self.build_2048_ann(nb, 700, 100)

    def build_rectified_linear2_ann(self, nb, nh, nh2):
        #784
        #620
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
        x3 = Tann.softmax(T.dot(x2, w3))
        error = T.sum(pow((target - x3), 2))
        params = [w1, w2, w3]
        gradients = T.grad(error, params)
        backprops = [(p, p - self.lrate*g) for p,g in zip(params,gradients)]

        self.trainer = theano.function(inputs=[input, target], outputs=error, updates=backprops, allow_input_downcast=True)
        self.predictor = theano.function(inputs=[input], outputs=x3, allow_input_downcast=True)
    
    
    def build_2048_ann(self, nb, nh, nh2):
        '''
        
        '''
        #nb = input nodes
        #nh = first hidden layer size
        #nh2 = second hidden layer size
        print("building")
        w1 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nb,nh)))
        w2 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nh,nh2)))
        w3 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nh2, 4)))
        input = T.dvector('input')
        target = T.wvector('target')
        x1 = T.switch(T.dot(input,w1) > 0, T.dot(input,w1), 0)
        x2 = T.switch(T.dot(x1,w2) > 0, T.dot(x1,w2), 0)
        x3 = Tann.softmax(T.dot(x2, w3))
        error = T.sum(pow((target - x3), 2))
        params = [w1, w2, w3]
        gradients = T.grad(error, params)
        backprops = [(p, p - self.lrate*g) for p,g in zip(params,gradients)]

        self.trainer = theano.function(inputs=[input, target], outputs=error, updates=backprops, allow_input_downcast=True)
        self.predictor = theano.function(inputs=[input], outputs=x3, allow_input_downcast=True)
        print("Built")

    def do_training(self, epochs=1, test_interval=None, errors=[]):
        '''

        '''
        self.cases, self.labels = file_handler.get_cases()
        for i in range(epochs):
            print("epoch: ", i)
            error = 0
            for j in range(len(self.cases)):
                if j % 1000 == 0:
                    print(str(float(round((j/len((self.cases)) * 100)))) + "% complete")
                case = self.convert_to_list(self.cases[j])
                case = self.preprosessing(case)
                error += self.trainer(case, self.labels[j])
            errors.append(error)
        return errors

    def convert_to_list(self, str):
        '''

        '''
        return json.loads(str)

    def do_testing(self,scatter=True, blind_test_images=None):
        '''

        '''
        hidden_activations = []
        for c in self.self.cases:
            end = self.predictor(c)
            hidden_activations.append(end)
        self.check_result(hidden_activations)
        return self.test_labels, hidden_activations

    def blind_test(self, images):
        '''

        '''
        #Raw images is a list with sublist of raw_images
        results = []
        for i in range(len(images)):
            answer = np.argmax(self.predictor(images[i]))
            results.append(answer)
        return results

    def preprosessing(self, flat_board):
        '''

        '''
        results = []
        l1 = [flat_board[x] for x in range(4)]
        l2 = [flat_board[x] for x in range(4, 8)]
        l3 = [flat_board[x] for x in range(8, 12)]
        l4 = [flat_board[x] for x in range(12, 16)]

        l5 = [flat_board[0], flat_board[4], flat_board[8], flat_board[12]]
        l6 = [flat_board[1], flat_board[5], flat_board[9], flat_board[13]]
        l7 = [flat_board[2], flat_board[6], flat_board[10], flat_board[14]]
        l8 = [flat_board[3], flat_board[7], flat_board[11], flat_board[15]]
        
        results.append(self.scoring_horizontal(l1))
        results.append(self.scoring_horizontal(l2))
        results.append(self.scoring_horizontal(l3))
        results.append(self.scoring_horizontal(l4))
        results.append(self.scoring_horizontal(l5))
        results.append(self.scoring_horizontal(l6))
        results.append(self.scoring_horizontal(l7))
        results.append(self.scoring_horizontal(l8))

        gradient = [10,9,8,7,9,5,4,3,8,4,2,2,7,3,2,1]
        gradient_repr = []
        for i in range(0, len(gradient)):
             gradient_repr.append(gradient[i]*flat_board[i])


        norm_result = self.normalized_list(results)
        norm_gradient_repr = self.normalized_list(gradient_repr)
        norm_flat_board = self.normalized_list(flat_board)

        return norm_flat_board+norm_result+norm_gradient_repr

    def scoring_horizontal(self, l):
        score = 0
        for i in range(len(l) - 1):
            if l[i] == l[i+1]:
                score += l[i]
        return score

    def normalized_list(self, l):
        normalized_list = []
        largest = max(l)
        for i in l:
            if largest != 0:
                normalized_list.append(i/largest)
            else:
                normalized_list.append(0)
        return normalized_list

    def check_result(self, result):
        '''

        '''
        count = 0
        for i in range(len(self.test_labels)):
            b = int(self.test_labels[i]) == np.argmax(result[i])# == max(result[i]))[0][0])
            if b:
                count += 1
        print("statistics:", (count/float(len(self.test_labels))) * 100)

    def build_custom_ann(self, layer_list, ann_type = "rlu", nb = 784):
        '''

        '''
        layer_list = [nb] + layer_list
        input = T.dvector('input')
        target = T.wvector('target')
        w_list = []
        x_list = []
        w_list.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(layer_list[0],layer_list[1]))))
        if ann_type == "rlu":
            x_list.append(T.switch(T.dot(input,w_list[0]) > 0, T.dot(input,w_list[0]), 0))
        elif ann_type == "sigmoid":
            x_list.append(Tann.sigmoid(T.dot(input, w_list[0])))
        elif ann_type == "ht":
            x_list.append(T.tanh(T.dot(input, w_list[0])))

        for count in range(0, len(layer_list) - 2):
            w_list.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(layer_list[count + 1],layer_list[count + 2]))))
            if ann_type=="rlu":
                x_list.append(T.switch(T.dot(x_list[count],w_list[count + 1]) > 0, T.dot(x_list[count], w_list[count + 1]), 0))
            elif ann_type == "sigmoid":
                x_list.append(Tann.sigmoid(T.dot(x_list[count],w_list[count + 1])))
            elif ann_type == "ht":
                x_list.append(T.tanh(T.dot(x_list[count],w_list[count + 1])))
        w_list.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(layer_list[-1], 10))))
        x_list.append(T.switch(T.dot(x_list[-1],w_list[-1]) > 0, T.dot(x_list[-1],w_list[-1]), 0))

        error = T.sum(pow((target - x_list[-1]), 2))
        params = w_list
        gradients = T.grad(error, params) 
        backprops = [(p, p - self.lrate*g) for p,g in zip(params,gradients)]

        self.trainer = theano.function(inputs=[input, target], outputs=error, updates=backprops, allow_input_downcast=True)
        self.predictor = theano.function(inputs=[input], outputs=x_list[-1], allow_input_downcast=True)


def start():
    '''

    '''
    custom = input("Custom net: y/n ")
    ann_type = input("Options: sigmoid, rlu, ht: ")
    print("---------")
    if custom == "N" or custom == "n":
        image_recog = ANN(ann_type)
        image_recog.preprosessing(image_recog.images)
    else:
        layerlist = input("Enter layer list: ")
        layerlist = layerlist.split()
        for x in range(len(layerlist)):
            layerlist[x] = int(layerlist[x])
        image_recog = ANN(custom = True, layer_list = layerlist, ann_type = ann_type)
        image_recog.preprosessing(image_recog.images)

    errors = []
    print("Successfully loaded the images and built the neural network")
    print("----------")
    while True:
        num = input(" 1: Train \n 2: Test \n 3: Blind test \n 4: Restart \n 5: Minor demo \n")
        if int(num) == 1:
            errors = image_recog.do_training(epochs=5, errors=errors)
        elif int(num) == 2:
            test_labels, result = image_recog.do_testing()
        elif int(num) == 3:
            results = image_recog.blind_test(images)
        elif int(num) == 4:
            start()
        elif int(num) == 5:
            minor_demo(image_recog)
        else:
            errors = image_recog.do_training(epochs=int(action), errors=errors)

if __name__ == "__main__":
    start()
    
