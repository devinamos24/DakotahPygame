import pygame
import ecs

RESOLUTION = 640, 640
SCREEN_CAPTION = "Super Fun Roguelike!"


def run_game() -> None:
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    screen_rect = screen.get_rect()
    pygame.display.set_caption(SCREEN_CAPTION)
    entities_manager = ecs.EntitiesManager()


if __name__ == "__main__":
    run_game()
