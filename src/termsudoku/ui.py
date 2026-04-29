"""Rich-based TUI rendering for Sudoku."""

from typing import Optional
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from .game import GameState, GRID_SIZE, EMPTY


BOX_SIZE = 3


class SudokuUI:
    """Rich-based Sudoku TUI renderer."""

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self.game: Optional[GameState] = None

    def render_board(self, game: GameState) -> Panel:
        """Render the Sudoku board."""
        self.game = game
        grid = Table(show_header=False, box=None, pad_cell=False, cell_padding=0)

        for r in range(GRID_SIZE):
            row_cells = []
            for c in range(GRID_SIZE):
                cell = game.get_cell(r, c)
                cell_text = self._render_cell(cell, r, c, game)
                row_cells.append(cell_text)

            grid.add_row(*row_cells)

            if r in (2, 5):
                grid.add_row(*["─" * 7 for _ in range(GRID_SIZE)])

        title = self._build_title(game)
        return Panel(grid, title=title, border_style="cyan")

    def _render_cell(self, cell, row: int, col: int, game: GameState) -> Text:
        """Render a single cell."""
        is_selected = game.selected_row == row and game.selected_col == col
        has_conflict = game.has_conflict(row, col)

        if cell.value != EMPTY:
            style = self._get_cell_style(is_selected, has_conflict, cell.is_given)
            return Text(f"  {cell.value}  ", style=style, justify="center")
        elif cell.pencil_marks:
            marks = " ".join(str(m) for m in sorted(cell.pencil_marks))
            marks = marks.ljust(5)
            if len(cell.pencil_marks) > 3:
                marks = marks[:5]
            style = self._get_cell_style(is_selected, has_conflict, False)
            return Text(f" {marks}", style=style)
        else:
            content = "    " if is_selected else "  .  "
            style = self._get_cell_style(is_selected, has_conflict, False)
            return Text(content, style=style)

    def _get_cell_style(self, is_selected: bool, has_conflict: bool, is_given: bool) -> str:
        """Get style for cell."""
        if has_conflict:
            return "bold red on red"
        if is_selected:
            return "bold white on cyan"
        if is_given:
            return "bold white"
        return "white"

    def _build_title(self, game: GameState) -> str:
        """Build title with timer and moves."""
        timer_str = self._format_timer(game.timer)
        moves_str = len(game.moves)
        return f"[cyan]SUDOKU[/cyan]  Timer: {timer_str}  Moves: {moves_str}"

    def _format_timer(self, seconds: float) -> str:
        """Format seconds as MM:SS."""
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes:02d}:{secs:02d}"

    def render_help(self) -> Panel:
        """Render help panel."""
        help_table = Table(box=None, show_header=False)
        help_table.add_column(style="cyan")
        help_table.add_column()

        help_table.add_row("Arrow Keys", "Navigate cells")
        help_table.add_row("1-9", "Fill cell with number")
        help_table.add_row("Backspace", "Clear cell")
        help_table.add_row("p", "Toggle pencil mark mode")
        help_table.add_row("Ctrl+Z", "Undo")
        help_table.add_row("h", "Get hint")
        help_table.add_row("Space", "Pause/Resume timer")
        help_table.add_row("q", "Quit")

        return Panel(help_table, title="Controls", border_style="yellow")
