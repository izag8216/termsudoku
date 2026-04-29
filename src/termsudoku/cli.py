"""CLI entry point for termsudoku."""

import sys
import time
import signal
from typing import Optional

import click
from rich.console import Console
from rich.layout import Layout

from .generator import generate_puzzle, parse_puzzle, to_string
from .game import GameState, EMPTY
from .ui import SudokuUI
from .hints import get_hint


console = Console()
ui = SudokuUI()
current_game: Optional[GameState] = None


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully."""
    console.print("\n[yellow]Goodbye![/yellow]")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Terminal Sudoku with Pencil Marks and Hints."""
    pass


@main.command()
@click.option("--difficulty", "-d", default="medium",
              type=click.Choice(["easy", "medium", "hard", "expert"]),
              help="Puzzle difficulty")
def play(difficulty: str):
    """Start a new game."""
    global current_game
    current_game = generate_puzzle(difficulty)
    _run_game(current_game)


@main.command()
@click.argument("puzzle_file", type=click.File("r"))
def solve(puzzle_file):
    """Solve a puzzle from file."""
    puzzle_str = puzzle_file.read().strip()
    try:
        game = parse_puzzle(puzzle_str)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

    global current_game
    current_game = game
    _run_game(current_game)


@main.command()
@click.option("--cell", "-c", required=True, help="Cell coordinates (e.g., r3c5)")
@click.option("--difficulty", "-d", default="medium",
              type=click.Choice(["easy", "medium", "hard", "expert"]),
              help="Hint complexity")
def hint(cell: str, difficulty: str):
    """Get a hint for a specific cell."""
    global current_game
    if current_game is None:
        console.print("[yellow]No game in progress. Start a game first with 'termsudoku play'[/yellow]")
        sys.exit(1)

    try:
        row = int(cell[1]) - 1
        col = int(cell[3]) - 1
        if not (0 <= row < 9 and 0 <= col < 9):
            raise ValueError
    except (ValueError, IndexError):
        console.print("[red]Invalid cell format. Use r1c1 through r9c9[/red]")
        sys.exit(1)

    hint_obj = get_hint(current_game, difficulty)
    if hint_obj:
        console.print(f"[cyan]Hint[/cyan]: Row {hint_obj.row + 1}, Col {hint_obj.col + 1} = {hint_obj.value}")
        console.print(f"[cyan]Technique[/cyan]: {hint_obj.technique}")
        console.print(f"[yellow]{hint_obj.explanation}[/yellow]")
    else:
        console.print("[yellow]No hint available[/yellow]")


@main.command()
def status():
    """Show current game status."""
    global current_game
    if current_game is None:
        console.print("[yellow]No game in progress[/yellow]")
        return

    console.print(f"[cyan]Timer[/cyan]: {current_game.timer:.0f}s")
    console.print(f"[cyan]Moves[/cyan]: {len(current_game.moves)}")
    console.print(f"[cyan]Puzzle[/cyan]: {to_string(current_game)}")


def _run_game(game: GameState):
    """Run interactive game loop."""
    from rich.live import Live
    from .ui import SudokuUI

    ui.game = game
    game.is_paused = False
    start_time = time.time()

    with Live(ui.render_board(game), console=console, refresh_per_second=10) as live:
        while not game.is_complete():
            if not game.is_paused:
                game.timer = time.time() - start_time

            key = console.input("> ")
            key = key.strip().lower()

            if key == "q":
                break
            elif key in ("h", "?"):
                hint_obj = get_hint(game, "medium")
                if hint_obj:
                    console.print(f"Hint: Row {hint_obj.row+1} Col {hint_obj.col+1} = {hint_obj.value} ({hint_obj.technique})")
            elif key == " ":
                if game.is_paused:
                    game.is_paused = False
                    start_time = time.time() - game.timer
                else:
                    game.is_paused = True
                    game.timer = time.time() - start_time
            elif key in ("z", "ctrl+z"):
                game.undo()
            elif key == "p":
                pass
            elif key in ("arrowup", "k"):
                game.selected_row = max(0, game.selected_row - 1)
            elif key in ("arrowdown", "j"):
                game.selected_row = min(8, game.selected_row + 1)
            elif key in ("arrowleft", "h"):
                game.selected_col = max(0, game.selected_col - 1)
            elif key in ("arrowright", "l"):
                game.selected_col = min(8, game.selected_col + 1)
            elif key.isdigit() and 1 <= int(key) <= 9:
                game.set_cell(game.selected_row, game.selected_col, int(key))
            elif key == "backspace":
                game.clear_cell(game.selected_row, game.selected_col)

            live.update(ui.render_board(game))

        if game.is_complete():
            console.print("[bold green]Congratulations! Puzzle solved![/bold green]")
            console.print(f"Time: {game.timer:.0f}s, Moves: {len(game.moves)}")


if __name__ == "__main__":
    main()
