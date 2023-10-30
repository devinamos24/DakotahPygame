# This module will be used to form a layer of abstraction over the pygame rendering functions
import os.path
from enum import unique, IntEnum
from sys import stderr
from typing import Union, List
import pygame

#constint set up
IMAGES_FORMAT = ".png"
SCREEN_RESOLUTION = (640, 640)
TILE_SIDES = 32
HORIZONTAL_OFFSET = 80

#gives a number for each texture
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
    lightning_bolt = 8
    fire_ball = 9
    scarecrow = 10
    refresh_energy_card = 11
    end_turn = 12

#sets up path (needs to be fixed to work be deafult on linux and windows)
path = os.path.join("resources")

#gets teh sprite sheet and give each sprite its assigned texture name
def load_sprite_sheet() -> List[pygame.Surface]:
    # Load the tileset image
    tileset_image = pygame.image.load(os.path.join(path, "tileset" + IMAGES_FORMAT))

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
            surfaces.append(pygame.image.load(os.path.join(path, image_idx.name + IMAGES_FORMAT)))
        except pygame.error:
            print(pygame.get_error(), file=stderr)
            exit(-1)
    return load_sprite_sheet() + surfaces


graphics = load_textures()


def initialize_screen() -> Union[pygame.Surface, pygame.SurfaceType]:
    return pygame.display.set_mode(SCREEN_RESOLUTION)


"""
This function draws textures based on grid x and y instead of pixel x and y
"""


def draw_on_grid(screen: Union[pygame.Surface, pygame.SurfaceType], texture_id: TextureIndices, x: int, y: int):
    x = x * TILE_SIDES + HORIZONTAL_OFFSET
    y = y * TILE_SIDES
    screen.blit(graphics[texture_id], (x, y))


def draw(screen: Union[pygame.Surface, pygame.SurfaceType], texture_id: TextureIndices, x: int, y: int):
    screen.blit(graphics[texture_id], (x, y))
