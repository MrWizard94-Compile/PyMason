# Hosting PyMason as the WPAI front door

PyMason is designed to sit on **wpaistudio.net** (or a subpath) with a **login gate** before the builder.

## Files to deploy

```
index.html          # App + login UI
auth.config.js      # Users / API endpoint (edit for production)
landing.html        # Marketing entry
docs/               # Optional
```

## Login

1. User hits `index.html` → **login card** (WPAI forge styling).
2. Credentials checked via:
   - **`auth.config.js` → `demoUsers`** (local / invite demos), or
   - **`endpoint`** POST JSON `{ username, password }` → `{ ok, token, user }`
3. Session stored in `sessionStorage` / `localStorage` (`wpai_session`) for `sessionHours` (default 72).
4. **Sign out** clears session and returns to the gate.

### Default demo accounts (change these)

| Username | Password   | Display   |
|----------|------------|-----------|
| studio   | wpai-forge | Studio    |
| wizard   | weaponized | Mrwizard94 |

### Free feedback trial notice

The login gate shows a short **limited free trial** note and requires a checkbox:

> By participating in this free trial, you agree to provide thoughtful feedback after using PyMason.

Agreement is stored in `localStorage` as `pymason_feedback_agree` (`{ at, user }`) for your own follow-up; it is not a legal contract by itself—pair with your real feedback channel (form/email) on the WPAI site.

### Production `auth.config.js` example

```js
window.WPAI_AUTH = {
  studioName: 'Wizard Productions AI Studio',
  studioUrl: 'https://wpaistudio.net',
  gumroadUrl: 'https://wpaistudio.gumroad.com',
  endpoint: 'https://wpaistudio.net/api/auth/login', // your backend
  allowDemo: false,
  demoUsers: [],
  sessionHours: 24,
};
```

Server contract:

```http
POST /api/auth/login
Content-Type: application/json

{ "username": "...", "password": "..." }

→ 200 { "ok": true, "token": "...", "user": { "username", "displayName", "email" } }
→ 401 { "ok": false, "error": "Invalid credentials" }
```

**Security note:** Client-side `demoUsers` are only for demos/invites. Real production security requires `endpoint` + HTTPS + hashed passwords server-side.

## Branding

UI tokens match **wpaistudio.net**:

- Primary orange `#FF7A26`
- Dark forge background `#0A0807`
- Headings: **Cinzel**
- UI: **Inter**
- Accent ember `#E84A18`

## Suggested site routes

| URL | Content |
|-----|---------|
| `https://wpaistudio.net/` | Main studio site |
| `https://wpaistudio.net/pymason/` or subdomain | This app (`index.html` + `auth.config.js`) |
| Gumroad | Paid products |

## Electron

Desktop still works; login gate applies the same (local demo users or endpoint).
