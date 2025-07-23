import pygame
import sys
from copy import deepcopy


def is_board_full_(board):
    for row in board:
        if 'NA' in row:
            return False
    return True


def valid_moves(board) -> list:
    moves = []
    columns_order = [3, 2, 4, 1, 5, 0, 6]

    for col in columns_order:
        for row in range(5, -1, -1):
            if board[row][col] == 'NA':
                moves.append([row, col])
                break
    return moves


def get_all_windows(board):
    rows = 6
    cols = 7
    windows = []

    for row in range(rows):
        for col in range(cols - 3):
            window = [board[row][col + i] for i in range(4)]
            if any(cell != 'NA' for cell in window):
                windows.append(window)

    for col in range(cols):
        for row in range(rows - 3):
            window = [board[row + i][col] for i in range(4)]
            if any(cell != 'NA' for cell in window):
                windows.append(window)

    for row in range(rows - 3):
        for col in range(cols - 3):
            window = [board[row + i][col + i] for i in range(4)]
            if any(cell != 'NA' for cell in window):
                windows.append(window)

    for row in range(3, rows):
        for col in range(cols - 3):
            window = [board[row - i][col + i] for i in range(4)]
            if any(cell != 'NA' for cell in window):
                windows.append(window)

    return windows


def check_victory(board, symbol):
    for row in range(6):
        for col in range(4):
            token = board[row][col]
            if token != 'NA' and token == board[row][col + 1] == board[row][col + 2] == board[row][col + 3]:
                if token == symbol:
                    return 1
                else:
                    return -1

    for col in range(7):
        for row in range(3):
            token = board[row][col]
            if token != 'NA' and token == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]:
                if token == symbol:
                    return 1
                else:
                    return -1

    for row in range(3):
        for col in range(4):
            token = board[row][col]
            if token != 'NA' and token == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]:
                if token == symbol:
                    return 1
                else:
                    return -1

    for row in range(3, 6):
        for col in range(4):
            token = board[row][col]
            if token != 'NA' and token == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]:
                if token == symbol:
                    return 1
                else:
                    return -1

    return 0


def score_window(window, symbol):
    score = 0
    token_count = window.count(symbol)
    empty_count = window.count('NA')

    if token_count == 4:
        score += 500
    if token_count == 3 and empty_count == 1:
        score += 100
    if token_count == 2 and empty_count == 2:
        score += 10
    return score


def evaluate_board(board, root_symbol, opp_symbol):
    score = 0

    for window in get_all_windows(board):
        root_score = score_window(window, root_symbol)
        opp_score = score_window(window, opp_symbol)
        score += root_score
        score -= opp_score * 10
    return score


def negamax_connect_4_ab(board, depth, color, root_symbol, opp_symbol, alpha, beta):
    score = -float('inf')
    if depth > 5 or is_board_full_(board):
        return evaluate_board(board, root_symbol, opp_symbol) * color

    moves = valid_moves(board)
    for play in moves:
        if color == 1:
            board[play[0]][play[1]] = root_symbol
        else:
            board[play[0]][play[1]] = opp_symbol

        score = max(score, -negamax_connect_4_ab(board, depth + 1, -color, root_symbol, opp_symbol, -beta, -alpha))
        board[play[0]][play[1]] = 'NA'
        alpha = max(alpha, score)

        if alpha >= beta:
            break

    return score


def play_one_shot_negamax_ab(board, depth, root_symbol, opp_symbol) -> tuple:
    all_moves = valid_moves(board)
    best_score = -float('inf')
    best_move = None

    alpha = -float('inf')
    beta = float('inf')

    for play in all_moves:
        board[play[0]][play[1]] = root_symbol
        score = -negamax_connect_4_ab(board, depth, -1, root_symbol, opp_symbol, -beta, -alpha)
        board[play[0]][play[1]] = 'NA'

        if score > best_score:
            best_score = score
            best_move = (play[0], play[1])
        alpha = max(alpha, best_score)

    return best_move


# Game Constants
ROWS = 6
COLS = 7
CELL_SIZE = 100
WIDTH = COLS * CELL_SIZE
HEIGHT = (ROWS + 1) * CELL_SIZE
RADIUS = CELL_SIZE // 2 - 5

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def create_board():
    return [['NA'] * COLS for _ in range(ROWS)]


