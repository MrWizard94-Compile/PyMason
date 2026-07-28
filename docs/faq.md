# PyMason FAQ

## What version is this?

**1.5.0** (app `index.html` status bar, `package.json`, `CHANGELOG.md`). Marketing/docs versions track the same cut after the SOUL docs sync.

## Who owns PyMason?

© 2026 Wizard Productions AI Studio. All Rights Reserved. The product is private / unlicensed for redistribution unless you have explicit permission from the studio.

## Why are some toolbox categories called “sketch”?

**Web sketch** and **Concurrency** are intentional teaching scaffolds: they generate readable, real-shaped Python for APIs/threads/async so you can study and export — but the browser Pyodide runner is not a full network or multi-thread lab. Tooltips and [block-reference.md](block-reference.md) spell out the limits. Pair with desktop CPython when you need real `requests` or concurrency.

## How do I see every block category?

Header toolbox mode → **Show all**, or Educate → **Unlock all toolbox**. **Core** mode is for assessments / lower cognitive load.

## Is this for beginners?

Yes. PyMason is designed so you can build real programs without memorizing syntax first. The generated Python is real, so you learn the language while building.

## Is this only for beginners?

No. Experienced developers use it to sketch control flow, teach, or prototype algorithms visually before dropping into a full IDE.

## What Python version?

Code targets modern Python 3 (including `match`/`case` where available). Execution uses **Pyodide** (CPython compiled to WebAssembly), so behavior matches browser-supported stdlib modules.

## Does it work offline?

- **After first load**: Blockly and the app shell can be cached by the browser; Pyodide caches after first Run.
- **Electron**: best offline experience once dependencies are installed; pre-bundled Pyodide is on the roadmap.

## Do I need an account?

No. No login. Workspaces save in browser localStorage (or Electron storage).

## Is the AI required?

No. AI Chat is optional. Without it, building and running still work.

## Which AI providers are supported?

- **xAI Grok** (default) — key from [console.x.ai](https://console.x.ai)
- **Ollama** — local models (`ollama serve`)
- **Claude** — Anthropic API key

Details: [ai-providers.md](ai-providers.md).

## Where are my API keys stored?

In this browser’s **localStorage** (per provider). Keys go only to the provider you select. Clear via Chat → **Setup** → Clear key.

**Ollama CORS:** if the browser cannot connect, try `OLLAMA_ORIGINS=* ollama serve`.

**Shared computers:** private window or clear keys when done.

## Does Run send my code to a server?

No. **Run** uses Pyodide in your browser. AI Chat is different: if you use it, blocks/code go to the selected provider as context.

## Can I use this for real projects?

You can prototype and download `.py` files for use elsewhere. PyMason is **not** a full multi-file IDE or production runtime (no project tree, git, or package manager).

## Why don’t some modules import in Run?

Pyodide includes much of the standard library, but not every package (e.g. full `numpy` may need extra install steps). Prefer stdlib modules listed in the Imports dropdown for demos.

## My workspace disappeared?

Check **Workspaces** for named saves. Auto-save writes the last session to localStorage — clearing site data or private browsing can wipe it. Use **Export** for important work.

## Can I generate JavaScript or other languages?

Not yet. Multi-language generators are on the roadmap (Blockly supports them architecturally).

## Is the web demo limited?

The current web app is full-featured. Product plans may add soft limits later to differentiate a paid desktop build; the free demo remains useful for learning.

## Keyboard doesn’t do anything in the workspace

Click the block workspace first so it has focus. Some shortcuts are global (Run, Save, Help); Blockly’s own undo/selection also needs workspace focus.

## Who made this / license?

Private / UNLICENSED product intended for paid desktop distribution with a free web demo. See the repo root README.
