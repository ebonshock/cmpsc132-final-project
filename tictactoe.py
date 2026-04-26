# CMPSC 132 - Final Project
# Tic-Tac-Toe Game (2-Player, Terminal-Based)
# Author: Evan Bonshock


import os


# ANSI escape codes for terminal colors and text formatting
RED    = "\033[91m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
BOLD   = "\033[1m"
RESET  = "\033[0m"  # resets color back to default after each colored print


def clear_screen():
    """Clear the terminal screen."""
    # runs a different shell command depending on the OS (Windows vs everything else)
    os.system("cls" if os.name == "nt" else "clear")


def colorize(symbol):
    """Return a colorized version of a player symbol."""
    # wrap the symbol in the right color codes, or return a blank space if empty
    if symbol == "X":
        return f"{RED}{BOLD}X{RESET}"
    elif symbol == "O":
        return f"{CYAN}{BOLD}O{RESET}"
    return " "


def print_board(board):
    """Display the current state of the board."""
    # board is a 2D list (list of lists), so we loop through rows then cells
    print()
    print("    0   1   2")
    print("  +---+---+---+")
    for i, row in enumerate(board):
        row_str = f"{i} |"
        for cell in row:
            display = colorize(cell) if cell != " " else " "
            row_str += f" {display} |"
        print(row_str)
        print("  +---+---+---+")
    print()


def check_winner(board, player):
    """Check if the given player has won."""
    # check all 3 rows, if every cell in a row matches the player, they won
    for row in board:
        won = True
        for cell in row:
            if cell != player:
                won = False
                break
        if won:
            return True

    # check all 3 columns, iterate by index instead of directly over the list
    for col in range(3):
        won = True
        for row in range(3):
            if board[row][col] != player:
                won = False
                break
        if won:
            return True

    # check main diagonal (top-left to bottom-right), row and col index are the same
    won = True
    for i in range(3):
        if board[i][i] != player:
            won = False
            break
    if won:
        return True

    # check anti-diagonal (top-right to bottom-left), col index is 2 - row index
    won = True
    for i in range(3):
        if board[i][2 - i] != player:
            won = False
            break
    if won:
        return True

    return False


def is_draw(board):
    """Return True if the board is full and there is no winner."""
    # nested loop to check every cell, if any space is still empty, it's not a draw yet
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


# Input Helpers


def get_move(board, player, history):
    """
    Prompt the current player for a valid move.
    Type 'u' to undo the last two moves (one per player).
    Returns (row, col) or the string 'undo'.
    """
    while True:
        try:
            # read as a string first so we can check for the 'u' undo command
            raw = input(f"Player {player} - Enter ROW # (0-2) or 'u' to undo: ").strip().lower()

            if raw == "u":
                # need at least 2 moves in history to undo one full round of turns
                if len(history) < 2:
                    print("Not enough moves to undo. Try again.")
                    continue
                return "undo"

            row = int(raw)  # convert to int after ruling out the 'u' case
            col = int(input(f"Player {player} - Enter COLUMN # (0-2): "))

            # bounds check, range(3) gives [0, 1, 2]
            if row not in range(3) or col not in range(3):
                print("Invalid input. Row and column must be between 0 and 2. Try again.")
                continue

            # make sure the cell isn't already taken
            if board[row][col] != " ":
                print("That cell is already occupied. Choose another. Try again.")
                continue

            return row, col

        except ValueError:
            # int() throws ValueError if the input isn't a valid number
            print("Invalid input. Please enter integers only. Try again.")


def get_player_names():
    """Prompt for custom player names. Returns (name_x, name_o)."""
    # the 'or' fallback kicks in if the player just hits Enter (empty string is falsy)
    name_x = input("Enter name for Player X: ").strip() or "Player X"
    name_o = input("Enter name for Player O: ").strip() or "Player O"
    return name_x, name_o


# Score Tracking


