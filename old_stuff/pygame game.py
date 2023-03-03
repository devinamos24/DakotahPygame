import pygame
import os
import random

def display_move_indicator(card_clicked, indicator_image, player_x, player_y, map):
    indicator_height = indicator_image.get_height()

    if card_clicked is None:  # Skip if card_clicked is None
        return

    for index in valid_move_positions(card_clicked, player_x, player_y, map):
        x,y  = get_tile_coordinates(index, indicator_height)
        screen.blit(indicator_image, (x, y))

def valid_move_positions(card_clicked, player_x, player_y, map):
    #Return a list of valid positions the player can move to based on the clicked card.
    valid_move = []

    if card_clicked == 0:  # Rook
        rook_movement = [(player_x + i, player_y) for i in range(-3, 4) if i != 0] + [(player_x, player_y + i) for i in range(-3, 4) if i != 0]
        #due to how the game gets the valid cords per peice, i need to have two nested for loops
        for direction in (0,2):
            for distance in reversed(range(3)):
                current_movement = rook_movement[distance + (direction * 3)]
                current_movement_x,current_movement_y = current_movement[0],current_movement[1]
                #in the 2d array, the y goes first then the x so all the checks on the map need to have the y first
                if map[current_movement_y][current_movement_x] == 0:
                    valid_move.append(current_movement)
                else:
                    break
        for direction in (1,3):
            for distance in range(3):
                current_movement = rook_movement[distance + (direction * 3)]
                current_movement_x,current_movement_y = current_movement[0],current_movement[1]
                if map[current_movement_y][current_movement_x] == 0:
                    valid_move.append(current_movement)
                else:
                    break
        return valid_move

    elif card_clicked == 1:  # Bishop
        bishop_movement = [(player_x + i, player_y + i) for i in range(-3, 4) if i != 0] + [(player_x + i, player_y - i) for i in range(-3, 4) if i != 0]
        for direction in (0,2):
            for distance in reversed(range(3)):
                current_movement = bishop_movement[distance + (direction * 3)]
                current_movement_x,current_movement_y = current_movement[0],current_movement[1]
                #check if the main movement space isnt blocked
                #in the 2d array, the y goes first then the x so all the checks on the map need to have the y first
                if map[current_movement_y][current_movement_x] == 0:
                    #check if the two spaces before it both arent blocked
                    if direction == 0 and not (map[current_movement_y][(current_movement_x + 1)] == 1 and map[(current_movement_y + 1)][current_movement_x] == 1):
                        valid_move.append(current_movement)
                    elif direction == 2 and not (map[current_movement_y][(current_movement_x + 1)] == 1 and map[(current_movement_y - 1)][current_movement_x] == 1):
                        valid_move.append(current_movement)
                    else:
                        break
                else:
                    break
        for direction in (1,3):
            for distance in range(3):
                current_movement = bishop_movement[distance + (direction * 3)]
                current_movement_x,current_movement_y = current_movement[0],current_movement[1]
                #check if the main movement space isnt blocked
                if map[current_movement_y][current_movement_x] == 0:
                    #check if the two spaces before it both arent blocked
                    if direction == 1 and not (map[current_movement_y][(current_movement_x - 1)] == 1 and map[(current_movement_y - 1)][current_movement_x] == 1):
                        valid_move.append(current_movement)
                    elif direction == 3 and not (map[current_movement_y][(current_movement_x - 1)] == 1 and map[(current_movement_y + 1)][current_movement_x] == 1):
                        valid_move.append(current_movement)
                    else:
                        break
                else:
                    break
        return valid_move

    elif card_clicked == 2:  # Knight
        knight_movement = [(player_x + 1, player_y + 2),
                (player_x + 2, player_y + 1),
                (player_x - 1, player_y + 2),
                (player_x - 2, player_y + 1),
                (player_x + 1, player_y - 2),
                (player_x + 2, player_y - 1),
                (player_x - 1, player_y - 2),
                (player_x - 2, player_y - 1)]
        sets = ((1,1),(1,-1),(-1,1),(-1,-1))
        for k, value in enumerate(sets):
            y, x = value
            # this will check the movements going more up and down
            if map[knight_movement[k * 2][1]][knight_movement[k * 2][0]] == 0:
                if not ((map[player_y][player_x + (1 * x)] == 1 and map[player_y + (1 * y)][player_x] == 1) or (map[player_y + (1 * y)][player_x + (1 * x)] == 1 and map[player_y + (1 * y)][player_x] == 1) or (map[player_y + (1 * y)][player_x + (1 * x)] == 1 and map[player_y + (2 * y)][player_x] == 1)):
                    valid_move.append(knight_movement[k * 2])
                else:
                    pass
            # This will check the movements going more left and right
            if map[knight_movement[(k * 2) + 1][1]][knight_movement[(k * 2) + 1][0]] == 0:
                if not ((map[player_y][player_x + (1 * x)] == 1 and map[player_y + (1 * y)][player_x] == 1) or (map[player_y + (1 * y)][player_x + (1 * x)] == 1 and map[player_y][player_x + (1 * x)] == 1) or (map[player_y + (1 * y)][player_x + (1 * x)] == 1 and map[player_y][player_x + (2 * x)] == 1)):
                    valid_move.append(knight_movement[(k * 2) + 1])
                else:
                    pass
        return valid_move

    else:
        return

def get_tile_coordinates(position, tile_size):
    #Return the screen coordinates for a given tile position and tile size.
    return (position[0] * tile_size, position[1] * tile_size)

# Initialize the game
pygame.init()

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Join the current directory with the filename of the tileset image
tileset_image_path = os.path.join(current_dir, "../resources/tileset.png")

# Set the screen size
screen = pygame.display.set_mode((1000, 800))

# Load the tileset image
tileset_image = pygame.image.load(tileset_image_path)

# Divide the tileset image into individual tiles
tile_width, tile_height = 32, 32
tiles = []
for y in range(0, tileset_image.get_height(), tile_height):
    for x in range(0, tileset_image.get_width(), tile_width):
        tiles.append(tileset_image.subsurface(pygame.Rect(x, y, tile_width, tile_height)))

#set game screen size
screen_width = 640
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# Map dimensions
min_map_size = 15
max_map_size = 20
map_width = random.randint(min_map_size, max_map_size)
map_height = random.randint(min_map_size, max_map_size)

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
                display_move_indicator(card_clicked, tiles[3], player_x, player_y, map)
        
    # Redraw the indicators
    display_move_indicator(card_clicked, tiles[3], player_x, player_y, map)

    # Update the screen
    pygame.display.update()

    # Control the framerate
    clock.tick(30)

# Quit the game
pygame.quit()