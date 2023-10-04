#main game loop, creates display, initially generates world and
#has the game update the state and redraw the updated state
#to the game display

import pygame

from data.game import Game

if __name__ == "__main__":
    # Initialize world and render it
    pygame.init()
    game = Game()
    #set window
    game.startup()

    #main game loop
    running = True
    while running:
        #check is get is exited with quit type
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        #update game then draw updated display display
        game.update(events)
        game.draw()
        pygame.display.update()

    pygame.quit()
