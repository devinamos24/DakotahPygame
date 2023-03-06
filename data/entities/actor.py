from enum import IntEnum
from data.engine import gfxengine
from data.engine.gfxengine import TextureIndices
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.entities.input_handler import _InputHandler
    from data.environment.level import Level


class Direction(IntEnum):
    north = 1
    east = 2
    south = 3
    west = 4


"""
An actor is anything that can move around and interact with the world/level including the player
"""


class _Actor:
    def __init__(self, x: int, y: int, health: int, hand, sprite_id: TextureIndices, level: "Level",
                 input_handler: "_InputHandler"):
        self.x = x
        self.y = y
        self.health = health
        self.hand = hand
        self.sprite_id = sprite_id
        self.level = level
        self.input_handler = input_handler

    # TODO make a list of move throughable dumb objects and store a move throughable boolean on smart objects and check that
    def check_valid_move(self, x, y) -> bool:
        if self.level.DumbObjects[y][x] != TextureIndices.wall:
            if self.level.SmartObjects[y][x] is None:
                return True
        return False

    def move(self, direction: Direction):
        new_x = self.x
        new_y = self.y
        if direction == Direction.north:
            new_y -= 1
        elif direction == Direction.east:
            new_x += 1
        elif direction == Direction.south:
            new_y += 1
        elif direction == Direction.west:
            new_x -= 1
        else:
            raise Exception(f"Direction: {direction} is not valid!")
        if self.check_valid_move(new_x, new_y):
            self.level.move_buffer.append((self.x, self.y, new_x, new_y))
            self.x = new_x
            self.y = new_y

    def update(self, events):
        action = self.input_handler.handle_input(events)
        if action is not None:
            action.execute(self)

    def draw(self, screen):
        gfxengine.draw_on_grid(screen, self.sprite_id, self.x, self.y)


class Player(_Actor):
    def __init__(self, x: int, y: int, health: int, hand, level: "Level",
                 input_handler: "_InputHandler"):
        _Actor.__init__(self, x, y, health, hand, TextureIndices.player, level, input_handler)
