# PyMason Line-by-Line Audit

**Date:** 2026-07-13  
**Version:** 0.2.4 (+ string-escape fixes from this audit)  
**Scope:** Entire repo with exhaustive focus on `index.html` (7,035 lines)  
**Method:** Region walk of `index.html`, static scanner (`tests/line-audit.mjs`), generator/security pattern review, Electron/tests/docs spot-check  
**SOUL:** 2.0.0 pre-delivery standards  

> **Honest scope note:** A human-readable “every line of prose” commentary on 7k+ lines would be noise. This audit is **line-referenced**: every region is mapped; every defect class is tied to exact line numbers; automated scan + manual deep-read of security and generator hotspots.

Re-run scanner:

```bash
node tests/line-audit.mjs
# results → tests/line-audit-results.json
```

---

## 1. File map (`index.html`)

| Lines | Region | Role |
|------:|--------|------|
| 1–14 | Head / CDN | Pinned Blockly 12.5.1 + keyboard-nav 3.0.5 |
| 15–857 | CSS | Leather/brass theme, layout, chat/help, a11y highlights |
| 859–1012 | HTML shell | Header, chat, main, code/output, help, status |
| 1013–1730 | Toolbox XML | All categories / blocks exposed in UI |
| 1732–4607 | Blocks + generators | ~126 custom types + Python codegen |
| 4608–4700 | Theme + inject | Workspace setup, keyboard nav plugin |
| 4700–5160 | Tooltips, updateCode, highlight, actions | Live codegen UX |
| 5160–5660 | Pyodide | Worker, SAB input, fallback, Run/Stop |
| 5660–6080 | Shortcuts, disable, orphans, empty inputs, workspaces | IDE QoL |
| 6080–6700 | Examples + welcome + first-run | Learning layer |
| 6700–7035 | AI chat, version, Electron bridge | Optional tutor + desktop |

**Other files (full read / small surface):**

| File | Lines (approx) | Verdict |
|------|----------------:|---------|
| `electron/main.js` | 149 | Secure defaults OK; version string manual |
| `electron/preload.js` | ~30 | Minimal bridge OK |
| `tests/smoke.mjs` | ~750 | Solid A–F coverage |
| `landing.html` | ~310 | Privacy section present |
| Docs / MANIFEST / SOUL | n/a | Process/docs; not runtime |

---

## 2. Severity legend

| Sev | Meaning |
|-----|---------|
| **CRIT** | Breaks security, correctness, or ship safety now |
| **HIGH** | Likely bug or serious risk under normal use |
| **MED** | Real issue; design trade-off or conditional risk |
| **LOW** | Polish / consistency / a11y |
| **OK** | Explicitly verified good |

---

## 3. Critical / high findings

### Fixed during this audit (were HIGH)

