Sudoku Solver using Constraint Satisfaction Problem (CSP)
=========================================================
• Arc Consistency (AC-3) + Backtracking with MRV heuristic
• Interactive Tkinter GUI — user fills cells, system validates & solves
"""

import tkinter as tk
from tkinter import messagebox
import copy, time

# ─────────────────────────────────────────────
#  EASY PUZZLE  (0 = empty)
# ─────────────────────────────────────────────
EASY_PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

# ═══════════════════════════════════════════════════════════════
#  CSP ENGINE
# ═══════════════════════════════════════════════════════════════

def get_peers(r, c):
    """All cells that share a row, column, or 3×3 box with (r,c)."""
    peers = set()
    for i in range(9):
        if i != c: peers.add((r, i))
        if i != r: peers.add((i, c))
    br, bc = 3*(r//3), 3*(c//3)
    for dr in range(3):
        for dc in range(3):
            nr, nc = br+dr, bc+dc
            if (nr, nc) != (r, c):
                peers.add((nr, nc))
    return peers

PEERS = {(r, c): get_peers(r, c) for r in range(9) for c in range(9)}


def init_domains(grid):
    domains = {}
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                domains[(r, c)] = {grid[r][c]}
            else:
                domains[(r, c)] = set(range(1, 10))
    return domains


def ac3(domains):
    """AC-3 arc-consistency algorithm. Returns False if inconsistency found."""
    queue = [(xi, xj) for xi in domains for xj in PEERS[xi]]
    while queue:
        xi, xj = queue.pop(0)
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False
            for xk in PEERS[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True


def revise(domains, xi, xj):
    revised = False
    for val in set(domains[xi]):
        if not any(val != v for v in domains[xj]):
            domains[xi].discard(val)
            revised = True
    return revised


def select_unassigned(domains):
    """MRV (Minimum Remaining Values) heuristic."""
    unassigned = [(len(d), cell) for cell, d in domains.items() if len(d) > 1]
    if not unassigned:
        return None
    return min(unassigned)[1]


def is_complete(domains):
    return all(len(d) == 1 for d in domains.values())


def backtrack(domains):
    if is_complete(domains):
        return domains
    cell = select_unassigned(domains)
    if cell is None:
        return None
    for value in sorted(domains[cell]):
        new_domains = copy.deepcopy(domains)
        new_domains[cell] = {value}
        if ac3(new_domains):
            result = backtrack(new_domains)
            if result is not None:
                return result
    return None


def solve_csp(grid):
    domains = init_domains(grid)
    if not ac3(domains):
        return None
    result = backtrack(domains)
    if result is None:
        return None
    solution = [[0]*9 for _ in range(9)]
    for (r, c), d in result.items():
        solution[r][c] = next(iter(d))
    return solution


# ═══════════════════════════════════════════════════════════════
#  GUI
# ═══════════════════════════════════════════════════════════════

CELL = 58          # px per cell
PAD  = 18          # outer padding
GAP  = 3           # thin grid line
THICK= 4           # box border

# Colour scheme — dark editorial
BG        = "#1a1a2e"
PANEL_BG  = "#16213e"
ACCENT    = "#e94560"
ACCENT2   = "#0f3460"
GOLD      = "#f5a623"
WHITE     = "#f0f0f0"
MUTED     = "#8888aa"
GIVEN_BG  = "#0f3460"
USER_BG   = "#1a1a2e"
SOLVED_BG = "#0d3b26"
ERROR_BG  = "#3b0d0d"
GIVEN_FG  = "#c8d8ff"
USER_FG   = "#f0f0f0"
SOLVED_FG = "#4ecca3"
ERROR_FG  = "#ff6b6b"


class SudokuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku — CSP Solver")
        self.resizable(False, False)
        self.configure(bg=BG)

        self.puzzle   = copy.deepcopy(EASY_PUZZLE)
        self.solution = solve_csp(self.puzzle)   # pre-compute
        self.user     = [[0]*9 for _ in range(9)]
        self.selected = None
        self.solved_display = False

        self._build_ui()
        self._draw_grid()

    # ── Layout ──────────────────────────────────────────────

    def _build_ui(self):
        # Title bar
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=PAD, pady=(PAD, 6))
        tk.Label(hdr, text="SUDOKU", font=("Georgia", 26, "bold"),
                 fg=ACCENT, bg=BG).pack(side="left")
        tk.Label(hdr, text="CSP Solver", font=("Georgia", 13),
                 fg=MUTED, bg=BG).pack(side="left", padx=10, pady=6)

        # Canvas
        size = CELL*9 + THICK*4 + GAP*6   # 3 box borders + 6 thin lines inside
        self.canvas = tk.Canvas(self, width=size, height=size,
                                bg=PANEL_BG, highlightthickness=0)
        self.canvas.pack(padx=PAD, pady=4)
        self.canvas.bind("<Button-1>", self._on_click)
        self.bind("<Key>", self._on_key)

        # Status label
        self.status_var = tk.StringVar(value="Fill in the empty cells and press Validate.")
        self.status_lbl = tk.Label(self, textvariable=self.status_var,
                                   font=("Georgia", 12), fg=MUTED, bg=BG,
                                   wraplength=520, justify="center")
        self.status_lbl.pack(pady=(4, 6))

        # Buttons
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=(0, PAD))
        self._btn(btn_frame, "Validate ✓", self._validate, ACCENT).pack(side="left", padx=6)
        self._btn(btn_frame, "Show Solution", self._show_solution, GOLD).pack(side="left", padx=6)
        self._btn(btn_frame, "Reset", self._reset, MUTED).pack(side="left", padx=6)

        # Legend
        leg = tk.Frame(self, bg=BG)
        leg.pack(pady=(0, PAD))
        for color, label in [(GIVEN_FG,"Given"), (USER_FG,"Your input"),
                              (SOLVED_FG,"Solved"), (ERROR_FG,"Error")]:
            tk.Label(leg, text="■", fg=color, bg=BG, font=("Courier",14)).pack(side="left")
            tk.Label(leg, text=label, fg=MUTED, bg=BG, font=("Georgia",10)).pack(side="left", padx=(0,10))

    def _btn(self, parent, text, cmd, color):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=ACCENT2, fg=color, activebackground=ACCENT2,
                      activeforeground=WHITE, relief="flat",
                      font=("Georgia", 12), padx=14, pady=7,
                      cursor="hand2", bd=0)
        return b

    # ── Drawing ─────────────────────────────────────────────

    def _cell_xy(self, r, c):
        """Top-left pixel of cell (r,c)."""
        # Count thick borders (every 3 cells) and thin gaps
        x = c*CELL + (c//3)*THICK + (c - c//3)*GAP + THICK//2 + 1
        y = r*CELL + (r//3)*THICK + (r - r//3)*GAP + THICK//2 + 1
        return x, y

    def _draw_grid(self):
        self.canvas.delete("all")
        c = self.canvas

        # Draw cells
        for r in range(9):
            for col in range(9):
                x, y = self._cell_xy(r, col)
                given = self.puzzle[r][col] != 0

                if self.solved_display and not given:
                    bg = SOLVED_BG
                elif (r, col) == self.selected and not given:
                    bg = "#2a2a4e"
                elif given:
                    bg = GIVEN_BG
                else:
                    bg = USER_BG

                # Error highlight
                uval = self.user[r][col]
                err = (not given and uval != 0 and
                       self.solution and uval != self.solution[r][col])
                if err: bg = ERROR_BG

                c.create_rectangle(x, y, x+CELL, y+CELL,
                                   fill=bg, outline="")

                # Number
                val = 0
                if given:
                    val = self.puzzle[r][col]
                elif self.solved_display and self.solution:
                    val = self.solution[r][col]
                else:
                    val = self.user[r][col]

                if val != 0:
                    if given:        fg = GIVEN_FG
                    elif self.solved_display: fg = SOLVED_FG
                    elif err:        fg = ERROR_FG
                    else:            fg = USER_FG
                    c.create_text(x+CELL//2, y+CELL//2,
                                  text=str(val), fill=fg,
                                  font=("Georgia", 20, "bold" if given else "normal"))

        # Grid lines
        W = self.canvas.winfo_reqwidth()
        H = self.canvas.winfo_reqheight()

        for i in range(10):
            thick = (i % 3 == 0)
            lw = THICK if thick else GAP
            col_or_row = i * CELL + (i//3)*THICK + max(0,(i - i//3))*GAP
            if thick:
                col_or_row = i * (CELL*3 + GAP*2 + THICK)
                col_or_row = (i * (CELL*3 + GAP*2)) + i*(THICK - GAP) if i>0 else 0
            # recompute cleanly
            px = i*CELL + (i//3)*(THICK-GAP) + i*GAP
            c.create_line(px, 0, px, H,
                          fill=ACCENT if thick else "#2a2a5e",
                          width=THICK if thick else 1)
            c.create_line(0, px, W, px,
                          fill=ACCENT if thick else "#2a2a5e",
                          width=THICK if thick else 1)

        # Selection highlight border
        if self.selected and not self.solved_display:
            r, col = self.selected
            if self.puzzle[r][col] == 0:
                x, y = self._cell_xy(r, col)
                c.create_rectangle(x+1, y+1, x+CELL-1, y+CELL-1,
                                   outline=ACCENT, width=2)

    # ── Events ──────────────────────────────────────────────

    def _on_click(self, event):
        if self.solved_display:
            return
        # Find which cell was clicked
        for r in range(9):
            for col in range(9):
                x, y = self._cell_xy(r, col)
                if x <= event.x < x+CELL and y <= event.y < y+CELL:
                    if self.puzzle[r][col] == 0:
                        self.selected = (r, col)
                        self._draw_grid()
                    return

    def _on_key(self, event):
        if self.solved_display or not self.selected:
            return
        r, col = self.selected
        if event.keysym in ("BackSpace", "Delete", "0"):
            self.user[r][col] = 0
        elif event.char.isdigit() and event.char != "0":
            self.user[r][col] = int(event.char)
        elif event.keysym == "Up"    and r > 0: self.selected = (r-1, col)
        elif event.keysym == "Down"  and r < 8: self.selected = (r+1, col)
        elif event.keysym == "Left"  and col > 0: self.selected = (r, col-1)
        elif event.keysym == "Right" and col < 8: self.selected = (r, col+1)
        self._draw_grid()

    # ── Actions ─────────────────────────────────────────────

    def _validate(self):
        # Build complete grid from puzzle + user input
        grid = copy.deepcopy(self.puzzle)
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    grid[r][c] = self.user[r][c]

        # Check if completely filled
        if any(grid[r][c] == 0 for r in range(9) for c in range(9)):
            self.status_var.set("⚠  Some cells are still empty.")
            self.status_lbl.config(fg=GOLD)
            self._draw_grid()
            return

        # Validate against CSP solution
        if self.solution and grid == self.solution:
            self.status_var.set("🎉  You Won!  All constraints satisfied — perfect solution!")
            self.status_lbl.config(fg=SOLVED_FG)
            self._celebrate()
        else:
            self.status_var.set("✗  Try Again.  One or more cells violate Sudoku constraints.")
            self.status_lbl.config(fg=ERROR_FG)
        self._draw_grid()

    def _celebrate(self):
        """Flash the title accent colour briefly."""
        def flash(n=6, on=True):
            if n == 0: return
            color = SOLVED_FG if on else ACCENT
            self.status_lbl.config(fg=color)
            self.after(180, lambda: flash(n-1, not on))
        flash()

    def _show_solution(self):
        if not self.solution:
            messagebox.showerror("CSP Error", "No solution found for this puzzle.")
            return
        self.solved_display = True
        self.selected = None
        self.status_var.set("CSP solution displayed (AC-3 + Backtracking with MRV heuristic).")
        self.status_lbl.config(fg=SOLVED_FG)
        self._draw_grid()

    def _reset(self):
        self.user = [[0]*9 for _ in range(9)]
        self.selected = None
        self.solved_display = False
        self.status_var.set("Fill in the empty cells and press Validate.")
        self.status_lbl.config(fg=MUTED)
        self._draw_grid()


# ═══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()
