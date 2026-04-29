"""Hint generation for Sudoku puzzles."""

from dataclasses import dataclass
from typing import Optional
from .game import GameState, GRID_SIZE, EMPTY


@dataclass
class Hint:
    """A hint for the player."""
    row: int
    col: int
    value: int
    technique: str
    explanation: str


def get_hint(game: GameState, difficulty: str = "medium") -> Optional[Hint]:
    """Get a hint for the current puzzle state.

    Args:
        game: Current game state
        difficulty: Hint complexity level

    Returns:
        Hint object or None if no hint available
    """
    board = [[game.board[r][c].value for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]

    hint = _naked_single(game, board)
    if hint:
        return hint

    hint = _hidden_single(game, board)
    if hint:
        return hint

    if difficulty in ("hard", "expert"):
        hint = _pointing_pair(game, board)
        if hint:
            return hint

        hint = _box_line_reduction(game, board)
        if hint:
            return hint

    return _random_fill_hint(game, board)


def _naked_single(game: GameState, board: list[list[int]]) -> Optional[Hint]:
    """Naked Single: cell has only one candidate."""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == EMPTY:
                candidates = _get_candidates(board, r, c)
                if len(candidates) == 1:
                    val = next(iter(candidates))
                    return Hint(
                        row=r,
                        col=c,
                        value=val,
                        technique="Naked Single",
                        explanation=f"Cell ({r+1},{c+1}) can only be {val} - all other numbers are eliminated by row, column, or box constraints.",
                    )
    return None


def _hidden_single(game: GameState, board: list[list[int]]) -> Optional[Hint]:
    """Hidden Single: number can only go in one cell in a unit."""
    for num in range(1, GRID_SIZE + 1):
        for unit in range(GRID_SIZE):
            possible_cells = []
            for i in range(GRID_SIZE):
                if board[unit][i] == EMPTY and num in _get_candidates(board, unit, i):
                    possible_cells.append((unit, i))
            if len(possible_cells) == 1:
                r, c = possible_cells[0]
                return Hint(
                    row=r,
                    col=c,
                    value=num,
                    technique="Hidden Single",
                    explanation=f"Number {num} must go in cell ({r+1},{c+1}) because it's the only cell in row {unit+1} where it can fit.",
                )

            possible_cells = []
            for i in range(GRID_SIZE):
                if board[i][unit] == EMPTY and num in _get_candidates(board, i, unit):
                    possible_cells.append((i, unit))
            if len(possible_cells) == 1:
                r, c = possible_cells[0]
                return Hint(
                    row=r,
                    col=c,
                    value=num,
                    technique="Hidden Single",
                    explanation=f"Number {num} must go in cell ({r+1},{c+1}) because it's the only cell in column {unit+1} where it can fit.",
                )

        box_row = (unit // 3) * 3
        box_col = (unit % 3) * 3
        possible_cells = []
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == EMPTY and num in _get_candidates(board, r, c):
                    possible_cells.append((r, c))
        if len(possible_cells) == 1:
            r, c = possible_cells[0]
            return Hint(
                row=r,
                col=c,
                value=num,
                technique="Hidden Single",
                explanation=f"Number {num} must go in cell ({r+1},{c+1}) because it's the only cell in box {(unit // 3) + 1}-{(unit % 3) + 1} where it can fit.",
            )

    return None


def _pointing_pair(game: GameState, board: list[list[int]]) -> Optional[Hint]:
    """Pointing Pair: candidates in a box that point to a row/column."""
    for box_r in range(0, GRID_SIZE, 3):
        for box_c in range(0, GRID_SIZE, 3):
            for num in range(1, GRID_SIZE + 1):
                cells_with_num = []
                for r in range(box_r, box_r + 3):
                    for c in range(box_c, box_c + 3):
                        if board[r][c] == EMPTY and num in _get_candidates(board, r, c):
                            cells_with_num.append((r, c))
                if len(cells_with_num) >= 2:
                    same_row = all(r == cells_with_num[0][0] for r, _ in cells_with_num)
                    same_col = all(c == cells_with_num[0][1] for _, c in cells_with_num)
                    if same_row:
                        row = cells_with_num[0][0]
                        return Hint(
                            row=row,
                            col=0,
                            value=num,
                            technique="Pointing Pair",
                            explanation=f"Number {num} in box {(box_r//3)+1}-{(box_c//3)+1} is confined to row {row+1}. Eliminate {num} from other cells in that row outside this box.",
                        )
                    if same_col:
                        col = cells_with_num[0][1]
                        return Hint(
                            row=0,
                            col=col,
                            value=num,
                            technique="Pointing Pair",
                            explanation=f"Number {num} in box {(box_r//3)+1}-{(box_c//3)+1} is confined to column {col+1}. Eliminate {num} from other cells in that column outside this box.",
                        )
    return None


def _box_line_reduction(game: GameState, board: list[list[int]]) -> Optional[Hint]:
    """Box Line Reduction: candidates in a row/column confined to one box."""
    for row in range(GRID_SIZE):
        for num in range(1, GRID_SIZE + 1):
            cells = [(row, c) for c in range(GRID_SIZE) if board[row][c] == EMPTY and num in _get_candidates(board, row, c)]
            if len(cells) >= 2:
                box_col_start = min(c // 3 for _, c in cells) // 3 * 3
                box_col_end = box_col_start + 3
                if all(c // 3 == cells[0][1] // 3 for _, c in cells):
                    return Hint(
                        row=row,
                        col=0,
                        value=num,
                        technique="Box Line Reduction",
                        explanation=f"Number {num} in row {row+1} is confined to box columns {box_col_start+1}-{box_col_end}. Eliminate {num} from other cells in that box outside this row.",
                    )
    return None


def _random_fill_hint(game: GameState, board: list[list[int]]) -> Optional[Hint]:
    """Fallback: fill any empty cell with a valid number."""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == EMPTY:
                candidates = _get_candidates(board, r, c)
                if candidates:
                    val = min(candidates)
                    return Hint(
                        row=r,
                        col=c,
                        value=val,
                        technique="Fallback",
                        explanation=f"No advanced technique found. Cell ({r+1},{c+1}) can be {val}.",
                    )
    return None


def _get_candidates(board: list[list[int]], row: int, col: int) -> set[int]:
    """Get valid candidates for a cell."""
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
