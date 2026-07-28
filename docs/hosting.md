# Hosting PyMason

PyMason is a static site: open or host `index.html` (and optionally `landing.html`) with no backend.

## Quick options

| Host | Entry | Notes |
|------|--------|--------|
| **Local file** | Open `index.html` | Works; Python uses **main-thread fallback** (no `SharedArrayBuffer`) so `input()` uses the browser `prompt` dialog |
| **Any static host** | Upload repo root | Same as local unless you add isolation headers |
| **Netlify** | Publish directory = repo root | Use included `netlify.toml` for headers |
| **Cloudflare Pages** | Same | Map headers from `docs/hosting.md` |
| **GitHub Pages** | `/docs` or root | Custom headers need GitHub Actions or a proxy; SAB often unavailable |

Recommended public layout:

```
/                 → landing.html (or rename to index and move app)
/app/             → full PyMason (index.html)
```

Or keep single-root:

```
/index.html       → app (or landing that links to app.html)
/landing.html     → marketing
```

## CDN pins (do not float)

`index.html` pins:

| Library | Version | URL pattern |
|---------|---------|-------------|
| Blockly | **12.5.1** | `https://unpkg.com/blockly@12.5.1/...` |
| @blockly/keyboard-navigation | **3.0.5** | peer of Blockly ^12.3 |
| Pyodide | **0.25.1** | `https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js` |

When upgrading Blockly, re-run smoke tests and check keyboard-navigation peer range.

## SharedArrayBuffer vs fallback

In-browser Python execution:

1. **Web Worker + inline `input()`** — requires `SharedArrayBuffer` and `Atomics`, which browsers only expose under **cross-origin isolation**.
2. **Main-thread fallback** — used automatically when SAB is missing; `input()` uses `window.prompt`.

### Enabling worker + inline input (optional)

Serve the app with:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

**Caveats:**

- Every cross-origin resource (CDNs) must send `Cross-Origin-Resource-Policy: cross-origin` (unpkg/jsDelivr generally do).
- Isolation can break OAuth popups and some embeds.
- If isolation fails, PyMason still runs via fallback — no user action required.

### Netlify

Root `netlify.toml` sets optional isolation headers for `index.html`. Disable them if a third-party script fails to load under COEP.

### GitHub Pages

No custom headers. Expect **fallback** path (prompt-based `input()`). That is fine for the free demo.

## Security checklist for public demos

- [x] Blockly/Pyodide **pinned** versions  
- [x] Landing `#privacy` documents AI key / localStorage / client-side Run  
- [x] FAQ documents API key storage and shared-machine risk  
- [x] Recommended CSP documented (optional Netlify header, test before enable)  
- [ ] Prefer **Subresource Integrity (SRI)** if you self-host CDN copies  
- [ ] Do not log or proxy API keys server-side without a clear privacy policy  

### Recommended Content-Security-Policy (host-level)

Blockly + Pyodide need CDN scripts, `unsafe-eval`, and `blob:` workers. Test on a deploy preview before enabling.

```
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self' https://cdn.jsdelivr.net https://unpkg.com https://api.anthropic.com; worker-src 'self' blob:; child-src blob:; frame-ancestors 'none'; base-uri 'self'; form-action 'self'
```

`netlify.toml` includes a commented CSP line you can uncomment after verification.

### AI key risk (shared machines)

API keys live in **browser localStorage**. Mitigations: private window, Chat → Key → Remove, avoid public kiosks. See `landing.html#privacy`.

## Deploy commands (examples)

### Netlify CLI

```bash
# from repo root
npx netlify deploy --prod --dir=.
```

### Cloudflare Pages

Connect the git repo; build command empty; output directory `.` (or a publish folder that contains `index.html` + assets).

### Simple Python static server (local)

```bash
# from repo root
python -m http.server 8080
# open http://localhost:8080/landing.html  or  /index.html
```

Note: `http://localhost` still may lack SAB unless you add isolation headers via a reverse proxy.

## Cross-browser manual checklist

After deploy or major UI change, smoke in:

| Browser | Check |
|---------|--------|
| Chrome / Edge | Load, drag print, Run Hello World, AI Setup opens |
| Firefox | Same (note SAB/worker may differ) |
| Safari | Same; first Pyodide load can be slower |

Mobile: toolbox + header wrap should remain usable; full mobile IDE is non-goal.

## Smoke tests before deploy

```bash
cd tests
npm install
npx playwright install chromium
npm test
# faster CI without Python download:
# SKIP_PYODIDE=1 npm test
```

Expect structural, example, DOM, page-load, and (unless skipped) Pyodide Hello World execute checks to pass.

## Related docs

- [User Guide](user-guide.md)
- [FAQ](faq.md)
- [Audit report](../AUDIT.md)
