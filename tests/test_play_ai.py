import importlib
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from bitboard_class import Position

# Import module without requiring pygame
play_AI = importlib.import_module('play_AI')
get_piece_at = play_AI.get_piece_at

def test_get_piece_at_detects_players():
    pos = Position()
    pos.play(0)
    assert get_piece_at(pos, 0, 0) == 'X'
    pos.play(1)
    assert get_piece_at(pos, 1, 0) == 'O'
