import pygame.display

from data.environment import World
from . import setup


class Game:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.world = None

    def startup(self):
        self.world = World()
        self.world.generate_floor()

    def update(self):
        self.world.update()

    def draw(self):
        self.world.draw(self.screen)
        pygame.display.update()
