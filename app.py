import operator
import random
import time
import os

class Player:
    def __init__(self, i, j):
        self.i = i
        self.j = j


row = 0
col = 0
body = []
last_key = ''
temp_score = 1
food_i = 0  # Row Of The Food
food_j = 0  # Col Of The Food
SIZE = 20   # Size Of The Map
SLEEP = 0.05
score = 1   # Score --> Length Of Body

choices = ['a', 'w', 's', 'd']
map = [['0' for i in range(SIZE)] for j in range(SIZE)]
paths = []
finalPath = []

def set_border():
    global map
    map = [['#' if i == 0 or j == 0 or i == (SIZE-1) or j == (SIZE-1) else ' ' for i in range(SIZE)] for j in range(SIZE)]
#     for i in range(SIZE):
#         for j in range(SIZE):
#             if i == 0 or j == 0 or i == (SIZE-1) or j == (SIZE-1):
#                 map[i][j] = '#'
#             else:
#                 map[i][j] = ' '


def print_map():
    # os.system('cls')  # on Windows System
    os.system('clear')  # on Linux System

    # [[print(u"\U0001F538", end='') if map[i][j] == 'p' else print(u"\U0001F920", end='') if map[i][j] == 'P' else print(u"\U0001F355", end='') if map[i][j] == '*' else print(u"\u2588"u"\u2588", end='') if i == 0 or i == (SIZE - 1) else print(u"\u2588", end='  ') if map[i][j] == '#' else print(map[i][j], end=' ') for i in range(SIZE)] for j in range(SIZE)]

    for i in range(SIZE):
        for j in range(SIZE):
            if map[i][j] == 'p':
                print(u"\U0001F538", end='')
            elif map[i][j] == 'P':
                print(u"\U0001F920", end='')
            elif map[i][j] == '*':
                print(u"\U0001F355", end='')
            elif map[i][j] == '#':
                if i == 0 or i == (SIZE - 1):
                    print(u"\u2588"u"\u2588", end='')
                else:
                    print(u"\u2588", end='  ')
            else:
                print(map[i][j], end=' ')
        print()


def start():
    global row, col, food_i, food_j

    # Create Empty Map and Set The Borders (walls)
    set_border()

    # Set The Head of Snake
    row = random.randint(1, SIZE - 1)
    col = random.randint(1, SIZE - 1)
    while map[row][col] == '#':
        row = random.randint(1, SIZE - 1)
        col = random.randint(1, SIZE - 1)
    map[row][col] = 'p'
    body.append(Player(row, col))

    # Set The First Food
    food_i = random.randint(1, SIZE - 1)
    food_j = random.randint(1, SIZE - 1)
    while map[food_i][food_j] == '#' or map[food_i][food_j] == 'P':
        food_i = random.randint(1, SIZE - 1)
        food_j = random.randint(1, SIZE - 1)
    map[food_i][food_j] = '*'

    # Now Start The Game
    move_player()


def calc_h_cost(_row, _col):
    global food_i, food_j
    h_row = abs(food_i - _row)
    h_col = abs(food_j - _col)
    h_cost = h_row + h_col
    return h_cost


def calc_g_cost(_row, _col):
    global row, col
    g_row = abs(_row - row)
    g_col = abs(_col - col)
    g_cost = g_row + g_col
    return g_cost


def calc_f_cost(_row, _col):
    f_cost = 2 * calc_h_cost(_row, _col) + calc_g_cost(_row, _col)
    return f_cost


def final_path(_row, _col):
    states = [(-1, 0),
              (0, -1), (0, 1),
              (1, 0)]

    for _ in range(len(states)):
        new_row = _row + (states[_][0])
        new_col = _col + (states[_][1])
        if map[new_row][new_col] == '.' or map[new_row][new_col] == 'P':
            g_and_pos = calc_g_cost(new_row, new_col), new_row, new_col
            finalPath.append(g_and_pos)
        else:
            continue

    # Sort The Array of Costs
    finalPath.sort(key=operator.itemgetter(0))

    try:
        new_row = finalPath[0][1]
        new_col = finalPath[0][2]
    except IndexError:
        return

    if finalPath[0][0] == 0:
        # If H_cost(g_cost of food with head) of Snake == 0
        next_pos = food_i, food_j
        return next_pos

    if calc_g_cost(new_row, new_col) == 1:
        next_pos = new_row, new_col
        return next_pos

    else:
        # Pop The Head cause we used it
        finalPath.reverse()
        finalPath.pop()
        return final_path(new_row, new_col)


