class Position(object):
    # Represents a Connect 4 position using bitboards

    WIDTH = 7  # Board width
    HEIGHT = 6  # Board height
    MIN_SCORE = -(WIDTH * HEIGHT) // 2 + 3
    MAX_SCORE = (WIDTH * HEIGHT + 1) // 2 - 3

    bottom_mask = None
    board_mask = None

    @staticmethod
    def bottom(width, height):
        # Generates a bitmask for the bottom row without recursion
        result = 0
        for w in range(width):
            result |= 1 << (w * (height + 1))
        return result

    @classmethod
    def initialize_bitmasks(cls):
        # Initializes the bottom and board bitmasks
        if not hasattr(cls, "bottom_mask"):
            cls.bottom_mask = cls.bottom(cls.WIDTH, cls.HEIGHT)
            cls.board_mask = cls.bottom_mask * ((1 << cls.HEIGHT) - 1)

    def __init__(self):
        # Initializes an empty board position
        self.current_position = 0  # Bitboard for the current player
        self.mask = 0  # Bitboard for all pieces
        self.moves = 0  # Move count

        if Position.bottom_mask is None:
            Position.bottom_mask = Position.bottom(Position.WIDTH, Position.HEIGHT)
            Position.board_mask = Position.bottom_mask * ((1 << Position.HEIGHT) - 1)

    def play(self, col):
        # Plays a move in a given column
        self.current_position ^= self.mask  # Toggle player pieces
        self.mask |= self.mask + self.bottom_mask_col(col)  # Add piece to bitboard
        self.moves += 1  # Increment move count

    def can_play(self, col):
        # Returns True if a move can be played in the column
        return (self.mask & self.top_mask_col(col)) == 0

    def play_sequence(self, seq):
        # Plays a sequence of moves (to initialize a position)
        for i, c in enumerate(seq):
            col = int(c) - 1  # Convert character to column index
            if col < 0 or col >= Position.WIDTH or not self.can_play(col) or self.is_winning_move(col):
                return i  # Invalid move, return the number of processed moves
            self.play(col)
        return len(seq)

    def can_win_next(self):
        # Returns True if the current player can win in the next move
        return self.winning_position() & self.possible()

    def nb_moves(self):
        # Returns the number of moves played from the beginning
        return self.moves

    def key(self):
        # Returns a compact representation of the board position
        return self.current_position + self.mask

    def possible_non_losing_moves(self):
        # Returns a bitmask of all possible moves that do NOT immediately lose
        if self.moves >= Position.WIDTH * Position.HEIGHT - 2:  # Board nearly full, prevent unnecessary deep checks
            return self.possible()

        if self.can_win_next():  # Avoid recursion explosion
            return self.possible()

        possible_mask = self.possible()
        opponent_win = self.opponent_winning_position()
        forced_moves = possible_mask & opponent_win

        if forced_moves:
            if forced_moves & (forced_moves - 1):  # More than one forced move
                return 0  # The opponent has two winning moves, and we can't stop both
            else:
                possible_mask = forced_moves  # Force the only move that prevents a loss

        return possible_mask & ~(opponent_win >> 1)  # Avoid playing below an opponent's winning spot

    def is_winning_move(self, col):
        # Checks if playing in a column results in a win
        return self.winning_position() & self.possible() & self.column_mask(col)

    def winning_position(self):
        # Returns a bitmask of all winning positions for the current player
        return self.compute_winning_position(self.current_position, self.mask)

    def opponent_winning_position(self):
        # Returns a bitmask of all winning positions for the opponent
        return self.compute_winning_position(self.current_position ^ self.mask, self.mask)

    def possible(self):
        # Returns a bitmask of all valid moves
        return (self.mask + self.bottom_mask) & self.board_mask

    @staticmethod
    def compute_winning_position(position, mask):
        # Computes the winning positions bitmask
        HEIGHT = Position.HEIGHT
        board_mask = Position.board_mask

        # Vertical
        r = (position << 1) & (position << 2) & (position << 3)

        # Horizontal
        p = (position << (HEIGHT + 1)) & (position << 2 * (HEIGHT + 1))
        r |= p & (position << 3 * (HEIGHT + 1))
        r |= p & (position >> (HEIGHT + 1))
        p = (position >> (HEIGHT + 1)) & (position >> 2 * (HEIGHT + 1))
        r |= p & (position << (HEIGHT + 1))
        r |= p & (position >> 3 * (HEIGHT + 1))

        # Diagonal 1
        p = (position << HEIGHT) & (position << 2 * HEIGHT)
        r |= p & (position << 3 * HEIGHT)
        r |= p & (position >> HEIGHT)
        p = (position >> HEIGHT) & (position >> 2 * HEIGHT)
        r |= p & (position << HEIGHT)
        r |= p & (position >> 3 * HEIGHT)

        # Diagonal 2
        p = (position << (HEIGHT + 2)) & (position << 2 * (HEIGHT + 2))
        r |= p & (position << 3 * (HEIGHT + 2))
        r |= p & (position >> (HEIGHT + 2))
        p = (position >> (HEIGHT + 2)) & (position >> 2 * (HEIGHT + 2))
        r |= p & (position << (HEIGHT + 2))
        r |= p & (position >> 3 * (HEIGHT + 2))

        return r & (board_mask ^ mask)

    @staticmethod
    def column_mask(col):
        # Returns a bitmask with all cells of a given column
        return ((1 << Position.HEIGHT) - 1) << col * (Position.HEIGHT + 1)

    @staticmethod
    def top_mask_col(col):
        # Returns a bitmask for the top cell of a given column
        return 1 << ((Position.HEIGHT - 1) + col * (Position.HEIGHT + 1))

    @staticmethod
    def bottom_mask_col(col):
        # Returns a bitmask for the bottom cell of a given column
        return 1 << (col * (Position.HEIGHT + 1))
