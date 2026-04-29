"""Sudoku solver using backtracking with constraint propagation."""

from typing import Optional
from .game import GRID_SIZE, EMPTY


def solve(board: list[list[int]]) -> Optional[list[list[int]]]:
    """Solve a Sudoku puzzle.

    Args:
        board: 9x9 grid where 0 represents empty cells

    Returns:
        Solved board or None if unsolvable
    """
    solution = [row[:] for row in board]
    if _solve_recursive(solution):
        return solution
    return None


def _solve_recursive(board: list[list[int]]) -> bool:
    """Recursive backtracking solver."""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == EMPTY:
                for num in range(1, GRID_SIZE + 1):
                    if _is_valid(board, r, c, num):
                        board[r][c] = num
                        if _solve_recursive(board):
                            return True
                        board[r][c] = EMPTY
                return False
    return True


def _is_valid(board: list[list[int]], row: int, col: int, num: int) -> bool:
    """Check if num is valid at row, col."""
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


def get_candidates(board: list[list[int]], row: int, col: int) -> set[int]:
    """Get all valid candidates for a cell."""
    if board[row][col] != EMPTY:
        return set()
    candidates = set(range(1, GRID_SIZE + 1))
    for c in range(GRID_SIZE):
        candidates.discard(board[row][c])
    for r in range(GRID_SIZE):
        candidates.discard(board[r][col])
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            candidates.discard(board[r][c])
    return candidates


def has_unique_solution(board: list[list[int]]) -> bool:
    """Check if puzzle has exactly one solution."""
    solution = [row[:] for row in board]
    count = [0]
    _count_solutions(solution, count)
    return count[0] == 1


def _count_solutions(board: list[list[int]], count: list[int]) -> None:
    """Count solutions (stop at 2)."""
    if count[0] > 1:
        return
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == EMPTY:
                for num in range(1, GRID_SIZE + 1):
                    if _is_valid(board, r, c, num):
                        board[r][c] = num
                        _count_solutions(board, count)
                        board[r][c] = EMPTY
                return
    count[0] += 1
