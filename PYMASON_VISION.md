# PyMason — Product Vision & Roadmap

> **Building Code. Logically.**

---

## 1. What PyMason Is

PyMason is a visual Python builder powered by Google Blockly. Users drag and connect blocks to construct Python programs, and the corresponding Python code appears in real time in a side panel. It exists at the intersection of two audiences:

- **Beginners and ADHD/ND developers** who struggle with syntax-first learning. PyMason removes the blank-page problem — you can't write invalid syntax when you're snapping blocks together. The generated code teaches Python by osmosis: you see what each block produces, you learn the language without memorizing it.

- **Senior developers** who want to prototype quickly, sketch control flow visually, or use PyMason as a thinking tool for algorithm design. The visual representation makes structure visible in a way that text can't.

PyMason is a single HTML+JS file. No server, no build step, no dependencies beyond Blockly loaded from a CDN. It runs in any browser, offline-capable, and will eventually ship as a paid Electron desktop app via Gumroad alongside a free web demo.

---

## 2. Design Principles

### 2.1 Teaches By Design, Not By Lecturing
PyMason doesn't have a "tutorial mode." The act of using it IS the tutorial. Every block you drag generates real Python. Every connection you make teaches you how Python structures nest. The tool teaches through doing, not through reading.

### 2.2 No Dead Ends
If Python can do it, PyMason should be able to express it. A user should never hit a wall where they think "I know what I want to do in Python but there's no block for it." Every gap in the block library is a broken promise.

### 2.3 One File, Zero Friction
The entire app lives in a single HTML file. No npm, no webpack, no React, no build pipeline. Open the file, start building. This is a product decision, not a limitation — it keeps the deployment story dead simple and the codebase navigable.

### 2.4 Professional Aesthetic
PyMason uses a dark leather-and-brass theme that looks like a craftsman's workshop, not a children's toy. This is intentional — visual programming tools carry a stigma of being "for kids." The aesthetic signals that this is a serious tool for serious work.

### 2.5 Respect the User's Time
Auto-save, keyboard shortcuts, persistent workspaces, sensible defaults. Every interaction should feel fast and recoverable. For ADHD users especially, losing work or having to repeat steps is catastrophic to motivation.

---

## 3. Current State (as of July 2026 — v0.2.3)

### 3.1 What Exists

**Block categories (16 toolbox groups, 126 custom block types + Blockly built-ins):**  
Imports · I/O · Variables · Assign · Text · Convert · Math · Logic · Loops · Lists · Tuples & Sets · Dicts · Errors · Functions · Func Tools · Classes  

Coverage includes control flow (`pass`, ternary, `with`, `assert`, `match`/`case`), data structures (list/dict/set/tuple + comprehensions), string/math/random helpers, file I/O, JSON, OOP (`class`, `self`, `super`, dunders), async/`await`/`yield`, imports with module presets, and more. Generators are smoke-tested headlessly.

**Execution:**
- Pyodide 0.25.1 (CDN) — Web Worker when `SharedArrayBuffer` is available, main-thread fallback otherwise
- Run / Stop, stdout/stderr, inline `input()` (worker) or `prompt` (fallback), execution time, variable inspector
- Empty-`input()` wake protocol and Stop cancel fixed (audit 0.2.1)

**IDE features:**
- Live Python generation + syntax highlighting + line numbers
- Block ↔ code highlighting (select block or click code line)
- Block search (Ctrl+F), disable block, “Show Python for this block”
- Auto-save (30s) + last-saved timestamp; named multi-slot workspaces; JSON export/import
- F1 Help panel; welcome overlay + first-block hint
- Orphan / empty-input warnings; keyboard shortcuts; ARIA roles
- AI chat (optional Anthropic key in localStorage) + Build This / Explain / Debug / Review

**Learning:**
- 10 example programs (Hello World through Word Counter / Simple Class / Temperature Converter)
- Enhanced tooltips with Python syntax samples

