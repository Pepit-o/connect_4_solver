import time
from transposition_table_class import TranspositionTable
from bitboard_class import Position


class Solver:
    """
    A class to solve Connect 4 positions using the Negamax variant of Min-Max algorithm
    with Alpha-Beta pruning and a Transposition Table.
    """

    def __init__(self):
        self.node_count = 0
        self.trans_table = TranspositionTable(8388593)  # Prime number for hash table (64MB)
        self.column_order = [Position.WIDTH // 2 + (1 - 2 * (i % 2)) * (i + 1) // 2 for i in range(Position.WIDTH)]
        # Example for WIDTH=7: column_order = [3, 4, 2, 5, 1, 6, 0]

    def reset(self):
        """Resets the solver's node count and transposition table."""
        self.node_count = 0
        self.trans_table.reset()

    def get_node_count(self):
        """Returns the number of explored nodes."""
        return self.node_count

    def negamax(self, P, alpha, beta, depth=0, max_depth=4):  # Add depth tracking
        """Recursive negamax function with alpha-beta pruning."""
        assert alpha < beta
        assert not P.can_win_next()

        if depth > max_depth:  # Prevent infinite recursion
            return 0  # Return neutral score instead of recursing infinitely

        self.node_count += 1

        next_moves = P.possible_non_loosing_moves()
        if next_moves == 0:  # No non-losing move, opponent wins next move
            return -(Position.WIDTH * Position.HEIGHT - P.nb_moves()) // 2

        if P.nb_moves() >= Position.WIDTH * Position.HEIGHT - 2:
            return 0  # Draw game

        min_score = -(Position.WIDTH * Position.HEIGHT - 2 - P.nb_moves()) // 2
        if alpha < min_score:
            alpha = min_score
            if alpha >= beta:
                return alpha  # Prune if no better moves possible

        max_score = (Position.WIDTH * Position.HEIGHT - 1 - P.nb_moves()) // 2
        key = P.key()
        val = self.trans_table.get(key)

        if val:
            max_score = val + Position.MIN_SCORE - 1

        if beta > max_score:
            beta = max_score
            if alpha >= beta:
                return beta  # Prune search if best possible score is exceeded

        for col in self.column_order:
            if next_moves & Position.column_mask(col):
                P2 = Position()
                P2.current_position = P.current_position
                P2.mask = P.mask
                P2.moves = P.moves
                P2.play(col)

                score = -self.negamax(P2, -beta, -alpha, depth + 1, max_depth)

                if score >= beta:
                    return score  # Beta cutoff
                if score > alpha:
                    alpha = score  # Update best move

        self.trans_table.put(key, alpha - Position.MIN_SCORE + 1)  # Store upper bound
        return alpha

    def solve(self, P, weak=False):
        """Solves the given Connect 4 position."""
        if P.can_win_next():
            return (Position.WIDTH * Position.HEIGHT + 1 - P.nb_moves()) // 2

        min_score = -(Position.WIDTH * Position.HEIGHT - P.nb_moves()) // 2
        max_score = (Position.WIDTH * Position.HEIGHT + 1 - P.nb_moves()) // 2

        if weak:
            min_score, max_score = -1, 1

        while min_score < max_score:
            mid = min_score + (max_score - min_score) // 2
            if 0 >= mid > min_score // 2:
                mid = min_score // 2
            elif 0 <= mid < max_score // 2:
                mid = max_score // 2

            result = self.negamax(P, mid, mid + 1)
            if result <= mid:
                max_score = result
            else:
                min_score = result

        return min_score


def get_time_microsec():
    """Returns the current timestamp in microseconds."""
    return int(time.time() * 1_000_000)
