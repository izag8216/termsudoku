"""Sudoku board logic and game state."""

from dataclasses import dataclass, field
from typing import Optional


EMPTY = 0
BOX_SIZE = 3
GRID_SIZE = 9


@dataclass
class Cell:
    """Represents a single Sudoku cell."""

    value: int = EMPTY
    pencil_marks: set[int] = field(default_factory=set)
    is_given: bool = False


@dataclass
class GameState:
    """Complete Sudoku game state."""

    board: list[list[Cell]] = field(default_factory=list)
    timer: float = 0.0
    is_paused: bool = True
    selected_row: int = 0
    selected_col: int = 0
    moves: list[tuple[int, int, int]] = field(default_factory=list)
    undos: list[tuple[int, int, int]] = field(default_factory=list)

    def __post_init__(self):
        if not self.board:
            self.board = [[Cell() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def get_cell(self, row: int, col: int) -> Cell:
        """Get cell at position."""
        return self.board[row][col]

    def set_cell(self, row: int, col: int, value: int) -> None:
        """Set cell value and record move for undo."""
        cell = self.board[row][col]
        if cell.is_given:
            return
        if cell.value != EMPTY:
            self.undos.append((row, col, cell.value))
        self.moves.append((row, col, value))
        cell.value = value
        if value != EMPTY:
            cell.pencil_marks.clear()
            self._eliminate_pencil_marks(row, col, value)

    def clear_cell(self, row: int, col: int) -> None:
        """Clear a cell."""
        cell = self.board[row][col]
        if cell.is_given:
            return
        if cell.value != EMPTY:
            self.undos.append((row, col, cell.value))
        cell.value = EMPTY

    def undo(self) -> bool:
        """Undo last move. Returns True if successful."""
        if not self.undos:
            return False
        row, col, value = self.undos.pop()
        self.board[row][col].value = value
        return True

    def toggle_pencil(self, row: int, col: int, num: int) -> None:
        """Toggle pencil mark for a number."""
        cell = self.board[row][col]
        if cell.value != EMPTY:
            return
        if num in cell.pencil_marks:
            cell.pencil_marks.discard(num)
        else:
            cell.pencil_marks.add(num)

    def _eliminate_pencil_marks(self, row: int, col: int, value: int) -> None:
        """Remove pencil marks from row, column, and box after setting a value."""
        box_row_start = (row // BOX_SIZE) * BOX_SIZE
        box_col_start = (col // BOX_SIZE) * BOX_SIZE

        for c in range(GRID_SIZE):
            self.board[row][c].pencil_marks.discard(value)
        for r in range(GRID_SIZE):
            self.board[r][col].pencil_marks.discard(value)
        for r in range(box_row_start, box_row_start + BOX_SIZE):
            for c in range(box_col_start, box_col_start + BOX_SIZE):
                self.board[r][c].pencil_marks.discard(value)

    def is_complete(self) -> bool:
        """Check if puzzle is solved."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c].value == EMPTY:
                    return False
        return self._is_valid()

    def _is_valid(self) -> bool:
        """Validate current state."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                val = self.board[r][c].value
                if val == EMPTY:
                    continue
                if not self._is_valid_placement(r, c, val):
                    return False
        return True

    def _is_valid_placement(self, row: int, col: int, value: int) -> bool:
        """Check if value placement is valid."""
        for c in range(GRID_SIZE):
            if c != col and self.board[row][c].value == value:
                return False
        for r in range(GRID_SIZE):
            if r != row and self.board[r][col].value == value:
                return False
        box_row_start = (row // BOX_SIZE) * BOX_SIZE
        box_col_start = (col // BOX_SIZE) * BOX_SIZE
        for r in range(box_row_start, box_row_start + BOX_SIZE):
            for c in range(box_col_start, box_col_start + BOX_SIZE):
                if (r, c) != (row, col) and self.board[r][c].value == value:
                    return False
        return True

    def has_conflict(self, row: int, col: int) -> bool:
        """Check if cell has conflict with row/col/box."""
        val = self.board[row][col].value
        if val == EMPTY:
            return False
        return not self._is_valid_placement(row, col, val)
