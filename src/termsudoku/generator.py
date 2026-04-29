"""Backtracking-based Sudoku puzzle generator."""

import random
from typing import Optional
from .game import GameState, GRID_SIZE, EMPTY


DIFFICULTIES = {
    "easy": (35, 40),
    "medium": (28, 34),
    "hard": (22, 27),
    "expert": (17, 21),
}


def generate_puzzle(difficulty: str = "medium") -> GameState:
    """Generate a new Sudoku puzzle of given difficulty.

    Args:
        difficulty: One of 'easy', 'medium', 'hard', 'expert'

    Returns:
        GameState with puzzle loaded
    """
    if difficulty not in DIFFICULTIES:
        difficulty = "medium"

    solved = _generate_solved_board()
    game = GameState()

    min_cells, max_cells = DIFFICULTIES[difficulty]
    num_givens = random.randint(min_cells, max_cells)

    all_positions = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
    random.shuffle(all_positions)

    for r, c in all_positions[:num_givens]:
        game.board[r][c].value = solved[r][c]
        game.board[r][c].is_given = True

    return game


def _generate_solved_board() -> list[list[int]]:
    """Generate a complete valid Sudoku solution."""
    board = [[EMPTY] * GRID_SIZE for _ in range(GRID_SIZE)]
    _fill_board(board)
    return board


def _fill_board(board: list[list[int]]) -> bool:
    """Fill board using backtracking. Returns True if successful."""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == EMPTY:
                numbers = list(range(1, GRID_SIZE + 1))
                random.shuffle(numbers)
                for num in numbers:
                    if _is_validPlacement(board, r, c, num):
                        board[r][c] = num
                        if _fill_board(board):
                            return True
                        board[r][c] = EMPTY
                return False
    return True


def _is_validPlacement(board: list[list[int]], row: int, col: int, num: int) -> bool:
    """Check if num can be placed at row, col."""
    for c in range(GRID_SIZE):
        if board[row][c] == num:
            return False
    for r in range(GRID_SIZE):
        if board[r][col] == num:
            return False
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False
    return True


def parse_puzzle(puzzle_str: str) -> GameState:
    """Parse puzzle from string format.

    Args:
        puzzle_str: 81 character string with digits 1-9 or . for empty

    Returns:
        GameState with puzzle loaded
    """
    game = GameState()
    puzzle_str = puzzle_str.replace(".", "0").replace(" ", "")

    if len(puzzle_str) != 81:
        raise ValueError(f"Puzzle must be 81 characters, got {len(puzzle_str)}")

    for i, char in enumerate(puzzle_str):
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        if char.isdigit():
            val = int(char)
            if 1 <= val <= 9:
                game.board[row][col].value = val
                game.board[row][col].is_given = True

    return game


def to_string(game: GameState) -> str:
    """Convert game board to string representation."""
    result = []
    for r in range(GRID_SIZE):
        row_str = ""
        for c in range(GRID_SIZE):
            val = game.board[r][c].value
            row_str += str(val) if val != EMPTY else "."
        result.append(row_str)
    return "".join(result)
