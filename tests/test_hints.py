"""Tests for hint system."""

import pytest
from termsudoku.hints import get_hint
from termsudoku.generator import generate_puzzle


class TestHints:
    def test_get_hint_returns_hint(self):
        game = generate_puzzle("easy")
        hint = get_hint(game, "easy")
        assert hint is not None
        assert 0 <= hint.row < 9
        assert 0 <= hint.col < 9
        assert 1 <= hint.value <= 9

    def test_get_hint_technique_valid(self):
        game = generate_puzzle("medium")
        hint = get_hint(game, "medium")
        assert hint.technique in ("Naked Single", "Hidden Single", "Pointing Pair", "Box Line Reduction", "Fallback")

    def test_get_hint_explanation_provided(self):
        game = generate_puzzle("easy")
        hint = get_hint(game, "easy")
        assert hint.explanation is not None
        assert len(hint.explanation) > 10
