# Changelog

All notable changes to PyMason will be documented in this file.

## [1.5.0] — 2026-07-13 / docs sync 2026-07-14

### Even more blocks

Seven toolbox categories (~65 generators) for stdlib-flavored practice:

- **Collections** — Counter, defaultdict, deque, namedtuple, heapq, bisect  
- **Stats** — mean/median/mode/stdev, floor/ceil, sqrt, log, trig, degrees, clamp  
- **Encode** — base64, JSON pretty/file, CSV, urllib quote/qs, hashlib, uuid4, secrets  
- **Text+** — partition, zfill, remove prefix/suffix, expandtabs, translate, chr/ord, multiply, center, f-string expr  
- **Itertools** — chain, cycle, repeat, count, islice, product, combinations, permutations, groupby, reduce, partial  
- **Web sketch** — HTTP GET sketch, urljoin, html.escape, query build, User-Agent header (**teaching scaffold**)  
- **Concurrency** — Thread start/join, Queue put/get, asyncio.run/gather/sleep (**teaching scaffold**)  

**~250** custom `py_*` block types with generators (mutator-only tuple helpers excluded).

### SOUL alignment (docs / packaging)

- `MANIFEST.md` rewritten for **1.5.0** (§29 handoff + §0 self-audit table)  
- `docs/block-reference.md`, `user-guide.md`, `faq.md` synchronized; README / landing / DISTRIBUTE / electron version banners  
- Sketch categories documented as intentional scaffolds (not fake completeness)

## [1.4.0] — 2026-07-13

### More blocks

New toolbox categories and generators (~50 types):

- **Time** — sleep, time.time, datetime.now, strftime/strptime  
- **Random** — seed, random, randint, choice, sample, shuffle, uniform  
- **Path & OS** — getcwd, listdir, path join/exists/basename, makedirs, pathlib.Path  
- **Regex** — search, match, findall, sub, split  
- **Bitwise** — & | ^ << >> ~, pow, round, divmod  
- **Advanced** — getitem/setitem, walrus, bool ops, is None, hasattr/getattr, next/iter, enumerate/zip values, copy/deepcopy, encode/decode, dict merge, list repeat, async for/with, @staticmethod/@classmethod/@property  

**~187** custom `py_*` block types (smoke-verified).

## [1.3.1] — 2026-07-13

### Bridge practice + syntax coach (web pain research)

Research: block→text transition is the #1 learner cliff (syntax shock, indentation, lost confidence).

- **Bridge practice** (Learn menu): guided / fill-blanks / from-memory typing against block-generated Python
- Line-level coach for indent, colon, quotes, print() parentheses
- **Syntax coach** under Output on run errors (IndentationError, SyntaxError, NameError, …) with Bridge shortcut

## [1.3.0] — 2026-07-13

### Lifelong forge — learn → career

- **Profiles:** Learner / Classroom / Professional (header badge + Career menu)
- **Growth path:** Milestone tracker in status bar; **Learn → Your path**
- **Career templates:** CLI tool, data script, class library, API client sketch, test-first module
- **Portfolio package:** README, main.py, tests, requirements, gitignore, workspace JSON
- **GitHub README copy** for portfolio repos
- Docs: `docs/LIFELONG_PATH.md`

## [1.2.0] — 2026-07-13

### Deep AST · worker debugger · distribution

- **AST→blocks:** `def` / `class` / `return` / `from import` / `try` / break/continue / richer expressions
- **Worker debugger:** SharedArrayBuffer step/continue/stop on worker (`debug_run`); falls back to main-thread debug without SAB
- **Public demo packaging:** `landing.html` v1.2 marketing + pricing + download CTAs; Netlify `/` → landing, `/app` → app
- **Store path:** `docs/DISTRIBUTE.md`; Gumroad license verify hook in Electron (`GUMROAD_PRODUCT_ID`); `npm run desktop:build`
- electron-builder `publish` GitHub stub for future auto-update

## [1.1.0] — 2026-07-13

### Best-in-class hardening (close real dual-edit / agent / test gaps)

