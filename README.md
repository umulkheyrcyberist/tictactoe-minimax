# Tic-Tac-Toe with Minimax

A mini project: play Tic-Tac-Toe against a computer that uses the Minimax algorithm.

**Play online:** https://umulkheyrcyberist.github.io/tictactoe-minimax/

- `tictactoe.py`: the command-line game in Python (you are X, the computer is O). Run it with `python tictactoe.py`.
- `index.html`: the web version, with a short explanation of how Minimax works.

## Features

- Easy level (random moves) and Hard level (Minimax, never loses)
- Input validation and "Play again?"
- Win and draw detection with all 8 winning lines

## How Minimax works

The computer tries every possible move until the game ends and scores each ending: +1 if the computer wins, -1 if the player wins, 0 for a draw. It then picks the move with the highest score, assuming the player always picks the lowest.
