import pygame
import os
import random
from GameStart import game_start
from ChessMovement import  *

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

screen, tiles, tile_width, tile_height, screen_width, screen_height = game_start(current_dir)

# Map dimensions
map_width, map_height = 15, 15

# Initialize map
map = []
for i in range(map_height):
    map.append([0] * map_width)

# Set all the edge tiles to be walls
for y in range(map_height):
    map[y][0] = 1
    map[y][map_width-1] = 1
for x in range(map_width):
    map[0][x] = 1
    map[map_height-1][x] = 1

# Place walls randomly
num_walls = int(map_width * map_height * 0.3) - (2 * map_width + 2 * map_height - 4)
for i in range(num_walls):
    wall_x = random.randint(1, map_width-2)
    wall_y = random.randint(1, map_height-2)
    map[wall_y][wall_x] = 1

# Ensure that there are no walled off segments
for y in range(map_height):
    for x in range(map_width):
        if map[y][x] == 1:
            continue
        num_walls = 0
        if y > 0 and map[y-1][x] == 1:
            num_walls += 1
        if y < map_height-1 and map[y+1][x] == 1:
            num_walls += 1
        if x > 0 and map[y][x-1] == 1:
            num_walls += 1
        if x < map_width-1 and map[y][x+1] == 1:
            num_walls += 1
        if num_walls >= 3:
            map[y][x] = 1

# Set the player starting position
spawn_x = 1
spawn_y = 1
while True:
    if spawn_x == spawn_y:
        if map[spawn_x][spawn_y] == 0: # 0 represents a free space
            player_y = spawn_y
            player_x = spawn_x
            break
    if spawn_x != spawn_y:
        if map[spawn_x][spawn_y] == 0:
            player_x = spawn_y
            player_y = spawn_x
            break
        if map[spawn_y][spawn_x] == 0:
            player_x = spawn_x
            player_y = spawn_y
            break
    if spawn_x >= spawn_y:
        spawn_y += 1
    else:
        spawn_x += 1

# Set the clock to control the framerate
clock = pygame.time.Clock()

#set Card clicked
card_clicked = None
is_hovered = None

# Start the main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the map
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            screen.blit(tiles[tile], (x * tile_width, y * tile_height))

    # Draw the player
    screen.blit(tiles[2], (player_x * tile_width, player_y * tile_height))

    # Create a list to store the images of the cards in the hand
    hand = [pygame.image.load(os.path.join(current_dir, "../resources/rook_card.png")), pygame.image.load(os.path.join(current_dir,
                                                                                                                       "../resources/bishop_card.png")), pygame.image.load(os.path.join(current_dir,
                                                                                                                                                                                        "../resources/knight_card.png"))]
    
    # Get the width and height of a single card
    card_width = hand[0].get_width()
    card_height = hand[0].get_height()

    # Scale the cards to double their size
    for i in range(3):
        hand[i] = pygame.transform.scale(hand[i], (card_width * 2, card_height * 2))

    # Draw the hand of cards and dont redraw hovering card (it will get redrawn in the event)
    for i in range(3):
        if is_hovered != i:
            screen.blit(hand[i], (screen_width - (5 - i) * card_width * 2, screen_height - card_height * 2))
    
    # Keep track of whether the mouse is hovering over a card
    if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
        # Check if the mouse is hovering over a card
        mouse_x, mouse_y = pygame.mouse.get_pos()
        card_hover = None
        for i in range(3):
            x_min = screen_width - (5 - i) * card_width * 2
            x_max = x_min + card_width * 2
            y_min = screen_height - card_height * 2
            y_max = y_min + card_height * 2
            if x_min <= mouse_x <= x_max and y_min <= mouse_y <= y_max:
                card_hover = i
                is_hovered = i
            else:
                is_hovered = -1

        # Move the hovered card up from its position
        if card_hover is not None:
            screen.blit(hand[card_hover], (screen_width - (5 - card_hover) * card_width * 2, screen_height - card_height * 2 - 10))

    if card_clicked is not None:
        screen.blit(hand[card_clicked], (screen_width - (5 - card_clicked) * card_width * 2, screen_height - card_height * 2 - 10))

    # Check which card was clicked and move the player accordingly
    if event.type == pygame.MOUSEBUTTONUP:
        x, y = pygame.mouse.get_pos()
        # Check if any of the indicators were clicked
        if card_clicked is not None:
            for position in valid_move_positions(card_clicked, player_x, player_y, map):
                indicator_x, indicator_y = position[0] * tile_width, position[1] * tile_height
                indicator_rect = pygame.Rect(indicator_x, indicator_y, tile_width, tile_height)
                if indicator_rect.collidepoint(event.pos):
                    clicked_position = position
                    if (clicked_position[0] * tile_width <= mouse_x <= x * tile_width + tile_width and
                        clicked_position[1] * tile_height <= mouse_y <= y * tile_height + tile_height):
                        # The player has clicked on this indicator, move the player to this position
                        player_x, player_y = clicked_position[0], clicked_position[1]
                    break
        card_clicked = None
        for i in range(3):
            x_min = screen_width - (5 - i) * card_width * 2
            x_max = x_min + card_width * 2
            y_min = screen_height - card_height * 2
            y_max = y_min + card_height * 2
            if x_min <= mouse_x <= x_max and y_min <= mouse_y <= y_max:
                card_clicked = i
                break

        if card_clicked is not None:
                # Show indicators for valid move positions
                display_move_indicator(card_clicked, tiles[3], player_x, player_y, map, screen)
        
    # Redraw the indicators
    display_move_indicator(card_clicked, tiles[3], player_x, player_y, map, screen)

    # Update the screen
    pygame.display.update()

    # Control the framerate
    clock.tick(30)

# Quit the game
pygame.quit()