- **Python → Blocks:** `→ Blocks` converts Free Python via pure-JS subset parser + **Pyodide AST** when available
- **Import .py** file → Free Python + convert to blocks
- **Dual mode:** show live Blocks→Code and Free Python together
- **Studio undo snapshots:** `Ctrl+Shift+Z` after AI apply / convert
- **AI Apply:** workspace JSON **or** Python fence → blocks; streaming replies (xAI/OpenAI-compatible)
- **Debugger:** Step-in, Run-to-line, clear breakpoints
- **Stage:** grid, PNG export, circle, fill
- **Tests:** assert blocks + **Tests** runner panel
- Toolbox **Tests** category

## [1.0.0] — 2026-07-13

### Best-in-class competitive release (Target 1.0+)

- **Dual surface:** Blocks→Code live sync **or Free Python** editable buffer (Run uses active mode; ↻ Sync)
- **Debugger:** Debug bar, line-number breakpoints, block BP, Step / Cont / Stop, live locals, current-block highlight (main-thread Pyodide)
- **Stage:** turtle + plot canvas; **Stage** toolbox category; free-Python `turtle` / `plot` helpers
- **AI Agent Apply:** system prompt requests `pymason-json` workspace serialization; **Apply to workspace** on replies; **Agent Apply** quick action
- **Multi-module projects:** module tabs, add module, download all `.py` + project JSON
- **Curriculum:** packs with **autograde** checks (Foundations, Data)
- **Command palette:** `Ctrl+K` / ⌘K for all studio actions
- Docs: `docs/COMPETITIVE_ROADMAP.md` scorecard targets implemented in-app

### Version
- Semantic **1.0.0** — competitive studio baseline

## [0.5.0] — 2026-07-13

### Added — Studio feature pack (A/B/C/E)

- **Share** workspace via URL hash (`#ws=…`) + **Ctrl+Shift+L**
- **Fit** zoom-to-fit (**Ctrl+0**)
- **Run history** (last 15 runs; Output → History)
- **Jump to error block** (click `line N` in red error output)
- **Packages** UI — micropip install into Pyodide package host
- **Guided paths** — 5 mini-challenges (Paths)
- **Python peek** — selected-block snippet in status bar
- **Favorites** toolbox category + right-click “Add to Favorites”
- **Diff** two named workspaces (line-oriented Python)
- **Minimap** (Map toggle)
- **Collapse / Expand** all collapsible blocks
- **Snap to grid** (context menu)
- Soft input warnings for common missing number sockets
- **Lua** output language (Blockly lua generator; custom blocks partial)
- **Format+Copy** light code cleanup; downloads use formatted text
- **Voice** input for AI chat (Web Speech API where available)
- Docs: `docs/FEATURES_NEXT.md` marked implemented for in-app items

### Fixed

- Toolbox category label alignment with colour tabs (flex rows)
- Empty toolbox after login (`updateToolbox` + no destructive `render()`)

## [0.4.0] — 2026-07-13

