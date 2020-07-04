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
SIZE = 18   # Size Of The Map
score = 1   # Score --> Lenght Of Body

choises = ['a', 'w', 's', 'd']
map = [[0 for i in range(SIZE)] for j in range(SIZE)]



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
    os.system('clear') #on Linux System

    for i in range(SIZE):
        for j in range(SIZE):
            if map[i][j] == 'p':
                print('o', end=' ')
            elif map[i][j] == 'P':
                print('O', end=' ')
            elif map[i][j] == '*':
                print('*', end=' ')
            else:
                print(map[i][j], end=' ')
        print()

def startGame(i, j):
    global row, col
    row = i
    col = j
    map[row][col] = 'p'
    map[row+1][col+1] = '*'
    body.append(Player(row, col))
    printMap()
    movePlayer()

def movePlayer():
    global last_key, score
    while True:
        printMap()
        get_key = choises[random.randint(0, 3)]
        while (last_key == 'w' and get_key == 's') or (last_key == 'a' and get_key == 'd') or \
                (last_key == 's' and get_key == 'w') or (last_key == 'd' and get_key == 'a'):
            get_key = choises[random.randint(0, 3)]
        print("last_key: ", last_key)
        print("get_key: ", get_key)
        print("score: ", score)
        last_key = get_key
        switcher = {
            'w': goUp,
            'a': goLeft,
            's': goDown,
            'd': goRight,
        }
        switcher[get_key]()

# False mean there was no wall
def checkForWall(i, j):
    if map[i][j] == '#':
        print("wall")
        return True
    return False

def checkForBody(i, j):
    if map[i][j] == 'p':
        print("body")
        return True
    return False

def checkForFood(i, j):
    global score
    if map[i][j] == '*':
        score = score + 1
        setFood()

def setFood():
    global food_i, food_j
    rand_i = random.randint(1, SIZE-1)
    rand_j = random.randint(1, SIZE-1)
    while map[rand_i][rand_j] == '#' or map[rand_i][rand_j] == 'p':
        rand_i = random.randint(1, SIZE - 1)
        rand_j = random.randint(1, SIZE - 1)
    food_i = rand_i
    food_j = rand_j
    map[rand_i][rand_j] = '*'


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
    print("up        ")
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
    print("left")
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
    print("down")
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
    print("right")
    checkForFood(row, col)
    move(row, col)
    time.sleep(0.1)
    return


def main():
    setBorder()
    startGame(4, 3)


if __name__ == '__main__':
    main()
