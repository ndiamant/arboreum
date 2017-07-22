import numpy as np
import random


class BasePlant(object):

    def __init__(self, branch_id, leaf_id):
        self.branch_id = branch_id
        self.leaf_id = leaf_id
        self.set_colors()
        self.randomize_colors()

    def randomize_colors(self):
        self.branch_col = self.branch_col.astype(float)
        self.leaf_col = self.leaf_col.astype(float)
        self.branch_col /= np.max(self.branch_col)
        self.leaf_col /= np.max(self.leaf_col)
        self.branch_col += np.random.rand(3)/2
        self.leaf_col += np.random.rand(3)/2
        self.branch_col /= np.max(self.branch_col)
        self.leaf_col /= np.max(self.leaf_col)
        self.branch_col = np.abs(self.branch_col)
        self.leaf_col = np.abs(self.leaf_col)

    def choose_move(self, moves):
        return random.choice(moves)

    def set_colors(self):
        self.branch_col = np.array([139, 69, 19])
        self.leaf_col = np.array([0, 100, 0])



class Brancher(BasePlant):

    def choose_move(self, moves):
        for move in moves:
            if move.type_ == 1:
                return move

        return random.choice(moves)

    def set_colors(self):
        self.branch_col = np.array([0, 0, 200])
        self.leaf_col = np.array([0, 200, 0])



class LeftPlant(BasePlant):

    def choose_move(self, moves):
        m = moves[0]
        for move in moves[1:]:
            if move.coords[1] < m.coords[1]:
                m = move

        return m

    def set_colors(self):
        self.branch_col = np.array([100, 0, 100])
        self.leaf_col = np.array([100, 100, 0])


class RightPlant(BasePlant):

    def choose_move(self, moves):
        m = moves[0]
        for move in moves[1:]:
            if move.coords[1] > m.coords[1]:
                m = move

        return m

    def set_colors(self):
        self.branch_col = np.array([100, 0, 100])
        self.leaf_col = np.array([100, 100, 0])

class UpPlant(BasePlant):

    def choose_move(self, moves):
        m = moves[0]
        for move in moves[1:]:
            if move.coords[0] < m.coords[0]:
                m = move

        return m

    def set_colors(self):
        self.branch_col = np.array([100, 100, 0])
        self.leaf_col = np.array([50, 50, 200])


