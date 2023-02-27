from enum import IntEnum
import random


class GameMap:

    def __init__(self):
        self.MapEntity = []
        map_width, map_height = 15, 15

        for i in range(map_height):
            self.MapEntity.append([0] * map_width)
