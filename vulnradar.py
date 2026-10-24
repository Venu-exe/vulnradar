#!/usr/bin/env python3
"""
VulnRadar - Terminal mission control for bug bounty hunters.
A curses-based TUI: radar, targets, findings, loot tracker, mission log.
Zero dependencies (stdlib curses). Runs on Linux/macOS.
"""
import curses
import json
import os
import random
import time
from datetime import datetime

DATA = os.path.expanduser("~/.vulnradar.json")

def load():
    if os.path.exists(DATA):
        try:
            return json.load(open(DATA))
        except Exception:
            pass
    return {"targets": [], "findings": [], "loot": 0, "log": []}

def save(d):
    json.dump(d, open(DATA, "w"), indent=2)

VIEWS = ["radar", "targets", "findings", "loot", "log"]
VIEW_NAMES = ["1:Radar", "2:Targets", "3:Findings", "4:Loot", "5:Log"]

class App:
    def __init__(self, stdscr):
        self.s = stdscr
        self.d = load()
        self.view = 0
        self.sel = 0
        self.radar_angle = 0
        self.blips = []
        self.msg = ""
        curses.curs_set(0)
        self.s.nodelay(True)
        self.init_colors()

    def init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)   # ok
        curses.init_pair(2, curses.COLOR_RED, -1)     # alert
        curses.init_pair(3, curses.COLOR_YELLOW, -1)  # warn
        curses.init_pair(4, curses.COLOR_CYAN, -1)    # info
        curses.init_pair(5, curses.COLOR_MAGENTA, -1) # accent
        curses.init_pair(6, 8, -1)                    # dim

    def c(self, pair): return curses.color_pair(pair)

    def run(self):
        while True:
            self.s.erase()
            h, w = self.s.getmaxyx()
            self.draw_header(h, w)
            self.draw_body(h, w)
            self.draw_footer(h, w)
            self.s.refresh()
            try:
                ch = self.s.getch()
            except Exception:
                ch = -1
            if ch == ord('q'):
                break
            elif ch in (ord('1'), ord('2'), ord('3'), ord('4'), ord('5')):
                self.view = ch - ord('1')
                self.sel = 0
            elif ch == curses.KEY_UP:
                self.sel = max(0, self.sel - 1)
            elif ch == curses.KEY_DOWN:
                self.sel += 1
            elif ch == ord('a'):
                self.add_target()
            elif ch == ord('f'):
                self.add_finding()
            elif ch == ord('l'):
                self.add_loot()
            elif ch == ord('r'):
                self.radar_pulse()
            self.radar_angle = (self.radar_angle + 2) % 360
            time.sleep(0.05)

    def draw_header(self, h, w):
        title = "  VULNRADAR  ·  bug bounty mission control  "
        self.s.addstr(0, 0, "═" * w, self.c(4))
        self.s.addstr(1, max(0, (w - len(title)) // 2), title, self.c(5) | curses.A_BOLD)
        self.s.addstr(2, 0, "═" * w, self.c(4))
        # tabs
        x = 2
        for i, name in enumerate(VIEW_NAMES):
            attr = self.c(2) | curses.A_BOLD if i == self.view else self.c(6)
            self.s.addstr(3, x, f" {name} ", attr)
            x += len(name) + 3
        self.s.addstr(4, 0, "─" * w, self.c(6))

    def draw_body(self, h, w):
        body_h = h - 7
        if body_h < 5:
            return
        if self.view == 0:
            self.draw_radar(body_h, w)
        elif self.view == 1:
            self.draw_targets(body_h, w)
        elif self.view == 2:
            self.draw_findings(body_h, w)
        elif self.view == 3:
            self.draw_loot(body_h, w)
        elif self.view == 4:
            self.draw_log(body_h, w)

    def draw_radar(self, bh, w):
        cx, cy = w // 4, bh // 2
        radius = min(cx - 2, cy - 2, 14)
        # draw rings
        for r in range(1, radius + 1, 2):
            for ang in range(0, 360, 3):
                import math
                x = int(cx + r * math.cos(math.radians(ang)))
                y = int(cy + (r // 2) * math.sin(math.radians(ang)))
                if 0 <= x < w and 0 <= y < bh:
                    try:
                        self.s.addch(y, x, ".", self.c(6))
                    except curses.error:
                        pass
        # sweep line
        import math
        for i in range(radius):
            x = int(cx + i * math.cos(math.radians(self.radar_angle)))
            y = int(cy + (i // 2) * math.sin(math.radians(self.radar_angle)))
            if 0 <= x < w and 0 <= y < bh:
                try:
                    self.s.addch(y, x, "·", self.c(1) | curses.A_BOLD)
                except curses.error:
                    pass
        # center
        try:
            self.s.addstr(cy, cx, "◎", self.c(2) | curses.A_BOLD)
        except curses.error:
            pass
        # blips
        for b in self.blips:
            x, y = b
            if 0 <= x < w and 0 <= y < bh:
                try:
                    self.s.addstr(y, x, "✦", self.c(3) | curses.A_BOLD)
                except curses.error:
                    pass
        # right panel: targets
        px = w // 2 + 2
        self.s.addstr(0 + 5, px, "TARGETS IN SCOPE", self.c(4) | curses.A_BOLD)
        for i, t in enumerate(self.d["targets"][:bh - 2]):
            try:
                self.s.addstr(6 + i, px, f"  ▸ {t}", self.c(1))
            except curses.error:
                pass
        # legend
        try:
            self.s.addstr(bh - 1, 2, "a:add target  f:add finding  l:add loot  r:pulse  1-5:views  q:quit", self.c(6))
        except curses.error:
            pass

    def draw_targets(self, bh, w):
        self.s.addstr(5, 2, "TARGETS", self.c(4) | curses.A_BOLD)
        self.s.addstr(6, 2, "─" * (w - 4), self.c(6))
        for i, t in enumerate(self.d["targets"]):
            attr = self.c(3) | curses.A_BOLD if i == self.sel else self.c(1)
            marker = "▸" if i == self.sel else " "
            try:
                self.s.addstr(7 + i, 2, f"{marker} {t}", attr)
            except curses.error:
                pass
        if not self.d["targets"]:
            self.s.addstr(8, 4, "(none yet — press 'a' to add)", self.c(6))

    def draw_findings(self, bh, w):
        self.s.addstr(5, 2, "FINDINGS", self.c(4) | curses.A_BOLD)
        self.s.addstr(6, 2, "─" * (w - 4), self.c(6))
        for i, f in enumerate(self.d["findings"]):
            sev_color = {"Critical": 2, "High": 2, "Medium": 3, "Low": 4, "Info": 6}.get(f.get("sev"), 1)
            attr = curses.color_pair(sev_color) | curses.A_BOLD
            marker = "▸" if i == self.sel else " "
            line = f"{marker} [{f.get('sev','?')}] {f.get('title','?')}  · {f.get('target','')}"
            try:
                self.s.addstr(7 + i, 2, line[:w - 4], attr)
            except curses.error:
                pass
        if not self.d["findings"]:
            self.s.addstr(8, 4, "(none yet — press 'f' to add)", self.c(6))

    def draw_loot(self, bh, w):
        self.s.addstr(5, 2, "LOOT (BOUNTY TRACKER)", self.c(4) | curses.A_BOLD)
        self.s.addstr(6, 2, "─" * (w - 4), self.c(6))
        total = self.d.get("loot", 0)
        self.s.addstr(8, 4, f"Total earned: ${total:,}", self.c(1) | curses.A_BOLD)
        bar_w = min(40, w - 10)
        filled = min(bar_w, int(bar_w * min(total, 10000) / 10000))
        self.s.addstr(10, 4, "[" + "█" * filled + "░" * (bar_w - filled) + "]", self.c(3))
        self.s.addstr(11, 4, "Press 'l' to add a payout.", self.c(6))

    def draw_log(self, bh, w):
        self.s.addstr(5, 2, "MISSION LOG", self.c(4) | curses.A_BOLD)
        self.s.addstr(6, 2, "─" * (w - 4), self.c(6))
        for i, entry in enumerate(self.d.get("log", [])[-bh + 8:]):
            try:
                self.s.addstr(7 + i, 2, entry[:w - 4], self.c(1))
            except curses.error:
                pass

    def draw_footer(self, h, w):
        self.s.addstr(h - 2, 0, "─" * w, self.c(6))
        status = f" targets:{len(self.d['targets'])}  findings:{len(self.d['findings'])}  loot:${self.d.get('loot',0):,} "
        if self.msg:
            status += f"  │  {self.msg}"
        self.s.addstr(h - 1, 2, status[:w - 4], self.c(4))

    def prompt(self, label):
        curses.echo()
        self.s.nodelay(False)
        self.s.addstr(0, 0, " " * 200)
        self.s.addstr(0, 2, label, self.c(3) | curses.A_BOLD)
        self.s.refresh()
        val = self.s.getstr(0, len(label) + 4, 60).decode().strip()
        curses.noecho()
        self.s.nodelay(True)
        return val

    def add_target(self):
        name = self.prompt("Target name:")
        if name:
            self.d["targets"].append(name)
            self.d.setdefault("log", []).append(f"[{datetime.now().strftime('%H:%M')}] added target: {name}")
            self.log_blip()
            save(self.d)
            self.msg = f"added target {name}"

    def add_finding(self):
        title = self.prompt("Finding title:")
        if not title:
            return
        sev = self.prompt("Severity (Critical/High/Medium/Low):") or "Medium"
        target = self.prompt("Target:") or ""
        self.d["findings"].append({"title": title, "sev": sev, "target": target})
        self.d.setdefault("log", []).append(f"[{datetime.now().strftime('%H:%M')}] finding: {title} ({sev})")
        save(self.d)
        self.msg = f"logged finding: {title}"

    def add_loot(self):
        amt = self.prompt("Payout amount ($):")
        try:
            n = int(amt.replace("$", "").replace(",", ""))
        except ValueError:
            self.msg = "invalid amount"
            return
        self.d["loot"] = self.d.get("loot", 0) + n
        self.d.setdefault("log", []).append(f"[{datetime.now().strftime('%H:%M')}] loot +${n:,}")
        save(self.d)
        self.msg = f"+${n:,} loot"

    def radar_pulse(self):
        for _ in range(8):
            self.blips.append((random.randint(2, 30), random.randint(2, 12)))
        self.d.setdefault("log", []).append(f"[{datetime.now().strftime('%H:%M')}] radar pulse")
        save(self.d)
        self.msg = "radar pulse fired"
        # keep blips bounded
        self.blips = self.blips[-40:]

def main():
    curses.wrapper(lambda s: App(s).run())

if __name__ == "__main__":
    main()
