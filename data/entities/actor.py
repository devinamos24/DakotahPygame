import pygame

from data.entities.action import Action


class Actor:
    def __init__(self, x: int, y: int, health: int, hand, sprite: pygame.Surface):
        self.x = x
        self.y = y
        self.health = health
        self.hand = hand
        self.sprite = sprite

    def use_action(self, action: Action):
        Action.do_thing(self)
