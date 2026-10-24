# 📡 VulnRadar

> Terminal mission control for bug bounty hunters — a curses-based TUI.

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Deps](https://img.shields.io/badge/dependencies-zero-blue)](#)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey)](#)

A keyboard-driven terminal dashboard for bug bounty hunters who live in the shell.
No browser, no Electron, no web server — just `curses` and your terminal.
Tracks targets, findings, bounty payouts (loot), and a mission log, with an
animated radar sweep and color-coded severity.

---

## 📑 Table of Contents

- [Why VulnRadar](#why-vulnradar)
- [Features](#features)
- [Screenshots](#screenshots)
- [Quick start](#quick-start)
- [Keybindings](#keybindings)
- [Views](#views)
- [Data storage](#data-storage)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Roadmap](#roadmap)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Author](#author)

---

## 🤔 Why VulnRadar

Most bounty trackers are web apps or spreadsheets. VulnRadar is for hunters who
already live in the terminal: a fast, offline, zero-dependency TUI that you can
pop open in a tmux pane alongside your recon pipeline. Track what you're hunting,
what you've found, and what you've earned — without leaving the shell.

## ✨ Features

| Area | Details |
|------|---------|
| UI | `curses`-based TUI, keyboard-driven, color-coded |
| Radar view | Animated sweep with rings, target blips, legend |
| Targets view | Scrollable list of in-scope targets |
| Findings view | Severity-colored (Critical/High/Medium/Low) findings |
| Loot view | Bounty payout tracker with progress bar |
| Log view | Timestamped mission log |
| Persistence | JSON file at `~/.vulnradar.json` |
| Dependencies | Zero — Python stdlib only |

## 🖥️ Screenshots

```
  VULNRADAR  ·  bug bounty mission control
═══════════════════════════════════════════════════════════════════
 1:Radar  2:Targets  3:Findings  4:Loot  5:Log
───────────────────────────────────────────────────────────────────────
        .  .  .  .  .                        TARGETS IN SCOPE
      .     .   .   .                       ▸ example.com
    .    .   ◎   .   .                      ▸ api.target.io
      .     .   .   .                       ▸ staging.target.io
        .  .  .  .  .
   ✦ blip  ·  sweep
───────────────────────────────────────────────────────────────────────
 targets:3  findings:7  loot:$4,200
```

## 🚀 Quick start

```bash
git clone https://github.com/Venu-exe/vulnradar.git
cd vulnradar
python3 vulnradar.py
```

No `pip install`. No config. Just run.

## ⌨️ Keybindings

| Key | Action |
|-----|--------|
| `1` – `5` | Switch views (Radar / Targets / Findings / Loot / Log) |
| `↑` / `↓` | Navigate lists |
| `a` | Add a target |
| `f` | Add a finding (title, severity, target) |
| `l` | Add a loot payout ($) |
| `r` | Fire a radar pulse (random blips) |
| `q` | Quit |

## 📺 Views

- **Radar** — animated sweep, concentric rings, target blips, in-scope target list on the side.
- **Targets** — scrollable list of targets you're hunting.
- **Findings** — color-coded by severity (red = Critical/High, yellow = Medium, cyan = Low).
- **Loot** — total bounty earned with a progress bar toward a $10k goal.
- **Log** — timestamped mission log of every action.

## 💾 Data storage

All data is stored in `~/.vulnradar.json`:

```json
{
  "targets": ["example.com", "api.target.io"],
  "findings": [{"title": "IDOR on /api/user", "sev": "High", "target": "api.target.io"}],
  "loot": 4200,
  "log": ["[14:32] added target: example.com"]
}
```

Back it up, sync it, or version-control it — it's just JSON.

## 📁 Project structure

```
vulnradar/
├── vulnradar.py    # single-file TUI (curses)
└── README.md
```

## 📋 Requirements

- Python 3.8+
- A terminal with color support (most modern terminals)
- Linux or macOS (`curses` is part of the stdlib on Unix)

> Windows users: use WSL.

## 🗺️ Roadmap

- [ ] Edit/delete targets and findings in-app
- [ ] Import targets from a file
- [ ] CVSS score per finding
- [ ] Export findings to Markdown/JSON
- [ ] Configurable loot goal
- [ ] Theming (color schemes)

## ⚠️ Disclaimer

VulnRadar is a personal tracking tool. It does not perform any scanning or
testing itself — you bring your own recon. Use responsibly and only against
targets you're authorized to test.

## 📜 License

MIT — see [LICENSE](LICENSE).

## 👤 Author

**Venu-exe** — cybersecurity student & bug bounty hunter

- GitHub: [@Venu-exe](https://github.com/Venu-exe)
- Project: [vulnradar](https://github.com/Venu-exe/vulnradar)

---

> ⭐ If this helped you, consider starring the repo!
EOF
cd /home/venu/vulnradar && git add README.md && git commit -m "Rewrite README: comprehensive, professional, everyone-knows-about-it" && git pull --rebase 2>&1 | tail -2 && git push 2>&1 | tail