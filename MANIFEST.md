# Delivery MANIFEST — v1.5.0

**Title:** Even-more blocks + SOUL documentation alignment  
**Date:** 2026-07-14  
**One sentence:** Seven stdlib-flavored toolbox categories (~65 generators) shipped at product **1.5.0**, with docs, versions, and §29 handoff synchronized to SOUL.md.

## Why

Director requested more blocks after 1.4.0, then a full alignment pass against **SOUL.md** §0 / §7 / §29 (docs sync, MANIFEST, review packaging, sketch transparency).

## Files changed (this delivery package)

| File | Purpose |
|------|---------|
| `index.html` | App shell; Collections/Stats/Encode/Text+/Itertools/Web sketch/Concurrency; `PYMASON_VERSION = 1.5.0` |
| `package.json` | Root version `1.5.0` |
| `electron/package.json` | Desktop package version aligned to `1.5.0` |
| `CHANGELOG.md` | `[1.5.0]` entry |
| `MANIFEST.md` | This handoff package (replaces stale 0.3.0 manifest) |
| `README.md` | Features table + version → 1.5.0 |
| `landing.html` | Footer product version → 1.5.0 |
| `docs/block-reference.md` | Full category map including 1.4 + 1.5 packs |
| `docs/user-guide.md` | Toolbox category list + sketch scaffold note |
| `docs/DISTRIBUTE.md` | Version banner → 1.5.0 |
| `docs/COMPETITIVE_ROADMAP.md` | Product version banner → 1.5.0 |
| `docs/faq.md` | Toolbox / sketch FAQ notes |
| `AUDIT.md` | SOUL tests row updated (smoke suite exists) |
| `tools/add_even_more_blocks.py` | Idempotent inject script for the 1.5 pack |
| `tools/add_more_blocks.py` | Prior 1.4 pack inject (already present) |

## Verify

```bash
# From repo root
npm test
# Expect: version 1.5.0 · blocks≈252 · generators≈250 · passed: 175 · failed: 0

# Optional faster checks
cd tests && SKIP_PYODIDE=1 npm test
# SKIP_BROWSER=1 npm test   # no Chromium
```

Manual:

1. Hard-refresh `index.html` (`Ctrl+Shift+R`).
2. Header toolbox → **Show all** (or Educate → **Unlock all toolbox**).
3. Confirm categories: **Collections**, **Stats**, **Encode**, **Text+**, **Itertools**, **Web sketch**, **Concurrency**.
4. Drag `Counter` + import block → Run / inspect generated Python.
5. Status bar shows **v1.5.0**.

## Suggested commit message(s)

```
feat: stdlib toolbox pack + SOUL docs/MANIFEST sync (v1.5.0)

Add Collections, Stats, Encode, Text+, Itertools, Web sketch, and
Concurrency blocks with generators. Align versions, block reference,
user guide, MANIFEST, and AUDIT with SOUL §0/§7/§29.
```

Optional split:

```
feat(blocks): even-more stdlib categories (v1.5.0)
docs: SOUL handoff — MANIFEST, block ref, version sync
```

## Known risks & deliberate trade-offs

1. **Web sketch / Concurrency** are **teaching scaffolds**, not production runtimes. HTTP GET emits a `print` sketch (browser Pyodide has no full `requests` stack). Threading/asyncio blocks generate real-shaped Python; true concurrency in the browser is limited — tooltips and docs say so.
2. **Monolith** `index.html` (~800KB) remains a maintainability tax (SOUL §6 spirit). Inject scripts keep packs idempotent without a bundler.
3. **Free-text identifiers** on some blocks (class names, targets, etc.) are intentional for learning; line-audit tracks injection surface. Not a multi-tenant server app.
4. **Human-owned:** Netlify deploy, Gumroad product, real Release installer URLs — not automated in this package.
5. Mutator helpers `py_tuple_container` / `py_tuple_item` have no generators by design (same as pre-1.5).

## Section 0 self-audit (executed)

| # | Item | Result |
|---|------|--------|
| 1 | Completeness | Pass for pack scope; sketches intentional & documented |
| 2 | Dependency-first | Pass — toolbox + defs + gens + docs together |
| 3 | Zero warnings | Pass smoke; no separate ESLint on monolith |
| 4 | Tests | Pass — `npm test` 175/0 |
| 5 | Docs synchronized | Pass after this package |
| 6 | Security | Partial accepted (educational free-text; no secrets added) |
| 7 | Performance | Pass — Blockly defs only |
| 8 | Version fidelity | Pass — Blockly 12.5.1 |
| 9 | Clean package | Pass — no temp inject residue required |
| 10 | Resource/cognitive | Pass — progressive toolbox + Show all |
| 11 | Reproducibility | Pass — smoke deterministic |
| 12 | IP hygiene | N/A |
| 13 | Multi-agent | N/A |
| 14 | Review packaging | Pass — this MANIFEST |
| 15 | Self-audit log | Pass — this table |

## What the human should do next (priority)

1. **Commit** with the suggested message when ready.
2. **Hard-refresh** app and spot-check new categories (optional 2 min).
3. **Deploy** static site when ready (`docs/DISTRIBUTE.md`) — account-owned.
4. **Gumroad / installers** still human-owned; point landing CTAs after first `electron` dist.

## Review path (optimal order)

1. `CHANGELOG.md` → what shipped  
2. `docs/block-reference.md` → category map  
3. Toolbox in live app (Show all)  
4. `tests/smoke.mjs` result / `npm test`  
5. `MANIFEST.md` (this file) for risks + next actions  
