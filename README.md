# AI_ProblemSolving_RA2411026050022
# 🧩 AI Problem Solving — CSP Sudoku Solver
### Repository: `AI_ProblemSolving_<RegisterNumber>`

> **Course:** Artificial Intelligence | **Problem:** 6 — Sudoku Solver using Constraint Satisfaction Problem (CSP)

---

## 📁 Folder Structure

```
AI_ProblemSolving_<RegisterNumber>/
│
├── Problem6_Sudoku_CSP/
│   ├── sudoku_csp_solver.html       ← Main GUI (open in any browser)
│   ├── sudoku_logic.py              ← Core CSP logic (Python reference)
│   └── screenshots/
│       ├── ui_main.png
│       ├── ui_solved.png
│       └── ui_win.png
│
└── README.md                        ← You are here
```

---

## 📌 Problem Description

**Sudoku** is a logic-based number placement puzzle played on a **9×9 grid**.

- Some cells are **pre-filled** (given clues).
- The player must fill the remaining cells so that all constraints are satisfied.
- The system evaluates the solution and displays **"You Won"** or **"Try Again"**.

### Objective
Fill every cell in the 9×9 grid such that:
- Each **row** contains digits 1–9 without repetition
- Each **column** contains digits 1–9 without repetition
- Each **3×3 sub-grid** contains digits 1–9 without repetition

---

## 🤖 Algorithm Used — Constraint Satisfaction Problem (CSP)

### What is CSP?
A **Constraint Satisfaction Problem** consists of:
| Component | Sudoku Mapping |
|-----------|---------------|
| **Variables** | Each empty cell in the 9×9 grid |
| **Domains** | Digits {1, 2, 3, 4, 5, 6, 7, 8, 9} |
| **Constraints** | Row, Column, and 3×3 Box uniqueness |

### Techniques Implemented

#### 1. Backtracking Search
The core algorithm explores assignments recursively:
```
function BACKTRACK(assignment, csp):
    if assignment is complete → return assignment
    var ← SELECT-UNASSIGNED-VARIABLE(csp)
    for each value in DOMAIN(var):
        if value is consistent with constraints:
            assign var = value
            result ← BACKTRACK(assignment, csp)
            if result ≠ failure → return result
        remove var = value
    return failure
```

#### 2. MRV Heuristic (Minimum Remaining Values)
- Also called **"Fail-First"** heuristic
- Selects the unassigned variable (empty cell) with the **fewest legal values** in its domain
- Detects failures earlier → prunes the search tree significantly

#### 3. Forward Checking
- After every assignment, immediately computes the **valid domain** for the selected cell
- If any variable's domain becomes **empty** → backtrack immediately (no point exploring further)

### Constraint Propagation
At each step, the algorithm filters the domain by checking:
- **Row constraint:** No other cell in the same row has the same value
- **Column constraint:** No other cell in the same column has the same value
- **Box constraint:** No other cell in the same 3×3 box has the same value

---

## 🖥️ GUI Interface

The interactive interface is built using **HTML5 + CSS3 + Vanilla JavaScript**.

### Features
| Feature | Description |
|---------|-------------|
| 🎮 Interactive Grid | Click any cell and type a digit |
| ⌨️ Keyboard Navigation | Arrow keys move between cells |
| 🔢 Number Pad | On-screen digit buttons |
| 3 Difficulty Levels | Easy / Medium / Hard puzzles |
| ✅ Check Solution | Validates and highlights correct/wrong cells |
| ⚡ Auto-Solve (CSP) | Runs the CSP algorithm and fills the solution |
| 💡 Hint | Reveals one random correct cell |
| 🔄 Reset | Clears all user entries |
| 📊 Live Stats | Tracks filled, empty, correct, wrong count |

---

## ▶️ Execution Steps

