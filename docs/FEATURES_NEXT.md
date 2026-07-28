# PyMason — Feature Exploration & Delivery (v0.5.0)

**Date:** 2026-07-13  
**Backup:** `C:\WPAI\Software\PyMason-backup-20260713-183142`  
**Status:** In-app packs **implemented** in v0.5.0. External launch items remain human-owned.

---

## Implemented in v0.5.0

| ID | Feature | Where |
|----|---------|--------|
| **A1** | Share workspace link | Header **Share**, `Ctrl+Shift+L`, load `#ws=` on enter |
| **A2** | Zoom to fit | Header **Fit**, `Ctrl+0` |
| **A3** | Run history | Output → **History** (15 entries, localStorage) |
| **A4** | micropip packages | Header **Packages** |
| **A5** | Jump to error block | Click `line N` in error output |
| **B1** | Guided mini-paths | Header **Paths** (5 challenges) |
| **B2** | Always-on Python peek | Status bar `#pythonPeek` |
| **B3** | Favorites | Toolbox **Favorites** + context menu |
| **B4** | Diff workspaces | Header **Diff** |
| **C1** | Minimap | Header **Map** |
| **C2** | Collapse / expand regions | **Collapse** / **Expand** |
| **C3** | Snap guides | Context menu **Snap to grid** (+ inject grid snap) |
| **C4** | Soft type/input warnings | Status bar when multiple missing inputs |
| **C5** | Lua generator | Language select **Lua** |
| **E1** | Format generated code | **Format+Copy**; downloads formatted |
| **E2** | Voice → chat | 🎤 beside Send |
| **E3** | Offline pack note | See hosting docs (Electron can cache CDN) |

---

## Still external / human-only (D)

| ID | Item |
|----|------|
| **D1** | Public Netlify/Pages deploy |
| **D2** | Gumroad listing + live license API |
| **D3** | Signed installers + auto-update feed |
| **D4** | Production auth endpoint |

---

## Stretch not fully built (by design)

| ID | Notes |
|----|--------|
| **E4** Multi-file projects | Would break single-canvas purity — deferred |
| **E5** Live multiplayer share | Needs server — out of single-file ethos |
| **C4** Full type checker | Soft warnings only; full connection checker is deep R&D |

---

## Verify

```bash
cd tests && node check-login-ui.mjs && node check-studio-features.mjs
# full suite
npm test
```

Hard-refresh the app after upgrade: `Ctrl+F5`.
