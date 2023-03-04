from enum import IntEnum
import random
from ..engine import gfxengine
from ..engine.gfxengine import TextureIndices

map_width, map_height = 15, 15


class World:

    def __init__(self):
        self.DumbObjects = [TextureIndices]

        for i in range(map_height):
            self.DumbObjects.append([0] * map_width)

        self.SmartObjects = self.DumbObjects.copy()

    def update(self):
        pass

    def draw(self, screen):
        for y, row in enumerate(self.DumbObjects):
            for x, tile_id in enumerate(row):
                gfxengine.draw_on_grid(screen, tile_id, x, y)

    def generate_floor(self):
        self.DumbObjects.clear()

        # Place floor tiles
        for i in range(map_height):
            self.DumbObjects.append([TextureIndices.floor] * map_width)

        # Place walls along outside
        for y in range(map_height):
            self.DumbObjects[y][0] = TextureIndices.wall
            self.DumbObjects[y][map_width - 1] = TextureIndices.wall
        for x in range(map_width):
            self.DumbObjects[0][x] = TextureIndices.wall
            self.DumbObjects[map_height - 1][x] = TextureIndices.wall

        # Place walls randomly
        num_walls = int(map_width * map_height * 0.3) - (2 * map_width + 2 * map_height - 4)
        for i in range(num_walls):
            wall_x = random.randint(1, map_width - 2)
            wall_y = random.randint(1, map_height - 2)
            self.DumbObjects[wall_y][wall_x] = TextureIndices.wall

        # Ensure that there are no walled off segments
        for y in range(map_height):
            for x in range(map_width):
                if self.DumbObjects[y][x] == TextureIndices.wall:
                    continue
                num_walls = 0
                if y > 0 and self.DumbObjects[y - 1][x] == TextureIndices.wall:
                    num_walls += 1
                if y < map_height - 1 and self.DumbObjects[y + 1][x] == TextureIndices.wall:
                    num_walls += 1
                if x > 0 and self.DumbObjects[y][x - 1] == TextureIndices.wall:
                    num_walls += 1
                if x < map_width - 1 and self.DumbObjects[y][x + 1] == TextureIndices.wall:
                    num_walls += 1
                if num_walls >= 3:
                    self.DumbObjects[y][x] = TextureIndices.wall
