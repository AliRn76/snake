import operator
import random
import time
import math
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
SIZE = 18   # Size Of The Map
score = 1   # Score --> Lenght Of Body

choises = ['a', 'w', 's', 'd']
map = [['0' for i in range(SIZE)] for j in range(SIZE)]
paths = []
finalPath = []
closed_path = []



def setBorder():
    global map
    for i in range(SIZE):
        for j in range(SIZE):
            if i == 0 or j == 0 or i == (SIZE-1) or j == (SIZE-1):
                map[i][j] = '#'
            else:
                map[i][j] = ' '


def printMap():
    # os.system('cls')  # on Windows System
    os.system('clear') # on Linux System

    for i in range(SIZE):
        for j in range(SIZE):
            if map[i][j] == 'p':
                print('o', end=' ')
            elif map[i][j] == 'P':
                print('0', end=' ')
            elif map[i][j] == '*':
                print('*', end=' ')
            elif map[i][j] == '.':
                print('.', end=' ')
            else:
                print(map[i][j], end=' ')
        print()


def startGame(i, j):
    global row, col, food_i, food_j
    row = i
    col = j
    map[row][col] = 'p'
    # Set The First Food
    food_i = row + 1
    food_j = col + 1
    map[food_i][food_j] = '*'
    body.append(Player(row, col))
    printMap()
    movePlayer()


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
    global map
    # print("\nSTART OF FINAL PATH")
    states = [(-1, 0),
              (0, -1), (0, 1),
              (1, 0)]
    for _ in range(len(states)):
        new_row = _row + (states[_][0])
        new_col = _col + (states[_][1])
        if map[new_row][new_col] == '.' or map[new_row][new_col] == 'P':
            g_and_pos = calc_g_cost(new_row, new_col), new_row, new_col
            # print(g_and_pos)
            finalPath.append(g_and_pos)
        else:
            continue
    # Sort The Array of Costs
    # print(finalPath)
    finalPath.sort(key=operator.itemgetter(0))
    try:
        new_row = finalPath[0][1]
        new_col = finalPath[0][2]
        # print("ITS FINE")
        ## print(finalPath)

    except:
        # print("** ITS BUG")
        # print("NEW ROW: " + str(new_row))
        # print("NEW COL: " + str(new_col))
        return
    # print("New_Row: " + str(new_row))
    # print("New_Col: " + str(new_col))
    if finalPath[0][0] == 0:
        # Age 'P' chasbide bood be '*'
        next_pos = food_i, food_j
        return next_pos
    if calc_g_cost(new_row, new_col) == 1:
        # map[new_row][new_col] = '$'
        # printMap()
        # time.sleep(300)
        # print("OK ITS DONE")
        next_pos = new_row, new_col
        return next_pos
    else:
        # Pop The Head cause we used it
        finalPath.reverse()
        finalPath.pop()
        # time.sleep(300)
        # map[new_row][new_col] = '$'
        # printMap()
        # paths.reverse()
        # print(paths)
        # time.sleep(0.1)
        return final_path(new_row, new_col)



def a_star(_row, _col):
    global map
    # All The Possible Ways For Next Move
    try:
        states = [(-1, 0),
                  (0, -1), (0, 1),
                  (1, 0)]
        # Check For Wall and Body For Next Move, We Have 4 Possible Move
        for _ in range(len(states)):
            new_row = _row + (states[_][0])
            new_col = _col + (states[_][1])
            if map[new_row][new_col] != 'p' and map[new_row][new_col] != '#' and map[new_row][new_col] != '.' and map[new_row][new_col]  != '*' and map[new_row][new_col] != 'P':
                # Append The F_Cost, Row, Col In paths
                # print(calc_f_cost(new_row, new_col))
                f_and_pos = calc_f_cost(new_row, new_col), new_row, new_col
                paths.append(f_and_pos)
            else:
                continue
        # Sort The Array of Costs
        paths.sort(key=operator.itemgetter(0))
        new_row = paths[0][1]
        new_col = paths[0][2]
        # print(paths)
        # print("Min F and Its Pos: " + str(paths[0]))
        if calc_h_cost(new_row, new_col) == 1:
            map[new_row][new_col] = '.'
            # printMap()
            # I should build another pathfinding here , but just using the squire where has '.' in it

            # print("OK ITS DONE")
            return
        else:
            # Pop The Head cause we used it
            paths.reverse()
            paths.pop()
            # print("new_row: " + str(new_row))
            # print("new_col: " + str(new_col))
            map[new_row][new_col] = '.'
            # printMap()
            # paths.reverse()
            # print(paths)
            # time.sleep(0.1)
            return a_star(new_row, new_col)
    except:
        # In idea bayad roosh kar beshe , baraye stack overflow shodn
        # Age az oonvar error e Max Depth dad, az Invar check kone
        paths.clear()
        print("Max Depth Error")
        states = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        # Check For Wall and Body For Next Move, We Have 4 Possible Move
        for _ in range(len(states)):
            new_row = _row + (states[_][0])
            new_col = _col + (states[_][1])
            if map[new_row][new_col] != 'p' and map[new_row][new_col] != '#' and map[new_row][new_col] != '.' and \
                    map[new_row][new_col] != '*' and map[new_row][new_col] != 'P':
                # Append The F_Cost, Row, Col In paths
                # print(calc_f_cost(new_row, new_col))
                f_and_pos = calc_f_cost(new_row, new_col), new_row, new_col
                paths.append(f_and_pos)
            else:
                continue
        # Sort The Array of Costs
        paths.sort(key=operator.itemgetter(0))
        new_row = paths[0][1]
        new_col = paths[0][2]
        # print(paths)
        # print("Min F and Its Pos: " + str(paths[0]))
        if calc_h_cost(new_row, new_col) == 1:
            map[new_row][new_col] = '.'
            # printMap()
            # I should build another pathfinding here , but just using the squire where has '.' in it

            # print("OK ITS DONE")
            return
        else:
            # Pop The Head cause we used it
            paths.reverse()
            paths.pop()
            # print("new_row: " + str(new_row))
            # print("new_col: " + str(new_col))
            map[new_row][new_col] = '.'
            # printMap()
            # paths.reverse()
            # print(paths)
            # time.sleep(0.1)
            return a_star(new_row, new_col)



