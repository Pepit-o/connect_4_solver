import pygame
import sys
from bitboard_class import Position
from solver import Solver


# Game Constants
ROWS = Position.HEIGHT
COLS = Position.WIDTH
CELL_SIZE = 100
WIDTH = COLS * CELL_SIZE
HEIGHT = (ROWS + 1) * CELL_SIZE
RADIUS = CELL_SIZE // 2 - 5

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 - Play vs AI")


def draw_board(screen, position):
    pygame.draw.rect(screen, BLUE, (0, CELL_SIZE, WIDTH, HEIGHT - CELL_SIZE))

    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.circle(screen, BLACK, (c * CELL_SIZE + CELL_SIZE // 2, (r + 1) * CELL_SIZE + CELL_SIZE // 2),
                               RADIUS)
            piece = get_piece_at(position, c, r)
            if piece == "X":
                pygame.draw.circle(screen, RED, (c * CELL_SIZE + CELL_SIZE // 2, (r + 1) * CELL_SIZE + CELL_SIZE // 2),
                                   RADIUS)
            elif piece == "O":
                pygame.draw.circle(screen, YELLOW,
                                   (c * CELL_SIZE + CELL_SIZE // 2, (r + 1) * CELL_SIZE + CELL_SIZE // 2), RADIUS)
    pygame.display.update()


def get_piece_at(position, col, row):
    # Returns the piece ('X' or 'O') at a given board position
    bitmask = 1 << ((col * (Position.HEIGHT + 1)) + row)
    if position.current_position & bitmask:
        return "X" if position.moves % 2 == 0 else "O"
    return None


def drop_piece(position, col):
    # Attempts to play a piece in the given column
    if position.can_play(col):
        position.play(col)
        return True
    return False


def check_victory(position):
    for col in range(COLS):
        if position.is_winning_move(col):
            return True
    return False


def ai_move(position, solver):
    # AI selects the best move using negamax
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    position = Position()
    solver = Solver()
    draw_board(screen, position)
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
                    if drop_piece(position, col):
                        draw_board(screen, position)
                        if check_victory(position):
                            print("Player Wins!")
                            game_over = True
                        turn = 1 - turn

            else:
                ai_col = ai_move(position, solver)
                if ai_col is not None:
                    drop_piece(position, ai_col)
                    draw_board(screen, position)
                    if check_victory(position):
                        print("AI Wins!")
                        game_over = True
                    turn = 1 - turn

        if game_over:
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
