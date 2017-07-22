from collections import namedtuple
from scipy.misc import imsave
import numpy as np
import random
import matplotlib.pyplot as plt
import gif_writer
import greenhouse

ITERS = 100
WIDTH = 201
HEIGHT = 100
NUM_PLANTS = 50
IGNORE_LEAVES = False
SAVE_BOARD = True

board = np.zeros((HEIGHT, WIDTH), dtype=np.int16)
# only recalculate possible moves around changed pixel
# potentially store plant bounding box


Move = namedtuple('Move', 'coords id_ type_')


def add_plants(type_, num, plants):
    offset = plants[-1].leaf_id
    plants = [type_(i + offset, i + offset + 1) for i in range(1, num * 2 + 1, 2)]
    return plants
    
plants = [greenhouse.BasePlant(1, 2)]
plants += add_plants(greenhouse.BasePlant, NUM_PLANTS, plants)
plants += add_plants(greenhouse.Brancher, NUM_PLANTS, plants)
plants += add_plants(greenhouse.LeftPlant, 1, plants)
plants += add_plants(greenhouse.RightPlant, 1, plants)
plants += add_plants(greenhouse.UpPlant, 2, plants)

seeds = np.random.choice(WIDTH, len(plants), replace=False)
for seed, plant in zip(seeds, plants):
    board[HEIGHT-1, seed] = plant.branch_id 
    board[HEIGHT-2, seed] = plant.branch_id 
    board[HEIGHT-3, seed] = plant.leaf_id 


def adjacent_empties(coord, ignore_leaves=False):
    adjacents = np.array([[1,0], [-1,0], [0,1], [0,-1]])
    empties = []
    for adjacent in adjacents:
        place = coord + adjacent
        try: 
            if ignore_leaves:
                if board[tuple((place).tolist())] % 2 == 0 and (place >= 0).all():
                    empties.append(coord + adjacent) 
            else:
                if board[tuple((place).tolist())] == 0 and (place >= 0).all():
                    empties.append(coord + adjacent) 

        except IndexError:
            continue
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
            moves.append(Move(empty, plant.leaf_id, 2))

        empties = adjacent_empties(np.array([y,x]), ignore_leaves=IGNORE_LEAVES)
        for empty in empties:
            moves.append(Move(empty, plant.branch_id, 1))

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
    moves = []
    for i in np.where(resources == 0)[0]:
        kill_plant(plants[i])
    while np.sum(resources) > 0:
        choice = np.random.choice(len(resources), p=resources/np.sum(resources))
        plant = plants[choice]
        possible_moves = get_possible_moves(plant)
        if not possible_moves:
            kill_plant(plant)
        resource_count = resources[choice]
        if resource_count == 1:
            possible_moves = list(filter(lambda m: m.type_ == 1, possible_moves))
        if possible_moves:
            move = plant.choose_move(possible_moves)
            board[move.coords[0], move.coords[1]] = move.id_
            resources[choice] -= move.type_
            if SAVE_BOARD:
                moves.append(move) 
        else:
            resources[choice] = 0

    if SAVE_BOARD:
        save_board(moves)
        

def get_resources():
    resources = np.zeros(len(plants))
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[y, x] != 0:
                if board[y, x] % 2 == 0:
                    resources[int(board[y, x] / 2 - 1)] += 2
                break
    return np.sqrt(2 * resources).astype(int)


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
    return to_display


def save_board(moves):
    to_display = draw_board()
    
    for move in moves:
        coords = tuple(move.coords.tolist())
        # white last move so highlighted
        to_display[coords] = np.ones(3)

    save_board.arrays.append(to_display)

save_board.arrays = []


def run():
    for _ in range(ITERS):
        next_move()
    to_display = draw_board()
    plt.imshow(to_display, interpolation='nearest')
    plt.show()
    if SAVE_BOARD:
        gif_writer.write_gif_from_arrays(save_board.arrays)
