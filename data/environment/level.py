#level.py is the play area of the game, it keeps track of the stage, and actors

import random

from ..engine import gfxengine
from ..engine.gfxengine import TextureIndices
from ..entities.card import RookCard, BishopCard, KnightCard, LightningBoltCard, FireBallCard
from ..entities.input_handler import PlayerInputHandler, AIInputHandler
from ..entities.actor import Player, Scarecrow
from ..ui.hand import Hand

#sets size of stage
map_width, map_height = 15, 15

class Level:
    def __init__(self):
        self.player_hand = None
        self.Stage_Layer = [TextureIndices]
        self.actors = []
        self.Mod_Stage_Layer = []

        #sets up the stage textures
        for i in range(map_height):
            self.Stage_Layer.append([0] * map_width)
            self.Mod_Stage_Layer.append([None] * map_width)

        #unsure what this does
        self.move_buffer = []

    #update actor
    def update(self, events):
        for actor in self.actors:
            actor.update(events)

    #draws the stage then actors on top of stage, then finally the players hand
    def draw(self, screen):
        for y, row in enumerate(self.Stage_Layer):
            for x, tile_id in enumerate(row):
                gfxengine.draw_on_grid(screen, tile_id, x, y)

        for actor in self.actors:
            gfxengine.draw_on_grid(screen, actor.sprite_id, actor.x, actor.y)

        self.player_hand.draw(screen)

    #create floor plan for the stage
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

    #spawns an enemy on a random unoccupied space
    def spawn_enemy_randomly(self, enemy_class):
        while True:
            #randomly select an x and y for spawning
            spawn_x = random.randint(1, map_width-1)
            spawn_y = random.randint(1, map_height-1)

            #Check each layer the make sure the selected x,y position is free
            if self.Stage_Layer[spawn_y][spawn_x] == 0:
                if len([actor for actor in self.actors if actor.x == spawn_x and actor.y == spawn_y]) == 0:
                    enemy = enemy_class(spawn_x, spawn_y, self, AIInputHandler())
                    self.actors.append(enemy)
                    return

    def spawn_player(self):
        # Set the player starting position
        spawn_x = 1
        spawn_y = 1
        while True:
            if self.Stage_Layer[spawn_y][spawn_x] == 0:  # 0 represents a free space
                break
            # Inc + Reset
            if spawn_x == spawn_y:
                spawn_y += 1
                spawn_x = 1
                continue
            # Inc
            if spawn_x == spawn_y + 1:
                spawn_y += 1
                continue
            # Inc + Flip
            if spawn_y < spawn_x - 1:
                spawn_y += 1
                spawn_x, spawn_y = spawn_y, spawn_x
                continue
            # Flip
            spawn_x, spawn_y = spawn_y, spawn_x
        
        #when the player is spawned, creates player object, makes the player hand, adds cards to it
        #then spawns two random enemies
        player = Player(spawn_x, spawn_y, self, PlayerInputHandler())
        self.player_hand = Hand(player)
        player.hand.add_card(RookCard())
        player.hand.add_card(KnightCard())
        player.hand.add_card(BishopCard())
        player.hand.add_card(LightningBoltCard())
        player.hand.add_card(FireBallCard())
        self.actors.append(player)
        self.spawn_enemy_randomly(Scarecrow)
        self.spawn_enemy_randomly(Scarecrow)
