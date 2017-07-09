from collections import namedtuple
import numpy as np
import random
import matplotlib.pyplot as plt

ITERS = 10
WIDTH = 15
HEIGHT = 10


board = np.zeros((HEIGHT, WIDTH), dtype=np.int8)
# only recalculate possible moves around changed pixel
# potentially store plant bounding box


Move = namedtuple('Move', 'coords id_ type_')


class lame_plant:

    def __init__(self, branch_id, leaf_id):
        self.branch_id = branch_id
        self.leaf_id = leaf_id


    def choose_move(self, moves):
        # bad bc empty move probs
        return random.choice(moves)


plants = [lame_plant(i, i+1) for i in range(1, 11, 2)]


seeds = np.random.choice(WIDTH, len(plants), replace=False)
for seed, plant in zip(seeds, plants):
    board[HEIGHT-1, seed] = plant.branch_id 
    board[HEIGHT-2, seed] = plant.leaf_id 



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

    return moves # TODO: make unique

def next_move():
    resources = get_resources()
    choice = np.random.choice(len(resources), p=resources/np.sum(resources))
    plant = plants[choice]
    possible_moves = get_possible_moves(plant)
    if possible_moves:
        move = plant.choose_move(possible_moves)
        board[move.coords[0], move.coords[1]] = move.id_
        resources[choice] -= move.type_

        


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
            if board[y, x] != 0 and board[y, x] % 2 == 0:
                resources[board[y, x] / 2 - 1] += 2
                break
    return resources



def draw_board():
    to_display = np.zeros((HEIGHT, WIDTH, 3), dtype=np.int8)
    to_display[board != 0] = np.array([0, 1, 0])
    to_display[board % 2 != 0] = np.array([1, 0, 0])
    plt.imshow(to_display, interpolation='nearest')
    plt.show()



def run():
    for _ in range(ITERS):
        draw_board()
        next_move()
    draw_board()