def a_star(_row, _col):
    # All The Possible Ways For Next Move
    states = [(-1, 0),
              (0, -1), (0, 1),
              (1, 0)]

    # Check For Wall and Body For Next Move, We Have 4 Possible Move
    for _ in range(len(states)):
        new_row = _row + (states[_][0])
        new_col = _col + (states[_][1])
        new_location = map[new_row][new_col]
        if new_location != 'p' and new_location != '#' and new_location != '.' and new_location != '*' and new_location != 'P':
            f_and_pos = calc_f_cost(new_row, new_col), new_row, new_col
            paths.append(f_and_pos)

        else:
            continue

    # Sort The Array of Costs
    paths.sort(key=operator.itemgetter(0))
    try:
        new_row = paths[0][1]
        new_col = paths[0][2]
    except IndexError:
        return

    if calc_h_cost(new_row, new_col) == 1:
        map[new_row][new_col] = '.'
        # Print the final path
        # print_map()
        # This Func just set the '.' in map , and we will use it for pathfinding
        return

    else:
        # Pop The Head cause we used it
        paths.reverse()
        paths.pop()
        map[new_row][new_col] = '.'
        # This Print is for debugging (finding the path)
        # print_map()
        return a_star(new_row, new_col)


def find_path():
    global food_i, food_j, row, col
    paths.clear()
    finalPath.clear()
    a_star(row, col)
    next_pos = final_path(food_i, food_j)
    return next_pos


def move_player():
    global last_key, score, row, col
    while True:
        print_map()
        print("Score: ", score)

        try:
            ### GET KEY WITH AI
            next_pos = find_path()
            if next_pos is None:
                return print("\n* I'm Done *\n\n")
            new_row = next_pos[0]
            new_col = next_pos[1]
            if new_row > row:
                print("Down")
                get_key = 's'
            elif new_row < row:
                print("Up")
                get_key = 'w'
            elif new_col > col:
                print("Right")
                get_key = 'd'
            else:
                print("Left")
                get_key = 'a'
        # time.sleep(0.05)

        except RecursionError:
            ### GET KEY RANDOMLY
            # IF AI Couldn't Find the path to food, we use random choice
            print("Thinking ...")
            get_key = choices[random.randint(0, 3)]
            while (last_key == 'w' and get_key == 's') or (last_key == 'a' and get_key == 'd') or \
                    (last_key == 's' and get_key == 'w') or (last_key == 'd' and get_key == 'a'):
                get_key = choices[random.randint(0, 3)]

        ### GET KEY MANUAL
        # get_key = input()

        last_key = get_key
        switcher = {
            'w': go_up,
            'a': go_left,
            's': go_down,
            'd': go_right,
        }
        switcher[get_key]()
        for i in range(SIZE):
            for j in range(SIZE):
                if map[i][j] == '.':
                    map[i][j] = ' '


def check_for_wall(i, j):
    if map[i][j] == '#':
        return True
    # False mean there was no wall
    return False


def check_for_body(i, j):
    if map[i][j] == 'p':
        return True
    return False


def check_for_food(i, j):
    global score
    if map[i][j] == '*':
        score = score + 1
        set_food()


def set_food():
    global food_i, food_j
    food_i = random.randint(1, SIZE-1)
    food_j = random.randint(1, SIZE-1)
    while map[food_i][food_j] == '#' or map[food_i][food_j] == 'p' or map[food_i][food_j] == 'P':
        food_i = random.randint(1, SIZE - 1)
        food_j = random.randint(1, SIZE - 1)
    map[food_i][food_j] = '*'


def move(_row, _col):
    global temp_score, score

    # Is He Ate The Food Or Not
    if temp_score == score:
        body.reverse()
        body.pop()
        body.reverse()
        body.append(Player(_row, _col))
    else:
        body.append(Player(_row, _col))
        temp_score = score

    # Clear The Map
    for i in range(SIZE):
        for j in range(SIZE):
            if map[i][j] == 'p' or map[i][j] == 'P':
                map[i][j] = ' '

    # The Length Of Snake Is Equal To Score , So Set The Body in Map with help of Score
    for number in range(score):
        # Set The Head
        if number == score-1:
            map[body[number].i][body[number].j] = 'P'
        # Set The Rest Of Body
        else:
            map[body[number].i][body[number].j] = 'p'


def go_up():
    global row, col
    if check_for_wall(row-1, col):  # Check For Wall
        return
    if check_for_body(row-1, col):  # Check For Body
        return
    row = row - 1  # Set New Row For Head Of Body
    check_for_food(row, col)  # Check For Food In New Position
    move(row, col)  # Move The Body
    time.sleep(SLEEP)
    return


def go_left():
    global row, col
    if check_for_wall(row, col-1):
        return
    if check_for_body(row, col-1):
        return
    col = col - 1
    check_for_food(row, col)
    move(row, col)
    time.sleep(SLEEP)
    return


def go_down():
    global row, col
    if check_for_wall(row+1, col):
        return
    if check_for_body(row+1, col):
        return
    row = row + 1
    check_for_food(row, col)
    move(row, col)
    time.sleep(SLEEP)
    return


def go_right():
    global row, col
    if check_for_wall(row, col+1):
        return
    if check_for_body(row, col+1):
        return
    col = col + 1
    check_for_food(row, col)
    move(row, col)
    time.sleep(SLEEP)
    return


def main():
    start()


if __name__ == '__main__':
    main()

