class Menu:
    def __init__(self, caption, items):
        self.caption = caption
        self.items = items


main_menu = Menu('Monty the Python', {1: 'Start new game',
                                      2: 'Load an existing game',
                                      3: 'Quit'})

pause_menu = Menu('Game paused', {1: 'Resume game',
                                  2: 'Save game',
                                  3: 'Load game',
                                  4: 'Exit to main menu'})

level_selection_menu = Menu('Level selection', {1: 'Plain levels',
                                                2: 'Random levels',
                                                3: 'Free run',
                                                4: 'Go back'})

dead_menu = Menu("Don't eat that next time!", {1: 'Start new game',
                                               2: 'Exit to main menu'})

next_level_menu = Menu('Level completed!', {1: 'Go on',
                                            2: 'Save game',
                                            3: 'Exit to main menu'})
