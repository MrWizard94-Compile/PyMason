# PyMason Full Audit Report

**Date:** 2026-07-13  
**Version audited:** 0.2.0 (post-fix)  
**Scope:** Product completeness, block library integrity, runtime execution, IDE/UX, security, Electron, docs consistency  
**Auditor:** automated + manual code review  

---

## Executive summary

PyMason is a **mature single-file visual Python builder** with broad block coverage, live code generation, browser execution (Pyodide), workspaces, examples, AI chat, and an Electron shell. Architecture matches the stated vision (one HTML file, CDN Blockly, leather/brass UI).

This pass found **several high-severity runtime bugs** (execution stop hang, empty `input()` deadlock, SharedArrayBuffer assumptions) and **medium security issues** (chat HTML injection, f-string quote breakage). Those were **fixed in this audit**. Remaining gaps are mostly product/distribution, polish, and automated testing—not core block coverage.

| Severity | Found | Fixed this pass | Still open |
|----------|------:|----------------:|-----------:|
| Critical | 3 | 3 | 0 |
| High | 4 | 4 | 0 |
| Medium | 8 | 2 | 6 |
| Low / backlog | many | 0 | see backlog |

**Overall health:** Ship-ready for local/demo use after fixes. Not yet “paid product launch” ready (hosting, Gumroad, license, automated tests).

---

## 1. Inventory & structure

| Path | Role | Status |
|------|------|--------|
| `index.html` (~330KB) | Entire web app | Primary surface — healthy |
| `landing.html` | Marketing entry | Complete enough for demo |
| `electron/*` | Desktop wrapper | Functional shell |
| `docs/*` | User guide, FAQ, block ref | Present |
| `README.md`, `CHANGELOG.md` | Project meta | Consistent at 0.2.0 |
| `PYMASON_VISION.md` / `TODO` | Roadmap | TODO still has open nice-to-haves |
| `SOUL.md` | AI coding guidelines | Present (process, not product) |
| `PyMason.png` | Branding | Used by landing + Electron |

**Version consistency:** `0.2.0` aligned across `index.html`, Electron `package.json` / About dialog, README, landing, CHANGELOG.

**No git repo** in workspace at audit time — release tags / history tracking not available.

---

## 2. Block library integrity

### Metrics
- **Custom block definitions:** 126  
- **Python generators:** 124  
- **Missing generators:** only `py_tuple_container`, `py_tuple_item` (mutator internals — expected)  
- **Custom toolbox types without definitions:** 0  
- **Toolbox categories:** Imports, I/O, Variables, Assign, Text, Convert, Math, Logic, Loops, Lists, Tuples & Sets, Dicts, Errors, Functions, Func Tools, Classes  

### Verdict
Coverage matches vision Phase 1–2 + 1B expansions. No orphan toolbox types. Generators generally emit correct statement/value forms.

### Residual block risks (medium/low)
| Issue | Severity | Notes |
|-------|----------|--------|
| f-string field content previously unescaped | **High → Fixed** | Quotes/newlines could break generated code |
| Comment field newlines | **Medium → Fixed** | Collapsed to single-line `#` comments |
| Import dropdown vs old workspaces | Medium | Workspaces saved with free-text modules (e.g. `numpy`) may fall back to first dropdown option on load |
| Fine-grained child-block line maps | Low | Block↔code map uses top-level span for descendants |
| No automated generator matrix tests | Medium | TODO still open: edge-case generation + serialization round-trip |

---

## 3. Runtime / Pyodide audit

### Architecture
1. Prefer **Web Worker** + Pyodide CDN when `SharedArrayBuffer` exists  
2. Else **main-thread fallback** (browser `prompt` for `input`)  
3. Stop = `worker.terminate()` + reload next run  

### Critical bugs found & fixed

#### C1 — Empty `input()` deadlock (Critical) — **FIXED**
- **Was:** Main wrote `sharedInt32[0] = val.length`. Empty string → `0`. Worker `Atomics.wait(..., 0, 0)` never wakes.  
- **Fix:** Protocol uses **length + 1** as wake flag; worker stores `length = flag - 1`.

#### C2 — Stop leaves `runCode()` promise hanging (Critical) — **FIXED**
- **Was:** `executionAborted` early-return ignored terminal messages; after `terminate()` no message arrived → `await` never settled; subsequent UI races.  
- **Fix:** `runResolve` settled from `stopCode()`; aborted path no longer double-prints “Finished”.

#### C3 — Worker used without SharedArrayBuffer (Critical) — **FIXED**
- **Was:** Worker init could succeed without SAB; any `input()` then crashed/hung on missing buffer.  
- **Fix:** If `SharedArrayBuffer` undefined, skip worker and use main-thread Pyodide.