def find_path():
    global food_i, food_j, row, col
    paths.clear()
    finalPath.clear()
    a_star(row, col)
    next_pos = final_path(food_i, food_j)
    # next_pos = final_path()
    # print(next_pos)
    return next_pos


    # print(next_pos)

def movePlayer():
    global last_key, score, row, col
    while True:
        printMap()
        print("Score: ", score)

        try:
            # print("TRY")
            ### GET KEY WITH AI
            next_pos = find_path()
            new_row = next_pos[0]
            new_col = next_pos[1]
            # print("NEXT POS: ")
            # print(row, col)
            # print(new_row, new_col)
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
            time.sleep(0.01)
        except:
            ### GET KEY RANDOMLY
            print("Use Random Choise")
            get_key = choises[random.randint(0, 3)]
            while (last_key == 'w' and get_key == 's') or (last_key == 'a' and get_key == 'd') or \
                    (last_key == 's' and get_key == 'w') or (last_key == 'd' and get_key == 'a'):
                get_key = choises[random.randint(0, 3)]

        ### GET KEY MANUAL
        # get_key = input()


        last_key = get_key
        switcher = {
            'w': goUp,
            'a': goLeft,
            's': goDown,
            'd': goRight,
        }
        switcher[get_key]()
        for i in range(SIZE):
            for j in range(SIZE):
                if  map[i][j] == '.' or map[i][j] == '$':
                    map[i][j] = ' '


def checkForWall(i, j):
    if map[i][j] == '#':
        # print("wall")
        return True
    # False mean there was no wall
    return False


def checkForBody(i, j):
    if map[i][j] == 'p':
        # print("body")
        return True
    return False


def checkForFood(i, j):
    global score, map
    if map[i][j] == '*':
        score = score + 1
        setFood()


def setFood():
    global food_i, food_j, map
    rand_i = random.randint(1, SIZE-1)
    rand_j = random.randint(1, SIZE-1)
    while map[rand_i][rand_j] == '#' or map[rand_i][rand_j] == 'p':
        rand_i = random.randint(1, SIZE - 1)
        rand_j = random.randint(1, SIZE - 1)
    food_i = rand_i
    food_j = rand_j
    map[food_i][food_j] = '*'


def move(_row, _col):
    global temp_score, score, map

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

    # The Lenght Of Snake Is Equel To Score , So Set The Body In Map With Help Of Score
    for number in range(score):
        # Set The Head
        if number == score-1:
            map[body[number].i][body[number].j] = 'P'
        # Set The Rest Of Body
        else:
            map[body[number].i][body[number].j] = 'p'


def goUp():
    global row, col
    # Check For Wall
    if checkForWall(row-1, col):
        return
    # Check For Body
    if checkForBody(row-1, col):
        return
    # Set New Row For Head Of Body
    row = row - 1
    # print("up        ")
    # Check For Food In New Position
    checkForFood(row, col)
    # Move The Body
    move(row, col)
    time.sleep(0.1)
    return


def goLeft():
    global row, col
    if checkForWall(row, col-1):
        return
    if checkForBody(row, col-1):
        return
    col = col - 1
    # print("left")
    checkForFood(row, col)
    move(row, col)
    time.sleep(0.1)
    return


def goDown():
    global row, col
    if checkForWall(row+1, col):
        return
    if checkForBody(row+1, col):
        return
    row = row + 1
    # print("down")
    checkForFood(row, col)
    move(row, col)
    time.sleep(0.1)
    return


def goRight():
    global row, col
    if checkForWall(row, col+1):
        return
    if checkForBody(row, col+1):
        return
    col = col + 1
    # print("right")
    checkForFood(row, col)
    move(row, col)
    time.sleep(0.1)
    return


def main():
    setBorder()
    startGame(4, 3)


if __name__ == '__main__':
    main()

# I have to fix the corner bug , I think that the Ali's idea was good for it