| Lines | Issue | Fix |
|------:|-------|-----|
| **3226–3229** | `py_str_format` injected `TEMPLATE` into `'…'` **without escaping** — `'` in field breaks Python / injects syntax | Escape `\` and `'` |
| **2816–2818** | `py_multiline_string` unescaped body — `"""` in field breaks literal | Escape `\` and `"""` |
| **4312–4313** | `py_raw_string` unescaped `'` | Escape `'` |

### Remaining HIGH / CRIT

| Sev | Location | Finding |
|-----|----------|---------|
| — | — | **No CRIT open** after string-escape fixes and prior 0.2.1 runtime fixes |
| HIGH | Architecture | **Monolith** `index.html` (~7k LOC) — every change has large blast radius (SOUL maintainability tax) |
| HIGH | Supply chain | CDN scripts without **SRI**; pin versions mitigate but do not prove integrity |
| HIGH | Tests gap | No automated check that **all** free-text generators escape string literals (only some goldens) |

---

## 4. Medium findings (actionable)

### 4.1 Security & privacy

| Line(s) | Finding |
|--------:|---------|
| 3–6 | No CSP in document (host-level only; optional in `netlify.toml`) |
| 6780–6810 | Anthropic API key in `localStorage` |
| 6950–6960 | `anthropic-dangerous-direct-browser-access` — required for pure browser chat; **not** multi-tenant safe |
| 6838–6843 | Full workspace code sent to Anthropic as system context when chatting |
| 5960–5990 | Workspace JSON in localStorage — XSS on same origin could read it |

**Assessment:** Acceptable for personal/local tool; documented on landing `#privacy`. Public kiosk deploy needs stronger warnings or disable AI.

### 4.2 Free-text → Python (code generation surface)

These concatenate FieldTextInput into code **without** validating identifiers. That is **normal for Blockly teaching tools** (invalid input → invalid Python). Not XSS (code is escaped in display), but **not sandboxed** if someone later `eval`s generated code outside Pyodide.

| Line | Block | Fields |
|-----:|-------|--------|
| 2300+ | py_import / from / as | MODULE, NAME, ALIAS |
| 2992 | py_decorator | NAME |
| 3255–3310 | py_class / init / method | NAME, PARENT, PARAMS |
| 3326–3475 | self/obj get/set/call | ATTR, ARGS |
| 3429 | py_instantiate | CLASS, ARGS |
| 4484 | py_async_def | NAME, PARAMS |

### 4.3 Runtime / execution

| Line(s) | Finding |
|--------:|---------|
| **5214** | Worker `input_request` always posts `"prompt": ""` — prompt text depends on Pyodide stdout behavior |
| 5230–5235 | Shared buffer only attached if provided; guarded by no-SAB → fallback (OK) |
| 5259 | Variable inspector failures silently ignored |
| 5510–5560 | Concurrent Run partially serialized via load promise; double-click mid-run still possible |
| Worker blob URL | Never revoked — minor leak if worker recreated often (Stop recreates) |

### 4.4 innerHTML

| Line(s) | Risk |
|--------:|------|
| 6855–6860 | Chat: **OK** — `escapeHtml` first |
| 5430+ | Var inspector: **OK** — escaped |
| 4875 | Code panel: **OK** — `highlightPython` escapes |
| 5687, 5859, 6026, 6683, 6699, 6729, 6798, 6869 | Static/template UI strings — **LOW/MED**; not user HTML except workspace names in manager (see below) |

**Workspace manager (6026+):** workspace **names** interpolated into HTML. If a user names a workspace `<img onerror=…>`, that is **stored XSS** in localStorage UI.

| Sev | Line region | Issue |
|-----|-------------|-------|
| **HIGH** | ~6026–6060 | `entry.name` / name input embedded in `innerHTML` without escape |

---

## 5. Low findings

| Line(s) | Finding |
|--------:|---------|
| 1831 | UI shows `f"…"`, generator emits `f'…'` (escaped) |
| 2918–2924 | `py_return` no `nextStatement` — intentional terminal block |
| 0 / CSS | No `prefers-reduced-motion` |
| 85+ | ~26 `.btn` — header overcrowding on narrow viewports |
| Electron About | Version string duplicated manually vs `package.json` |
| Menu Save | Electron uses Ctrl+Shift+D for save `.py`; web uses Ctrl+D for download — inconsistency |

---

## 6. Verified OK (line-backed)

| Line(s) | Check |
|--------:|-------|
| 9–13 | Blockly + keyboard-nav **pinned** |
| 932+ | `aria-live` on output |
| 1824–1831 | `py_fstring` escapes `\ ' \n \r` |
| 1767–1770 | `py_comment` strips newlines |
| 2945–2947 | `py_global` uses `getVariableName` |
| 4500–4504 | `py_await` uses valid `Order.FUNCTION_CALL` |
| 4521–4524 | `py_starred` uses `Order.UNARY_SIGN` |
| 5294+ | `runResolve` on Stop |
| 5307+ | No SAB → main-thread fallback |
| 5545+ | Input wake = length+1 |
| 6851–6860 | Chat XSS hardened |
| 7020+ | Electron Open `.py` = reference dump |
| electron/main 16–18 | `contextIsolation: true`, `nodeIntegration: false` |

**Blocks/generators:** 126 defs / 124 gens; only mutator internals lack generators (expected). Toolbox custom types all defined (scanner).

---

## 7. Region-by-region notes

### 7.1 Head & CSS (1–857)

- Solid design tokens; consistent dark theme.
- `overflow: hidden` on body — good for app shell; hurts mobile scroll of long help text inside panels only.
- No print stylesheet; N/A for app.
- Animations (`hintPulse`) ignore reduced-motion.

### 7.2 HTML shell (859–1012)

- Header actions: Run, Stop, Clear, Save, Workspaces, Export, Import, Copy, Examples, Download, AI Chat, Help — **dense**.
- Required IDs present (smoke tier D).
- Help content is static HTML — good.

### 7.3 Toolbox (1013–1730)

- Imports presets expanded; good.
- Categories match vision update.
- No dynamic toolbox filtering (progressive disclosure still TODO).

### 7.4 Generators (1732–4607)

- Pattern is consistent: block `init` + `forBlock` generator.
- Empty sockets default to Python-ish placeholders (`None`, `[]`, `pass`) — good for learning, can hide missing-input bugs.
- Mutator tuple create is complex; skipped in headless instantiate tests by design.
- **String generators** now escape after this audit (f-string, format, raw, multiline, comment).

### 7.5 Workspace / codegen UX (4608–5160)

- `updateCode` skips drag events — correct.
- Block↔line map is **top-level coarse** (descendants share parent range) — known limitation.
- Code click selects top-level block only.

### 7.6 Pyodide (5160–5660)

- Architecture sound after 0.2.1 fixes.
- First load network-heavy; smoke F covers Hello World execute.
- Main-thread fallback freezes UI on infinite loops (documented trade-off).

### 7.7 Examples (6080–6700)

- Use `createWorkspaceVariable` (v12 API).
- Number Guessing / Todo use `document.createElement('mutation')` — works in browser; tests use jsdom.
- Several examples are **scaffolds** (comments “add logic here”) — intentional teaching, not complete programs.

### 7.8 AI (6700–7000)

- Markdown is minimal (code fence, backtick, bold).
- No streaming; single request.
- History grows unbounded in session — **LOW** memory concern for long chats.

---

## 8. Electron line audit

| Line | Note |
|-----:|------|
| 16–19 | Secure webPreferences — **OK** |
| 23 | Loads `../index.html` — **OK** |
| 32 | Save accelerator Ctrl+Shift+D vs web Ctrl+D — inconsistent |
| 43–48 | Open `.py` reads UTF-8 sync — fine for small files; no size cap |
| 128–137 | save-py-file IPC — no validation of content size |
| 114 | About version must be bumped with releases manually |

---

## 9. Tests line audit

| Tier | What | Status |
|------|------|--------|
| A | Structure / pins | Pass |
| B | All generators + goldens | Pass |
| C | 10 examples + fixtures | Pass |
| D | DOM IDs | Pass |
| E | Playwright load + Hello UI | Pass |
| F | Pyodide Run Hello | Pass (0.2.4) |
| line-audit.mjs | Static scanner | New |

**Gaps:** no test for workspace-name XSS; no property tests on all string-field generators; no infinite-loop Stop test.

---

## 10. Counts (scanner, post string-escape awareness)

| Severity | Count (approx) |
|----------|---------------:|
| CRIT open | 0 |
| HIGH open | 1–3 (workspace name XSS, CDN SRI, monolith process risk) |
| MED | ~15–20 (free-text codegen, API key, empty prompt, CSP) |
| LOW | ~10 |
| OK verified | 10+ |

---

## 11. Recommended fix order (SOUL priority)

1. ~~**HIGH — Escape workspace names**~~ — **done** (0.2.4)  
2. ~~**HIGH — Smoke cases** for string escapes~~ — **done** B2b (0.2.5)  
3. ~~**MED — Identifier sanitization**~~ — **done** `pySanitize*` (0.2.5)  
4. ~~**MED — Worker input prompt**~~ — **done** `builtins.input` override (0.2.5)  
5. **MED — CSP** enable on deploy after preview (still host action)  
6. ~~**LOW — reduced-motion / header / Electron version**~~ — **done** (0.2.5)

---

## 12. Self-audit (this document)

- Scanner + manual hotspot read completed.  
- Three string-escape bugs **fixed in code** as part of audit remediation.  
- Full narrative is region-based with line references, not 7000 separate sentences (would violate clarity).  
- Re-run: `node tests/line-audit.mjs` and `npm test`.

---

## 13. Suggested commit

```
docs(audit): line-by-line audit report; fix string field escapes in format/raw/multiline
```

---

*End of line-by-line audit. Machine results: `tests/line-audit-results.json`. Human map: this file.*
