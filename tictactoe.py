"""
Tic-Tac-Toe Mini-Project
------------------------
Human player = X  |  Computer = O
The computer uses:
    - Minimax  (Hard level)  -> it never loses
    - Random   (Easy level)  -> picks any empty spot
"""

# random: used so the computer can pick a random empty spot (Easy) and
# choose between equally good moves (Hard).
import random

# The two player symbols. To change them (for example to "Z"), edit them
# here only - nothing else in the program needs to change.
HUMAN = "X"        # the human player - goes first
COMPUTER = "O"     # the computer

# ---------- Phase 3: the 8 winning combinations ----------
# The numbers below are list POSITIONS (0 to 8), not the numbers you see
# on screen (1 to 9). The board positions look like this:
#       0 | 1 | 2
#       3 | 4 | 5
#       6 | 7 | 8
WIN_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # the 3 rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # the 3 columns
    (0, 4, 8), (2, 4, 6),              # the 2 diagonals
]


# ======================================================================
# Phase 1: Build and display the board
# ======================================================================

def new_board():
    """Create a new board of 9 cells: ["1", "2", ..., "9"].
    An empty cell shows its own number. When a move is played, the number
    is replaced by "X" or "O"."""
    # range(1, 10) gives 1,2,...,9 ; str(i) turns each number into text
    return [str(i) for i in range(1, 10)]


def print_board(board):
    """Print the board as 3 rows."""
    print()
    # row will be 0, 3, 6 = the start of each row
    for row in range(0, 9, 3):
        # print the three cells of this row, separated by "|"
        print(f" {board[row]} | {board[row + 1]} | {board[row + 2]} ")
        # draw a divider line between rows (not after the last row)
        if row < 6:
            print("---+---+---")
    print()


def empty_spots(board):
    """Return the list of positions (0-8) that are still empty.
    An empty cell is any cell that is neither X nor O."""
    return [i for i in range(9) if board[i] not in (HUMAN, COMPUTER)]


# ======================================================================
# Phase 3: Win and draw detection
# ======================================================================

def winner(board):
    """Return "X" or "O" if someone has 3 in a row.
    Return None if nobody has won yet."""
    # check one winning combination at a time (a, b, c = its 3 positions)
    for a, b, c in WIN_COMBOS:
        # if the three cells are equal and belong to a player -> win
        # (the "in (HUMAN, COMPUTER)" check is an extra safety check)
        if board[a] == board[b] == board[c] and board[a] in (HUMAN, COMPUTER):
            return board[a]      # return the winner
    return None                  # nobody has won yet


def is_full(board):
    """If no empty spot is left, the board is full (a draw if nobody
    has won)."""
    return len(empty_spots(board)) == 0


# ======================================================================
# Phase 2: Let the player move
# ======================================================================

def get_player_move(board):
    """Ask the player for a number (1-9) until a valid one is entered."""
    while True:   # repeat until we get a valid move
        # input() reads what the player typed; strip() removes extra
        # spaces at the start and end
        choice = input("Your move (1-9): ").strip()

        # isdigit() checks that only digits were typed (not letters,
        # symbols or an empty answer)
        if not choice.isdigit():
            print("Invalid move: please type a number from 1 to 9.")
            continue   # go back to the start of the loop

        # convert the number (1-9) into a list position (0-8): subtract 1
        spot = int(choice) - 1

        if spot < 0 or spot > 8:
            # the number is not between 1 and 9
            print("Invalid move: the number must be between 1 and 9.")
        elif spot not in empty_spots(board):
            # the cell was already taken
            print("Invalid move: that spot is already taken.")
        else:
            return spot   # valid move -> return it and stop the loop


# ======================================================================
# Phase 4: Computer moves
# ======================================================================

def random_move(board):
    """Step 1 (Easy): the computer picks a random empty spot."""
    return random.choice(empty_spots(board))