### Added
- **WPAI Studio branding** aligned with [wpaistudio.net](https://wpaistudio.net) (forge orange, Cinzel + Inter, dark warm surfaces)
- **Login gate** as studio front door (`auth.config.js` + session; demo users or remote `endpoint`)
- Sign-out chip; docs: `docs/auth-hosting.md`

### Removed
- Matrix digital-rain theme (replaced by WPAI forge UI)

## [0.3.0] — 2026-07-13

### Added
- **Multi-provider AI Chat:** xAI Grok (default), Ollama (local), Claude — provider dropdown + Setup (key/model/base URL)
- Progressive toolbox: Core categories vs Show All
- Output language selector: Python / JavaScript
- Block counts by category in status bar
- Electron system tray (show / run / stop / quit)
- Electron local license key entry (`PM-XXXX-XXXX-XXXX`)
- Landing live demo iframe
- `docs/ai-providers.md`
- Opt-in local session counter (no network)

### Changed
- TODO.md closed for implementable items; external launch steps documented
- Version **0.3.0**

## [0.2.6] — 2026-07-13

### Changed
- **Matrix film UI theme**: phosphor green on black, monospace chrome, green glow, digital-rain canvas background
- Blockly workspace/toolbox themed to match; landing page aligned
- Tagline: “Wake up, Neo… // Building Code. Logically.”

## [0.2.5] — 2026-07-13

### Added
- Soft identifier/param sanitizers for class/method/attr/import-as/async generators (blocks statement injection via free-text fields)
- Smoke **B2b**: string escape + identifier sanitization goldens
- `prefers-reduced-motion` CSS; header actions wrap on narrow widths
- Electron About version read from `package.json`; Save as `.py` accelerator aligned to Ctrl+D

### Fixed
- Worker path overrides `builtins.input` so `input("prompt")` prompt text reaches the Output panel UI

## [0.2.4] — 2026-07-13

### Added
- Smoke **tier F**: Playwright runs Hello World through **Run** and asserts Output contains `Hello` (Pyodide E2E; skip with `SKIP_PYODIDE=1`)
- Landing `#privacy` section — localStorage workspaces, AI key risk, client-side Run
- Hosting/FAQ CSP + shared-machine API key guidance; optional CSP comment in `netlify.toml`
- `AUDIT-LINEBYLINE.md` + `tests/line-audit.mjs` static region/line scanner

### Fixed
- Escape string fields in `py_str_format`, `py_raw_string`, `py_multiline_string` (quote breakout)
- Escape workspace names in Workspaces manager HTML (stored XSS)

### Notes
- Full suite: `npm test` (includes first-time ~7MB Pyodide download). CI tip: `SKIP_PYODIDE=1`.

## [0.2.3] — 2026-07-13

### Added
- Expanded smoke suite tiers C–E: all 10 example builders, Python fixtures under `tests/fixtures/examples/`, DOM contract, Playwright page-load + Hello World UI path
- `jsdom` for headless `controls_if` mutations in example tests

### Changed
- `PYMASON_VISION.md` refreshed for v0.2.3 (current capabilities, stack pins, real file tree)
- Example variable creation uses Blockly v12 `getVariableMap().createVariable` helper

### Notes
- Full suite: `npm test` (~140 assertions). Use `SKIP_BROWSER=1` for headless-only.

## [0.2.2] — 2026-07-13

### Added
- Headless smoke suite (`tests/smoke.mjs`) — structure, blockToCode for all custom blocks, golden outputs, save/load round-trip
- `docs/hosting.md` — deploy notes, SAB vs fallback, CDN pins
- `netlify.toml` — static publish + optional COOP/COEP for worker input
- Root `package.json` with `npm test` / `npm run serve`

### Changed
- Blockly CDN pinned to **12.5.1** (was floating latest)
- keyboard-navigation CDN pinned to **3.0.5**

### Fixed
- `py_await` / `py_yield` used non-existent `Order.AWAIT` / `Order.YIELD` (invalid order under Blockly 12)
- `py_starred` used non-existent `Order.UNARY_PREFIX` → `UNARY_SIGN`

## [0.2.1] — 2026-07-13

### Fixed (full audit pass)
- Empty `input()` no longer deadlocks the Web Worker (`Atomics.wait` wake flag uses length+1)
- **Stop** settles the in-flight run promise (no hung Run button / orphan await)
- Without `SharedArrayBuffer`, load main-thread Pyodide instead of a worker that cannot service `input()`
- Single-flight Pyodide loader (concurrent first Run no longer races)
- AI chat messages HTML-escaped before markdown (XSS hardening)
- f-string and comment generators escape quotes/newlines
- Electron **Open .py** shows file contents in the Output panel as reference
- Full audit written to `AUDIT.md`

## [0.2.0] — 2026-07-13

### Added

**Block Library**
- Common module dropdown presets on import blocks (`os`, `sys`, `math`, `random`, `json`, `datetime`, `re`, …)
- Custom module entry via **custom…** (persisted in workspace serialization)
- Toolbox shortcuts for frequent import combinations

**Execution**
- Variable inspector after each run (user globals with truncated `repr`)

**IDE**
- Code-to-block highlighting (click a line in the code panel → highlight block)
- Right-click **Show Python for this block**
- F1 / Help panel with shortcuts and Python quick reference
- Last-saved timestamp in the status bar
- **Build This** AI quick action (guides natural language → block plan)

**Learning**
- Temperature Converter example
- Word Counter example (string methods + dict scaffold)

**Product**
- `landing.html` marketing entry page
- `README.md`, `docs/user-guide.md`, `docs/faq.md`, `docs/block-reference.md`

### Changed
- Version badge and Electron About dialog → v0.2.0

## [0.1.0] — 2026-04-05

### Added

**Block Library — Complete Python Coverage**
- Control flow: `pass`, ternary, `with`, `assert`, `match/case` (3.10+)
- Data structures: tuples (variable items), sets (create/add/discard/operations), slice notation
- Strings: f-strings, multiline, split/strip/replace/join/startswith/endswith/count/format, upper/lower/title/capitalize, isdigit/isalpha/isalnum, find, padding (zfill/ljust/rjust/center), raw strings
- Numeric: range, floor division, abs, min/max, len, sum, math functions (sqrt/ceil/floor/log/trig/factorial), math constants (pi/e/inf/nan)
- Random: random.choice, random.random, random.shuffle
- Functions: return, global, nonlocal, lambda, decorator, yield/yield from, async def, await, starred unpacking
- Iteration: enumerate, zip, list/dict/set comprehensions, sorted, reversed, any/all, map, filter, for/else, while/else
- Imports: import, from import, import as
- Assignment: augmented (+=, -=, etc.), multiple/tuple unpacking, del, walrus operator
- Lists: append, insert, remove, pop, sort, reverse, extend, index, count, copy, clear
- Dicts: create, get, set, keys/values/items, has_key, get(default), update, pop, setdefault, dict literal
- Sets: create, add, discard, union/intersection/difference/symmetric_diff
- Errors: try/except, try/except as, try/except/finally, try/full (else+finally), raise, bare raise
- File I/O: open (with mode dropdown), file.read/readline/readlines, file.write/writelines
- Built-ins: print(end/sep), input with cast, chr/ord, isinstance, type, introspection (hash/id/dir/repr/vars/callable), getattr/setattr/delattr, collection casting
- JSON: json.dumps/loads
- OOP: class (with inheritance), __init__, methods, self get/set/call, super init/call, instantiation, obj.attribute, obj.method, dunder methods (__str__/__repr__/__len__/__eq__ + 12 more)
- Logic: is/is not identity operators
- Comments: # comment block

**Code Execution**
- Pyodide (Python in WebAssembly) integrated for in-browser execution
- Web Worker execution for non-blocking run (with main-thread fallback)
- Inline input field in output panel (replaces browser prompt)
- Prompt text display from `input("...")` calls
- True execution cancellation via worker termination
- stdout/stderr capture with styled output
- Execution time display
- Error highlighting — block that caused the error gets highlighted

**IDE Features**
- Live Python code generation with syntax highlighting
- Line numbers in code panel
- Block-to-code highlighting (select block → corresponding code lines highlight)
- Block search (Ctrl+F)
- Block disable/enable via right-click context menu
- Orphan block warnings (disconnected blocks show warning)
- Empty input warnings (red dashed outline on blocks missing required inputs)
- Auto-save every 30 seconds
- Named workspaces with save/load/delete
- Export/import workspace as JSON
- Copy Python to clipboard
- Download as .py file
- Resizable divider between block editor and code panel

**Keyboard Shortcuts**
- Ctrl+Enter — Run code
- Ctrl+S — Save workspace
- Ctrl+Shift+S — Export workspace
- Ctrl+D — Download .py
- Ctrl+C — Copy Python (when no block selected)
- Ctrl+F — Block search
- Ctrl+Z / Ctrl+Y — Undo / Redo
- Escape — Close flyout / deselect

**Learning & Onboarding**
- 8 example programs: Hello World, Name Greeter, FizzBuzz, Calculator, Number Guessing Game, Todo List, Rock Paper Scissors, Simple Class
- Welcome overlay explaining the three-panel layout
- Guided first-block hint animation for new users
- Enhanced tooltips with Python syntax examples on 100+ blocks

**AI Chat Assistant**
- Collapsible chat panel with Anthropic Claude integration
- Context-aware: sends current blocks and generated Python with each message
- Quick action buttons: Explain Code, Debug Help, What Blocks?, Review
- API key management (stored locally, never sent elsewhere)
- Simple markdown rendering in responses

**Accessibility**
- ARIA roles on all major panels
- Keyboard navigation via @blockly/keyboard-navigation plugin
- Screen reader friendly output panel (aria-live)

**UI/Theme**
- Dark leather-and-brass visual theme
- Custom Blockly theme with matching colors
- Toast notifications
- Status bar with block count and version number

**Electron Desktop App**
- Desktop wrapper with native menus
- File system save/load for .py files
- Cross-platform build support (Windows/macOS/Linux)
