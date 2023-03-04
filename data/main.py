import pygame

from data.environment import World

if __name__ == "__main__":
    # Initialize world and render it
    world = World()
    world.generate_floor()
    world.draw_dumb_objects()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
