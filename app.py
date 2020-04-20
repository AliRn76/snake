import random
import time

class Player:
    def __init__(self, i, j):
        self.i = i
        self.j = j


row = 0
col = 0
SIZE = 18
score = 1
temp_score = 1
last_key = ''
map = [[0 for i in range(SIZE)] for j in range(SIZE)]

body = []

choises = ['a', 'w', 's', 'd']

def setBorder():
    global map
    for i in range(SIZE):
        for j in range(SIZE):
            if i == 0 or j == 0 or i == (SIZE-1) or j == (SIZE-1):
                map[i][j] = '#'
            else:
                map[i][j] = ' '

            # print("map[" + str(i) + "][" + str(j) + "]: " + map[i][j])


def printMap():
    # print("\033[0;0H")
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

# f = 0
def movePlayer():
    # win = False
    # global f
    global last_key, score
    while True:
        # time.sleep(0.1)
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
        # f = f + 1
        # for s in range(len(body)):
        #     print(body[s].i, body[s].j, "        ")
        #     time.sleep(10.5)
        switcher[get_key]()
        # try:
        #     # print(f)
        #     # if f == 5 :
        #     for s in range(len(body)):
        #         print(body[s].i, body[s].j, "        ")
        #     #     time.sleep(10.5)
        #     switcher[get_key](i, j)
        # except:
        #     print("invalid input")

# False mean there was no wall
def checkForWall(i, j):
    if map[i][j] == '#':
        print("wall      ")
        return True
    return False

def checkForBody(i, j):
    if map[i][j] == 'p':
        print("body      ")
        return True
    return False

def checkForFood(i, j):
    global score
    if map[i][j] == '*':
        # print("food      ")
        score = score + 1
        setFood()

def setFood():
    rand_i = random.randint(1, SIZE-1)
    rand_j = random.randint(1, SIZE-1)
    while map[rand_i][rand_j] == '#' or map[rand_i][rand_j] == 'p':
        rand_i = random.randint(1, SIZE - 1)
        rand_j = random.randint(1, SIZE - 1)
    map[rand_i][rand_j] = '*'


def move(i, j):
    global temp_score, score

    # print("tmp_scr: ", temp_score)
    # print("score: ", score, "  ")
    if temp_score == score:
        body.reverse()
        body.pop()
        body.reverse()
        body.append(Player(i, j))
    else:
        body.append(Player(i, j))
        temp_score = score

    for i in range(SIZE):
        for j in range(SIZE):
            if map[i][j] == 'p' or map[i][j] == 'P':
                map[i][j] = ' '
    for number in range(score):
        if number == score-1:
            map[body[number].i][body[number].j] = 'P'
        else:
            map[body[number].i][body[number].j] = 'p'

def goUp():
    global row, col
    if checkForWall(row-1, col):
        return
    if checkForBody(row-1, col):
        return
    row = row - 1
    print("up        ")
    checkForFood(row, col)
    move(row, col)
    # map[i-1][j] = 'p'
    time.sleep(0.1)
    return


def goLeft():
    global row, col
    if checkForWall(row, col-1):
        return 
    if checkForBody(row, col-1):
        return
    col = col - 1
    print("left      ")
    checkForFood(row, col)
    move(row, col)
    # map[i][j-1] = 'p'
    time.sleep(0.1)
    return


def goDown():
    global row, col
    if checkForWall(row+1, col):
        return
    if checkForBody(row+1, col):
        return
    row = row + 1
    print("down      ")
    checkForFood(row, col)
    move(row, col)
    # map[i+1][j] = 'p'
    time.sleep(0.1)
    return


def goRight():
    global row, col
    if checkForWall(row, col+1):
        return
    if checkForBody(row, col+1):
        return
    col = col + 1
    print("right     ")
    checkForFood(row, col)
    move(row, col)
    # map[i][j+1] = 'p'
    time.sleep(0.1)
    return



setBorder()
startGame(4, 3)

