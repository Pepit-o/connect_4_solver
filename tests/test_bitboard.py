import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from bitboard_class import Position


def test_possible_non_losing_moves_empty_board():
    pos = Position()
    assert pos.possible_non_losing_moves() == pos.possible()


def test_possible_non_losing_moves_forced_loss():
    pos = Position()
    # Opponent has vertical threats in columns 0 and 1
    col0_bits = (1 << 0) | (1 << 1) | (1 << 2)
    col1_bits = (1 << 7) | (1 << 8) | (1 << 9)
    pos.current_position = 0
    pos.mask = col0_bits | col1_bits
    pos.moves = 6
    assert pos.possible_non_losing_moves() == 0
