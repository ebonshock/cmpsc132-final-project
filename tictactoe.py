# CMPSC 132 - Final Project
# Tic-Tac-Toe Game (2-Player, Terminal-Based)
# Author: Evan Bonshock


import os


def clear_screen():
    """Clear the terminal screen."""
    # runs a different shell command depending on the OS (Windows vs everything else)
    os.system("cls" if os.name == "nt" else "clear")


def print_board(board):
    """Display the current state of the board."""
    # board is a 2D list (list of lists), so we loop through rows then cells
    print()
    print("    0   1   2")
    print("  +---+---+---+")
    for i, row in enumerate(board):
        row_str = f"{i} |"
        for cell in row:
            row_str += f" {cell} |"
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


def get_move(board, player):
    """Prompt the current player for a valid move and return (row, col)."""
    while True:
        try:
            row = int(input(f"Player {player} - Enter ROW # (0-2): "))
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


# Game Modes


def play_game():
    """Main game loop."""
    # 2D list, each inner list is a row, each element is a cell (" ", "X", or "O")
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current = 0  # index into players list, toggles between 0 and 1

    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        player = players[current]

        row, col = get_move(board, player)
        board[row][col] = player

        clear_screen()
        print_board(board)

        # check win/draw after every move, no point checking before at least 5 moves,
        # but keeping it simple here is fine for a 3x3 board
        if check_winner(board, player):
            print(f"Player {player} wins! Congratulations!")
            break

        if is_draw(board):
            print("It's a draw! Well played by both players.")
            break

        # toggle current between 0 and 1, 1 - 0 = 1, 1 - 1 = 0
        current = 1 - current


if __name__ == "__main__":
    play_game()