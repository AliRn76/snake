import random
import time


SIZE = 20

map = [[0 for i in range(SIZE)] for j in range(SIZE)]

choises = ['a', 'w', 's', 'd']

def setBorder():
    for i in range(SIZE):
        for j in range(SIZE):
            if i == 0 or j == 0 or i == (SIZE-1) or j == (SIZE-1):
                map[i][j] = '#'
            else:
                map[i][j] = ' '

            # print("map[" + str(i) + "][" + str(j) + "]: " + map[i][j])


def printMap():
    print("\033[0;0H")
    for i in range(SIZE):
        for j in range(SIZE):
            if map[i][j] == 'p':
                print('O', end=' ')
            else:
                print(map[i][j], end=' ')
        print()

def setPlayer(i, j):
    map[i][j] = 'p'
    printMap()
    movePlayer(i, j)

def movePlayer(i, j):
    win = False

    while True:
        time.sleep(0.5)
        printMap()
        get_key = choises[random.randint(0,3)]
        switcher = {
            'w': goUp,
            'a': goLeft,
            's': goDown,
            'd': goRight,
        }
        try:
           switcher[get_key](i, j)
        except:
            print("invalid input")

# False mean there was no wall
def checkForWall(i, j):
    if map[i][j] == '#':
        print("wall ")
        return True
    return False
    
    
def goUp(i, j):
    if checkForWall(i-1, j):
        movePlayer(i, j)
        
    print("up   ")
    map[i][j] = ' '
    map[i-1][j] = 'p'
    movePlayer(i-1, j)


def goLeft(i, j):
    if checkForWall(i, j-1):
        movePlayer(i, j)
        
    print("left ")
    map[i][j] = ' '
    map[i][j-1] = 'p'
    movePlayer(i, j-1)


def goDown(i , j):
    if checkForWall(i+1, j):
        movePlayer(i, j)
        
    print("down ")
    map[i][j] = ' '
    map[i+1][j] = 'p'
    movePlayer(i+1, j)


def goRight(i, j):
    if checkForWall(i, j+1):
        movePlayer(i, j)
        
    print("right")
    map[i][j] = ' '
    map[i][j+1] = 'p'
    movePlayer(i, j+1)
    
setBorder()
setPlayer(4, 3)

