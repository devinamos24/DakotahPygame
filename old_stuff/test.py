import random

# Initialize a 5x5 2D array of all zeros
map = [[0 for i in range(5)] for j in range(5)]

# Randomly select a starting row and column
cur_row = random.randint(0, 4)
cur_col = random.randint(0, 4)

# Initialize the current number to 1
cur_num = 1

# Randomly choose the ending number (between 6 and 9 inclusive)
end_num = random.randint(6, 9)

# Keep looping until we've placed all the numbers up to the ending number
while cur_num <= end_num:
    
    # Place the current number in the current row and column
    map[cur_row][cur_col] = cur_num
    
    # Increment the current number
    cur_num += 1
    
    # Randomly choose the next row and column to place the next number
    # We'll keep randomly choosing until we find a valid location
    valid_location = False
    loop_catch = 0
    while not valid_location:
        next = [cur_row - 1, cur_col],[cur_row + 1, cur_col],[cur_row, cur_col - 1],[cur_row, cur_col + 1]
        next_area = random.choice(next)
        
        # Check if the location is empty and not in sequential order
        try:
            map[next_area[0]][next_area[1]]
        except:
            pass
        else:
            if map[next_area[0]][next_area[1]] == 0 and not (next_area[0] > 3 or next_area[0] < 0) and not (next_area[1] > 3 or next_area[1] < 0):
                cur_row = next_area[0]
                cur_col = next_area[1]
                valid_location = True
            else:
                loop_catch += 1
            
            if loop_catch > 20:
                cur_num = end_num + 1
                break

# Print the final map
for row in map:
    print(row)