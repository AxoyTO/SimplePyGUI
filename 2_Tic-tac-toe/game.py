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
                        elif PLAYER_MARK == 'O':
                            board[row][column] = 'O'
                        display_board()
                        state = check_state()
                        if state == 1:
                            game_is_running = False
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


def check_state():
    winner = horizontal_check()
    if winner != ' ':
        announce_result(winner)
        return 1

    winner = vertical_check()
    if winner != ' ':
        announce_result(winner)
        return 1

    winner = diagonal_check()
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


def horizontal_check():
    winner = ' '
    for i in range(len(board)):
        O_count = 0
        X_count = 0
        for j in range(len(board[i])):
            if O_count == 5:
                winner = 'X'
                break
            if X_count == 5:
                winner = 'O'
                break
            if board[i][j] == 'X':
                X_count += 1
                O_count = 0
            elif board[i][j] == 'O':
                O_count += 1
                X_count = 0
            else:
                O_count = 0
                X_count = 0

    return winner


def vertical_check():
    winner = ' '
    for i in range(len(board)):
        O_count = 0
        X_count = 0
        for j in range(len(board[i])):
            if O_count == 5:
                winner = 'X'
                break
            if X_count == 5:
                winner = 'O'
                break
            if board[j][i] == 'X':
                X_count += 1
                O_count = 0
            elif board[j][i] == 'O':
                O_count += 1
                X_count = 0
            else:
                O_count = 0
                X_count = 0

    return winner


def diagonal_check():
    winner = ' '

    flat_board = [j for sub in board for j in sub]

    for i in range(len(flat_board)+1):
        if flat_board[i] == flat_board[i+11] == flat_board[i+11*2] == flat_board[i+11*3] == flat_board[i+11*4] == 'X':
            winner = 'O'
            break
        elif flat_board[i] == flat_board[i+11] == flat_board[i+11*2] == flat_board[i+11*3] == flat_board[i+11*4] == 'O':
            winner = 'X'
            break

    return winner


start()
pygame.quit()
