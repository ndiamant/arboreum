from abc import ABCMeta
from abc import abstractmethod
from collections import namedtuple
import numpy as np
import random
import matplotlib.pyplot as plt

ITERS = 15
WIDTH = 200
HEIGHT = 30
NUM_PLANTS = 10

board = np.zeros((HEIGHT, WIDTH), dtype=np.int8)
# only recalculate possible moves around changed pixel
# potentially store plant bounding box


Move = namedtuple('Move', 'coords id_ type_')


class BasePlant(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def branch_col(self): 
        pass

    @property
    @abstractmethod
    def leaf_col():
        pass
    
    def __init__(self, branch_id, leaf_id):
        self.branch_id = branch_id
        self.leaf_id = leaf_id

    @abstractmethod
    def choose_move(self, moves):
        pass

class LamePlant(BasePlant):

    branch_col = np.array([139, 69, 19])/255.
    leaf_col = np.array([0, 100, 0])/255.


    def __init__(self, branch_id, leaf_id):
        self.branch_id = branch_id
        self.leaf_id = leaf_id


    def choose_move(self, moves):
        return random.choice(moves)


class Brancher(BasePlant):
    branch_col = np.array([0, 0, 200])/255.
    leaf_col = np.array([0, 200, 0])/255.


    def __init__(self, branch_id, leaf_id):
        self.branch_id = branch_id
        self.leaf_id = leaf_id


    def choose_move(self, moves):
        for move in moves:
            if move.type_ == 1:
                return move

        return random.choice(moves)

plants = [LamePlant(i, i+1) for i in range(1, NUM_PLANTS*2+1, 2)]
plants += [Brancher(i + 2*NUM_PLANTS, i+1+2*NUM_PLANTS) for i in range(1, NUM_PLANTS*2+1, 2)]


seeds = np.random.choice(WIDTH, len(plants), replace=False)
for seed, plant in zip(seeds, plants):
    board[HEIGHT-1, seed] = plant.branch_id 
    board[HEIGHT-2, seed] = plant.branch_id 
    board[HEIGHT-3, seed] = plant.leaf_id 


def adjacent_empties(coord):
    adjacents = np.array([[1,0], [-1,0], [0,1], [0,-1]])
    empties = []
    for adjacent in adjacents:
        try: 
            place = coord + adjacent
            
            if (place >= 0).all() and board[tuple((place).tolist())] == 0:
                empties.append(coord + adjacent) 
        except IndexError:
            pass
    return empties


def get_possible_moves(plant):
    """ returns 
    dictionary id: [branch_move_coords], [leaf move coordinates]
    """
    moves = []
    branch_coords = np.where(board == plant.branch_id)
    leaf_coords = np.where(board == plant.leaf_id)

    for y,x in zip(branch_coords[0], branch_coords[1]):
        empties = adjacent_empties(np.array([y,x]))
        for empty in empties:
            moves.append(Move(empty, plant.branch_id, 1))
            moves.append(Move(empty, plant.leaf_id, 2))

    for y,x in zip(leaf_coords[0], leaf_coords[1]):
        empties = adjacent_empties(np.array([y,x]))
        for empty in empties:
            moves.append(Move(empty, plant.leaf_id, 2))

    random.shuffle(moves)
    return moves # TODO: make unique


def kill_plant(plant):
    plant.branch_col = np.array([.3, .3, .3])
    plant.leaf_col = np.array([.6, .6, .6])




def next_move():
    resources = get_resources()
    for i in np.where(resources == 0)[0]:
        if i:
            kill_plant(plants[int(i)])
    while np.sum(resources) > 0:
        choice = np.random.choice(len(resources), p=resources/np.sum(resources))
        plant = plants[choice]
        possible_moves = get_possible_moves(plant)
        resource_count = resources[choice]
        if resource_count == 1:
            possible_moves = list(filter(lambda m: m.type_ == 1, possible_moves))
        if possible_moves:
            move = plant.choose_move(possible_moves)
            board[move.coords[0], move.coords[1]] = move.id_
            resources[choice] -= move.type_
        else:
            resources[choice] = 0
        


def update_moves(new_move, possible_moves):
    """ takes coordinate of new_move, possible_moves dict
    modifies possible_moves to have new moves

    write later if slow
    """
    pass


def get_resources():
    resources = np.zeros(len(plants))
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[y, x] != 0:
                if board[y, x] % 2 == 0:
                    resources[int(board[y, x] / 2 - 1)] += 2
                break
    return resources


def draw_board():
    to_display = np.zeros((HEIGHT, WIDTH, 3), dtype=float)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            b = board[y,x]
            if b!=0:
                color = np.array([(b%2) * b, ((b+1)%2) * b, 0], dtype=float)
                to_display[y,x] = color
    for plant in plants:
        to_display[board == plant.branch_id] = plant.branch_col
        to_display[board == plant.leaf_id] = plant.leaf_col
    plt.imshow(to_display, interpolation='nearest')
    plt.show()


def run():
    for _ in range(ITERS):
        next_move()
    draw_board()
