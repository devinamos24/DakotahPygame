#passed from main.py

import pygame.display

from data.environment.world import World
from . import setup


class Game:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.world = None

    #initial setup of the world stage
    def startup(self):
        self.world = World()
        self.world.generate_world()

    #updates world stage and everything in it
    def update(self, events):
        self.world.update(events)

    #draws the current world to display
    def draw(self):
        self.world.draw(self.screen)
        pygame.display.update()
