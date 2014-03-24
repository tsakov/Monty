import random

BOARD_WIDTH = 64
BOARD_HEIGHT = 48

directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}


class Snake:
    def __init__(self, x, y):
        self.body = [(x, y - 2), (x, y - 1), (x, y)]
        self.direction = directions['right']

    def head(self):
        return self.body[-1]

    def tail(self):
        return self.body[0]

    def new_head(self):
        return tuple(map(lambda x, y, m: (x + y + m) % m,
                         self.head(), self.direction,
                         (BOARD_HEIGHT, BOARD_WIDTH)))

    def step(self, eaten):
        self.body.append(self.new_head())
        if not eaten:
            self.body.pop(0)

    def turn(self, new_direction):
        if tuple(map(lambda x, y: x + y, self.direction, new_direction)) != (0, 0):
            self.direction = new_direction


class Board:
    def __init__(self, level_difficulty, random_levels, free_run=False):
        self.walls = []

        if not free_run:
            for i in range(BOARD_WIDTH):
                self.walls.extend([(0, i), (BOARD_HEIGHT - 1, i)])
            for i in range(1, BOARD_HEIGHT - 1):
                self.walls.extend([(i, 0), (i, BOARD_WIDTH - 1)])

        self.snake = Snake(1, 3)

        if random_levels and not free_run:
            self.generate_walls()

        self.apple = self.generate_apple()
        self.level_difficulty = level_difficulty
        self.random_levels = random_levels
        self.score = 0
        if free_run:
            self.target = 'Survive!'
        else:
            self.target = 5 + level_difficulty * 5
        self.level_completed = False

    def step(self):
        head = self.snake.new_head()

        if head in self.walls + self.snake.body:
            raise Exception("dead")

        self.snake.step(head == self.apple)

        if head == self.apple:
            self.apple = self.generate_apple()
            self.score += 1
            if self.score == self.target:
                self.level_completed = True

    def generate_apple(self):
        (x, y) = self.snake.head()

        while True:
            while (x, y) in self.walls + self.snake.body:
                x = random.randrange(1, BOARD_HEIGHT - 1)
                y = random.randrange(1, BOARD_WIDTH - 1)

            surroundings = 0
            for (dx, dy) in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
                if (x + dx, y + dy) in self.walls:
                    surroundings += 1

            if surroundings < 3:
                return (x, y)

    def generate_walls(self):
        x = random.randrange(BOARD_HEIGHT / 4, BOARD_HEIGHT / 2)
        y = random.randrange(BOARD_WIDTH / 4, BOARD_WIDTH / 2)

        x_limit = (x == BOARD_HEIGHT / 2 - 1)
        y_limit = (y == BOARD_WIDTH / 2 - 1)

        k = random.randrange(10, (BOARD_WIDTH + BOARD_HEIGHT) / 2)

        while x > x_limit and y > y_limit and k > 0:
            self.walls.extend([(x, y), (BOARD_HEIGHT - 1 - x, y),
                               (x, BOARD_WIDTH - 1 - y),
                               (BOARD_HEIGHT - 1 - x, BOARD_WIDTH - 1 - y)])
            if random.randrange(2):
                x -= 1
            else:
                y -= 1
            k -= 1

        if x == 0:
            self.snake.direction = directions['down']
            self.snake.body = [(1, 1), (2, 1), (3, 1)]