def print_scoreboard(scores, names):
    """Display the current win/draw/loss record for both players."""
    # scores is a dict with keys 'X', 'O', and 'draws'
    name_x, name_o = names
    print(f"{BOLD}─── Scoreboard ───{RESET}")
    print(f"  {RED}{name_x}{RESET}:  {scores['X']} wins  |  {scores['draws']} draws  |  {CYAN}{name_o}{RESET}: {scores['O']} wins")
    print()


# Game Modes


def play_game(scores, names):
    """
    Main game loop for a single round.
    Supports undo (type 'u' at the row prompt to revert the last two moves).
    Returns the winner symbol ('X', 'O') or 'draw', and the full move history.
    """
    # 2D list, each inner list is a row, each element is a cell (" ", "X", or "O")
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current = 0  # index into players list, toggles between 0 and 1
    history = []  # list of (player, row, col) tuples, used as a stack for undo
    name_x, name_o = names

    clear_screen()
    print_scoreboard(scores, names)
    print(f"{BOLD}New Round — {name_x} (X) vs {name_o} (O){RESET}")
    print(f"{YELLOW}Tip: type 'u' at the row prompt to undo the last two moves.{RESET}")
    print_board(board)

    while True:
        player = players[current]
        display_name = name_x if player == "X" else name_o

        print(f"{BOLD}{display_name}'s turn ({player}){RESET}")
        result = get_move(board, player, history)

        # undo branch, pop the last two moves off the stack and clear those cells
        if result == "undo":
            _, prev_row, prev_col = history.pop()  # .pop() removes and returns the last item
            board[prev_row][prev_col] = " "

            _, prev_row, prev_col = history.pop()
            board[prev_row][prev_col] = " "

            # undoing both players' last moves leaves current unchanged, no need to toggle
            clear_screen()
            print_scoreboard(scores, names)
            print(f"{YELLOW}Undo successful. Two moves reversed.{RESET}")
            print_board(board)
            continue

        row, col = result
        board[row][col] = player
        history.append((player, row, col))  # push this move onto the stack

        clear_screen()
        print_scoreboard(scores, names)
        print_board(board)

        # check win/draw after every move, no point checking before at least 5 moves,
        # but keeping it simple here is fine for a 3x3 board
        if check_winner(board, player):
            winner_name = name_x if player == "X" else name_o
            print(f"{GREEN}{BOLD}{winner_name} wins!{RESET}\n")
            return player, history

        if is_draw(board):
            print(f"{YELLOW}{BOLD}It's a draw! Well played by both players.{RESET}\n")
            return "draw", history

        # toggle current between 0 and 1, 1 - 0 = 1, 1 - 1 = 0
        current = 1 - current


# Main Menu


def main_menu():
    """Display the main menu and return the user's choice."""
    print(f"{BOLD}{'─'*32}{RESET}")
    print(f"{YELLOW}{BOLD}    TIC-TAC-TOE{RESET}")
    print(f"{BOLD}{'─'*32}{RESET}")
    print("  (1) 2-Player Mode")
    print("  (2) Quit")
    print(f"{BOLD}{'─'*32}{RESET}")
    while True:
        choice = input("Select an option: ").strip()
        if choice in ("1", "2"):
            return choice
        print("Invalid choice. Enter 1 or 2.")


def play_again_prompt():
    """Ask the players if they want to play another round. Returns True/False."""
    while True:
        choice = input("Play again? (y/n): ").strip().lower()
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print("Invalid input. Enter y or n.")


# Entry Point


def main():
    """Entry point: show menu, run sessions, track scores across rounds."""
    clear_screen()
    while True:
        choice = main_menu()

        if choice == "2":
            print("\nThanks for playing! Goodbye.\n")
            break

        names = get_player_names()
        scores = {"X": 0, "O": 0, "draws": 0}  # dict to track wins and draws across rounds

        while True:
            # play_game now returns a tuple — unpack both the result and the move history
            result, history = play_game(scores, names)

            if result == "draw":
                scores["draws"] += 1
            else:
                # result is either "X" or "O", so we can use it directly as a dict key
                scores[result] += 1

            print_scoreboard(scores, names)

            if not play_again_prompt():
                break

        clear_screen()


if __name__ == "__main__":
    main()