def draw_board(screen, board):
    pygame.draw.rect(screen, BLUE, (0, CELL_SIZE, WIDTH, HEIGHT))

    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.circle(screen, BLACK, (c * CELL_SIZE + CELL_SIZE // 2, (r + 1) * CELL_SIZE + CELL_SIZE // 2),
                               RADIUS)
            if board[r][c] == 'X':
                pygame.draw.circle(screen, RED, (c * CELL_SIZE + CELL_SIZE // 2, (r + 1) * CELL_SIZE + CELL_SIZE // 2),
                                   RADIUS)
            elif board[r][c] == 'O':
                pygame.draw.circle(screen, YELLOW,
                                   (c * CELL_SIZE + CELL_SIZE // 2, (r + 1) * CELL_SIZE + CELL_SIZE // 2), RADIUS)
    pygame.display.update()


def drop_piece(board, col, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == 'NA':
            board[row][col] = symbol
            return True
    return False


def ai_move(board, ai_symbol, player_symbol):
    move = play_one_shot_negamax_ab(deepcopy(board), 0, ai_symbol, player_symbol)
    return move


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4")
    board = create_board()
    draw_board(screen, board)
    game_over = False
    turn = 0
    player_symbol = 'X'
    ai_symbol = 'O'

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if turn == 0:
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, CELL_SIZE))
                    posx = event.pos[0]
                    pygame.draw.circle(screen, RED, (posx, CELL_SIZE // 2), RADIUS)
                    pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // CELL_SIZE
                    if drop_piece(board, col, player_symbol):
                        draw_board(screen, board)
                        if check_victory(board, player_symbol):
                            print("Player wins!")
                            game_over = True
                        turn = 1 - turn
            else:
                ai_best_move = ai_move(board, ai_symbol, player_symbol)
                if ai_best_move:
                    drop_piece(board, ai_best_move[1], ai_symbol)
                    draw_board(screen, board)
                    if check_victory(board, ai_symbol):
                        print("AI wins!")
                        game_over = True
                    turn = 1 - turn
        if game_over:
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()


#############################################
# New bitboard-based implementation
#############################################

from bitboard_class import Position
from solver import Solver


def draw_board_bb(screen, position):
    pygame.draw.rect(screen, BLUE, (0, CELL_SIZE, WIDTH, HEIGHT))

    for r in range(Position.HEIGHT):
        for c in range(Position.WIDTH):
            pygame.draw.circle(screen, BLACK,
                               (c * CELL_SIZE + CELL_SIZE // 2, (r + 1) * CELL_SIZE + CELL_SIZE // 2),
                               RADIUS)
            bitmask = 1 << ((c * (Position.HEIGHT + 1)) + r)
            if position.mask & bitmask:
                if position.current_position & bitmask:
                    color = RED if position.moves % 2 == 0 else YELLOW
                else:
                    color = YELLOW if position.moves % 2 == 0 else RED
                pygame.draw.circle(screen, color,
                                   (c * CELL_SIZE + CELL_SIZE // 2, (r + 1) * CELL_SIZE + CELL_SIZE // 2),
                                   RADIUS)
    pygame.display.update()


def drop_piece_bb(position, col):
    if position.can_play(col):
        position.play(col)
        return True
    return False


def check_victory_bb(position):
    for col in range(Position.WIDTH):
        if position.is_winning_move(col):
            return True
    return False


def ai_move_bb(position, solver):
    best_score = -Position.WIDTH * Position.HEIGHT
    best_col = None

    for col in range(Position.WIDTH):
        if position.can_play(col):
            temp_pos = Position()
            temp_pos.current_position = position.current_position
            temp_pos.mask = position.mask
            temp_pos.moves = position.moves
            temp_pos.play(col)
            score = -solver.solve(temp_pos)
            if score > best_score:
                best_score = score
                best_col = col

    if best_col is None:
        for col in range(Position.WIDTH):
            if position.can_play(col):
                return col

    return best_col


def main_bitboard():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4 - Bitboard")

    position = Position()
    solver = Solver()
    draw_board_bb(screen, position)
    game_over = False
    turn = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if turn == 0:
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, CELL_SIZE))
                    posx = event.pos[0]
                    pygame.draw.circle(screen, RED, (posx, CELL_SIZE // 2), RADIUS)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // CELL_SIZE
                    if drop_piece_bb(position, col):
                        draw_board_bb(screen, position)
                        if check_victory_bb(position):
                            print("Player wins!")
                            game_over = True
                        turn = 1 - turn
            else:
                ai_col = ai_move_bb(position, solver)
                if ai_col is not None:
                    drop_piece_bb(position, ai_col)
                    draw_board_bb(screen, position)
                    if check_victory_bb(position):
                        print("AI wins!")
                        game_over = True
                    turn = 1 - turn

        if game_over:
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()
