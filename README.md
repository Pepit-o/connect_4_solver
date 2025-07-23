# Connect 4 Solver

This project provides a simple implementation of Connect 4 with an AI opponent. The main interface lives in `main.py`. The code is organized into small helper functions that make it easier to experiment with different algorithms.

## Overview of `main.py`

`main.py` is a pygame program that launches a graphical Connect 4 board and lets a human play against a very small negamax‑based AI. The script is divided into logical blocks described below.

### Board Helpers

- **`create_board()`** – creates a 6×7 board filled with `"NA"` markers.
- **`draw_board(screen, board)`** – draws the board and all pieces on the pygame screen.
- **`drop_piece(board, col, symbol)`** – places a symbol (`'X'` or `'O'`) in the lowest empty row of the given column.
- **`is_board_full_(board)`** – checks if there are still empty cells.
- **`valid_moves(board)`** – returns a list of the next playable cells. Columns are tried in the classical center‑out order.

### Window Evaluation

- **`get_all_windows(board)`** – enumerates every horizontal, vertical and diagonal group of four cells. Only windows containing at least one piece are stored.
- **`check_victory(board, symbol)`** – checks whether a player has four in a row. It returns `1` if the given symbol wins, `-1` if the opponent wins and `0` otherwise.
- **`score_window(window, symbol)`** – assigns a heuristic value to a length‑4 window for the specified symbol.
- **`evaluate_board(board, root_symbol, opp_symbol)`** – sums the scores of all windows from the perspective of `root_symbol` while penalising the opponent.

### AI with Negamax and Alpha–Beta Pruning

- **`negamax_connect_4_ab(board, depth, color, root_symbol, opp_symbol, alpha, beta)`** – recursive search that uses the negamax formulation with alpha–beta pruning. The depth is limited to keep the search fast.
- **`play_one_shot_negamax_ab(board, depth, root_symbol, opp_symbol)`** – helper that picks the best move by exploring each legal play with the search above.
- **`ai_move(board, ai_symbol, player_symbol)`** – wrapper to call `play_one_shot_negamax_ab` on a copy of the current board.

### Game Loop

`main()` initialises pygame, creates an empty board and handles user input. The loop alternates between the human (red `'X'`) and the AI (yellow `'O'`). When one player wins or the board fills up, the game pauses briefly before quitting.

To start a match, run:

```bash
python main.py
```

The file also defines constants such as `ROWS`, `COLS` and colour values used by pygame for rendering.

## Tests

A small test suite in the `tests/` directory checks the bitboard helper functions and piece detection logic used by the UI. Run all tests with:

```bash
pytest -q
```