def minimax(board, computer_turn):
    """
    Step 2 (Hard): Minimax.

    Idea: the computer "plays in its head" every possible move until the
    game ends, then scores the result:
        +1 = the computer (O) wins
        -1 = the player (X) wins
         0 = draw

    computer_turn = True  -> it is the computer's turn; it picks the
                             HIGHEST score (MAX)
    computer_turn = False -> it is the player's turn; we assume the player
                             picks the LOWEST score (MIN), because the
                             player wants the computer to lose

    This function calls itself (RECURSION) until the game is over.
    """
    # ---- Base cases: the game is over ----
    result = winner(board)
    if result == COMPUTER:
        return 1       # the computer won
    if result == HUMAN:
        return -1      # the player won
    if is_full(board):
        return 0       # board is full and nobody won = draw

    # ---- The game continues: try every possible move ----
    if computer_turn:
        best = -2      # lower than any possible score (-1), so any
                       # real score will replace it
        for spot in empty_spots(board):
            # "Try" the move: put O on the spot, and save the old value
            # of the cell (saved).
            board[spot], saved = COMPUTER, board[spot]
            # now it is the player's turn -> computer_turn = False
            score = minimax(board, False)
            # "Undo" the move: restore the cell so the board is back to
            # how it was and we can try the next move
            board[spot] = saved
            # keep the highest score (MAX)
            best = max(best, score)
        return best
    else:
        best = 2       # higher than any possible score (+1)
        for spot in empty_spots(board):
            board[spot], saved = HUMAN, board[spot]   # try X
            score = minimax(board, True)              # now the computer
            board[spot] = saved                       # undo
            best = min(best, score)                   # keep the lowest (MIN)
        return best


def minimax_move(board):
    """Pick the empty spot with the highest Minimax score."""
    best_score = -2     # best score found so far
    best_spots = []     # list: all spots that have that best score
    for spot in empty_spots(board):
        # try the computer playing here
        board[spot], saved = COMPUTER, board[spot]
        # after the computer's move it is the player's turn -> False
        score = minimax(board, False)
        board[spot] = saved     # undo the move

        if score > best_score:
            # a new higher score: start a new list
            best_score, best_spots = score, [spot]
        elif score == best_score:
            # same score: add it to the list (both moves are equally good)
            best_spots.append(spot)
    # if several moves are equally good, pick one at random so the games
    # are not always the same
    return random.choice(best_spots)


# ======================================================================
# Phase 5 and 6: The full game and the enhancements
# ======================================================================

def choose_difficulty():
    """Let the player choose Easy or Hard."""
    while True:
        # lower() turns the text into lowercase, so "E" and "e" are the same
        level = input("Choose difficulty - (E)asy or (H)ard: ").strip().lower()
        if level in ("e", "easy"):
            return "easy"
        if level in ("h", "hard"):
            return "hard"
        print("Invalid choice. Type E or H.")


def play_game(difficulty):
    """Play one full game, until someone wins or it is a draw."""
    board = new_board()     # a fresh board
    print_board(board)      # show the board first

    while True:  # every round: player -> computer -> player ...
        # ---- Player's turn (X goes first) ----
        board[get_player_move(board)] = HUMAN   # put X on the chosen spot
        print_board(board)
        if winner(board) == HUMAN:              # check for a win
            print("You win!")
            return                              # end the game
        if is_full(board):                      # check for a draw
            print("It's a draw!")
            return

        # ---- Computer's turn ----
        print("Computer is thinking...")
        if difficulty == "easy":
            spot = random_move(board)           # Easy: random
        else:
            spot = minimax_move(board)          # Hard: Minimax
        board[spot] = COMPUTER                  # put O on the spot
        print(f"Computer plays {spot + 1}")     # +1 to show a 1-9 number
        print_board(board)
        if winner(board) == COMPUTER:           # check for a win
            print("Computer wins!")
            return
        if is_full(board):                      # check for a draw
            print("It's a draw!")
            return


def main():
    """Main program: play a game, then ask "Play again?"."""
    print("=== Tic-Tac-Toe: You (X) vs Computer (O) ===")
    while True:
        play_game(choose_difficulty())          # choose a level, then play
        again = input("Play again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):           # anything except "y": stop
            print("Thanks for playing!")
            break


# This line checks that the file is being run directly
# (python tictactoe.py). If another file imports this one, main() does
# not start automatically.
if __name__ == "__main__":
    main()
