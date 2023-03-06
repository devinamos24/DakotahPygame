import pygame

from data.game import Game

if __name__ == "__main__":
    # Initialize world and render it
    pygame.init()
    game = Game()
    game.startup()

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        game.update(events)
        game.draw()
        pygame.display.update()

    pygame.quit()
