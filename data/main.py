import pygame

from data.environment import World
from data.game import Game

if __name__ == "__main__":
    # Initialize world and render it
    pygame.init()
    game = Game()
    game.startup()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.update()
        game.draw()
        pygame.display.update()

    pygame.quit()
