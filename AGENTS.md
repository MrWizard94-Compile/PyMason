# AGENTS — PyMason project entry

**Status:** Level 4 project instructions  
**Canonical Constitution:** https://github.com/MrWizard94-Compile/Agents-Constitution  
**Accepted source commit:** `5d5aa0c79a9bcad095f58ebe315bf44adc94fbff`

The accepted GitHub repository is the only editable WPAI Constitution source.
This file owns PyMason-specific context, not a copy of universal law. Load
`SKILL.md`, `AGENTS.md`, `SOP.md`, `references/always-load.md`, and applicable
`law/*` files from one verified commit above. A local generated mirror is
usable only when its manifest matches that commit. If verification is
unavailable, disclose the gap; do not fall back to a retired SOUL copy.

## Mission and architecture

- PyMason is a visual Python builder. The core web application is
  `index.html` with Blockly and Pyodide; `landing.html` is its marketing
  entry, and `electron/` is an optional desktop wrapper. Do not introduce
  React or webpack into the core app without an explicit architecture decision.
- Preserve block-to-Python generation, examples, saved workspaces and their
  migration, and the distinction between block and free-Python editing.
- Product intent is in `PYMASON_VISION.md`; current work is in
  `PYMASON_TODO.md`; `AUDIT.md` and `MANIFEST.md` are dated historical records.

## Delivery checks and trust boundary

- Run `npm test` from the repository root. Its headless Blockly, golden,
  browser, and Pyodide tiers are all required for delivery; do not use
  `SKIP_BROWSER`, `SKIP_PYODIDE`, or fixture-update mode as acceptance.
- Run `npm --prefix tests audit --audit-level=low` against the locked smoke
  dependencies; resolve reported advisories rather than hiding them.
- Test the feedback-consent gate before a successful trial sign-in. Uncaught
  browser page errors are defects, including errors from incorrect Blockly
  APIs; do not filter them as harmless noise.
- The client-side local demo login is a trial UI, not server-enforced access
  control. Never treat its visible demo credentials or local session as a
  production authentication boundary. A public or paid deployment requires
  a separate security and release review.
- When Electron, hosting, or persistence changes, verify the actual relevant
  runtime in addition to the browser smoke suite.

CI checks out the exact accepted Constitution commit, validates its source
and tests, audits active consumers, and runs the complete PyMason smoke suite.
Advance the pin only with another accepted, verified canonical commit.

Historical recovery (not active law): `git show 1fe2ec4ec519d0c0cc818b990423dfd0e822bd27:SOUL.md.legacy-pre-pack-20260727-205752`
