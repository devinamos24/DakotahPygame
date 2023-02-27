import pygame
import random

def display_move_indicator(card_clicked, indicator_image, player_x, player_y, map, screen):
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