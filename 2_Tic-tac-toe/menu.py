import pygame
import pygame_menu
import game


pygame.init()


def set_mark(value, mark):
    game.PLAYER_MARK = mark
    game.COMPUTER_MARK = 'O' if mark == 'X' else 'X'


def start():
    screen = pygame.display.set_mode((400, 400))
    menu = pygame_menu.Menu('Tic-tac-toe YLAB', 400, 400,
                            theme=pygame_menu.themes.THEME_DARK)

    menu.add.clock()
    menu.add.selector(
        'Mark :', [('X', 'X'), ('O', 'O')], onchange=set_mark)

    menu.add.button('Play', game.start)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)


# start()
