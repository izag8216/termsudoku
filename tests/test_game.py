"""Tests for Sudoku game state."""

import pytest
from termsudoku.game import GameState, Cell, EMPTY, GRID_SIZE


class TestGameState:
    def test_init_creates_empty_board(self):
        game = GameState()
        assert len(game.board) == GRID_SIZE
        assert len(game.board[0]) == GRID_SIZE
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                assert game.board[r][c].value == EMPTY

    def test_set_cell(self):
        game = GameState()
        game.set_cell(0, 0, 5)
        assert game.board[0][0].value == 5

    def test_set_cell_given_stays(self):
        game = GameState()
        game.board[0][0].is_given = True
        game.board[0][0].value = 5
        game.set_cell(0, 0, 3)
        assert game.board[0][0].value == 5

    def test_clear_cell(self):
        game = GameState()
        game.set_cell(0, 0, 5)
        game.clear_cell(0, 0)
        assert game.board[0][0].value == EMPTY

    def test_clear_cell_given_fails(self):
        game = GameState()
        game.board[0][0].is_given = True
        game.board[0][0].value = 5
        game.clear_cell(0, 0)
        assert game.board[0][0].value == 5

    def test_undo(self):
        game = GameState()
        game.set_cell(0, 0, 5)
        game.clear_cell(0, 0)
        assert game.board[0][0].value == EMPTY

    def test_undo_returns_false_when_empty(self):
        game = GameState()
        assert game.undo() is False

    def test_toggle_pencil(self):
        game = GameState()
        game.toggle_pencil(0, 0, 3)
        assert 3 in game.board[0][0].pencil_marks
        game.toggle_pencil(0, 0, 3)
        assert 3 not in game.board[0][0].pencil_marks

    def test_toggle_pencil_when_filled(self):
        game = GameState()
        game.set_cell(0, 0, 5)
        game.toggle_pencil(0, 0, 3)
        assert 3 not in game.board[0][0].pencil_marks

    def test_eliminate_pencil_marks(self):
        game = GameState()
        for c in range(GRID_SIZE):
            game.board[0][c].pencil_marks.add(5)
        game.set_cell(0, 0, 5)
        for c in range(1, GRID_SIZE):
            assert 5 not in game.board[0][c].pencil_marks

    def test_is_complete_false(self):
        game = GameState()
        assert game.is_complete() is False

    def test_is_complete_true(self):
        game = GameState()
        puzzle = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9],
        ]
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                game.board[r][c].value = puzzle[r][c]
        assert game.is_complete() is True

    def test_has_conflict_true(self):
        game = GameState()
        game.set_cell(0, 0, 5)
        game.set_cell(0, 1, 5)
        assert game.has_conflict(0, 0) is True
        assert game.has_conflict(0, 1) is True

    def test_has_conflict_false_empty(self):
        game = GameState()
        assert game.has_conflict(0, 0) is False
