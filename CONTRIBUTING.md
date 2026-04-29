# Contributing to termsudoku

Thank you for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/izag8216/termsudoku.git
cd termsudoku
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
pytest --cov=src/termsudoku
```

## Code Style

We use ruff for linting:

```bash
ruff check .
ruff format .
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Commit Convention

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Refactoring
