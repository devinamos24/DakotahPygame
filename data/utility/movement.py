from enum import Enum


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False


class Direction(Enum):
    N = Coordinate(0, -1)
    E = Coordinate(1, 0)
    S = Coordinate(0, 1)
    W = Coordinate(-1, 0)
