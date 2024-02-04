import pygame
import sys

pygame.init()

# The screen dimensions
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3

# RGB colors
PURPLE = (186, 85, 211)
BG_COLOR = (128, 0, 128)
LINE_COLOR = (186, 85, 211)
PLAYER_X = 1
PLAYER_O = 2

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)

# The Tic-Tac-Toe board
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# Function to draw the lines for the Tic-Tac-Toe board
def draw_lines():
    # Draw horizontal lines
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, PURPLE, (0, row * HEIGHT // BOARD_ROWS), (WIDTH, row * HEIGHT // BOARD_ROWS), LINE_WIDTH)
    # Draw vertical lines
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, PURPLE, (col * WIDTH // BOARD_COLS, 0), (col * WIDTH // BOARD_COLS, HEIGHT), LINE_WIDTH)

def draw_symbols():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == PLAYER_X:
                # Draw X
                pygame.draw.line(screen, PURPLE, (col * WIDTH // BOARD_COLS, row * HEIGHT // BOARD_ROWS),
                                 ((col + 1) * WIDTH // BOARD_COLS, (row + 1) * HEIGHT // BOARD_ROWS), LINE_WIDTH)
                pygame.draw.line(screen, PURPLE, ((col + 1) * WIDTH // BOARD_COLS, row * HEIGHT // BOARD_ROWS),
                                 (col * WIDTH // BOARD_COLS, (row + 1) * HEIGHT // BOARD_ROWS), LINE_WIDTH)
            elif board[row][col] == PLAYER_O:
                # Draw O
                pygame.draw.circle(screen, PURPLE,
                                   (col * WIDTH // BOARD_COLS + WIDTH // BOARD_COLS // 2, row * HEIGHT // BOARD_ROWS + HEIGHT // BOARD_ROWS // 2),
                                   min(WIDTH // BOARD_COLS, HEIGHT // BOARD_ROWS) // 2 - LINE_WIDTH, LINE_WIDTH)

def make_move(row, col, player):
    if board[row][col] == 0:
        board[row][col] = player
        return True
    else:
        return False

def is_winner(player):
    for row in range(BOARD_ROWS):
        if all([board[row][col] == player for col in range(BOARD_COLS)]):
            return True
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True
    if all([board[i][i] == player for i in range(min(BOARD_ROWS, BOARD_COLS))]) or all(
            [board[i][BOARD_COLS - i - 1] == player for i in range(min(BOARD_ROWS, BOARD_COLS))]):
        return True
    return False

def is_board_full():
    return all([board[row][col] != 0 for row in range(BOARD_ROWS) for col in range (BOARD_COLS)])

def restart_game():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

# Main game loop
current_player = PLAYER_X
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if game_over:
            continue
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = x // (WIDTH // BOARD_COLS)
            row = y // (HEIGHT // BOARD_ROWS)
            if make_move(row, col, current_player):
                current_player = PLAYER_X if current_player == PLAYER_O else PLAYER_O
                if is_winner(PLAYER_X):
                    game_over = True
                    print("Player X wins!")
                elif is_winner(PLAYER_O):
                    game_over = True
                    print("Player O wins!")
                elif is_board_full():
                    game_over = True
                    print("It's a draw!")
    screen.fill(BG_COLOR)
    draw_lines()
    draw_symbols()
    pygame.display.update()
