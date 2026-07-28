# PyMason User Guide

**Building Code. Logically.**

## Overview

PyMason is a visual Python builder. You drag blocks from a toolbox, snap them together on a workspace, and read (or run) the Python generated on the right.

| Panel | Purpose |
|-------|---------|
| **Toolbox** (left) | Categories of blocks (I/O, Logic, Loops, Classes, …) |
| **Workspace** (center) | Where you assemble your program |
| **Code panel** (right) | Live Python + Run output |

## First five minutes

1. Open `index.html` (or the Electron app).
2. Dismiss the welcome overlay if shown.
3. Open **I/O** → drag a **print** block → attach a text block.
4. Click **Run** (or press `Ctrl+Enter`).
5. Try **Examples → Hello World** or **Name Greeter**.

## Running code

- **Run** loads Pyodide (Python in WebAssembly) on first use, then executes your program.
- **Output** appears below the code panel (stdout in green, errors in red).
- **`input()`** shows an inline field in the output panel.
- **Stop** terminates a runaway run (worker is killed and recreated next time).
- After a successful run, the **variable inspector** lists user variables and their values.

## Saving work

| Action | How |
|--------|-----|
| Quick save | **Save** or `Ctrl+S` (browser localStorage) |
| Auto-save | Every 30 seconds when blocks exist |
| Named slots | **Workspaces** → name → Save |
| Share / backup | **Export** JSON (`Ctrl+Shift+S`) |
| Download script | **Download .py** (`Ctrl+D`) |
| Restore | **Import** a previously exported JSON |

## Finding blocks

- Browse categories in the toolbox.
- **`Ctrl+F`** opens block search — type a name, click a result to open its category.
- Hover blocks for tooltips with Python examples.
- Right-click a block → **Show Python for this block**.

## Block ↔ code navigation

- **Select a block** → matching lines highlight in the code panel.
- **Click a code line** → matching top-level block is highlighted and centered.
- Right-click → **Disable Block** to comment it out of generation.

## AI assistant (optional)

1. Click **AI Chat**.
2. Choose **xAI Grok**, **Ollama**, or **Claude**.
3. Open **Setup** — API key (if needed), model, base URL.
4. Quick actions: Explain, Debug, What Blocks?, **Build This**, Review.

See [ai-providers.md](ai-providers.md). Blocks + generated code are sent as context.

## Toolbox & languages

- **Core categories** / **Show all** — progressive toolbox in the header.
- **Python** / **JavaScript** — output language toggle (Run always uses Python/Pyodide).
- **Unlock all toolbox** (Educate menu) — same as Show all, for classroom machines.

### Toolbox map (v1.5 — Show all)

| Group | Categories |
|-------|------------|
| **Core craft** | Favorites, Stage, Tests, Imports, I/O, Variables, Assign, Text, Convert, Math, Logic, Loops, Lists, Tuples & Sets, Dicts, Errors, Functions, Func Tools, Classes |
| **Stdlib packs (1.4–1.5)** | Time, Random, Path & OS, Regex, Bitwise, Advanced, Collections, Stats, Encode, Text+, Itertools |
| **Teaching scaffolds** | **Web sketch**, **Concurrency** |

**Scaffolds (deliberate, not incomplete):** Web sketch and Concurrency emit *learning-shaped* Python (API/client and thread/async mental models). Browser Pyodide will not fully run real HTTP clients or multi-thread labs the way desktop CPython does. Tooltips say so; replace sketches with `requests` / real threads on desktop when you graduate a project. Full tables: [block-reference.md](block-reference.md).

## Bridge practice (block → text)

Research and classroom reports show the hardest drop-off is not “logic” — it is **text precision** after blocks: colons, indentation, quotes, and the confidence hit when `SyntaxError` appears.

| Mode | How |
|------|-----|
| **Guided** | Free Python is pre-filled from blocks — retype lines, then **Check my typing** |
| **Fill blanks** | Strings/numbers blanked — restore exact values |
| **From memory** | Reference hidden — recreate, then Peek or Check |

Open via **Learn → Bridge practice…**. Coach panel explains indent/colon/quote mismatches.

**Syntax coach:** when Run fails with SyntaxError / IndentationError / NameError, a coach strip appears under Output with plain-language tips and a shortcut back into Bridge practice.

## Learn → career (lifelong use)

PyMason is designed so a student **does not outgrow the product** — they change *how* they use it.

| Profile | Intent |
|---------|--------|
| **Learner** | Tour, examples, blocks-first |
| **Classroom** | Same studio + Educate tools |
| **Professional** | Full forge, portfolio export, career templates |

Open **Learn → Your path (learn → career)** or click the profile badge in the header.  
**Career** menu: templates (CLI, data, class library, API client, test-first), portfolio package, Dual/Free shortcuts.

