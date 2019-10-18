SIZE = 4

map = [[0]*SIZE]*SIZE

def setBorder():
    for i in range(SIZE):
        for j in range(SIZE):
            if i == 0 or j == 0 or i == (SIZE-1) or j == (SIZE-1):
                map[i][j] = '#'
            else:
                map[i][j] = 'c'

            print("map[" + str(i) + "][" + str(j) + "]: " + map[i][j])


def printMap():
    for i in range(SIZE):
        print(map[i])

setBorder()
printMap()