**Product / packaging:**
- `landing.html` marketing entry
- Electron shell (`electron/`) with native menus; Save as `.py`; Open `.py` as reference dump
- Docs: user guide, FAQ, block reference, hosting; `AUDIT.md`; smoke suite (`npm test`)
- CDN pins: Blockly **12.5.1**, keyboard-navigation **3.0.5**, Pyodide **0.25.1**
- `netlify.toml` ready for deploy (optional COOP/COEP)

### 3.2 What's Missing (remaining product / polish)

Ordered by launch impact, not educational fundamentals (those are largely done):

1. **Public hosting** — connect Netlify/Pages account (config exists)
2. **Gumroad / license / auto-update** for paid Electron
3. **Deeper E2E** — Pyodide execute-in-browser automation still light
4. **A11y polish** — high contrast, reduced motion
5. **IDE niceties** — minimap, code folding, progressive toolbox disclosure
6. **Multi-language generators** (JS/Lua) — architectural option, not started
7. **CSP / SRI** for public demo hardening

Detailed checklist: `PYMASON_TODO.md`.

---

## 4. Roadmap — Detailed

### Phase 1: Complete the Block Library (Python Fundamentals)

These are blocks that should exist because they represent core Python that any user will need within their first few hours of building.

#### 1.1 Control Flow Additions
- **`pass` statement block** — A statement block that generates `pass`. Needed inside empty `if` branches, empty function bodies, empty `except` blocks. Currently Blockly auto-generates `pass` for empty statement slots, but users should be able to place it intentionally.
- **Ternary expression block** — `value_if_true if condition else value_if_false`. This is a value block (has output). Extremely common Python pattern that currently has no block representation.
- **`with` / context manager block** — `with EXPRESSION as VARIABLE:` with a statement input for the body. Essential for file I/O (`with open('file') as f:`), locks, database connections.
- **`assert` statement block** — `assert condition, message`. Statement block with a boolean input and an optional string input for the message.

#### 1.2 Data Structure Additions
- **Tuple creation block** — `(a, b, c)`. Value block that creates a tuple. Should support variable number of items (like `lists_create_with`).
- **Set creation block** — `{a, b, c}` or `set()`. Value block. Include basic set operations as additional blocks: `.add()`, `.discard()`, `union`, `intersection`, `difference`.
- **Slice notation block** — `sequence[start:stop:step]`. Value block that takes a list/string and three optional number inputs. Generates `my_list[1:3]`, `text[:5]`, `nums[::2]`, etc.
- **`in` / `not in` operator block** — `item in collection`. Currently exists for dicts only (`py_dict_has_key`). Needs to work generically for lists, strings, tuples, sets. Should be a boolean value block.

#### 1.3 String Additions
- **Multi-line string block** — Triple-quoted strings (`"""text"""`). Text area input instead of single-line field. Useful for docstrings and multi-line output.
- **String formatting with `.format()`** — While f-strings are preferred, `.format()` is still widely used and appears in tons of learning materials.
- **`str.startswith()` / `str.endswith()`** — Boolean value blocks. Very common string checks.
- **`str.join()`** — `delimiter.join(list)`. Value block. The inverse of `.split()`.
- **`str.count()`** — Count occurrences of a substring. Value block.

#### 1.4 Numeric Additions
- **`range()` as a standalone value block** — Currently `range()` is generated implicitly by Blockly's `for` loop. But users need `range()` as a value they can assign to variables, pass to `list()`, use in comprehensions.
- **Integer division `//` operator** — Python's floor division. Currently only standard division exists in the math arithmetic block. Should be added to the arithmetic dropdown.
- **`abs()` block** — Absolute value. Value block.
- **`min()` / `max()` block** — Takes two or more values. Value block.
- **Power operator `**`** — Exponentiation. Either add to arithmetic dropdown or as a standalone block.

#### 1.5 Function / Scope Additions
- **`return` with no value** — Blockly's procedure blocks handle `return value` but not bare `return` (exits a function without returning anything).
- **`global` statement** — `global variable_name`. Statement block. Needed when modifying global variables inside functions.
- **`lambda` block** — `lambda args: expression`. Value block. Debatable for a visual tool, but senior developers will want it and it appears frequently in `sorted(key=lambda x: x.name)` patterns.
- **Decorator block** — `@decorator` that attaches above a function definition. At minimum `@staticmethod` and `@classmethod`, ideally with a text field for custom decorators.

