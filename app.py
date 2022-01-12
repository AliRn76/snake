import operator
import random
import time
import os


choices = ['a', 'w', 's', 'd']
SIZE = 20   # Size Of The Map
SLEEP = 0.001
DEBUG = False
board = [['0' for i in range(SIZE)] for j in range(SIZE)]
snakes = []
food_row: int
food_col: int


class Snake:
    def __init__(self, id):
        self.id = id
        self.key: str
        self.last_key = ''
        self.body = []
        self.paths = []
        self.final_path = []
        self.length = 1
        self.temp_len = self.length
        self._set_snake_head()
        self.row = random.randint(1, SIZE - 1)
        self.col = random.randint(1, SIZE - 1)

    def _set_snake_head(self):
        self.row = random.randint(1, SIZE - 1)
        self.col = random.randint(1, SIZE - 1)
        while board[self.row][self.col] in ['#', 'P']:
            self.row = random.randint(1, SIZE - 1)
            self.col = random.randint(1, SIZE - 1)
        board[self.row][self.col] = 'P'
        self.body.append((self.row, self.col))

    def _set_key_with_ai(self):
        next_pos = self._find_path()
        if next_pos is None:
            return print("\n* I'm Done *\n\n")
        new_row = next_pos[0]
        new_col = next_pos[1]
        if new_row > self.row:
            self.key = 's'
        elif new_row < self.row:
            self.key = 'w'
        elif new_col > self.col:
            self.key = 'd'
        else:
            self.key = 'a'

    def _set_key_randomly(self):
        self.key = random.choice(choices)
        while (self.last_key == 'w' and self.key == 's') or (self.last_key == 'a' and self.key == 'd') or \
                (self.last_key == 's' and self.key == 'w') or (self.last_key == 'd' and self.key == 'a'):
            self.key = random.choice(choices)

    def _set_key_manually(self):
        self.key = input()

    def run(self):
        try:
            self._set_key_with_ai()
            # self.set_key_randomly()
        except RecursionError:
            # IF AI Couldn't Find the path to food, we use random choice
            self._set_key_randomly()

        # self._set_key_manually()

        self.last_key = self.key
        switcher = {
            'w': self._go_up,
            'a': self._go_left,
            's': self._go_down,
            'd': self._go_right,
        }
        switcher[self.key]()

        # Clean the board
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] == '.':
                    board[i][j] = ' '

    def _go_up(self):
        if check_for_wall(self.row-1, self.col):  # Check For Wall
            return
        if check_for_body(self.row-1, self.col):  # Check For Body
            return
        self.row -= 1  # Set New Row For Head Of Body
        self._check_for_food()  # Check For Food In New Position
        self._move()  # Move The Body
        time.sleep(SLEEP)
        return

    def _go_left(self):
        if check_for_wall(self.row, self.col-1):
            return
        if check_for_body(self.row, self.col-1):
            return
        self.col -= 1
        self._check_for_food()
        self._move()
        time.sleep(SLEEP)
        return

    def _go_down(self):
        if check_for_wall(self.row+1, self.col):
            return
        if check_for_body(self.row+1, self.col):
            return
        self.row += 1
        self._check_for_food()
        self._move()
        time.sleep(SLEEP)
        return

    def _go_right(self):
        if check_for_wall(self.row, self.col+1):
            return
        if check_for_body(self.row, self.col+1):
            return
        self.col += 1
        self._check_for_food()
        self._move()
        time.sleep(SLEEP)
        return

    def _check_for_food(self):
        """
        Increment the length if there was a food
        """
        if board[self.row][self.col] == '*':
            self.length += 1
            set_food()

    def _move(self):
        head = self.body[-1]
        board[head[0]][head[1]] = 'p'  # Set the last head as body

        # Is He Ate The Food Or Not
        # print(self.body)
        if self.temp_len == self.length:
            self.body.reverse()
            last = self.body.pop()  # Remove the last piece
            board[last[0]][last[1]] = ' '
            self.body.reverse()
        else:
            # snake just ate a food so just append a new head to body
            self.temp_len = self.length

        self.body.append((self.row, self.col))
        board[self.row][self.col] = 'P'  # Set new head

    def _find_path(self):
        self.paths.clear()
        self.final_path.clear()
        self.a_star(self.row, self.col)
        # print('here')
        # print_board()
        # time.sleep(0.1)
        next_pos = self.final_pos(food_row, food_col)
        return next_pos

    def _calc_h_cost(self, row: int, col: int):
        """
        Calculate the H Cost
        """
        global food_row, food_col
        h_row = abs(food_row - row)
        h_col = abs(food_col - col)
        h_cost = h_row + h_col
        return h_cost

    def _calc_g_cost(self, row: int, col: int):
        """
        Calculate the G Cost
        """
        g_row = abs(row - self.row)
        g_col = abs(col - self.col)
        g_cost = g_row + g_col
        return g_cost

    def _calc_f_cost(self, row: int, col: int):
        """ Calculate the F Cost """
        f_cost = 2 * self._calc_h_cost(row, col) + self._calc_g_cost(row, col)
        return f_cost

    def final_pos(self, row, col):
        global food_row, food_col

        states = [(-1, 0),
                  (0, -1), (0, 1),
                  (1, 0)]
        for index in range(len(states)):
            new_row = row + (states[index][0])
            new_col = col + (states[index][1])
            if board[new_row][new_col] in ['.', 'P']:
                g_and_pos = (self._calc_g_cost(row, col), new_row, new_col)
                self.final_path.append(g_and_pos)
            else:
                continue

        # Sort The Array of Costs
        self.final_path.sort(key=operator.itemgetter(0))

        try:
            new_row = self.final_path[0][1]
            new_col = self.final_path[0][2]
        except IndexError:
            return self.a_star(row, col)

        # print(path)
        if self.final_path[0][0] == 0:
            # If H_cost(g_cost of food with head) of Snake == 0
            next_pos = (food_row, food_col)
            return next_pos

        elif self._calc_g_cost(new_row, new_col) == 1:
            next_pos = (new_row, new_col)
            if DEBUG:
                print_board()
            return next_pos

        else:
            # Pop The Head cause we used it
            self.final_path.reverse()
            self.final_path.pop()
            return self.final_pos(new_row, new_col)

    def a_star(self, row: int, col: int):
        """
        Give it current snake head row and col, it will leave you the path with '.' in board
        """
        # All The Possible Ways For Next Move
        states = [(-1, 0),
                  (0, -1), (0, 1),
                  (1, 0)]

        # Check For Wall and Body For Next Move, We Have 4 Possible Move
        for _ in range(len(states)):
            new_row = row + (states[_][0])
            new_col = col + (states[_][1])
            try:
                new_location = board[new_row][new_col]
                if not (new_location in ['p', 'P', '#', '.', '*']):
                    f_and_pos = (self._calc_f_cost(new_row, new_col), new_row, new_col)
                    self.paths.append(f_and_pos)
                else:
                    continue
            except IndexError:
                continue

        # Sort The Array of Costs
        self.paths.sort(key=operator.itemgetter(0))
        try:
            new_row = self.paths[0][1]
            new_col = self.paths[0][2]
        except IndexError:
            return self.a_star(row, col)

        if self._calc_h_cost(new_row, new_col) == 1:
            board[new_row][new_col] = '.'
            # Print the final path
            # print_board()
            # This Func just set the '.' in board , and we will use it for pathfinding
            return

        else:
            # Pop The Head cause we used it
            self.paths.reverse()
            self.paths.pop()
            board[new_row][new_col] = '.'
            # if DEBUG:
            #     print_board()
            return self.a_star(new_row, new_col)


