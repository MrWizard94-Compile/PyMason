# PyMason — Master Todo List

> Each item is a discrete, completable task. Items marked with ✅ are done.
> Priority: 🔴 = critical (do first), 🟡 = important, 🟢 = nice to have.
> **Status: v0.4.0 — WPAI Studio + multi-provider AI + core product complete.** Remaining items are external (hosting accounts, Gumroad store) or optional R&D.
> **Next features ranked:** see [docs/FEATURES_NEXT.md](docs/FEATURES_NEXT.md) (post-backup exploration 2026-07-13).

---

## Phase 1–3, 1B

All block library, OOP, execution, and 1B expansions: **✅ complete** (see git history / CHANGELOG).

---

## Phase 4: IDE & Quality-of-Life

### 4.1 Workspace Management
- [x] ✅ Auto-save on timer (every 30 seconds)
- [x] ✅ Named workspaces (user can name their workspace)
- [x] ✅ Multiple workspace slots (save/load from a list via Workspaces manager)
- [x] ✅ Workspace list UI (names + load/delete; full pixel thumbnails deferred as low ROI)

### 4.2 Code Panel
- [x] ✅ Line numbers in code panel gutter
- [x] ✅ Fix `\n` literal in empty state text
- [x] ✅ Block-to-code highlighting
- [x] ✅ Code-to-block highlighting
- [x] ✅ Language toggle Python / JavaScript (header; JS partial for custom blocks)

### 4.3 Block Editor
- [x] ✅ Block search (Ctrl+F)
- [x] ✅ Block disable/enable
- [x] ✅ Block count per category (status bar)
- [x] ✅ Progressive disclosure — Core vs Show All categories
- [ ] 🟢 Minimap overview of workspace (optional R&D)
- [ ] 🟢 Block grouping / collapsible regions (optional R&D)
- [ ] 🟢 Snap-to alignment guides (optional R&D)

### 4.4 Keyboard Shortcuts
- [x] ✅ All primary shortcuts (undo/redo, save, export, run, copy, download, Esc, F1, search)

### 4.5 Error & Validation
- [x] ✅ Empty input warnings
- [x] ✅ Disconnected/orphan block warnings
- [x] ✅ Soft identifier/param sanitization on free-text generators
- [ ] 🟢 Full type-mismatch connection checker (optional R&D)

### 4.6 Accessibility
- [x] ✅ ARIA roles + keyboard navigation plugin
- [x] ✅ Reduced motion mode (`prefers-reduced-motion`)
- [x] ✅ High-contrast Matrix theme (default UI)

---

## Phase 5: Learning & Onboarding

### 5.1–5.3
- [x] ✅ 10 example programs
- [x] ✅ Welcome overlay + first-block hint
- [x] ✅ Progressive disclosure (Core categories)
- [x] ✅ Enhanced tooltips, Show Python, Help panel

### 5.4 AI Chat Interface
- [x] ✅ Chat panel UI
- [x] ✅ **xAI Grok** integration (`api.x.ai/v1/chat/completions`, default)
- [x] ✅ **Ollama** local integration (`/api/chat`)
- [x] ✅ **Claude / Anthropic** Messages API (retained)
- [x] ✅ Provider switcher + per-provider model/base URL/key in Setup
- [x] ✅ Context injection (blocks + generated code)
- [x] ✅ Quick actions: Explain, Debug, What Blocks?, Build This, Review
- [x] ✅ Local storage of settings (never hardcoded secrets)

---

## Phase 6: Product & Distribution

### 6.1 Web Demo
- [x] ✅ Static assets + `netlify.toml` + `docs/hosting.md`
- [ ] 🔴 Host on static site — **requires your Netlify/GitHub account**
- [ ] 🟡 Custom domain — **requires DNS/account**
- [x] ✅ Web demo vs paid framing documented on landing (no artificial cripple by default)

### 6.2 Electron Desktop App
- [x] ✅ Electron wrapper + FS save/load `.py`
- [x] ✅ System tray integration (show / run / stop / quit)
- [x] ✅ Native keyboard shortcuts
- [x] ✅ App icon (PyMason.png)
- [x] ✅ Local license key entry (format `PM-XXXX-XXXX-XXXX`, stored in userData)
- [ ] 🟢 Pre-bundled Pyodide — optional future packaging optimization

### 6.3 Gumroad Integration
- [x] ✅ Pricing strategy documented (one-time purchase, free web demo) — see landing + below
- [x] ✅ License key path ready in Electron (wire Gumroad license API when store exists)
- [ ] 🔴 Gumroad product listing — **requires your Gumroad account**
- [ ] 🟢 Auto-updates via Electron — enable when published builds exist

**Pricing strategy (locked for product copy):**
- Free: full web demo (`index.html` / hosted static)
- Paid desktop: **one-time purchase** (no subscription), Electron app with tray + offline-friendly shell + license key
- Suggested positioning: “pay once, own the desktop craftsman edition”

### 6.4 Landing Page
- [x] ✅ Value prop, pricing section, privacy, Matrix branding
- [x] ✅ Live embedded demo (iframe of `index.html`)
- [x] ✅ Hero image
- [x] ✅ Social-proof placeholder framing (features + privacy as trust)

### 6.5 Documentation
- [x] ✅ User guide, FAQ, block reference, changelog, README
- [x] ✅ `docs/ai-providers.md`
- [x] ✅ Hosting + CSP guidance

### 6.6 Multi-Language Code Generation
- [x] ✅ JavaScript generator toggle (header; custom `py_*` blocks fall back with comment wrapper)
- [x] ✅ Language selector in header
- [ ] 🟢 Lua generator (optional; same pattern as JS when needed)
- [ ] 🟢 Additional custom language generators (optional)

### 6.7 Analytics & Versioning
- [x] ✅ Semantic versioning + UI version (`v0.3.0`)
- [x] ✅ Opt-in local analytics stub (session counter in localStorage only — no network)
- [ ] 🟡 Git tags for releases — run when you create a git remote/release

---

## Bug Fixes & Polish

- [x] ✅ Generator/serialization/example/page/Pyodide smoke suite
- [x] ✅ Line-audit remediations (string escapes, workspace XSS, sanitizers)
- [x] ✅ Matrix UI + toolbox visibility (Blockly 12 class names)
- [x] ✅ Cross-browser **checklist** documented in `docs/hosting.md` (manual smoke)
- [x] ✅ Mobile/touch: header wrap + flexible panels (deep mobile app not targeted)
- [x] ✅ Performance: smoke with multi-block examples; 100+ block profile optional

---

## External / human-only remaining

| Item | Why open |
|------|----------|
| Host on Netlify/GitHub Pages | Needs your account credentials |
| Custom domain | Needs DNS ownership |
| Gumroad listing + payment | Needs your Gumroad store |
| Electron auto-update feed | Needs published installers + update URL |
| Git release tags | Needs git remote + release process |
| Deep minimap / code folding / Lua | Optional R&D, not launch blockers |

---

## Summary

**v0.3.0 is feature-complete for local + desktop use** with multi-provider AI (xAI, Ollama, Claude).  
Launch blockers left are **account/deploy/commerce**, not missing app code.
