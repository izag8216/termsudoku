# termsudoku

<div align="center">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
    <defs>
      <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#1a1a2e"/>
        <stop offset="100%" style="stop-color:#16213e"/>
      </linearGradient>
      <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#0f3460"/>
        <stop offset="100%" style="stop-color:#16213e"/>
      </linearGradient>
    </defs>
    <rect width="400" height="400" fill="url(#bg)" rx="16"/>
    <text x="200" y="52" text-anchor="middle" font-family="monospace" font-size="28" font-weight="bold" fill="#e94560">TERMINAL</text>
    <text x="200" y="82" text-anchor="middle" font-family="monospace" font-size="32" font-weight="bold" fill="#e94560">SUDOKU</text>
    <g transform="translate(60, 105)">
      <rect x="0" y="0" width="280" height="280" fill="none" stroke="#e94560" stroke-width="3" rx="4"/>
      <line x1="93" y1="0" x2="93" y2="280" stroke="#e94560" stroke-width="2"/>
      <line x1="187" y1="0" x2="187" y2="280" stroke="#e94560" stroke-width="2"/>
      <line x1="0" y1="93" x2="280" y2="93" stroke="#e94560" stroke-width="2"/>
      <line x1="0" y1="187" x2="280" y2="187" stroke="#e94560" stroke-width="2"/>
      <rect x="1" y="1" width="91" height="91" fill="url(#accent)" opacity="0.5"/>
      <rect x="94" y="1" width="92" height="91" fill="url(#accent)" opacity="0.3"/>
      <rect x="188" y="1" width="91" height="91" fill="url(#accent)" opacity="0.5"/>
      <rect x="1" y="94" width="91" height="92" fill="url(#accent)" opacity="0.3"/>
      <rect x="94" y="94" width="92" height="92" fill="url(#accent)" opacity="0.5"/>
      <rect x="188" y="94" width="91" height="92" fill="url(#accent)" opacity="0.3"/>
      <rect x="1" y="188" width="91" height="91" fill="url(#accent)" opacity="0.5"/>
      <rect x="94" y="188" width="92" height="91" fill="url(#accent)" opacity="0.3"/>
      <rect x="188" y="188" width="91" height="91" fill="url(#accent)" opacity="0.5"/>
      <text x="46" y="55" text-anchor="middle" font-family="monospace" font-size="24" font-weight="bold" fill="#eee">5</text>
      <text x="140" y="55" text-anchor="middle" font-family="monospace" font-size="24" font-weight="bold" fill="#eee">3</text>
      <text x="233" y="55" text-anchor="middle" font-family="monospace" font-size="24" font-weight="bold" fill="#eee">7</text>
      <text x="46" y="145" text-anchor="middle" font-family="monospace" font-size="24" font-weight="bold" fill="#eee">6</text>
      <text x="140" y="145" text-anchor="middle" font-family="monospace" font-size="24" font-weight="bold" fill="#eee">1</text>
      <text x="233" y="145" text-anchor="middle" font-family="monospace" font-size="24" font-weight="bold" fill="#eee">9</text>
      <text x="46" y="240" text-anchor="middle" font-family="monospace" font-size="24" font-weight="bold" fill="#eee">8</text>
      <text x="140" y="240" text-anchor="middle" font-family="monospace" font-size="24" font-weight="bold" fill="#eee">5</text>
      <text x="233" y="240" text-anchor="middle" font-family="monospace" font-size="24" font-weight="bold" fill="#eee">3</text>
      <text x="46" y="55" text-anchor="middle" font-family="monospace" font-size="10" fill="#888" dy="18">1</text>
      <text x="46" y="55" text-anchor="middle" font-family="monospace" font-size="10" fill="#888" dy="28">4</text>
      <text x="140" y="55" text-anchor="middle" font-family="monospace" font-size="10" fill="#888" dy="18">2</text>
      <text x="140" y="55" text-anchor="middle" font-family="monospace" font-size="10" fill="#888" dy="28">6</text>
      <text x="46" y="240" text-anchor="middle" font-family="monospace" font-size="10" fill="#888" dy="18">2</text>
      <text x="46" y="240" text-anchor="middle" font-family="monospace" font-size="10" fill="#888" dy="28">7</text>
      <rect x="35" y="35" width="24" height="24" fill="none" stroke="#e94560" stroke-width="2" rx="2"/>
    </g>
    <text x="200" y="420" text-anchor="middle" font-family="monospace" font-size="14" fill="#e94560">Pencil Marks · Hints · Timer</text>
  </svg>
</div>

<p align="center">
  <strong>Terminal Sudoku</strong> with pencil marks, hints, and rich TUI rendering<br>
  <a href="https://pypi.org/project/termsudoku/"><img src="https://img.shields.io/pypi/v/termsudoku?style=flat-square&label=pypi&color=e94560"></a>
  <img src="https://img.shields.io/pypi/pyversions/termsudoku?style=flat-square&label=python&color=0f3460">
  <img src="https://img.shields.io/pypi/l/termsudoku?style=flat-square&label=license&color=0f3460">
</p>

## Features

- **Rich TUI** -- Beautiful terminal interface with color-coded grid
- **Pencil Marks** -- Track candidate numbers in each cell
- **Conflict Detection** -- Highlights invalid placements instantly
- **Progressive Hints** -- Multiple solving techniques explained
- **Timer & Stats** -- Track your solve time and move count
- **Puzzle Generator** -- Four difficulty levels via backtracking algorithm

## Installation

```bash
pip install termsudoku
```

Or from source:

```bash
git clone https://github.com/izag8216/termsudoku.git
cd termsudoku
pip install -e .
```

## Quick Start

```bash
termsudoku play --difficulty hard
termsudoku play --difficulty easy
```

Navigate with arrow keys, fill with 1-9, press `h` for hints.

## Controls

| Key | Action |
|-----|--------|
| Arrow keys | Navigate cells |
| 1-9 | Fill cell |
| Backspace | Clear cell |
| p | Toggle pencil mark mode |
| Ctrl+Z | Undo |
| h | Get hint |
| Space | Pause/Resume timer |
| q | Quit |

## License

MIT License
