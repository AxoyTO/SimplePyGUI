import pygame

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


def adjust_screen():
    screen = pygame.display.set_mode(GAME_WINDOW_SIZE)
    screen.fill(COLORS["BLACK"])
    return screen


def adjust_board():
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (CELL["WIDTH"] + CELL["MARGIN"])
                row = pos[1] // (CELL["HEIGHT"] + CELL["MARGIN"])

                try:
                    if board[row][column] == ' ':
                        if PLAYER_MARK == 'X':
                            board[row][column] = 'X'
                        elif PLAYER_MARK == 'O':
                            board[row][column] = 'O'
                        display_board()
                        print("Click ", pos, "board coordinates: ", row, column)
                except IndexError:
                    pass
        draw_board(screen)
        pygame.display.flip()


def display_board():
    for i in board:
        print(i)


def draw_board(screen):
    for row in range(10):
        for column in range(10):
            color = COLORS["WHITE"]
            if board[row][column] == 'X':
                color = COLORS["GREEN"]
            elif board[row][column] == 'O':
                color = COLORS["RED"]
            pygame.draw.rect(screen,
                             color,
                             [(CELL["MARGIN"] + CELL["WIDTH"]) * column + CELL["MARGIN"],
                                 (CELL["MARGIN"] + CELL["HEIGHT"]) *
                                 row + CELL["MARGIN"],
                                 CELL["WIDTH"], CELL["HEIGHT"]])


def check_status(board):
    display_board()
# def set_turn(player):


#start()
pygame.quit()