Portfolio export drops real files: `README.md`, `main.py`, `tests/test_smoke.py`, `requirements.txt`, `.gitignore`, `pymason_workspace.json`.

See [LIFELONG_PATH.md](LIFELONG_PATH.md).

## Header menus

Primary actions stay visible: **Run**, **Stop**, **AI Chat**, account. Everything else is grouped:

| Menu | Contents |
|------|----------|
| **File** | Save, workspaces, project modules, import/export, download `.py`, portfolio package, share link |
| **Edit** | Clear, collapse/expand, copy, diff, Python→Blocks, command palette |
| **View** | Fit, minimap, stage, debug bar, toolbox mode, output language |
| **Learn** | Tour, growth path, examples, paths, curriculum, packages, help |
| **Career** | Profiles, project templates, portfolio / GitHub README |
| **Educate** | Class dashboard, roster, assignments, gradebook, timer, student mode |

## Studio tour (replayable)

After sign-in, the welcome dialog can start a **click-through tour**. Replay anytime:

- **Learn → Studio tour**  
- **Help → Replay studio tour**  
- **Ctrl+K** → “Studio tour (replay)”  
- Keys: **Next** Enter/→ · **Back** ← · **Esc** exit  

## Educator tools

Local-only classroom features (stored in this browser’s localStorage):

| Tool | Purpose |
|------|---------|
| **Roster** | Student names for gradebook rows |
| **New assignment** | Snapshot current workspace as starter + autograde checks |
| **Copy assignment link** | `#assign=…` URL students open to load starter (enters student mode) |
| **Autograde current** | Run rubric checks; record score for a student |
| **Gradebook / CSV** | Review and export scores |
| **Class timer** | Simple session countdown display in the header |
| **Student mode** | Hides the Educate menu for demos / learner machines |
| **Lock toolbox to Core** | Limit categories during assessments |

Demo login remains available for workshop machines; production auth is separate (`auth.config.js`).

## Studio features (v1.1+)

| Control | Action |
|---------|--------|
| **Tour** | Replay step-by-step UI walkthrough |
| **Blocks→Code / Free / Dual** | Live sync, editable buffer, or both at once |
| **→ Blocks** | Parse Free Python into blocks (AST when Pyodide ready) |
| **Import .py** | Load a script and convert to blocks |
| **↻ Sync** | Reload Free Python from blocks |
| **Tests** | Run assert harness on current program |
| **Debug** | Step-in, breakpoints, Step / Cont / To line, locals |
| **Stage** | Turtle/plot/circle/fill, grid, PNG export |
| **Agent Apply** | AI returns JSON or Python → Apply (+ snapshot undo) |
| **Ctrl+Shift+Z** | Undo last studio snapshot (AI/convert) |
| **Project** | Multi-module tabs; download all `.py` |
| **Curriculum** | Autograded units |
| **⌘K** / `Ctrl+K` | Command palette |
| **Fit** / `Ctrl+0` | Zoom workspace to fit |
| **Share** / `Ctrl+Shift+L` | Copy restore link |
| **Paths** | Guided mini-challenges |
| **Packages** | micropip install |
| **Diff** | Compare named workspaces |
| **Map** | Minimap |
| Output **History** | Last 15 runs |
| **Favorites** | Right-click block → Add to Favorites |

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Run |
| `Ctrl+S` | Save |
| `Ctrl+Shift+S` | Export workspace |
| `Ctrl+D` | Download `.py` |
| `Ctrl+F` | Search blocks |
| `Ctrl+0` | Zoom to fit |
| `Ctrl+Shift+L` | Copy share link |
| `Ctrl+C` | Copy Python (when no block selected) |
| `Ctrl+Z` / `Ctrl+Y` | Undo / Redo |
| `F1` | Help panel |
| `Esc` | Close flyouts / dialogs |

## Example programs

| Example | Concepts |
|---------|----------|
| Hello World | print |
| Name Greeter | input, f-string |
| FizzBuzz | for, if (scaffold) |
| Calculator | cast, input |
| Number Guessing Game | while, compare, input |
| Todo List | lists, while, if/elif |
| Rock Paper Scissors | random, lists |
| Simple Class | class, `__init__`, methods |
| Temperature Converter | math, f-strings |
| Word Counter | strings, dicts, loops |

## Tips

- Empty required sockets get a **red dashed outline**.
- Floating disconnected statement blocks show a **warning**.
- Use **Imports** dropdowns for common modules (`math`, `random`, `json`, …) or **custom…**.
- Prefer **with** + **open** for file I/O.
- Classes live under the **Classes** category; instantiate with the object block.

## Desktop (Electron)

From `electron/`:

```bash
npm install
npm start
```

Menus provide Save as `.py`, Export/Import workspace, and Run/Stop.

## Getting more help

- In-app: **Help** button or `F1`
- [FAQ](faq.md)
- [Block Reference](block-reference.md)
- [Changelog](../CHANGELOG.md)