#### 1.6 Iteration Additions
- **`enumerate()` block** — `for index, item in enumerate(list):`. Either a modified for-each block with an index variable, or a standalone value block.
- **`zip()` block** — `for a, b in zip(list1, list2):`. Same approach — either a loop variant or a value block.
- **List comprehension block** — `[expression for item in iterable if condition]`. Value block. This is one of Python's most distinctive features and a major gap.
- **Dict comprehension block** — `{key: value for item in iterable}`. Value block.
- **`sorted()` function block** — Returns a new sorted list (vs `.sort()` which modifies in place). Value block with optional `key` and `reverse` parameters.

#### 1.7 Import / Module System
- **`import` statement block** — `import module_name`. Statement block with a text field.
- **`from ... import ...` block** — `from module import name`. Statement block with two text fields.
- **`import ... as ...` block** — `import module as alias`. Statement block.
- **Common module presets** — Dropdown with frequently used modules: `random`, `math`, `os`, `sys`, `json`, `datetime`, `re`, `collections`, `itertools`, `functools`.

#### 1.8 Variable / Assignment Additions
- **Multiple assignment block** — `a, b = 1, 2`. Statement block.
- **Tuple unpacking block** — `a, b, c = my_tuple`. Statement block.
- **Augmented assignment blocks** — `+=`, `-=`, `*=`, `/=`. Statement blocks. Currently users must do `x = x + 1` which is verbose.

#### 1.9 Miscellaneous Fundamentals
- **`del` statement** — `del variable` or `del list[index]`. Statement block.
- **`isinstance()` check** — `isinstance(obj, Type)`. Boolean value block.
- **`type()` check** — `type(obj)`. Value block.
- **Walrus operator** — `(name := expression)`. Value block. Python 3.8+ feature, increasingly common.
- **`not` as prefix** — While `logic_negate` exists, it generates Blockly-style code. Ensure it generates clean Python `not x`.

---

### Phase 2: Classes & Object-Oriented Programming

This is a full new toolbox category. Without it, PyMason caps out at "scripting tool" and can't express most real-world Python.

#### 2.1 Class Basics
- **`class` definition block** — `class ClassName:` with a statement input for the body. Should have an optional parent class input for inheritance.
- **`__init__` method block** — Special function block that auto-includes `self` as first parameter. Statement input for body.
- **Method definition block** — `def method_name(self, params):`. Like the function block but auto-includes `self`.
- **`self.attribute` get block** — `self.name`. Value block.
- **`self.attribute` set block** — `self.name = value`. Statement block.
- **`self.method()` call block** — Call a method on self. Statement or value block depending on return.

#### 2.2 Inheritance & Advanced OOP
- **Inheritance notation** — `class Child(Parent):`. The class block should have an optional input for parent class.
- **`super().__init__()` block** — Statement block for calling parent constructor.
- **`super().method()` block** — Statement block for calling parent methods.
- **`@property` decorator block** — Getter/setter property pattern.
- **`@staticmethod` / `@classmethod`** — Decorator blocks.

#### 2.3 Object Usage (outside class body)
- **Object instantiation** — `my_obj = ClassName(args)`. Value block.
- **Attribute access** — `obj.attribute`. Value block.
- **Method call** — `obj.method(args)`. Statement or value block.

---

### Phase 3: Code Execution

The single most impactful feature for learning. Without execution, users build code but never see it run. The feedback loop is broken.

#### 3.1 Pyodide Integration
- Load Pyodide (Python compiled to WebAssembly) from CDN
- ~7MB initial load, cacheable in browser
- Runs entirely client-side — no server, no security concerns
- Handles all built-in Python: print, input, loops, lists, dicts, classes, imports (for standard library modules)

