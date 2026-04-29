# termsudoku -- PRD

## Problem Statement

Terminal-based sudoku players lack essential features like pencil mark (candidate) tracking, hint systems, and rich rendering. Players who prefer terminal workflows are stuck choosing between minimal implementations or switching to GUI applications.

## Solution Overview

termsudoku provides a full-featured terminal sudoku experience with backtracking-based puzzle generation, interactive pencil marks, conflict detection, and progressive hints. The rich-based TUI renders a beautiful grid with color-coded candidates, error highlighting, and timer display.

## Project Type

**Type:** TUI (Terminal User Interface) Tool
**Stack:** Python, rich, click

## Architecture

```
termsudoku/
├── src/termsudoku/
│   ├── __init__.py
│   ├── cli.py          # click CLI entry
│   ├── game.py         # Game state, Sudoku board logic
│   ├── generator.py   # Backtracking puzzle generator
│   ├── solver.py      # Sudoku solver (for hint system)
│   ├── ui.py          # Rich TUI rendering
│   └── hints.py       # Hint generation logic
├── tests/
│   ├── __init__.py
│   ├── test_generator.py
│   ├── test_solver.py
│   ├── test_game.py
│   └── test_hints.py
├── examples/
│   └── basic/
├── docs/
│   ├── api.md
│   └── usage.md
├── README.md
├── CONTRIBUTING.md
├── pyproject.toml
└── THIRD_PARTY_LICENSES.md
```

## Core Features

### 1. Puzzle Generation
- **Description:** Generate valid Sudoku puzzles using backtracking algorithm
- **Difficulty levels:** easy, medium, hard, expert
- **Acceptance criteria:**
  - Generated puzzle has unique solution
  - Difficulty affects number of given cells
  - Can generate from saved puzzle string

### 2. Interactive Play Mode
- **Description:** Full TUI experience with cell navigation and input
- **Acceptance criteria:**
  - Arrow keys navigate cells
  - Number keys (1-9) fill cells
  - Backspace clears cell
  - Undo/redo support

### 3. Pencil Marks
- **Description:** Track candidate numbers for each cell
- **Acceptance criteria:**
  - Toggle pencil mark mode
  - Show candidates in small text
  - Auto-remove when number placed in row/col/box
  - Conflict detection highlights invalid marks

### 4. Hint System
- **Description:** Progressive hints based on difficulty
- **Acceptance criteria:**
  - Hint reveals one correct cell
  - Hint explains technique used
  - Difficulty affects hint complexity

### 5. Timer & Stats
- **Description:** Track solve time and moves
- **Acceptance criteria:**
  - Running timer display
  - Pause/resume functionality
  - Stats shown on completion

## Testing Strategy

- **Unit tests:** Board logic, generator, solver, hints
- **Integration tests:** CLI commands, full game flow
- **Framework:** pytest with pytest-cov

## CI/CD

GitHub Actions: lint (ruff) -> test (pytest) -> coverage report

## Milestones

1. **M1:** Project scaffold, generator, basic board logic
2. **M2:** Interactive TUI with navigation and input
3. **M3:** Pencil marks and conflict detection
4. **M4:** Hint system
5. **M5:** Timer, stats, polish, CI/CD, publish

## Dependency License Audit

| Dependency | License | Use |
|------------|---------|-----|
| rich | MIT | TUI rendering |
| click | BSD-3-Clause | CLI framework |
| pytest | MIT | Testing |
| pytest-cov | MIT | Coverage |

All dependencies are MIT/BSD compatible. No GPL/AGPL.
