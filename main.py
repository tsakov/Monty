import pygame
from pygame.locals import *
from board import *
from menu import *
from save import *
from sys import exit


class Game:
    def __init__(self):
        self.current_menu = main_menu
        self.current_board = None
        self.clock = pygame.time.Clock()

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)

        #draw caption
        text = font.render(self.current_menu.caption, True, (0, 255, 0))
        text_pos = text.get_rect()
        text_pos.centerx = self.screen.get_rect().centerx
        text_pos.centery = 50
        self.screen.blit(text, text_pos)

        #draw menu items
        for i in range(1, len(self.current_menu.items) + 1):
            text = font.render('{0}. {1}'.
                               format(i, self.current_menu.items[i]),
                               True, (0, 255, 0))
            text_pos = text.get_rect()
            text_pos.centerx = self.screen.get_rect().centerx
            text_pos.centery = 100 + 75 * i
            self.screen.blit(text, text_pos)

        pygame.display.flip()

    def draw_board(self):
        self.screen.fill((0, 0, 0))

        #draw snake
        for i in range(len(self.current_board.snake.body)):
            (y, x) = self.current_board.snake.body[i]
            green = (0,
                     126 + 129 * i // (len(self.current_board.snake.body) - 1),
                     0)
            pygame.draw.circle(self.screen, green, (10 * x + 5, 10 * y + 5), 5)

        #draw walls
        for (y, x) in self.current_board.walls:
            pygame.draw.rect(self.screen, (155, 155, 155),
                             pygame.Rect(10 * x, 10 * y, 10, 10))

        #draw score
        font = pygame.font.Font(None, 20)
        text = font.render('Score: {0}  Target: {1}'.format(
            self.current_board.score,
            self.current_board.target),
                           True, (255, 255, 255))
        self.screen.blit(text, (10, 468))

        #draw apple
        (y, x) = self.current_board.apple
        pygame.draw.circle(self.screen, (255, 0, 0),
                           (10 * x + 5, 10 * y + 5), 5)

        pygame.display.flip()

    def game_input(self, key, snake):
        if key[K_LEFT] or key[K_a]:
            snake.turn(directions['left'])
        elif key[K_UP] or key[K_w]:
            snake.turn(directions['up'])
        elif key[K_RIGHT] or key[K_d]:
            snake.turn(directions['right'])
        elif key[K_DOWN] or key[K_s]:
            snake.turn(directions['down'])

    def in_main_menu(self):
        self.current_menu = main_menu
        self.draw_menu()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYUP:
                    key = event.key
                    if key == K_1:
                        return 'in_level_selection_menu'
                    elif key == K_2:
                        file_name = input("load file name: ")
                        board = load(file_name)
                        if board:
                            print("done")
                            self.current_board = board
                            return 'in_pause_menu'
                        else:
                            print('error loading file')
                    elif key == K_3:
                        exit()

    def in_level_selection_menu(self):
        self.current_menu = level_selection_menu
        self.draw_menu()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYUP:
                    key = event.key
                    if key == K_1:
                        self.current_board = Board(1, False)
                        return 'in_game'
                    elif key == K_2:
                        self.current_board = Board(1, True)
                        return 'in_game'
                    elif key == K_3:
                        self.current_board = Board(25, False, True)
                        return 'in_game'
                    elif key == K_4:
                        return 'in_main_menu'

    def in_pause_menu(self):
        self.current_menu = pause_menu
        self.draw_menu()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYUP:
                    key = event.key
                    if key == K_1 or key == K_ESCAPE:
                        return 'in_game'
                    elif key == K_2:
                        file_name = input("save file name: ")
                        save(file_name, self.current_board)
                        print("done!")
                    elif key == K_3:
                        file_name = input("load file name: ")
                        board = load(file_name)
                        if board:
                            print("done")
                            self.current_board = board
                            return 'in_pause_menu'
                        else:
                            print('error loading file')
                    elif key == K_4:
                        return 'in_main_menu'

    def in_dead_menu(self):
        self.current_menu = dead_menu
        self.draw_menu()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYUP:
                    key = event.key
                    if key == K_1 or key == K_ESCAPE:
                        return 'in_level_selection_menu'
                    elif key == K_2:
                        return 'in_main_menu'

    def in_next_level_menu(self):
        self.current_menu = next_level_menu
        self.draw_menu()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYUP:
                    key = event.key
                    if key == K_1 or key == K_ESCAPE:
                        self.current_board = Board(
                            self.current_board.level_difficulty + 1,
                            self.current_board.random_levels)
                        return 'in_game'
                    elif key == K_2:
                        file_name = input("save file name: ")
                        save(file_name, self.current_board)
                        print("done!")
                    elif key == K_3:
                        return 'in_main_menu'

    def in_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYUP and event.key == K_ESCAPE:
                    return 'in_pause_menu'

            key = pygame.key.get_pressed()
            self.game_input(key, self.current_board.snake)

            try:
                self.draw_board()
                self.current_board.step()
            except Exception as e:
                return 'in_dead_menu'

            if self.current_board.level_completed:
                return 'in_next_level_menu'

            #self.clock.tick(14 + self.current_board.level_difficulty / 2.5)
            self.clock.tick(10 + self.current_board.level_difficulty / 5)

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Monty the Python")

        state = 'in_main_menu'
        while True:
            state = Game.__dict__[state](self)


if __name__ == '__main__':
    Game().run()
