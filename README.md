# VulnRadar 📡

> Terminal mission control for bug bounty hunters — a curses-based TUI.

Zero-dependency Python. Runs in your terminal. Tracks targets, findings, loot (bounty payouts), and a mission log. Animated radar, keyboard-driven, persists to `~/.vulnradar.json`.

## Run
```bash
python3 vulnradar.py
```

## Keys
| Key | Action |
|-----|--------|
| `1`-`5` | Switch views (Radar / Targets / Findings / Loot / Log) |
| `↑`/`↓` | Navigate lists |
| `a` | Add target |
| `f` | Add finding |
| `l` | Add loot (payout) |
| `r` | Radar pulse |
| `q` | Quit |

## Why
A creative, fun, terminal-native mission control for hunters who live in the shell. No browser, no electron, no deps — just curses.

## License
MIT
