from enum import IntEnum
import random


class World:

    def __init__(self):
        self.DumbObjects = []
        map_width, map_height = 15, 15

        for i in range(map_height):
            self.DumbObjects.append([0] * map_width)

        self.SmartObjects = self.DumbObjects.copy()
