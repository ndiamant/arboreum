# -*- coding: utf-8 -*-
import numpy as np
import random


class BoardBase:

    empty = 0
    branch = 1
    leaf = 2
    
    def __init__(self, width, height, plants):
        self.width = width
        self.height = height
        self.board = np.ones((width, height)) * self.empty
        self.plants = plants
        seeds = np.random.choice(board.width, len(plants), replace=False)
        
    def update(self):
        for plant in plants:
            possible_moves = self.get_possible_moves(plant)
            move = plant.get_move(board, possible_moves)
            board.add(move)

    def get_possible_moves(self, plant):
        """ gets a list of valid moves for the given plant """
        pass

    def add(self, move):
        """ takes a move and adds to the board """
        pass

