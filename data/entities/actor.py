from enum import Enum
from data.engine import gfxengine
from data.engine.gfxengine import TextureIndices
from typing import TYPE_CHECKING
import data.entities.card as card
from data.utility.movement import Direction, Coordinate

if TYPE_CHECKING:
    from data.entities.input_handler import _InputHandler
    from data.entities.card import Damage
    from data.environment.level import Level


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
    def __init__(self, coordinate, health: int, turn_energy: int, sprite_id: TextureIndices, level: "Level",
                 input_handler: "_InputHandler"):
        self.coordinate = coordinate
        self.health = health
        self.hand = None
        self.sprite_id = sprite_id
        self.level = level
        self.input_handler = input_handler
        self.energy = Energy(turn_energy)

    def check_valid_move(self, coordinate) -> bool or list:
        if self.level.Stage_Layer[coordinate] != TextureIndices.wall:
            collided_actors = [actor for actor in self.level.actors if actor.coordinate == coordinate]
            if len(collided_actors) == 0:
                return False
            else:
                return collided_actors
        return True

    def check_valid_attack(self, coordinate) -> bool:
        if self.level.Stage_Layer[coordinate] != TextureIndices.wall:
            return True
        return False

    def move(self, coordinate):
        self.coordinate = coordinate

    def move_cardinal(self, direction: Direction) -> bool:
        coordinate = self.coordinate + direction.value
        collided_actors = self.check_valid_move(coordinate)
        if not collided_actors and isinstance(collided_actors, bool):
            self.move(coordinate)
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

    def die(self):
        self.level.actors.remove(self)

    def give_hand(self, hand):
        self.hand = hand

    def update(self, events):
        action = self.input_handler.handle_input(events)
        if action is not None:
            action.execute(self)

    def draw(self, screen):
        gfxengine.draw_on_grid(screen, self.sprite_id, self.coordinate)

    def click(self, x, y):
        pass


class Player(_Actor):
    def __init__(self, coordinate: Coordinate, level: "Level",
                 input_handler: "_InputHandler"):
        _Actor.__init__(self, coordinate, 10, 3, TextureIndices.player, level, input_handler)


class Scarecrow(_Actor):
    def __init__(self, coordinate: Coordinate, level: "Level", input_handler: "_InputHandler"):
        _Actor.__init__(self, coordinate, 5, 2, TextureIndices.scarecrow, level, input_handler)
