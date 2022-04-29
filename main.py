import os
import random
from typing import Callable

GUESSES_COUNT = 10
BOARD_SIZE_Y = 10
BOARD_SIZE_X = 10

HIDDEN = "-"
SHIP = "S"
GUESS = "X"


def read_int(prompt: str, min_value: int, max_value: int) -> int:
    """
    Reads an integer from the user.
    """
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a number.")
            continue
        if value < min_value or value > max_value:
            print(
                f"Please enter a number between {min_value} and {max_value}.")
            continue
        return value


class BattleshipBoard:

    def __init__(self, size_x: int, size_y: int) -> None:
        self.grid = [[HIDDEN] * size_x for _ in range(size_y)]
        ship_row = random.randint(0, size_y - 1)
        ship_col = random.randint(0, size_x - 1)
        self.grid[ship_row][ship_col] = SHIP

    def is_ship(self, row: int, col: int) -> bool:
        return self.grid[row][col] == SHIP

    def already_guessed(self, row: int, col: int) -> bool:
        return self.grid[row][col] != HIDDEN

    def place_guess(self, row: int, col: int) -> None:
        self.grid[row][col] = GUESS

    def to_string(self, show_ship: bool = False) -> str:
        rows_str: list[str] = []
        for row in self.grid:
            row = [
                HIDDEN if col == SHIP and not show_ship else col for col in row
            ]
            rows_str.append(" ".join(row))
        return "\n".join(rows_str)


def read_guess(already_guessed: Callable[[int, int], bool]) -> tuple[int, int]:
    while True:
        guess_row = read_int(
            "Guess Row: ", min_value=1, max_value=BOARD_SIZE_X) - 1
        guess_col = read_int(
            "Guess Col: ", min_value=1, max_value=BOARD_SIZE_Y) - 1

        if not already_guessed(guess_row, guess_col):
            return guess_row, guess_col

        print("You already guessed that location. Try again.")


def turn(board: BattleshipBoard) -> bool:
    print(board.to_string())
    guess_row, guess_col = read_guess(board.already_guessed)
    board.place_guess(guess_row, guess_col)

    return board.is_ship(guess_row, guess_col)


def play_game(player_count: int, board: BattleshipBoard) -> None:
    """Play a game of Battleship with a given number of players."""

    os.system("clear")

    total_guesses = 0
    won_game = False

    while total_guesses < GUESSES_COUNT * player_count:

        # determine the current player and the remaining guesses
        current_player = (total_guesses % player_count) + 1
        remaining_guesses = GUESSES_COUNT - total_guesses // player_count

        print(
            f"Player {current_player}'s turn: {remaining_guesses} guesses left."
        )

        if turn(board):
            print(f"Congratulations! Player {current_player} sank the ship!")
            won_game = True
            break
        else:
            print("Sorry, you missed!")

        total_guesses += 1

    # print the board one last time, showing the ship
    if not won_game:
        print("Game over, you didn't find the ship in time.")
    print(board.to_string(show_ship=True))


def main() -> None:
    os.system("clear")

    player_count = read_int(
        "Please enter how many players are going to play: ",
        max_value=2,
        min_value=1)
    board = BattleshipBoard(BOARD_SIZE_X, BOARD_SIZE_Y)
    play_game(player_count, board)


if __name__ == "__main__":
    main()