### High bugs found & fixed

#### H1 — Concurrent first-load race — **FIXED**
- **Was:** Second Run during load hit `pyodideLoading` and returned without waiting → “failed to load”.  
- **Fix:** Single-flight `pyodideLoadPromise`.

#### H2 — `pyodideLoading` never cleared on successful worker load — **FIXED**
- Cleared on success/failure paths; reset on stop.

#### H3 — Fallback could inject Pyodide script repeatedly — **FIXED**
- Checks `typeof loadPyodide` before re-injecting script.

### Residual runtime issues (open)

| Issue | Severity | Notes |
|-------|----------|--------|
| `input()` prompt text often empty in worker path | Medium | Worker posts empty prompt; real prompt relies on Pyodide writing to stdout (may vary) |
| Main-thread fallback uses browser `prompt`, not inline field | Medium | Documented tradeoff without SAB / COOP-COEP |
| No COOP/COEP headers for SAB on static hosts | Medium | Hosting must set `Cross-Origin-Opener-Policy` + `Cross-Origin-Embedder-Policy` for worker+inline input |
| Pyodide ~7MB first load | Low | Expected; pre-bundle on Electron is TODO |
| Infinite loop only stoppable via worker terminate | Low | Fallback main-thread may freeze UI on tight loops |
| Variable inspector misses some names / shows modules | Low | Filters `_` prefix and a skip set; imperfect |

---

## 4. IDE / UX audit

### Working well
- Live generation + syntax highlight (HTML-escaped)  
- Line numbers, block→code highlight, code→block click  
- Auto-save 30s + last-saved timestamp  
- Named workspaces, export/import JSON  
- Block search, disable block, show Python context menu  
- Orphan warnings, empty-input outline  
- Examples (10), welcome overlay, F1 help  
- Keyboard shortcuts largely as documented  

### Issues

| Issue | Severity | Status |
|-------|----------|--------|
| Electron **Open .py** previously only toasted | High | **Fixed** — shows file contents in Output as reference (cannot rebuild blocks) |
| `Ctrl+Shift+S` may conflict with browser “Save page” | Low | App calls `preventDefault` when focused |
| `Ctrl+C` copies Python when no block selected — surprises users selecting text in code panel | Medium | Open |
| Code panel not true editor (no selection-friendly copy path) | Low | By design |
| Mobile/touch not optimized | Medium | TODO |
| No progressive disclosure of categories | Low | TODO |

---

## 5. Security audit

| Finding | Severity | Status |
|---------|----------|--------|
| Chat messages rendered via `innerHTML` without escaping | **High** | **Fixed** — `escapeHtml` then light markdown |
| API key in `localStorage` + browser Anthropic call + `anthropic-dangerous-direct-browser-access` | Medium | Acceptable for personal tool; **not** ideal for public multi-user hosting (key exfil via XSS, CORS model) |
| Generated code displayed with escaping | OK | `highlightPython` escapes |
| Variable inspector values escaped | OK | After audit helpers |
| `prompt()` for custom module names | Low | UX only |
| No CSP meta tags | Medium | Open — recommend CSP when hosted |
| CDN scripts (unpkg, jsDelivr) without SRI | Medium | Supply-chain risk; pin versions (partially pinned Pyodide `0.25.1`) |
| Blockly from `unpkg.com/blockly` unpinned major | Medium | Floating latest can break |

### Recommendations
1. Pin Blockly to exact version + optional SRI.  
2. On public host, put Anthropic calls behind a small backend/proxy; never encourage long-lived keys in `localStorage` for shared machines.  
3. Add Content-Security-Policy when deploying.  
4. If enabling SAB, set COOP/COEP correctly and understand cross-origin isolation impact.

---

## 6. Electron audit

| Area | Status |
|------|--------|
| `contextIsolation: true`, `nodeIntegration: false` | Good |
| Preload bridge minimal | Good |
| Load `../index.html` | OK |
| Save `.py` via dialog | OK |
| Open `.py` | Improved (reference dump) — **cannot** reverse-engineer blocks |
| Menu Run/Stop/Export/Import | Wired |
| System tray / auto-update / license | Missing (TODO) |
| Pre-bundled Pyodide | Missing |
| `electron-builder` icons use PNG for all platforms | May need `.ico`/`.icns` for polished builds |
| No `package-lock` committed | Reproducible builds weaker |

---

## 7. Product / distribution audit

