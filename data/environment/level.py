import random

import pygame

from ..engine import gfxengine
from ..engine.gfxengine import TextureIndices
from ..entities.card import RookCard
from ..entities.input_handler import PlayerInputHandler
from ..entities.actor import Player
from ..ui.hand import Hand

map_width, map_height = 15, 15


class Level:
    def __init__(self):
        self.player_hand = None
        self.Stage_Layer = [TextureIndices]

        for i in range(map_height):
            self.Stage_Layer.append([0] * map_width)

        self.Actor_Layer = []
        self.move_buffer = []
        self.Mod_Stage_Layer = []

        for i in range(map_height):
            self.Actor_Layer.append([None] * map_width)

        for i in range(map_height):
            self.Mod_Stage_Layer.append([None] * map_width)

    def update(self, events):
        for y, row in enumerate(self.Actor_Layer):
            for x, tile_id in enumerate(row):
                if tile_id is not None:
                    tile_id.update(events)

        for pair in self.move_buffer:
            start_x = pair[0]
            start_y = pair[1]
            end_x = pair[2]
            end_y = pair[3]
            self.Actor_Layer[end_y][end_x] = self.Actor_Layer[start_y][start_x]
            self.Actor_Layer[start_y][start_x] = None
            self.move_buffer.remove(pair)

    def draw(self, screen):

        for y, row in enumerate(self.Stage_Layer):
            for x, tile_id in enumerate(row):
                gfxengine.draw_on_grid(screen, tile_id, x, y)

        for y, row in enumerate(self.Actor_Layer):
            for x, tile_id in enumerate(row):
                if tile_id is not None:
                    gfxengine.draw_on_grid(screen, tile_id.sprite_id, x, y)

        self.player_hand.draw(screen)

    def generate_floor(self):
        self.Stage_Layer.clear()

        # Place floor tiles
        for i in range(map_height):
            self.Stage_Layer.append([TextureIndices.floor] * map_width)

        # Place walls along outside
        for y in range(map_height):
            self.Stage_Layer[y][0] = TextureIndices.wall
            self.Stage_Layer[y][map_width - 1] = TextureIndices.wall
        for x in range(map_width):
            self.Stage_Layer[0][x] = TextureIndices.wall
            self.Stage_Layer[map_height - 1][x] = TextureIndices.wall

        # Place walls randomly
        num_walls = int(map_width * map_height * 0.3) - (2 * map_width + 2 * map_height - 4)
        for i in range(num_walls):
            wall_x = random.randint(1, map_width - 2)
            wall_y = random.randint(1, map_height - 2)
            self.Stage_Layer[wall_y][wall_x] = TextureIndices.wall

        # Ensure that there are no walled off segments
        for y in range(map_height):
            for x in range(map_width):
                if self.Stage_Layer[y][x] == TextureIndices.wall:
                    continue
                num_walls = 0
                if y > 0 and self.Stage_Layer[y - 1][x] == TextureIndices.wall:
                    num_walls += 1
                if y < map_height - 1 and self.Stage_Layer[y + 1][x] == TextureIndices.wall:
                    num_walls += 1
                if x > 0 and self.Stage_Layer[y][x - 1] == TextureIndices.wall:
                    num_walls += 1
                if x < map_width - 1 and self.Stage_Layer[y][x + 1] == TextureIndices.wall:
                    num_walls += 1
                if num_walls >= 3:
                    self.Stage_Layer[y][x] = TextureIndices.wall

    def spawn_player(self):
        # Set the player starting position
        spawn_x = 1
        spawn_y = 1
        while True:
            if spawn_x == spawn_y:
                if self.Stage_Layer[spawn_x][spawn_y] == 0:  # 0 represents a free space
                    break
            if spawn_x != spawn_y:
                if self.Stage_Layer[spawn_x][spawn_y] == 0:
                    break
                if self.Stage_Layer[spawn_y][spawn_x] == 0:
                    break
            if spawn_x >= spawn_y:
                spawn_y += 1
            else:
                spawn_x += 1
        player = Player(spawn_x, spawn_y, 10, self, PlayerInputHandler())
        self.player_hand = Hand(player)
        player.hand.add_card(RookCard())
        player.hand.add_card(RookCard())
        player.hand.add_card(RookCard())
        self.Actor_Layer[spawn_x][spawn_y] = player
