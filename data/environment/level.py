import random
from ..engine import gfxengine
from ..engine.gfxengine import TextureIndices
from ..entities.input_handler import PlayerInputHandler
from ..entities.actor import Player

map_width, map_height = 15, 15


class Level:
    def __init__(self):
        self.DumbObjects = [TextureIndices]

        for i in range(map_height):
            self.DumbObjects.append([0] * map_width)

        self.SmartObjects = []
        self.move_buffer = []

        for i in range(map_height):
            self.SmartObjects.append([None] * map_width)

    def update(self, events):
        for y, row in enumerate(self.SmartObjects):
            for x, tile_id in enumerate(row):
                if tile_id is not None:
                    tile_id.update(events)

        for pair in self.move_buffer:
            start_x = pair[0]
            start_y = pair[1]
            end_x = pair[2]
            end_y = pair[3]
            self.SmartObjects[end_y][end_x] = self.SmartObjects[start_y][start_x]
            self.SmartObjects[start_y][start_x] = None
            self.move_buffer.remove(pair)



    def draw(self, screen):
        for y, row in enumerate(self.DumbObjects):
            for x, tile_id in enumerate(row):
                gfxengine.draw_on_grid(screen, tile_id, x, y)

        for y, row in enumerate(self.SmartObjects):
            for x, tile_id in enumerate(row):
                if tile_id is not None:
                    gfxengine.draw_on_grid(screen, tile_id.sprite_id, x, y)

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

    def spawn_player(self):
        # Set the player starting position
        spawn_x = 1
        spawn_y = 1
        while True:
            if spawn_x == spawn_y:
                if self.DumbObjects[spawn_x][spawn_y] == 0:  # 0 represents a free space
                    break
            if spawn_x != spawn_y:
                if self.DumbObjects[spawn_x][spawn_y] == 0:
                    break
                if self.DumbObjects[spawn_y][spawn_x] == 0:
                    break
            if spawn_x >= spawn_y:
                spawn_y += 1
            else:
                spawn_x += 1

        self.SmartObjects[spawn_x][spawn_y] = Player(spawn_x, spawn_y, 10, 1, self, PlayerInputHandler())