#### 3.2 Execution UI
- **Run button** in the header (prominent, accent-colored)
- **Output panel** below or beside the code panel — collapsible/resizable
- **stdout capture** — `print()` output appears in the output panel with monospace formatting
- **stderr capture** — Errors appear in red with the traceback
- **Clear output button**
- **Stop/Kill button** — For infinite loops or long-running code. Pyodide runs in a web worker, so the main thread stays responsive and the worker can be terminated.

#### 3.3 Input Handling
- When `input()` is called during execution, pause and show a text input prompt in the output panel
- User types their input, presses Enter, execution resumes
- The prompt text from `input("Enter name: ")` should be visible

#### 3.4 Execution Feedback
- **Visual block highlighting** — Blockly supports highlighting blocks during execution. As each line runs, highlight the corresponding block. This connects the visual and textual representations in real time.
- **Variable inspector** — Show current variable values in a side panel during/after execution. Optional, but extremely useful for learning.
- **Execution time** — Show how long the script took to run

---

### Phase 4: IDE & Quality-of-Life Features

These are the features that turn PyMason from a functional tool into a pleasant tool.

#### 4.1 Workspace Management
- **Auto-save on timer** — Save to localStorage every 30-60 seconds automatically. Show a "last saved" timestamp.
- **Named workspaces** — Let users name their workspace. Use the name for exported filenames instead of generic `pymason_workspace.json`.
- **Multiple workspace slots** — Save/load from multiple named slots, not just one `pymason_workspace` key.
- **Workspace thumbnail** — When browsing saved workspaces, show a small preview of the block arrangement.

#### 4.2 Code Panel Enhancements
- **Line numbers** — Gutter with line numbers in the code panel. Helps when discussing code.
- **Fix `\n` literal in empty state** — The empty state text currently shows `\n` as literal text instead of a line break.
- **Code folding** — Collapse function bodies, class bodies, loops in the code panel (optional, advanced).
- **Match highlighting** — When a block is selected in the editor, highlight the corresponding lines in the code panel. And vice versa — click a line in code panel, highlight the block.

#### 4.3 Block Editor Enhancements
- **Block search** — Ctrl+F or a search bar in the toolbox. User types "append" and the toolbox filters to show only matching blocks. Critical when the block library grows large.
- **Block disable/enable** — Right-click a block to disable it (greys it out, excludes from code generation). Like commenting out code.
- **Minimap** — Small overview of the entire workspace in a corner, like VS Code's minimap. Clickable to navigate.
- **Block grouping / regions** — Let users group blocks visually and collapse/expand groups.
- **Snap-to guides** — Visual alignment guides when dragging blocks near other blocks.
- **Block count per category** — Show how many blocks of each category are in use.

#### 4.4 Keyboard Shortcuts
- **Ctrl+Z / Ctrl+Y** — Undo/Redo (Blockly supports this, needs binding)
- **Ctrl+S** — Save workspace
- **Ctrl+Shift+S** — Export workspace
- **Ctrl+Enter** — Run code (when execution is implemented)
- **Ctrl+C** — Copy generated Python
- **Ctrl+D** — Download .py file
- **Escape** — Close flyout / deselect
- **F1** — Open help/docs
- **Ctrl+F** — Open block search

#### 4.5 Error & Validation
- **Empty input warnings** — Visual indicator (red outline or icon) on blocks that have required inputs left empty.
- **Type mismatch hints** — If a user connects a number block where a string is expected, show a subtle warning.
- **Disconnected block warnings** — Highlight blocks that are on the workspace but not connected to anything (orphan blocks).

#### 4.6 Accessibility
- **Screen reader support** — Blockly has built-in accessibility features that need to be enabled and tested.
- **High contrast mode** — Alternative theme with higher contrast ratios for users with visual impairments.
- **Keyboard-only navigation** — Full toolbox and workspace navigation without a mouse.
- **Reduced motion mode** — Disable animations for users with motion sensitivity.

---

### Phase 5: Learning & Onboarding Features

These transform PyMason from a tool into a learning environment.

