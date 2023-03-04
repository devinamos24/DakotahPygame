# This module will be used to form a layer of abstraction over the pygame rendering functions
from enum import unique, IntEnum
from sys import stderr
from typing import Union, List
import pygame

IMAGES_FORMAT = ".png"
RESOURCE_PATH = "../resources/"
SCREEN_RESOLUTION = (640, 640)
TILE_SIDES = 32


@unique
class TextureIndices(IntEnum):
    floor = 0
    wall = 1
    player = 2
    move_indicator = 3
    bishop_card = 4
    knight_card = 5
    rook_card = 6
    shuffle_card = 7


def load_sprite_sheet() -> List[pygame.Surface]:
    # Load the tileset image
    tileset_image = pygame.image.load(f"{RESOURCE_PATH}/tileset{IMAGES_FORMAT}")

    # Divide the tileset image into individual tiles
    tile_width, tile_height = 32, 32
    tiles = []
    for y in range(0, tileset_image.get_height(), tile_height):
        for x in range(0, tileset_image.get_width(), tile_width):
            tiles.append(tileset_image.subsurface(pygame.Rect(x, y, tile_width, tile_height)))
    return tiles


def load_textures() -> List[pygame.Surface]:
    surfaces = list()
    for image_idx in TextureIndices:
        # the first four textures are from the tileset
        if image_idx < 4:
            continue
        try:
            surfaces.append(pygame.image.load(RESOURCE_PATH + image_idx.name + IMAGES_FORMAT))
        except pygame.error:
            print(pygame.get_error(), file=stderr)
            exit(-1)
    return load_sprite_sheet() + surfaces


graphics = load_textures()


def __initialize_screen() -> Union[pygame.Surface, pygame.SurfaceType]:
    return pygame.display.set_mode(SCREEN_RESOLUTION)


screen = __initialize_screen()

"""
This function draws textures based on grid x and y instead of pixel x and y
"""


def draw_on_grid(texture_id: TextureIndices, x: int, y: int):
    x = x * TILE_SIDES
    y = y * TILE_SIDES
    screen.blit(graphics[texture_id], (x, y))
