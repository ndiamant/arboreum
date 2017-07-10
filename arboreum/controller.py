# -*- coding: utf-8 -*-
#TODO: non-relative imports
from boards import board_base
import artists
import plants

ITERS = 100
WIDTH = 200
HEIGHT = 200
ARTIST = artists.artist_base()
PLANTS = [plants.plant_base()]
BOARD = board_base.BoardBase(WIDTH, HEIGHT, PLANTS)


class Controller:

    def __init__(self, iterations, board, artist, plants):
        # pick random plant starting places
        self.run()

    def step(self):
        """ Iterate through each plant and give it its possible moves
        and get each move.
        Then update the board accordingly
        """
        board.update()
        artist.draw_board(board)

    def run():
        for _ in range(self.iterations):
            self.step()


if __name__ == "__main__":
    Controller(ITERS, BOARD, ARTIST, PLANTS)