#### 5.1 Example Programs
Pre-built workspaces that users can load to see working examples:
- **Hello World** — Single print block. The "it works" test.
- **Name Greeter** — Input + f-string + print. First interactive program.
- **Number Guessing Game** — While loop, random, if/else, input, type conversion. Covers most fundamentals.
- **Todo List** — Lists, while loop, if/elif/else, input, append, remove, enumerate. Data structures in action.
- **Calculator** — Functions, if/elif, type conversion, try/except. Shows error handling.
- **FizzBuzz** — For loop, modulo, if/elif/else. Classic programming exercise.
- **Rock Paper Scissors** — Random, input, if/elif, functions. Game logic.
- **Temperature Converter** — Functions, math, f-strings. Practical utility.
- **Word Counter** — String methods (split, lower), dicts, for loop. Text processing.
- **Simple Class Example** — Class definition, __init__, methods, instantiation. OOP introduction.

#### 5.2 First-Run Experience
- **Welcome overlay** on first visit explaining the three-panel layout (toolbox, workspace, code)
- **Guided first block** — Subtle animation pointing to the I/O category with "Try dragging a print block" prompt
- **Progressive disclosure** — Don't show all categories at once. Start with I/O, Variables, Math, Logic, Loops. Unlock more as the user demonstrates competence (or let them toggle "Show All" immediately).

#### 5.3 Contextual Help
- **Block tooltips** — Every block already has tooltips. Enhance them with brief Python syntax examples.
- **"What does this generate?"** — Right-click a block to see just its Python output, isolated from the rest.
- **Python reference panel** — A collapsible panel with quick reference for Python syntax, accessible from a "?" button.

#### 5.4 AI Chat Interface
An AI chat panel alongside the block editor and code output. This is the tutor sitting next to the user.

- **Ask about blocks** — "How do I make a loop that counts backwards?"
- **Explain generated code** — "What does `for i in range(10):` mean?"
- **Debug assistance** — "Why is my list empty after the loop?"
- **Natural language to blocks** — "Build me a function that checks if a number is prime" → AI suggests which blocks to use and in what order.
- **Code review** — AI examines the current workspace and suggests improvements.

Implementation: Anthropic API integration (or model-agnostic). The AI sees the current block state and generated Python, and responds in context.

---

### Phase 6: Product & Distribution

#### 6.1 Web Demo (Free)
- Hosted on a simple static site (GitHub Pages, Netlify, or similar)
- Full functionality with all blocks and features
- May have limitations on workspace slots or example programs to incentivize the paid version
- No login required

#### 6.2 Electron Desktop App (Paid via Gumroad)
- Wraps the same single HTML file in Electron
- Benefits over web version: offline always, file system access (save/load .py files directly), larger localStorage, system tray, native keyboard shortcuts, potential Pyodide pre-bundled for instant execution
- License key validation on first launch
- Auto-updates

#### 6.3 Landing Page / Marketing Site
- Clear value proposition: "Learn Python by building, not by reading"
- Live embedded demo (the web version in an iframe or similar)
- Testimonials / social proof
- Pricing: one-time purchase (no subscription)
- Screenshots and GIF demos of key features

#### 6.4 Documentation
- **User Guide** — How to use PyMason, category by category
- **Block Reference** — Every block, what it does, what Python it generates, with examples
- **FAQ** — Common questions (Is this for beginners? Can I use it for real projects? What Python version? etc.)
- **Changelog** — Version history with what's new in each release

#### 6.5 Multi-Language Code Generation
PyMason's architecture (Blockly) supports multiple code generators. The same blocks could generate:
- **JavaScript** — Using Blockly's built-in JS generator
- **Lua** — Using Blockly's built-in Lua generator
- **Custom generators** — For other languages

This is a major expansion that multiplies PyMason's audience. A language toggle in the header would let users switch between Python, JavaScript, etc. The blocks are the same — only the output changes. This teaches the user that programming concepts are universal; only syntax differs.

#### 6.6 Analytics (Opt-In)
- Which blocks are used most
- Which example programs are loaded most
- Where users get stuck (blocks with the most undos)
- Session length and return rate
- All opt-in, privacy-respecting, lightweight (no third-party trackers)

