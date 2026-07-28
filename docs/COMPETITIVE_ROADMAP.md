# PyMason — Competitive Roadmap

**Product:** **v1.5.0**  
**Backup:** `PyMason-backup-20260713-191450` (pre-1.4 packs; re-backup before major refactors)

---

## Scorecard after “make it so” (all three tracks)

| Track | Status |
|-------|--------|
| **Deep AST→blocks** | `def` / `class` / `return` / try / from-import / richer exprs · subset parser + Pyodide AST |
| **Worker debugger** | SAB `debug_run` step/cont/stop on worker; main-thread fallback |
| **Public demo + store** | Landing, Netlify routes, DISTRIBUTE.md, Gumroad verify IPC, electron build scripts |

| Capability | **PyMason 1.5** |
|------------|-----------------|
| Real Python export | Multi-module + format + Import .py + portfolio package |
| Dual transition | Dual mode + →Blocks + AST deep + Bridge practice |
| Debugger | **Worker SAB** + main fallback |
| Stage / tests | Turtle/plot/grid/PNG + asserts |
| Stdlib toolbox | Time…Advanced (1.4) + Collections…Itertools + sketch Web/Concurrency (1.5) |
| AI agent | Stream + JSON/Python apply + undo |
| Distribution | Landing demo, store CTAs, build/license hooks |

### Human remaining (accounts only)

1. Click Netlify deploy  
2. Create Gumroad product + set `GUMROAD_PRODUCT_ID`  
3. Upload `electron/dist` installers  
4. Point landing download buttons at real Release URLs  

See **[DISTRIBUTE.md](DISTRIBUTE.md)**.

---

## Verify

```bash
cd tests && node check-v11.mjs && npm test
npm run serve   # landing + app
cd electron && npm start
```
