#used to take care of the game "world", everything in the game

from data.environment.level import Level

map_width, map_height = 15, 15

class World:

    def __init__(self):
        self.levels = [Level]
        self.current_level = None

    #initial setup of the world
    def generate_world(self):
        self.current_level = Level()
        self.current_level.generate_floor()
        self.current_level.spawn_player()

    #update world
    def update(self, events):
        self.current_level.update(events)

    #draw current world to display
    def draw(self, screen):
        self.current_level.draw(screen)

