import getch


SIZE = 10

map = [[0 for i in range(SIZE)] for j in range(SIZE)]

def setBorder():
    for i in range(SIZE):
        for j in range(SIZE):
            if i == 0 or j == 0 or i == (SIZE-1) or j == (SIZE-1):
                map[i][j] = '#'
            else:
                map[i][j] = ' '

            # print("map[" + str(i) + "][" + str(j) + "]: " + map[i][j])


def printMap():
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
        get_key = getch.getch()
        switcher = {
            'w': goUp,
            'a': goLeft,
            's': goDown,
            'd': goRight,
        }
        try:
            # while kbhit()       -------------->     khoob chon fahmidam kbhit() baraye windows o linux fargh dare, kolln bikhialesh shodam :(
            switcher[get_key](i, j)
        except:
            print("invalid input")

def goUp(i, j):
    print("up")

def goLeft(i, j):
    print("left")

def goDown(i , j):
    print("down")

def goRight(i, j):
    print("right")

setBorder()
setPlayer(4, 3)