### Option 1 — Run in Browser (Recommended)
```bash
# Step 1: Clone the repository
git clone https://github.com/<your-username>/AI_ProblemSolving_<RegisterNumber>.git

# Step 2: Navigate to the problem folder
cd AI_ProblemSolving_<RegisterNumber>/Problem6_Sudoku_CSP/

# Step 3: Open the HTML file in any browser
# Windows:
start sudoku_csp_solver.html

# macOS:
open sudoku_csp_solver.html

# Linux:
xdg-open sudoku_csp_solver.html
```
> No installation, no server, no dependencies — just open and play!

### Option 2 — Run Python Logic (Terminal)
```bash
# Step 1: Make sure Python 3 is installed
python --version

# Step 2: Navigate to the folder
cd AI_ProblemSolving_<RegisterNumber>/Problem6_Sudoku_CSP/

# Step 3: Run the CSP solver
python sudoku_logic.py
```

---

## 📤 Sample Output

### Terminal Output (Python)
```
==================================================
  SUDOKU CSP SOLVER — Backtracking + MRV
==================================================

Initial Puzzle:
+-------+-------+-------+
| 5 3 . | . 7 . | . . . |
| 6 . . | 1 9 5 | . . . |
| . 9 8 | . . . | . 6 . |
+-------+-------+-------+
| 8 . . | . 6 . | . . 3 |
| 4 . . | 8 . 3 | . . 1 |
| 7 . . | . 2 . | . . 6 |
+-------+-------+-------+
| . 6 . | . . . | 2 8 . |
| . . . | 4 1 9 | . . 5 |
| . . . | . 8 . | . 7 9 |
+-------+-------+-------+

Solving using CSP (Backtracking + MRV + Forward Checking)...
Variables assigned: 51
Backtracks performed: 0

Solved Puzzle:
+-------+-------+-------+
| 5 3 4 | 6 7 8 | 9 1 2 |
| 6 7 2 | 1 9 5 | 3 4 8 |
| 1 9 8 | 3 4 2 | 5 6 7 |
+-------+-------+-------+
| 8 5 9 | 7 6 1 | 4 2 3 |
| 4 2 6 | 8 5 3 | 7 9 1 |
| 7 1 3 | 9 2 4 | 8 5 6 |
+-------+-------+-------+
| 9 6 1 | 5 3 7 | 2 8 4 |
| 2 8 7 | 4 1 9 | 6 3 5 |
| 3 4 5 | 2 8 6 | 1 7 9 |
+-------+-------+-------+

✅ Puzzle solved successfully!
==================================================
```

### GUI Output States
| State | Description |
|-------|-------------|
| ✅ **You Won!** | All cells filled correctly — shown in green |
| ❌ **Try Again** | Wrong cells highlighted in red |
| ⚡ **Auto-Solved** | CSP fills all cells with animation |
| 💡 **Hint Given** | One cell revealed with teal flash |

---

## 🧪 Constraints Verification

The solver validates all three constraint types after each assignment:

```python
def is_valid(grid, row, col, num):
    # Row constraint
    if num in grid[row]:
        return False
    # Column constraint
    if num in [grid[r][col] for r in range(9)]:
        return False
    # 3x3 Box constraint
    box_r, box_c = (row // 3) * 3, (col // 3) * 3
    for dr in range(3):
        for dc in range(3):
            if grid[box_r + dr][box_c + dc] == num:
                return False
    return True
```

---

## 🔗 Live Demo

🌐 **[Click here to play the interactive Sudoku CSP Solver](#)**
> *(Replace `#` with your GitHub Pages URL after enabling Pages in repository settings)*


---

## 📝 Commit History Guide

| Commit # | Message | Contents |
|----------|---------|----------|
| 1 | `Initial commit: Add project structure and README` | Folder structure, README.md |
| 2 | `Add CSP logic: backtracking + MRV heuristic` | sudoku_logic.py |
| 3 | `Add GUI: interactive HTML Sudoku solver` | sudoku_csp_solver.html |
| 4 | `Add screenshots and sample outputs` | screenshots/ folder |
| 5 | `Update README with execution steps and live demo link` | README.md update |

---

