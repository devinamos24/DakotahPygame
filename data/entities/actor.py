from enum import IntEnum
from data.engine import gfxengine
from data.engine.gfxengine import TextureIndices
from typing import TYPE_CHECKING
import data.entities.card as card

if TYPE_CHECKING:
    from data.entities.input_handler import _InputHandler
    from data.entities.card import Damage
    from data.environment.level import Level
    from data.environment.turn_order import Turn_order

#sets names for directions
class Direction(IntEnum):
    north = 1
    east = 2
    south = 3
    west = 4

#energy class to allow limiting actions per turn
class Energy:
    def __init__(self, turn_energy: int):
        self.turn_energy = turn_energy
        self.current_energy = turn_energy

    def add_energy(self, energy: int):
        self.current_energy += energy

    def remove_energy(self, energy: int):
        self.current_energy -= energy

    def add_turn_energy(self, energy: int):
        self.turn_energy += energy

    def remove_turn_energy(self, energy: int):
        self.turn_energy += energy

    def reset_energy(self):
        self.current_energy = self.turn_energy


# An actor is anything that can move around and interact with the world/level including the player
class _Actor:
    def __init__(self, x: int, y: int, health: int, turn_energy: int, sprite_id: TextureIndices, level: "Level",
                 input_handler: "_InputHandler", speed: int, turn_order):
        self.x = x
        self.y = y
        self.health = health
        self.hand = None
        self.sprite_id = sprite_id
        self.level = level
        self.input_handler = input_handler
        self.energy = Energy(turn_energy)
        self.speed = speed
        self.turn_order = turn_order

    def check_valid_move(self, x, y) -> bool or list:
        if self.level.Stage_Layer[y][x] != TextureIndices.wall:
            collided_actors = [actor for actor in self.level.actors if actor.x == x and actor.y == y]
            if len(collided_actors) == 0:
                return False
            else:
                return collided_actors
        return True

    def check_valid_attack(self, x, y) -> bool:
        if self.level.Stage_Layer[y][x] != TextureIndices.wall:
            return True
        return False

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def move_cardinal(self, direction: Direction) -> bool:
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
        collided_actors = self.check_valid_move(new_x, new_y)
        if not collided_actors and isinstance(collided_actors, bool):
            self.move(new_x, new_y)
            return True
        elif collided_actors and not isinstance(collided_actors, bool):
            for actor in collided_actors:
                actor.take_damage(self.do_damage())
                return True
        return False

    def take_damage(self, damage: "Damage" or None):
        if damage is not None:
            self.health -= damage.damage_amount
            if self.health <= 0:
                self.die()

    def do_damage(self) -> "Damage" or None:
        return card.Damage("Physical", 1)
    
    def end_turn(self):
        self.turn_order.next_turn()

    def die(self):
        self.turn_order.remove_from_master(self)
        self.level.actors.remove(self)

    def give_hand(self, hand):
        self.hand = hand

    def update(self, events, turn_order):
        action = self.input_handler.handle_input(events)
        if action is not None:
            action.execute(self)

    def draw(self, screen):
        gfxengine.draw_on_grid(screen, self.sprite_id, self.x, self.y)

    def click(self, x, y):
        pass


class Player(_Actor):
    def __init__(self, x: int, y: int, level: "Level", input_handler: "_InputHandler", speed: int, turn_order):
        _Actor.__init__(self, x, y, 10, 3, TextureIndices.player, level, input_handler, speed, turn_order)

    def take_damage(self, damage: "Damage" or None):
        if damage is not None:
            self.health -= damage.damage_amount
            if self.health <= 0:
                self.die()


class Scarecrow(_Actor):
    def __init__(self, x: int, y: int, level: "Level", input_handler: "_InputHandler", speed: int, turn_order):
        _Actor.__init__(self, x, y, 5, 2, TextureIndices.scarecrow, level, input_handler, speed, turn_order)

    def take_damage(self, damage: "Damage" or None):
        if damage is not None:
            self.health -= damage.damage_amount
            if self.health <= 0:
                self.die()
