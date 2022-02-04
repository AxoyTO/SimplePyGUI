from math import ceil
import pygame
import os

COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GREEN": (0, 255, 0),
    "RED": (255, 0, 0)
}

PLAYER_MARK, COMPUTER_MARK = 'X', 'O'

BOARD = {
    "ROW_SIZE": 10,
    "COLUMN_SIZE": 10
}

CELL = {
    "WIDTH": 30,
    "HEIGHT": 30,
    "MARGIN": 9
}

GAME_WINDOW_SIZE = [400, 400]

pygame.font.init()


font = pygame.font.SysFont('Comic Sans MS', 30)
text = font.render('X', False, (0, 0, 0))
textRect = text.get_rect()
textRect.center = (114, 124)


board = []

current_dir = os.getcwd()
o_button_path = os.path.join(current_dir, 'assets', 'o.png')
x_button_path = os.path.join(current_dir, 'assets', 'x.png')

x_img = pygame.image.load(x_button_path)
o_img = pygame.image.load(o_button_path)

x_img = pygame.transform.scale(x_img, (40, 40))
o_img = pygame.transform.scale(o_img, (40, 40))


def adjust_screen():
    screen = pygame.display.set_mode(GAME_WINDOW_SIZE)
    screen.fill(COLORS["WHITE"])
    for i in range(1, 10):
        pygame.draw.line(screen, COLORS['BLACK'],
                         (400 / 10*i, 0), (400 / 10*i, 400), 2)
        pygame.draw.line(screen, COLORS['BLACK'],
                         (0, 400/10*i), (400, 400/10*i), 2)

    return screen


def adjust_board():
    board.clear()
    for row in range(BOARD["ROW_SIZE"]):
        board.append([])
        for column in range(BOARD["COLUMN_SIZE"]):
            board[row].append(' ')


def start():
    screen = adjust_screen()
    adjust_board()

    print('PLAYER_MARK: ', PLAYER_MARK)
    print('COMPUTER MARK: ', COMPUTER_MARK)

    game_is_running = True
    while game_is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (CELL["WIDTH"] + CELL["MARGIN"])
                row = pos[1] // (CELL["HEIGHT"] + CELL["MARGIN"])

                try:
                    if board[row][column] == ' ':
                        if PLAYER_MARK == 'X':
                            board[row][column] = 'X'
                            screen.blit(x_img, closest_cell(row, column))
                        elif PLAYER_MARK == 'O':
                            board[row][column] = 'O'
                            screen.blit(o_img, closest_cell(row, column))
                        display_board()
                        state = check_state()
                        if state == 1:
                            game_is_running = False
                        print("Click ", pos, "board coordinates: ", row, column)
                except IndexError:
                    pass
        pygame.display.flip()


def display_board():
    for i in board:
        print(i)


def closest_cell(row, column):
    pos = column*40, row*40
    print(pos)
    return pos


def check_state():
    flat_board = [i for x in board for i in x]

    winner = horizontal_check(flat_board)
    if winner != ' ':
        announce_result(winner)
        return 1

    winner = vertical_check(flat_board)
    if winner != ' ':
        announce_result(winner)
        return 1

    winner = diagonal_check(flat_board)
    if winner != ' ':
        announce_result(winner)
        return 1


def announce_result(winner):
    if winner == 'X':
        if PLAYER_MARK == 'O':
            print('You lost... Computer is the winner!')
        elif PLAYER_MARK == 'X':
            print('Good job!! You beat the computer, you are the winner!')
    else:
        if PLAYER_MARK == 'X':
            print('You lost... Computer is the winner!')
        elif PLAYER_MARK == 'O':
            print('Good job!! You beat the computer, you are the winner!')


def horizontal_check(flat_board):
    winner = ' '
    for i in range(len(flat_board)-4):
        if flat_board[i] == flat_board[i+1] == flat_board[i+2] == flat_board[i+3] == flat_board[i+4] == 'X':
            winner = 'O'
            break
        elif flat_board[i] == flat_board[i+1] == flat_board[i+2] == flat_board[i+3] == flat_board[i+4] == 'O':
            winner = 'X'
            break
    return winner


def vertical_check(flat_board):
    winner = ' '

    for i in range(int(len(flat_board)/2)+10):
        if flat_board[i] == flat_board[i+10] == flat_board[i+10*2] == flat_board[i+10*3] == flat_board[i+10*4] == 'X':
            winner = 'O'
            break
        elif flat_board[i] == flat_board[i+10] == flat_board[i+10*2] == flat_board[i+10*3] == flat_board[i+10*4] == 'O':
            winner = 'X'
            break

    return winner


def diagonal_check(flat_board):
    winner = ' '
    for i in range(len(flat_board)+1):
        if flat_board[i] == flat_board[i+11] == flat_board[i+11*2] == flat_board[i+11*3] == flat_board[i+11*4] == 'X' or \
                flat_board[i] == flat_board[i+9] == flat_board[i+9*2] == flat_board[i+9*3] == flat_board[i+9*4] == 'X':
            winner = 'O'
            break
        elif flat_board[i] == flat_board[i+11] == flat_board[i+11*2] == flat_board[i+11*3] == flat_board[i+11*4] == 'O' or \
                flat_board[i] == flat_board[i+9] == flat_board[i+9*2] == flat_board[i+9*3] == flat_board[i+9*4] == 'O':
            winner = 'X'
            break

    return winner


start()
pygame.quit()
