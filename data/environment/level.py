import random

from ..engine import gfxengine
from ..engine.gfxengine import TextureIndices
from ..entities.card import RookCard, BishopCard, KnightCard, LightningBoltCard, FireBallCard
from ..entities.input_handler import PlayerInputHandler, AIInputHandler
from ..entities.actor import Player, Scarecrow, Coordinate
from ..ui.hand import Hand
from ..utility.twodarray import TwoDArray

map_width, map_height = 15, 15


class Level:
    def __init__(self):
        self.player_hand = None
        self.actors = []

        self.Stage_Layer = TwoDArray(map_height, map_width, TextureIndices.floor)
        self.Mod_Stage_Layer = TwoDArray(map_height, map_width, None)

    def update(self, events):
        for actor in self.actors:
            actor.update(events)

    def draw(self, screen):

        for coordinate, item in self.Stage_Layer:
            gfxengine.draw_on_grid(screen, item, coordinate)

        for actor in self.actors:
            actor.draw(screen)

        self.player_hand.draw(screen)

    def generate_floor(self):
        # Place floor tiles
        self.Stage_Layer.reset(TextureIndices.floor)

        # Place walls along outside
        for coordinate, _ in self.Stage_Layer:
            if coordinate.x == 0 or coordinate.x == map_width-1:
                self.Stage_Layer[coordinate] = TextureIndices.wall
            elif coordinate.y == 0 or coordinate.y == map_height-1:
                self.Stage_Layer[coordinate] = TextureIndices.wall

        # Place walls randomly
        num_walls = int(map_width * map_height * 0.3) - (2 * map_width + 2 * map_height - 4)

        for i in range(num_walls):
            wall_x = random.randint(1, map_width - 2)
            wall_y = random.randint(1, map_height - 2)
            self.Stage_Layer[Coordinate(wall_x, wall_y)] = TextureIndices.wall

        # TODO: reimplement this with new coordinate system
        # Ensure that there are no walled off segments
        # for y in range(map_height):
        #     for x in range(map_width):
        #         if self.Stage_Layer[y][x] == TextureIndices.wall:
        #             continue
        #         num_walls = 0
        #         if y > 0 and self.Stage_Layer[y - 1][x] == TextureIndices.wall:
        #             num_walls += 1
        #         if y < map_height - 1 and self.Stage_Layer[y + 1][x] == TextureIndices.wall:
        #             num_walls += 1
        #         if x > 0 and self.Stage_Layer[y][x - 1] == TextureIndices.wall:
        #             num_walls += 1
        #         if x < map_width - 1 and self.Stage_Layer[y][x + 1] == TextureIndices.wall:
        #             num_walls += 1
        #         if num_walls >= 3:
        #             self.Stage_Layer[y][x] = TextureIndices.wall

    def spawn_enemy_randomly(self, enemy_class):
        while True:
            spawn_x = random.randint(1, map_width-1)
            spawn_y = random.randint(1, map_height-1)
            coordinate = Coordinate(spawn_x, spawn_y)
            if self.Stage_Layer[coordinate] == TextureIndices.floor:
                if len([actor for actor in self.actors if actor.coordinate == coordinate]) == 0:
                    enemy = enemy_class(coordinate, self, AIInputHandler())
                    self.actors.append(enemy)
                    return

    def spawn_player(self):
        # Set the player starting position
        coordinate = Coordinate(1, 1)
        while True:
            if self.Stage_Layer[coordinate] == TextureIndices.floor:
                break
            # Inc + Reset
            if coordinate.x == coordinate.y:
                coordinate.y += 1
                coordinate.x = 1
                continue
            # Inc
            if coordinate.x == coordinate.y + 1:
                coordinate.y += 1
                continue
            # Inc + Flip
            if coordinate.y < coordinate.x - 1:
                coordinate.y += 1
                coordinate.x, coordinate.y = coordinate.y, coordinate.x
                continue
            # Flip
            coordinate.x, coordinate.y = coordinate.y, coordinate.x
        player = Player(coordinate, self, PlayerInputHandler())
        self.player_hand = Hand(player)
        player.hand.add_card(RookCard())
        player.hand.add_card(KnightCard())
        player.hand.add_card(BishopCard())
        player.hand.add_card(LightningBoltCard())
        player.hand.add_card(FireBallCard())
        self.actors.append(player)
        self.spawn_enemy_randomly(Scarecrow)
        self.spawn_enemy_randomly(Scarecrow)
