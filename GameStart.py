import pygame
import os


def game_start(current_dir):
    # Initialize the game
    pygame.init()

    # Join the current directory with the filename of the tileset image
    tileset_image_path = os.path.join(current_dir, "game/res/tileset.png")

    # Load the tileset image
    tileset_image = pygame.image.load(tileset_image_path)

    # Divide the tileset image into individual tiles
    tile_width, tile_height = 32, 32
    tiles = []
    for y in range(0, tileset_image.get_height(), tile_height):
        for x in range(0, tileset_image.get_width(), tile_width):
            tiles.append(tileset_image.subsurface(pygame.Rect(x, y, tile_width, tile_height)))

    # set game screen size
    screen_width = 640
    screen_height = 640
    screen = pygame.display.set_mode((screen_width, screen_height))

    return (screen, tiles, tile_width, tile_height, screen_width, screen_height)
