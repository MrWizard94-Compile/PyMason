# PyMason — Public demo & store distribution

**Version:** 1.5.0  
This guide makes the product **deployable and sellable**. Hosting accounts and Gumroad login remain human-owned.

---

## 0. WPAI website page (StudioOps)

Product marketing page lives on the studio site (not only in this repo):

| Path | Role |
|------|------|
| `C:\WPAI\Software\StudioOps\site\pymason.html` | **Public product page** → `https://wpaistudio.net/pymason.html` |
| `StudioOps\site\products.html` / `index.html` | Linked cards + trial CTAs |
| `StudioOps\site\assets\pymason.png` | Product art |

**App trial URL** used on the site: `https://wpaistudio.net/pymason/`  

Deploy the PyMason app (at least `index.html` + `auth.config.js`) into the site’s **`pymason/`** folder (or equivalent host path) so “Start free trial” works:

```text
StudioOps/site/
  pymason.html          ← product page (done)
  pymason/
    index.html          ← app (copy/sync from this repo)
    auth.config.js
```

Redeploy the StudioOps `site/` folder to wpaistudio.net as you usually do for the main site.

---

## 1. Public web demo (Netlify / Cloudflare Pages / GitHub Pages)

### Netlify (recommended)

1. Push this repo (or drag the project folder) to [Netlify](https://app.netlify.com).
2. **Publish directory:** `.` (repo root)
3. **Build command:** leave empty / `echo ok` (see `netlify.toml`)
4. After deploy:
   - Marketing: `https://YOUR_SITE.netlify.app/` → `landing.html`
   - App: `https://YOUR_SITE.netlify.app/app` → `index.html`
5. Optional: attach custom domain (DNS).

`netlify.toml` already sets COOP/COEP on `/index.html` so SharedArrayBuffer + worker debug/input work when the host allows isolation.

### Local preview

```bash
python -m http.server 8080
# Marketing: http://localhost:8080/landing.html
# App:       http://localhost:8080/index.html
```

### Demo credentials (local auth.config.js)

| User   | Password    |
|--------|-------------|
| studio | wpai-forge  |
| wizard | weaponized  |

**Production:** set `window.WPAI_AUTH.endpoint` in `auth.config.js` and disable `allowDemo`.

---

## 2. Gumroad storefront (desktop license)

### Product setup (human)

1. Create product on [Gumroad](https://gumroad.com) (or wpaistudio.gumroad.com).
2. Price: one-time purchase (see `PYMASON_TODO.md` pricing).
3. Deliverable: link to desktop installers (GitHub Releases / Netlify large assets).
4. License keys: format accepted by Electron  
   `PM-XXXX-XXXX-XXXX` (local validation today).

### Optional Gumroad license API

When ready, set in Electron userData or env:

```
GUMROAD_PRODUCT_ID=...
GUMROAD_VERIFY_URL=https://api.gumroad.com/v2/licenses/verify
```

Hook point: `electron/main.js` → `isValidLicenseKey` / future `verifyLicenseOnline(key)`.

### Desktop builds

```bash
cd electron
npm install
npm start          # dev
npm run build-win  # NSIS installer → electron/dist/
npm run build-mac
npm run build-linux
```

Upload `dist/*` to Gumroad or GitHub Releases. Point landing **Download desktop** at that URL.

### Auto-update (later)

electron-builder `publish` config is stubbed for when you have a GitHub repo + token:

```json
"publish": [{ "provider": "github", "owner": "YOU", "repo": "PyMason" }]
```

---

## 3. Landing page CTAs

`landing.html` links:

| CTA | Target |
|-----|--------|
| Enter forge / Live demo | `/app` or `index.html` |
| Store | Gumroad |
| Desktop | `#download` section (set real installer URLs after first build) |
| Docs | `docs/user-guide.md` |

---

## 4. Checklist before “we’re live”

- [ ] Netlify (or Pages) deploy green
- [ ] COOP/COEP tested: Run + worker debug + `input()`
- [ ] Demo login works; production auth planned
- [ ] Landing iframe or “Open app” works
- [ ] Windows installer built and smoke-tested
- [ ] Gumroad product + license key test
- [ ] Privacy blurb (keys local, no server) reviewed

---

## 5. What the code does vs what only you can do

| Code ships | You must click |
|------------|----------------|
| Static site + headers | Create Netlify site / DNS |
| Electron package scripts | Run builds, upload binaries |
| License format + file store | Gumroad product + keys |
| Landing/store links | Final URLs |
| `auth.config.js` shape | Production endpoint + users |
