import tkinter as tk
from time import time
import numpy as np
import json
import copy
import random
import scipy
from math import log, ceil
import requests

from ann import ANN
from game2048 import Game2048
from state import State
import ai2048demo

class Gui(tk.Tk):
    def __init__(self, delay, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("2048-solver")
        self.cell_width = self.cell_height = 50
        self.dim = (4, 4)
        self.delay=delay
        screen_width = self.dim[0]*self.cell_width+1
        screen_height = self.dim[1]*self.cell_height+1
        self.canvas = tk.Canvas(self, width=screen_width, height=screen_height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.color_dict = self.fill_color_dict()

        self.results_from_nn_playing = []
        self.results_from_random_playing = []
        self.results = []
        self.start_time = time()

        self.setup_network()
        self.user_control()
        self.start_game()

    def start_game(self):
        if len(self.results) < self.results_length:
            print("run nr", len(self.results))
            self.game_board = Game2048(board=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
            self.board = self.game_board.board
            self.game_board.generate_new_node()
            self.depth = 3
            self.move_count = 0
            self.draw_board()
            self.time = time()
            self.run_algorithm()
        else:
            if self.action[0] == "p":
                self.results_from_nn_playing = copy.copy(self.results)
                print("p, largest tile", max(self.results_from_nn_playing))
                print("p, average tile", sum(self.results_from_nn_playing)/float(len(self.results_from_nn_playing)))
            elif self.action[0] == "r":
                self.results_from_random_playing = copy.copy(self.results)
                print("r, largest tile", max(self.results_from_random_playing))
                print("r, average tile", sum(self.results_from_random_playing)/float(len(self.results_from_random_playing)))
            elif self.action[0] == "c":
                self.results_from_nn_playing = copy.copy(self.results)
                self.results_from_random_playing = [112]*50
                self.print_comparison()
            self.results = []
            self.user_control()
            self.start_game()


    def setup_network(self):
        self.move_classifier = ANN(ann_type="rlu2")
        self.errors = []


    def user_control(self):

        while True:
            self.action = input("Press r to play random, t to train, p to play with nn, c to compare results: ")
            if self.action[0] == "t":
                if len(self.action) == 1:
                    output_activations = self.move_classifier.do_training()
                elif self.action[1] == "l":
                    output_activations = self.move_classifier.do_testing()
                elif self.action[1] == "a":
                    points = ai2048demo.welch(self.results_from_random_playing, self.results_from_nn_playing)
                    print("points", points)
            elif self.action[0] == "p" or self.action[0] == "r":
                self.results_length = 50
                return
            elif self.action[0] == "c":
                if len(self.results_from_nn_playing)+len(self.results_from_random_playing) < 100:
                    self.results_length = 50
                    return
                else:
                    self.print_comparison()
            else:
                self.errors = self.move_classifier.do_training(epochs=int(self.action), errors=self.errors)
                output_activations = self.move_classifier.do_testing(boards=self.move_classifier.test_boards)
                print("Statistics (test set):\t\t ", self.move_classifier.check_result(output_activations, labels=self.move_classifier.test_labels), "%")
                output_activations = self.move_classifier.do_testing(boards=self.move_classifier.boards)
                print("Statistics (training set):\t ", self.move_classifier.check_result(output_activations, labels=self.move_classifier.labels), "%")

            print("Total time elapsed: " + str(round((time() - self.start_time)/60, 1)) + " min")

    def run_algorithm(self):
        continuing = True
        if self.game_board.is_game_over():
            largest_tile = self.game_board.get_largest_tile()
            print("largest tile", largest_tile)
            self.results.append(largest_tile)
            print("average tile", sum(self.results)/float(len(self.results)))
            continuing = False
            return self.start_game()
        
        current_node = State(self.game_board, self.depth)
        self.move_count += 1
        flat_board = current_node.board.board[3] + current_node.board.board[2] + current_node.board.board[1] + current_node.board.board[0]
        if self.action[0] == "r":
            chosen_move = self.choose_legal_random_move()
        else:
            case = self.move_classifier.preprosessing(flat_board)
            result = self.move_classifier.predictor(case)
            chosen_move = self.choose_legal_move_from_nn(result)
        if chosen_move == 0:
            self.game_board.move_left()
        elif chosen_move == 1:
            self.game_board.move_right()
        elif chosen_move == 2:
            self.game_board.move_up()
        elif chosen_move == 3:
            self.game_board.move_down()
        else:
            print("Illegal move")
        self.game_board.generate_new_node()
        self.draw_board()
        if continuing:
            self.after(self.delay, lambda: self.run_algorithm())

    def choose_legal_random_move(self):
        while True:
            r = random.randint(0,3)
            if self.game_board.is_move_legal(r):
                return r

    def choose_legal_move_from_nn(self, result):
        chosen_move = None
        while chosen_move == None or not self.game_board.is_move_legal(chosen_move):
            if chosen_move != None:
                result[0][chosen_move] = -1
            chosen_move = np.argmax(result[0])
        return chosen_move

    def print_comparison(self):
        print("NN results:\t", self.results_from_nn_playing)
        print("Random results:\t", self.results_from_random_playing)
        print("largest tiles", max(self.results_from_nn_playing),  max(self.results_from_random_playing))
        print("average tiles", sum(self.results_from_nn_playing)/float(len(self.results_from_nn_playing)), sum(self.results_from_random_playing)/float(len(self.results_from_random_playing)))
        points = ai2048demo.welch(self.results_from_random_playing, self.results_from_nn_playing)
        print("points", points)

    def bind_keys(self):
        self.bind('<Up>', lambda event: self.move(self, self.game_board.move_up()))
        self.bind('<Down>', lambda event: self.move(self, self.game_board.move_down()))
        self.bind('<Right>', lambda event: self.move(self, self.game_board.move_right()))
        self.bind('<Left>', lambda event: self.move(self, self.game_board.move_left()))

    def move(self, event, is_moved):
        if is_moved:
            self.game_board.generate_new_node()
            self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for y in range(self.dim[1]):
                for x in range(self.dim[0]):
                    x1 = x * self.cell_width
                    y1 = self.dim[1]*self.cell_height - y * self.cell_height
                    x2 = x1 + self.cell_width
                    y2 = y1 - self.cell_height
                    cell_type = self.board[y][x]
                    text = str(self.board[y][x])
                    color = self.color_dict[str(self.board[y][x])]
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="rect")
                    if cell_type != 0:
                        self.canvas.create_text(x1+self.cell_width/2, y1-self.cell_height/2, text=text)

    def fill_color_dict(self):
        color_dict = {
            '0': "white",
            '2': "PaleVioletRed1",
            '4': "PaleVioletRed2",
            '8': "hot pink",
            '16': "maroon1",
            '32': "maroon2",
            '64': "DeepPink2",
            '128': "DeepPink3",
            '256': "medium violet red",
            '512': "purple",
            '1024': "dark violet",
            '2048': "dark violet",
            '4096': "purple3",
            '8192': "purple3",
        }
        return color_dict

if __name__ == "__main__":
    app = Gui(delay=2)
    app.mainloop()