#### 6.7 Version Management
- Semantic versioning (1.0.0 for first stable release)
- Changelog maintained in the repo
- Version number visible in the UI (status bar or about dialog)
- Git tags for releases

---

## 5. Technical Architecture

### 5.1 Current Stack
- **Single HTML application** (`index.html`) — inline CSS + JS; no React/webpack for the core app
- **Google Blockly 12.5.1** from unpkg (pinned): core, blocks, python generator, en messages
- **@blockly/keyboard-navigation 3.0.5** (pinned; peer of Blockly ^12.3)
- **Zelos renderer** + custom leather-and-brass theme
- **Pyodide 0.25.1** (jsDelivr) for in-browser Python; Web Worker + main-thread fallback
- **localStorage** for workspaces, API key, welcome flag
- **Anthropic Messages API** (optional; browser key) for AI chat
- **Electron** optional desktop wrapper under `electron/`
- **Tests:** Node smoke suite (`tests/`) with Blockly headless + Playwright Chromium page load
- **Static hosting:** no app server required; `netlify.toml` optional headers

### 5.2 Future / optional stack additions
- Service Worker for offline web demo
- Pre-bundled Pyodide inside Electron
- CSP + Subresource Integrity on public deploy
- License validation + auto-update for paid desktop
- Multi-language Blockly generators (JS/Lua)

### 5.3 File Structure (Current)
```
PyMason/
├── index.html                 ← Core application (blocks, IDE, Pyodide, AI, examples)
├── landing.html               ← Marketing / entry page
├── package.json               ← Root scripts: npm test, npm run serve
├── netlify.toml               ← Static deploy + optional COOP/COEP
├── PyMason.png                ← Branding / Electron icon source
├── README.md
├── CHANGELOG.md
├── AUDIT.md                   ← Full audit findings
├── SOUL.md                    ← Empire constitution v2 (canonical)
├── SOULv2.0.0.md              ← Versioned copy of SOUL
├── AGENTS.md                  ← Start-here for AIs / directors
├── PYMASON_VISION.md          ← This document
├── PYMASON_TODO.md            ← Task checklist
├── docs/
│   ├── user-guide.md
│   ├── faq.md
│   ├── block-reference.md
│   └── hosting.md
├── electron/
│   ├── main.js
│   ├── preload.js
│   └── package.json           ← electron + electron-builder
└── tests/
    ├── smoke.mjs              ← Structure, generators, examples, DOM, page load
    ├── package.json           ← blockly, playwright, jsdom
    └── fixtures/examples/     ← Generated Python snapshots per example
```

### 5.4 Intentional non-goals (architecture)
- Multi-file project IDE, terminal, git integration
- Server-side execution or user accounts
- Replacing Jupyter/VS Code for production work

---

## 6. Success Metrics

How we know PyMason is working:

1. **A complete beginner can build and run a number guessing game** within 30 minutes of first opening PyMason, without reading any documentation.
2. **A senior developer can prototype a data processing pipeline** (read input, transform, filter, output) faster in PyMason than typing it from scratch.
3. **Every Python concept taught in a CS101 course** has a corresponding block or block combination in PyMason.
4. **Zero "dead ends"** — no moment where a user thinks "I know what I want but PyMason can't do it" for standard Python functionality.
5. **Gumroad sales sustain development** — the paid Electron app generates enough revenue to justify continued development.

---

## 7. Non-Goals (Things PyMason Is NOT)

- **Not a full IDE** — No file management, no multi-file projects, no terminal, no git integration. PyMason builds one script at a time.
- **Not a Python runtime** — Pyodide handles execution, but PyMason isn't trying to replace Jupyter or VS Code for production work.
- **Not a course platform** — No lessons, no progress tracking, no certificates. PyMason is a tool, not a curriculum. It can be used alongside courses, but it doesn't replace them.
- **Not a toy** — Despite being visual, PyMason generates real, runnable Python. The code it produces should be indistinguishable from hand-written code.
