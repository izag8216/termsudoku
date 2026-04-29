"""Tests for Sudoku generator."""

import pytest
from termsudoku.generator import generate_puzzle, parse_puzzle, to_string, _generate_solved_board


class TestGenerator:
    def test_generate_puzzle_creates_valid_state(self):
        game = generate_puzzle("easy")
        filled_count = sum(1 for r in range(9) for c in range(9) if game.board[r][c].value != 0)
        assert 35 <= filled_count <= 40

    def test_generate_puzzle_difficulty_easy(self):
        game = generate_puzzle("easy")
        filled_count = sum(1 for r in range(9) for c in range(9) if game.board[r][c].value != 0)
        assert 35 <= filled_count <= 40

    def test_generate_puzzle_difficulty_medium(self):
        game = generate_puzzle("medium")
        filled_count = sum(1 for r in range(9) for c in range(9) if game.board[r][c].value != 0)
        assert 28 <= filled_count <= 34

    def test_generate_puzzle_difficulty_hard(self):
        game = generate_puzzle("hard")
        filled_count = sum(1 for r in range(9) for c in range(9) if game.board[r][c].value != 0)
        assert 22 <= filled_count <= 27

    def test_generate_puzzle_difficulty_expert(self):
        game = generate_puzzle("expert")
        filled_count = sum(1 for r in range(9) for c in range(9) if game.board[r][c].value != 0)
        assert 17 <= filled_count <= 21

    def test_generate_solved_board_returns_complete_board(self):
        board = _generate_solved_board()
        assert len(board) == 9
        assert len(board[0]) == 9
        for r in range(9):
            for c in range(9):
                assert 1 <= board[r][c] <= 9

    def test_parse_puzzle_valid_string(self):
        puzzle = "003000600" + "000590001" + "040000000" + "000070000" + "000603040" + "000010800" + "007100020" + "060005000" + "000002003"
        game = parse_puzzle(puzzle)
        assert game.board[0][0].value == 0
        assert game.board[0][2].value == 3
        assert game.board[0][2].is_given is True

    def test_parse_puzzle_with_dots(self):
        puzzle = "003000600000590001040000000000070000000603040000010800007100020060005000000002003"
        game = parse_puzzle(puzzle)
        assert game.board[0][0].value == 0
        assert game.board[0][2].value == 3

    def test_parse_puzzle_invalid_length(self):
        with pytest.raises(ValueError):
            parse_puzzle("123")

    def test_to_string(self):
        puzzle = "003000600" + "000590001" + "040000000" + "000070000" + "000603040" + "000010800" + "007100020" + "060005000" + "000002003"
        game = parse_puzzle(puzzle)
        result = to_string(game)
        assert len(result) == 81