def set_walls():
    """
    Create empty board and Set the walls
    """
    global board
    for i in range(SIZE):
        for j in range(SIZE):
            board[i][j] = '#' if i in [0, SIZE-1] or j in [0, SIZE-1] else ' '

def print_scores():
    # print('\033[{y};{x}H'.format(y=0, x=SIZE))
    _snakes = sorted(snakes, key=lambda x: x.length, reverse=True)
    print('\nRanking: \n')
    for s in _snakes:
        print(f'Snake {s.id}: ', s.length)

def print_board():
    """
    Print the board in console
    """
    global board

    # os.system('cls')  # on Windows System
    os.system('clear')  # on Linux System
    # print("\033[%d;%dH" % (0, 0))

    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 'p':
                print(u"\U0001F538", end='')
            elif board[i][j] == 'P':
                print(u"\U0001F920", end='')
                # print(u"\U0001F960", end='')
            elif board[i][j] == '*':
                print(u"\U0001F355", end='')
            elif board[i][j] == '#':
                if i in [0, SIZE-1]:
                    print(u"\u2588"u"\u2588", end='')
                else:
                    print(u"\u2588", end='  ')
            else:
                print(board[i][j], end=' ')
        print()
    print_scores()

def set_food():
    """
    Set Food in random position in board
    """
    global food_row, food_col
    food_row = random.randint(1, SIZE - 1)
    food_col = random.randint(1, SIZE - 1)
    while board[food_row][food_col] in ['#', 'P', 'p']:
        food_row = random.randint(1, SIZE - 1)
        food_col = random.randint(1, SIZE - 1)
    board[food_row][food_col] = '*'

def check_for_wall(row: int, col: int) -> bool:
    """
    return True if there was a wall
    """
    try:
        return board[row][col] == '#'
    except IndexError:  # TODO: this is a bug (actually I don't know why this is happening)
        return True

def check_for_body(row: int, col: int) -> bool:
    """
    return True if there was a body
    """
    return board[row][col] == 'p'

def start(n: int):
    set_walls()

    for id in range(n):
        snakes.append(Snake(id))
    set_food()

    while True:
        for snake in snakes:
            print_board()
            snake.run()

def main():
    start(15)


if __name__ == '__main__':
    main()

