import random
from time import sleep
import pygame
import os

COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
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
font = pygame.font.SysFont(pygame.font.get_fonts()[random.randint(1, 3)], 16)
game_over_texts = ['[X] WINS. ', '[O] WINS.', 'DRAW. ']
game_over_texts = [x + ' RETURNING TO MAIN MENU.' for x in game_over_texts]
x_wins_text = font.render(
    game_over_texts[0], True, COLORS['RED'], COLORS['BLACK'])
o_wins_text = font.render(
    game_over_texts[1], True, COLORS['RED'], COLORS['BLACK'])
no_winner_text = font.render(
    game_over_texts[2], True, COLORS['RED'], COLORS['BLACK'])

board = []

current_dir = os.getcwd()
if '2_Tic-tac-toe' not in current_dir:
    current_dir = os.path.join(current_dir, '2_Tic-tac-toe')
o_button_path = os.path.join(current_dir, 'assets', 'o.png')
x_button_path = os.path.join(current_dir, 'assets', 'x.png')

x_img = pygame.image.load(x_button_path)
o_img = pygame.image.load(o_button_path)

x_img = pygame.transform.scale(x_img, (40, 40))
o_img = pygame.transform.scale(o_img, (40, 40))


def start():
    screen = adjust_screen()
    adjust_board()

    turn_specifier = 0

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
                if turn_specifier == 0:
                    try:
                        if board[row][column] == ' ':
                            print(
                                f'[{PLAYER_MARK}] Player\'s Turn: {row,column}')
                            board[row][column] = PLAYER_MARK
                            screen.blit(o_img, closest_cell(row, column)) if PLAYER_MARK == 'O' else screen.blit(
                                x_img, closest_cell(row, column))
                            display_board()
                            turn_specifier = computer_turn(screen)
                            display_board()
                            state = check_state()
                            if state != ' ':
                                if state == 'D':
                                    screen.blit(no_winner_text, (10, 10))
                                elif state == 'X':
                                    screen.blit(x_wins_text, (10, 10))
                                else:
                                    screen.blit(o_wins_text, (10, 10))
                                game_is_running = False
                                pygame.display.flip()
                                sleep(5)
                    except IndexError:
                        pass
        pygame.display.flip()


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


def computer_turn(screen):
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    while board[x][y] != ' ':
        x = random.randint(0, 9)
        y = random.randint(0, 9)
    print(f'[{COMPUTER_MARK}] Computer\'s Turn: {x,y}')
    board[x][y] = COMPUTER_MARK
    screen.blit(o_img, closest_cell(x, y)) if COMPUTER_MARK == 'O' else screen.blit(
        x_img, closest_cell(x, y))
    return 0


def display_board():
    for i in board:
        print(i)
    print("===================================================")


def closest_cell(row, column):
    pos = column*40, row*40
    return pos


def check_state():
    flat_board = [i for x in board for i in x]
    if draw_check(flat_board):
        return 'D'

    winner = horizontal_check(flat_board)
    if winner != ' ':
        announce_result(winner)
        return winner

    winner = vertical_check(flat_board)
    if winner != ' ':
        announce_result(winner)
        return winner

    winner = diagonal_check(flat_board)
    if winner != ' ':
        announce_result(winner)
        return winner

    return ' '


def draw_check(flat_board):
    for i in flat_board:
        if i == ' ':
            return False

    return True


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


pygame.quit()