| Item | Status |
|------|--------|
| Landing value prop | Present (`landing.html`) |
| Live iframe demo | Not yet (needs hosting) |
| GitHub Pages / Netlify | Not deployed |
| Gumroad / pricing execution | Placeholder only |
| License validation | Missing |
| User docs | Present |
| Analytics | Missing (opt-in planned) |
| Multi-language generators | Not started |

**Launch blockers (business):** hosting, payment listing, license story, support contact.

**Launch blockers (technical):** automated smoke tests for generate/run/save; browser matrix; CSP + pinned CDNs for production demo.

---

## 8. Testing posture

| Layer | Status |
|-------|--------|
| Unit tests for generators | **Yes** — `tests/smoke.mjs` headless Blockly `blockToCode` for all custom types |
| Serialization round-trip tests | **Yes** — smoke tier B3 |
| E2E (Playwright) | **Yes** — page load, Blockly inject, Hello World UI + Pyodide Run |
| Manual examples | 10 loaders in-app + fixtures under `tests/fixtures/examples/` |
| JS parse check | Passes (`node --check` on extracted script) |

**SOUL.md (updated 2026-07-14):** smoke suite is the project gate (`npm test`, expect 175 pass). Remaining ROI: deeper negative-path tests per free-text field, cross-browser matrix, and non-monolith modularization — not “zero tests.”

---

## 9. Fixes applied in this audit

1. **Input wake protocol** (`length + 1`) — empty `input()` no longer deadlocks.  
2. **`runResolve` + stop unblocks** — Stop no longer leaves Run hung.  
3. **No-SAB → main-thread Pyodide** — predictable `input()` without cross-origin isolation.  
4. **Single-flight Pyodide load** — concurrent Run clicks share one init.  
5. **Chat XSS hardening** — escape before markdown.  
6. **f-string + comment escaping** — safer generated Python.  
7. **Electron Open .py** — surfaces source in Output panel as reference.  
8. **Fallback load flags / script inject** — cleaner readiness state.

---

## 10. Prioritized backlog (post-audit)

### P0 — before public demo host
- [x] Document SAB vs fallback + Netlify headers (`docs/hosting.md`, `netlify.toml`)  
- [x] Pin Blockly CDN version (12.5.1) + keyboard-nav 3.0.5  
- [x] Generator + save/load smoke tests (`tests/smoke.mjs`, `npm test`)  
- [x] Example fixtures + Playwright page-load smoke (v0.2.3)  
- [x] Vision doc file tree / current state refreshed  
- [x] Pyodide execute E2E — Hello World via Run asserts Output (v0.2.4)  
- [x] Public-demo privacy/CSP docs + landing `#privacy` (v0.2.4)  
- [ ] Deploy static site (connect Netlify/Cloudflare/GH Pages account)  

### P1 — product quality
- [ ] Inline `input()` prompt text parity on all paths  
- [ ] Improve import custom-module UX (show typed name on block)  
- [ ] CSP + tighten AI key handling for public deploy  
- [ ] Cross-browser pass (Chrome, Firefox, Edge, Safari)  

### P2 — paid desktop
- [ ] Gumroad + license key gate  
- [ ] Pre-bundle Pyodide  
- [ ] Proper app icons / auto-update  

### P3 — roadmap niceties
- Minimap, code folding, progressive disclosure, high-contrast theme, multi-language generators, thumbnails  

---

## 11. Compliance with project principles (`SOUL.md` / vision)

| Principle | Assessment |
|-----------|------------|
| Complete, production-ready slices | Core + 1.5 stdlib packs complete; human-owned deploy/store remains |
| No dead ends for standard Python | Strong coverage; Web/Concurrency are **documented teaching scaffolds** (not fake completeness) |
| One file, zero friction | Honored (`index.html`) — maintainability tax accepted for now |
| Teaches by doing | Examples + Bridge + tooltips + run loop |
| Tests required (SOUL) | **Met at smoke level** — `npm test` (175); expand depth over time |
| Zero warning tolerance | CDN pins present; no ESLint suite on monolith yet |
| Docs / MANIFEST (SOUL §7/§29) | **Aligned at 1.5.0** — see `MANIFEST.md` |

---

## 12. Verdict

**Technical core:** Healthy after this pass’s runtime/security fixes.  
**Release readiness:**

| Target | Ready? |
|--------|--------|
| Local teaching / personal use | **Yes** |
| Public free web demo | **Almost** (host + pin CDNs + quick smoke tests) |
| Paid Electron v1.0 | **No** (license, packaging polish, updates, tests) |

**Audit grade:** **B+** (functionality & scope) → **A-** for local use after fixes; **C** for commercial launch readiness.

---

*Re-run this audit after hosting setup and the first automated test harness.*
