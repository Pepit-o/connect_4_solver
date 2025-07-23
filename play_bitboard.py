try:
    import pygame
except ImportError:
    pygame = None
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


def init_screen():
    if not pygame:
        raise RuntimeError("pygame is required to run this UI")
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4 - Bitboard")
    return screen


def draw_board(screen, position):
    pygame.draw.rect(screen, BLUE, (0, CELL_SIZE, WIDTH, HEIGHT))

    for r in range(Position.HEIGHT):
        for c in range(Position.WIDTH):
            pygame.draw.circle(
                screen,
                BLACK,
                (c * CELL_SIZE + CELL_SIZE // 2, (r + 1) * CELL_SIZE + CELL_SIZE // 2),
                RADIUS,
            )
            bitmask = 1 << ((c * (Position.HEIGHT + 1)) + r)
            if position.mask & bitmask:
                if position.current_position & bitmask:
                    color = RED if position.moves % 2 == 0 else YELLOW
                else:
                    color = YELLOW if position.moves % 2 == 0 else RED
                pygame.draw.circle(
                    screen,
                    color,
                    (c * CELL_SIZE + CELL_SIZE // 2, (r + 1) * CELL_SIZE + CELL_SIZE // 2),
                    RADIUS,
                )
    pygame.display.update()


def drop_piece(position, col):
    if position.can_play(col):
        position.play(col)
        return True
    return False


def check_victory(position):
    for col in range(Position.WIDTH):
        if position.is_winning_move(col):
            return True
    return False


def ai_move(position, solver):
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
    screen = init_screen()

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
                            print("Player wins!")
                            game_over = True
                        turn = 1 - turn
            else:
                ai_col = ai_move(position, solver)
                if ai_col is not None:
                    drop_piece(position, ai_col)
                    draw_board(screen, position)
                    if check_victory(position):
                        print("AI wins!")
                        game_over = True
                    turn = 1 - turn

        if game_over:
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
