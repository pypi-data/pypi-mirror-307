from enum import Enum


class Directions(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4


DIRECTIONS_X = {Directions.NORTH: 0, Directions.SOUTH: 0, Directions.EAST: 1, Directions.WEST: -1}
DIRECTIONS_Y = {Directions.NORTH: -1, Directions.SOUTH: 1, Directions.EAST: 0, Directions.WEST: 0}
DIRECTIONS = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]


def get_new_coordinates(x, y, direction):
    n_x = x + DIRECTIONS_X[direction]
    n_y = y + DIRECTIONS_Y[direction]
    return n_x, n_y
