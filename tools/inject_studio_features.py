#!/usr/bin/env python3
"""Inject v0.5 studio feature pack into index.html (idempotent)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
text = INDEX.read_text(encoding="utf-8")

if "PYMASON_STUDIO_FEATURES_V05" in text:
    print("Already injected — skipping")
    raise SystemExit(0)

# ── 1. Lua script tag ──────────────────────────────────────────────
old_scripts = """    <script src="https://unpkg.com/blockly@12.5.1/javascript_compressed.js"></script>
    <script src="https://unpkg.com/blockly@12.5.1/msg/en.js"></script>"""
new_scripts = """    <script src="https://unpkg.com/blockly@12.5.1/javascript_compressed.js"></script>
    <script src="https://unpkg.com/blockly@12.5.1/lua_compressed.js"></script>
    <script src="https://unpkg.com/blockly@12.5.1/msg/en.js"></script>"""
if old_scripts not in text:
    raise SystemExit("script anchor missing")
text = text.replace(old_scripts, new_scripts, 1)

# ── 2. CSS ─────────────────────────────────────────────────────────
css = r"""
        /* ── Studio Features v0.5 ─────────────────────────── */
        .studio-toolbar-extra {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            align-items: center;
        }
        .python-peek {
            max-width: min(420px, 40vw);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-family: 'Cascadia Code', 'Fira Code', Consolas, monospace;
            font-size: 11px;
            color: var(--brass);
            opacity: 0.95;
        }
        .python-peek:empty { display: none; }
        .python-peek strong { color: var(--fg-muted); font-weight: 500; margin-right: 6px; font-family: var(--font-ui); }
        #minimapCanvas {
            position: absolute;
            right: 12px;
            bottom: 12px;
            width: 140px;
            height: 100px;
            border: 1px solid #2A211C;
            border-radius: 6px;
            background: rgba(10, 8, 7, 0.88);
            z-index: 25;
            cursor: pointer;
            box-shadow: 0 4px 16px rgba(0,0,0,0.45);
        }
        #minimapCanvas.hidden { display: none; }
        .run-history-panel {
            border-top: 1px solid var(--panel-border);
            max-height: 120px;
            overflow: auto;
            background: #0C0A09;
            display: none;
            flex-shrink: 0;
        }
        .run-history-panel.visible { display: block; }
        .run-history-title {
            font-size: 10px;
            color: var(--brass-dim);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            padding: 6px 12px 2px;
        }
        .run-history-item {
            padding: 4px 12px;
            font-size: 11px;
            color: var(--fg-muted);
            cursor: pointer;
            border-left: 2px solid transparent;
        }
        .run-history-item:hover { background: rgba(255,122,38,0.08); border-left-color: var(--brass); color: var(--fg); }
        .run-history-item .rh-time { color: var(--brass); margin-right: 8px; }
        .run-history-item.error { color: #FCA5A5; }
        .studio-modal-overlay {
            position: fixed; inset: 0; z-index: 30000;
            background: rgba(0,0,0,0.72);
            display: flex; align-items: center; justify-content: center;
            padding: 16px;
        }
        .studio-modal {
            background: #1A1614;
            border: 2px solid #FF7A26;
            border-radius: 12px;
            padding: 20px 22px;
            max-width: 560px;
            width: 100%;
            max-height: 85vh;
            overflow: auto;
            box-shadow: 0 12px 48px rgba(0,0,0,0.7);
            color: #E8DCC8;
        }
        .studio-modal h2 {
            font-family: var(--font-heading);
            color: #FF7A26;
            font-size: 1.15rem;
            margin: 0 0 12px;
        }
        .studio-modal .row { display: flex; gap: 8px; flex-wrap: wrap; margin: 10px 0; align-items: center; }
        .studio-modal input, .studio-modal select, .studio-modal textarea {
            background: #0A0807; border: 1px solid #2A211C; color: #E8DCC8;
            border-radius: 6px; padding: 6px 10px; font-size: 13px; font-family: var(--font-ui);
        }
        .studio-modal textarea { width: 100%; min-height: 100px; font-family: Consolas, monospace; }
        .studio-modal .muted { color: #A89078; font-size: 12px; line-height: 1.5; }
        .studio-modal .path-step {
            padding: 10px 12px; border: 1px solid #2A211C; border-radius: 8px; margin-bottom: 8px;
        }
        .studio-modal .path-step.done { border-color: rgba(255,122,38,0.45); background: rgba(255,122,38,0.06); }
        .studio-modal .path-step .check { color: #FF7A26; margin-right: 6px; }
        .err-jump-link {
            color: #FCA5A5; text-decoration: underline; cursor: pointer;
        }
        .err-jump-link:hover { color: #fecaca; }
        .pkg-chip {
            display: inline-block; padding: 4px 10px; margin: 3px;
            border: 1px solid #2A211C; border-radius: 999px; font-size: 12px;
            cursor: pointer; color: #E8DCC8;
        }
        .pkg-chip:hover { border-color: #FF7A26; color: #FF7A26; }
        .diff-pre {
            font-family: Consolas, monospace; font-size: 11px; white-space: pre-wrap;
            background: #0A0807; border: 1px solid #2A211C; border-radius: 6px;
            padding: 10px; max-height: 280px; overflow: auto;
        }
        .diff-add { color: #86efac; }
        .diff-del { color: #fca5a5; }
        .diff-same { color: #A89078; }

"""

css_anchor = "        .user-chip strong { color: var(--brass); font-weight: 600; }\n\n    </style>"
if css_anchor not in text:
    raise SystemExit("css anchor missing")
text = text.replace(css_anchor, "        .user-chip strong { color: var(--brass); font-weight: 600; }\n" + css + "\n    </style>", 1)

# ── 3. Header buttons ──────────────────────────────────────────────
old_header = """            <button class="btn" onclick="openExamplesMenu()" title="Load an example program">Examples</button>
            <button class="btn btn-accent" onclick="downloadPython()" title="Download as .py file (Ctrl+D)">Download .py</button>"""
new_header = """            <button class="btn" onclick="openExamplesMenu()" title="Load an example program">Examples</button>
            <button class="btn" onclick="openGuidedPaths()" title="Guided mini-paths">Paths</button>
            <button class="btn" onclick="zoomToFitWorkspace()" title="Zoom to fit (Ctrl+0)">Fit</button>
            <button class="btn" onclick="shareWorkspaceLink()" title="Copy shareable workspace link">Share</button>
            <button class="btn" onclick="openPackagesUI()" title="Install pure-Python packages (micropip)">Packages</button>
            <button class="btn" onclick="openWorkspaceDiff()" title="Diff two named workspaces">Diff</button>
            <button class="btn" onclick="toggleMinimap()" title="Toggle workspace minimap">Map</button>
            <button class="btn" onclick="collapseExpandAll(true)" title="Collapse all blocks">Collapse</button>
            <button class="btn" onclick="collapseExpandAll(false)" title="Expand all blocks">Expand</button>
            <button class="btn btn-accent" onclick="downloadPython()" title="Download as .py file (Ctrl+D)">Download .py</button>"""
if old_header not in text:
    raise SystemExit("header anchor missing")
text = text.replace(old_header, new_header, 1)

old_lang = """            <select id="langSelect" class="lang-select" onchange="onOutputLangChange()" title="Generated language" aria-label="Output language">
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
            </select>"""
new_lang = """            <select id="langSelect" class="lang-select" onchange="onOutputLangChange()" title="Generated language" aria-label="Output language">
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="lua">Lua</option>
            </select>"""
if old_lang not in text:
    raise SystemExit("lang select missing")
text = text.replace(old_lang, new_lang, 1)

# ── 4. Code panel + output history ─────────────────────────────────
old_code_actions = """                <div class="code-actions">
                    <button class="btn" onclick="copyCode()" title="Copy">Copy</button>
                </div>"""
new_code_actions = """                <div class="code-actions">
                    <button class="btn" onclick="copyFormattedCode()" title="Copy formatted code">Format+Copy</button>
                    <button class="btn" onclick="copyCode()" title="Copy">Copy</button>
                </div>"""
text = text.replace(old_code_actions, new_code_actions, 1)

old_output = """                <div class="output-header">
                    <div class="output-title">Output</div>
                    <div class="output-actions">
                        <button class="btn" onclick="clearOutput()" title="Clear output">Clear</button>
                        <button class="btn" onclick="toggleOutput()" title="Collapse output">Hide</button>
                    </div>
                </div>
                <div class="output-content" id="outputContent"></div>"""
new_output = """                <div class="output-header">
                    <div class="output-title">Output</div>
                    <div class="output-actions">
                        <button class="btn" onclick="toggleRunHistory()" title="Show recent runs">History</button>
                        <button class="btn" onclick="clearOutput()" title="Clear output">Clear</button>
                        <button class="btn" onclick="toggleOutput()" title="Collapse output">Hide</button>
                    </div>
                </div>
                <div class="run-history-panel" id="runHistoryPanel" aria-label="Run history">
                    <div class="run-history-title">Recent runs</div>
                    <div id="runHistoryList"></div>
                </div>
                <div class="output-content" id="outputContent"></div>"""
if old_output not in text:
    raise SystemExit("output panel anchor missing")
text = text.replace(old_output, new_output, 1)

# Minimap inside blockly panel
old_blockly = """        <div class="blockly-panel">
            <div id="blocklyDiv" role="application" aria-label="Block editor workspace"></div>
        </div>"""
new_blockly = """        <div class="blockly-panel">
            <div id="blocklyDiv" role="application" aria-label="Block editor workspace"></div>
            <canvas id="minimapCanvas" class="hidden" width="140" height="100" title="Minimap — click to pan" aria-label="Workspace minimap"></canvas>
        </div>"""
if old_blockly not in text:
    raise SystemExit("blockly panel missing")
text = text.replace(old_blockly, new_blockly, 1)

# Status bar python peek
old_status = """    <div class="status-bar">
        <span id="statusText">Ready</span>
        <span class="category-count-bar" id="categoryCountBar" title="Blocks in use by category"></span>
        <span>
            <span id="lastSaved" style="margin-right:12px;"></span>
            <span class="block-count" id="blockCount">0 blocks</span>
        </span>
    </div>"""
new_status = """    <div class="status-bar">
        <span id="statusText">Ready</span>
        <span class="python-peek" id="pythonPeek" title="Python for selected block"></span>
        <span class="category-count-bar" id="categoryCountBar" title="Blocks in use by category"></span>
        <span>
            <span id="lastSaved" style="margin-right:12px;"></span>
            <span class="block-count" id="blockCount">0 blocks</span>
        </span>
    </div>"""
if old_status not in text:
    raise SystemExit("status bar missing")
text = text.replace(old_status, new_status, 1)

# Chat voice button
old_chat_send = """                <button class="chat-send" id="chatSend" onclick="sendChat()">Send</button>"""
new_chat_send = """                <button class="btn" type="button" onclick="startVoiceToChat()" title="Voice input (Web Speech API)">🎤</button>
                <button class="chat-send" id="chatSend" onclick="sendChat()">Send</button>"""
text = text.replace(old_chat_send, new_chat_send, 1)

# Help shortcuts
old_help = """                <li><kbd>Ctrl+F</kbd> — Search blocks</li>
                <li><kbd>Ctrl+C</kbd> — Copy Python (no block selected)</li>
                <li><kbd>Ctrl+Z</kbd> / <kbd>Ctrl+Y</kbd> — Undo / Redo</li>
                <li><kbd>F1</kbd> — Toggle this help panel</li>
                <li><kbd>Esc</kbd> — Close flyout / dialogs</li>
            </ul>"""
new_help = """                <li><kbd>Ctrl+F</kbd> — Search blocks</li>
                <li><kbd>Ctrl+0</kbd> — Zoom to fit workspace</li>
                <li><kbd>Ctrl+Shift+L</kbd> — Copy share link</li>
                <li><kbd>Ctrl+C</kbd> — Copy Python (no block selected)</li>
                <li><kbd>Ctrl+Z</kbd> / <kbd>Ctrl+Y</kbd> — Undo / Redo</li>
                <li><kbd>F1</kbd> — Toggle this help panel</li>
                <li><kbd>Esc</kbd> — Close flyout / dialogs</li>
            </ul>
            <h3>Studio Features</h3>
            <ul>
                <li><strong>Share</strong> — copy a link that restores this workspace</li>
                <li><strong>Paths</strong> — short guided challenges</li>
                <li><strong>Packages</strong> — micropip install for pure-Python libs</li>
                <li><strong>History</strong> — recent run outputs; click to restore</li>
                <li><strong>Map</strong> — workspace minimap</li>
                <li>Right-click a block → <em>Add to Favorites</em></li>
                <li>Click red error lines with line numbers to jump to the block</li>
            </ul>"""
if old_help not in text:
    raise SystemExit("help shortcuts missing")
text = text.replace(old_help, new_help, 1)

# Favorites category at top of toolbox
old_toolbox_start = """    <xml id="toolbox" style="display: none">

        <!-- ── Imports ─────────────────────────────── -->
        <category name="Imports" colour="#2A7A4A">"""
new_toolbox_start = """    <xml id="toolbox" style="display: none">

        <!-- ── Favorites (populated dynamically) ───── -->
        <category name="Favorites" colour="#FF7A26" custom="PYMASON_FAVORITES"></category>

        <!-- ── Imports ─────────────────────────────── -->
        <category name="Imports" colour="#2A7A4A">"""
if old_toolbox_start not in text:
    raise SystemExit("toolbox start missing")
text = text.replace(old_toolbox_start, new_toolbox_start, 1)

# ── 5. JS feature pack ─────────────────────────────────────────────
js = r"""
        // ═══════════════════════════════════════════════════════════════════
        //  PYMASON_STUDIO_FEATURES_V05 — A/B/C/E studio pack
        // ═══════════════════════════════════════════════════════════════════

        const RUN_HISTORY_MAX = 15;
        let runHistory = [];
        try {
            runHistory = JSON.parse(localStorage.getItem('pymason_run_history') || '[]');
            if (!Array.isArray(runHistory)) runHistory = [];
        } catch (e) { runHistory = []; }

        function saveRunHistory() {
            try {
                localStorage.setItem('pymason_run_history', JSON.stringify(runHistory.slice(0, RUN_HISTORY_MAX)));
            } catch (e) { /* private mode */ }
        }

        function pushRunHistory(entry) {
            runHistory.unshift({
                ts: Date.now(),
                ok: !!entry.ok,
                ms: entry.ms || 0,
                preview: String(entry.preview || '').slice(0, 400),
                full: String(entry.full || '').slice(0, 8000),
            });
            runHistory = runHistory.slice(0, RUN_HISTORY_MAX);
            saveRunHistory();
            renderRunHistoryList();
        }

        function renderRunHistoryList() {
            const list = document.getElementById('runHistoryList');
            if (!list) return;
            if (!runHistory.length) {
                list.innerHTML = '<div class="run-history-item muted">No runs yet</div>';
                return;
            }
            list.innerHTML = runHistory.map(function(h, i) {
                const t = new Date(h.ts).toLocaleTimeString();
                const prev = escapeHtml((h.preview || '').replace(/\s+/g, ' ').slice(0, 80));
                return '<div class="run-history-item' + (h.ok ? '' : ' error') + '" onclick="restoreRunHistory(' + i + ')">' +
                    '<span class="rh-time">' + escapeHtml(t) + '</span>' +
                    (h.ok ? 'ok' : 'err') + ' · ' + (h.ms / 1000).toFixed(2) + 's · ' + prev +
                    '</div>';
            }).join('');
        }

        function restoreRunHistory(i) {
            const h = runHistory[i];
            if (!h) return;
            showOutput();
            clearOutput();
            const pre = document.createElement('pre');
            pre.style.cssText = 'margin:0;white-space:pre-wrap;font:inherit;color:inherit;';
            pre.textContent = h.full || h.preview || '';
            outputContent.appendChild(pre);
            showToast('Restored run from history');
        }

        function toggleRunHistory() {
            const p = document.getElementById('runHistoryPanel');
            if (!p) return;
            p.classList.toggle('visible');
            if (p.classList.contains('visible')) {
                renderRunHistoryList();
                showOutput();
            }
        }

        function clearRunHistoryOnLogout() {
            runHistory = [];
            saveRunHistory();
            renderRunHistoryList();
        }

        // ── A2 Zoom to fit ───────────────────────────────────────────
        function zoomToFitWorkspace() {
            if (!workspace) return;
            try {
                if (typeof workspace.zoomToFit === 'function') {
                    workspace.zoomToFit();
                } else {
                    const m = workspace.getMetrics && workspace.getMetrics();
                    if (m) {
                        const blocks = workspace.getAllBlocks(false);
                        if (blocks.length === 0) {
                            workspace.setScale(1);
                            workspace.scroll(0, 0);
                        } else {
                            Blockly.svgResize(workspace);
                            if (workspace.scrollCenter) workspace.scrollCenter();
                        }
                    }
                }
                Blockly.svgResize(workspace);
                updateMinimap();
                showToast('Zoom to fit');
            } catch (e) {
                try {
                    workspace.setScale(1);
                    if (workspace.scrollCenter) workspace.scrollCenter();
                } catch (e2) { /* ok */ }
            }
        }

        // ── A1 Share workspace link ──────────────────────────────────
        function encodeWorkspaceShare() {
            const state = Blockly.serialization.workspaces.save(workspace);
            const json = JSON.stringify(state);
            // base64 of utf-8
            const b64 = btoa(unescape(encodeURIComponent(json)));
            return b64;
        }

        function decodeWorkspaceShare(b64) {
            const json = decodeURIComponent(escape(atob(b64)));
            return JSON.parse(json);
        }

        function shareWorkspaceLink() {
            try {
                const blocks = workspace.getAllBlocks(false);
                if (!blocks.length) {
                    showToast('Nothing to share — add blocks first');
                    return;
                }
                const b64 = encodeWorkspaceShare();
                if (b64.length > 120000) {
                    showToast('Workspace too large for URL — use Export instead');
                    return;
                }
                const url = location.origin + location.pathname + location.search + '#ws=' + b64;
                navigator.clipboard.writeText(url).then(function() {
                    showToast('Share link copied (' + Math.round(b64.length / 1024) + ' KB)');
                }).catch(function() {
                    prompt('Copy this share link:', url);
                });
            } catch (e) {
                showToast('Share failed: ' + (e.message || e));
            }
        }

        function tryLoadSharedWorkspace() {
            try {
                const hash = location.hash || '';
                if (!hash.startsWith('#ws=')) return false;
                const b64 = hash.slice(4);
                if (!b64) return false;
                const state = decodeWorkspaceShare(b64);
                workspace.clear();
                Blockly.serialization.workspaces.load(state, workspace);
                updateCode();
                // Keep hash so refresh works; user can clear manually
                showToast('Loaded shared workspace');
                setTimeout(zoomToFitWorkspace, 100);
                return true;
            } catch (e) {
                console.warn('Share load failed', e);
                showToast('Could not load shared workspace');
                return false;
            }
        }

        // ── A5 Error → block jump ────────────────────────────────────
        function makeErrorOutputClickable(text) {
            // Match "line N" patterns and wrap; return HTML string
            const esc = escapeHtml(text);
            return esc.replace(/\bline (\d+)\b/gi, function(m, n) {
                return '<a class="err-jump-link" data-err-line="' + n + '" title="Jump to block for line ' + n + '">' + m + '</a>';
            });
        }

        function appendOutputSmart(text, isError) {
            if (!isError) {
                appendOutput(text, false);
                return;
            }
            const span = document.createElement('span');
            span.className = 'error';
            span.innerHTML = makeErrorOutputClickable(String(text));
            span.addEventListener('click', function(ev) {
                const a = ev.target.closest('[data-err-line]');
                if (!a) return;
                const line = parseInt(a.getAttribute('data-err-line'), 10);
                if (!line) return;
                jumpToGeneratedLine(line);
            });
            outputContent.appendChild(span);
            outputContent.scrollTop = outputContent.scrollHeight;
        }

        function jumpToGeneratedLine(lineNum) {
            // Prefer lineBlockMap (top-level statement mapping)
            let blockId = lineBlockMap[lineNum];
            if (!blockId) {
                // nearest line with mapping
                const keys = Object.keys(lineBlockMap).map(Number).sort(function(a, b) { return a - b; });
                for (let i = 0; i < keys.length; i++) {
                    if (keys[i] >= lineNum) { blockId = lineBlockMap[keys[i]]; break; }
                }
                if (!blockId && keys.length) blockId = lineBlockMap[keys[keys.length - 1]];
            }
            if (blockId) {
                highlightBlockForLine(lineNum);
                highlightCodeForBlock(blockId);
                try {
                    const block = workspace.getBlockById(blockId);
                    if (block && Blockly.common && Blockly.common.setSelected) {
                        Blockly.common.setSelected(block);
                    }
                } catch (e) { /* ok */ }
                showToast('Jumped to block for line ' + lineNum);
            } else {
                // Scroll code panel to line
                const lineEl = codeOutput.querySelector('[data-line="' + lineNum + '"]');
                if (lineEl) {
                    lineEl.classList.add('code-line-highlight');
                    lineEl.scrollIntoView({ block: 'center' });
                    showToast('Highlighted code line ' + lineNum);
                } else {
                    showToast('No block mapped for line ' + lineNum);
                }
            }
        }

        // ── A4 micropip packages ─────────────────────────────────────
        const SUGGESTED_PACKAGES = [
            'micropip', 'regex', 'pytz', 'packaging', 'six', 'attrs',
            'beautifulsoup4', 'lxml', 'python-dateutil', 'idna', 'certifi',
        ];

        function openPackagesUI() {
            closeStudioModal();
            const ov = document.createElement('div');
            ov.className = 'studio-modal-overlay';
            ov.id = 'studioModal';
            ov.onclick = function(e) { if (e.target === ov) closeStudioModal(); };
            ov.innerHTML =
                '<div class="studio-modal" role="dialog" aria-label="Python packages">' +
                '<h2>Python packages (micropip)</h2>' +
                '<p class="muted">Install pure-Python wheels into the in-browser Pyodide runtime. Not all PyPI packages work (no native C extensions unless Pyodide ships them).</p>' +
                '<div class="row"><input id="pkgNameInput" placeholder="package name" style="flex:1">' +
                '<button class="btn btn-accent" onclick="installMicropipPackage()">Install</button></div>' +
                '<div class="muted">Suggestions:</div>' +
                '<div id="pkgChips"></div>' +
                '<div class="row"><button class="btn" onclick="closeStudioModal()">Close</button></div>' +
                '<pre id="pkgLog" class="diff-pre" style="min-height:60px;"></pre>' +
                '</div>';
            document.body.appendChild(ov);
            const chips = document.getElementById('pkgChips');
            SUGGESTED_PACKAGES.forEach(function(p) {
                const s = document.createElement('span');
                s.className = 'pkg-chip';
                s.textContent = p;
                s.onclick = function() {
                    document.getElementById('pkgNameInput').value = p;
                };
                chips.appendChild(s);
            });
        }

        function pkgLog(msg) {
            const el = document.getElementById('pkgLog');
            if (el) el.textContent = (el.textContent ? el.textContent + '\n' : '') + msg;
        }

        async function installMicropipPackage() {
            const name = (document.getElementById('pkgNameInput')?.value || '').trim();
            if (!name || !/^[A-Za-z0-9_.\-\[\]]+$/.test(name)) {
                pkgLog('Invalid package name');
                return;
            }
            pkgLog('Loading Python runtime…');
            if (!pyodideReady) {
                await loadPyodide_();
                if (!pyodideReady) {
                    pkgLog('Failed to load Pyodide');
                    return;
                }
            }
            try {
                if (pyWorker) {
                    pkgLog('Installing via worker: ' + name);
                    await new Promise(function(resolve, reject) {
                        const prev = pyWorker.onmessage;
                        const t = setTimeout(function() {
                            pyWorker.onmessage = prev;
                            reject(new Error('Timeout'));
                        }, 120000);
                        pyWorker.onmessage = function(e) {
                            if (e.data.type === 'pkg_log') {
                                pkgLog(e.data.text);
                            } else if (e.data.type === 'pkg_done') {
                                clearTimeout(t);
                                pyWorker.onmessage = prev;
                                resolve(e.data);
                            } else if (e.data.type === 'pkg_error') {
                                clearTimeout(t);
                                pyWorker.onmessage = prev;
                                reject(new Error(e.data.text));
                            } else if (prev) {
                                prev(e);
                            }
                        };
                        pyWorker.postMessage({ type: 'install', package: name });
                    });
                    pkgLog('Done: ' + name);
                    showToast('Installed ' + name);
                } else if (pyodideFallback) {
                    pkgLog('Installing (main thread): ' + name);
                    await pyodideFallback.loadPackage('micropip');
                    const micropip = pyodideFallback.pyimport('micropip');
                    await micropip.install(name);
                    pkgLog('Done: ' + name);
                    showToast('Installed ' + name);
                } else {
                    pkgLog('No Python runtime available');
                }
            } catch (e) {
                pkgLog('Error: ' + (e.message || e));
                showToast('Install failed');
            }
        }

        // Patch worker to support install messages (wrap createPyWorker)
        const _origCreatePyWorker = typeof createPyWorker === 'function' ? createPyWorker : null;
        if (_origCreatePyWorker) {
            createPyWorker = function() {
                // Rebuild worker code with install handler by intercepting on main side:
                // We post install to worker — need worker to handle it.
                // Re-create with extended code:
                const workerCode = `
                let pyodide = null;
                let inputBuffer = null;
                self.onmessage = async function(e) {
                    const msg = e.data;
                    try {
                        if (msg.type === 'init') {
                            importScripts('https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js');
                            pyodide = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/' });
                            self.postMessage({ type: 'ready' });
                        } else if (msg.type === 'install') {
                            await pyodide.loadPackage('micropip');
                            const micropip = pyodide.pyimport('micropip');
                            self.postMessage({ type: 'pkg_log', text: 'micropip installing ' + msg.package + '…' });
                            await micropip.install(msg.package);
                            self.postMessage({ type: 'pkg_done', package: msg.package });
                        } else if (msg.type === 'run') {
                            inputBuffer = msg.sharedBuffer ? new Int32Array(msg.sharedBuffer) : null;
                            pyodide.setStdout({ batched: (t) => self.postMessage({ type: 'stdout', text: t }) });
                            pyodide.setStderr({ batched: (t) => self.postMessage({ type: 'stderr', text: t }) });
                            // input override
                            pyodide.runPython(\`
import builtins
def _pymason_input(prompt=''):
    from js import self as _self
    import js
    _self.postMessage(js.Object.fromEntries([['type','input_request'],['prompt', str(prompt)]]))
    if inputBuffer is None:
        return ''
    # wait handled on main — use Atomics in SAB path from original; simplified:
    return ''
\`);
                            // Prefer original worker behavior: re-use simpler run
                            try {
                                await pyodide.runPythonAsync(msg.code);
                                const varsJson = pyodide.runPython(\`
import json as _json
_skip = {'__builtins__','__name__','__doc__','__package__','__loader__','__spec__','sys','json','_json','_skip','_vars','_k','_v','_s'}
_vars = {}
for _k,_v in list(globals().items()):
    if _k in _skip or str(_k).startswith('_'):
        continue
    try:
        _s = repr(_v)
        if len(_s) > 180: _s = _s[:177]+'...'
        _vars[_k] = _s
    except Exception:
        _vars[_k] = '<unprintable>'
_json.dumps(_vars)
\`);
                                self.postMessage({ type: 'done', vars: varsJson });
                            } catch (err) {
                                self.postMessage({ type: 'error', text: String(err) });
                            }
                        }
                    } catch (err) {
                        if (msg.type === 'install') self.postMessage({ type: 'pkg_error', text: String(err) });
                        else self.postMessage({ type: 'error', text: String(err) });
                    }
                };
                `;
                // Actually: don't replace entire worker — it would break SAB input.
                // Use main-thread micropip only when worker; for install force fallback path.
                return _origCreatePyWorker();
            };
        }

        // Safer install: always use main-thread fallback for packages if worker
        async function ensureMicropipHost() {
            if (pyodideFallback && pyodideReady) return pyodideFallback;
            // Load main-thread pyodide for package installs without killing worker
            if (!window._pkgPyodide) {
                if (typeof loadPyodide !== 'function') {
                    await new Promise(function(resolve, reject) {
                        const script = document.createElement('script');
                        script.src = 'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js';
                        script.onload = resolve;
                        script.onerror = reject;
                        document.head.appendChild(script);
                    });
                }
                window._pkgPyodide = await loadPyodide({
                    indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/',
                });
            }
            return window._pkgPyodide;
        }

        // Override install to use dedicated package host (keeps run worker intact)
        installMicropipPackage = async function() {
            const name = (document.getElementById('pkgNameInput')?.value || '').trim();
            if (!name || !/^[A-Za-z0-9_.\-\[\]]+$/.test(name)) {
                pkgLog('Invalid package name');
                return;
            }
            try {
                pkgLog('Loading package host…');
                const py = await ensureMicropipHost();
                pkgLog('Loading micropip…');
                await py.loadPackage('micropip');
                const micropip = py.pyimport('micropip');
                pkgLog('Installing ' + name + '…');
                await micropip.install(name);
                pkgLog('Installed: ' + name);
                // Mirror into run fallback if same instance
                if (pyodideFallback === py) {
                    pkgLog('(available for Run on main-thread fallback)');
                } else {
                    pkgLog('Note: packages install on the package host. For Run, re-install after first Run if using worker isolation — or run once to init, then install again on fallback.');
                }
                // Also try inject into fallback / worker run path
                if (pyodideFallback) {
                    try {
                        await pyodideFallback.loadPackage('micropip');
                        await pyodideFallback.pyimport('micropip').install(name);
                        pkgLog('Also installed into Run fallback runtime');
                    } catch (e2) { /* ok */ }
                }
                showToast('Installed ' + name);
            } catch (e) {
                pkgLog('Error: ' + (e.message || e));
                showToast('Install failed');
            }
        };

        // ── B1 Guided mini-paths ─────────────────────────────────────
        const GUIDED_PATHS = [
            {
                id: 'hello',
                title: 'Hello, forge',
                blurb: 'Print a message — the first spark.',
                steps: [
                    { text: 'Open I/O and drag a print block', test: function() { return workspace.getAllBlocks(false).some(function(b){ return b.type === 'text_print'; }); } },
                    { text: 'Attach a text block with your message', test: function() {
                        return workspace.getAllBlocks(false).some(function(b){ return b.type === 'text_print' && b.getInputTargetBlock('TEXT'); });
                    }},
                    { text: 'Press Run (Ctrl+Enter)', test: function() { return runHistory.length > 0; } },
                ],
            },
            {
                id: 'input_loop',
                title: 'Ask & answer',
                blurb: 'input() → variable → print.',
                steps: [
                    { text: 'Add an input block (I/O)', test: function() { return workspace.getAllBlocks(false).some(function(b){ return b.type === 'py_input' || b.type === 'py_input_cast'; }); } },
                    { text: 'Store it with a variable set block', test: function() { return workspace.getAllBlocks(false).some(function(b){ return b.type === 'variables_set'; }); } },
                    { text: 'Print the variable', test: function() { return workspace.getAllBlocks(false).some(function(b){ return b.type === 'text_print'; }); } },
                ],
            },
            {
                id: 'loop_list',
                title: 'Loop a list',
                blurb: 'for each item in a list.',
                steps: [
                    { text: 'Create a list (Lists)', test: function() { return workspace.getAllBlocks(false).some(function(b){ return (b.type || '').indexOf('lists_') === 0 || (b.type || '').indexOf('py_list') === 0; }); } },
                    { text: 'Add a for loop (Loops)', test: function() { return workspace.getAllBlocks(false).some(function(b){ return b.type === 'controls_forEach' || b.type === 'controls_for' || (b.type || '').indexOf('py_for') === 0; }); } },
                    { text: 'Print inside the loop', test: function() {
                        return workspace.getAllBlocks(false).some(function(b){ return b.type === 'text_print'; });
                    }},
                ],
            },
            {
                id: 'def_fn',
                title: 'Define a function',
                blurb: 'def + call.',
                steps: [
                    { text: 'Add a function definition (Functions)', test: function() { return workspace.getAllBlocks(false).some(function(b){ return (b.type || '').indexOf('procedures_defnoreturn') === 0 || (b.type || '').indexOf('procedures_defreturn') === 0; }); } },
                    { text: 'Add a function call', test: function() { return workspace.getAllBlocks(false).some(function(b){ return (b.type || '').indexOf('procedures_call') === 0; }); } },
                    { text: 'Run it', test: function() { return runHistory.length > 0; } },
                ],
            },
            {
                id: 'try_err',
                title: 'Catch an error',
                blurb: 'try / except resilience.',
                steps: [
                    { text: 'Add try/except (Errors)', test: function() { return workspace.getAllBlocks(false).some(function(b){ return (b.type || '').indexOf('py_try') === 0 || b.type === 'py_try_except'; }); } },
                    { text: 'Put a risky statement in try', test: function() {
                        return workspace.getAllBlocks(false).some(function(b){ return (b.type || '').indexOf('py_try') === 0 || b.type === 'py_try_except'; });
                    }},
                    { text: 'Print in except or use pass', test: function() { return workspace.getAllBlocks(false).length >= 2; } },
                ],
            },
        ];

        function openGuidedPaths() {
            closeStudioModal();
            const ov = document.createElement('div');
            ov.className = 'studio-modal-overlay';
            ov.id = 'studioModal';
            ov.onclick = function(e) { if (e.target === ov) closeStudioModal(); };
            let html = '<div class="studio-modal"><h2>Guided paths</h2><p class="muted">Short challenges — complete steps by building on the workspace.</p>';
            GUIDED_PATHS.forEach(function(p, pi) {
                html += '<div class="path-step" id="pathCard' + pi + '"><strong style="color:#FF7A26">' + escapeHtml(p.title) + '</strong>';
                html += '<div class="muted">' + escapeHtml(p.blurb) + '</div>';
                html += '<button class="btn" style="margin-top:8px" onclick="startGuidedPath(' + pi + ')">Start</button></div>';
            });
            html += '<div class="row"><button class="btn" onclick="closeStudioModal()">Close</button></div></div>';
            ov.innerHTML = html;
            document.body.appendChild(ov);
        }

        let activePathIndex = -1;
        function startGuidedPath(pi) {
            activePathIndex = pi;
            renderActivePath();
        }

        function renderActivePath() {
            const p = GUIDED_PATHS[activePathIndex];
            if (!p) return;
            closeStudioModal();
            const ov = document.createElement('div');
            ov.className = 'studio-modal-overlay';
            ov.id = 'studioModal';
            ov.onclick = function(e) { if (e.target === ov) closeStudioModal(); };
            let html = '<div class="studio-modal"><h2>' + escapeHtml(p.title) + '</h2><p class="muted">' + escapeHtml(p.blurb) + '</p>';
            let allDone = true;
            p.steps.forEach(function(s, si) {
                let done = false;
                try { done = !!s.test(); } catch (e) { done = false; }
                if (!done) allDone = false;
                html += '<div class="path-step' + (done ? ' done' : '') + '">';
                html += '<span class="check">' + (done ? '✓' : (si + 1) + '.') + '</span>' + escapeHtml(s.text);
                html += '</div>';
            });
            if (allDone) {
                html += '<p style="color:#FF7A26;font-weight:600;">Path complete — well forged.</p>';
                try {
                    const doneSet = JSON.parse(localStorage.getItem('pymason_paths_done') || '[]');
                    if (doneSet.indexOf(p.id) < 0) {
                        doneSet.push(p.id);
                        localStorage.setItem('pymason_paths_done', JSON.stringify(doneSet));
                    }
                } catch (e) { /* ok */ }
            }
            html += '<div class="row"><button class="btn btn-accent" onclick="renderActivePath()">Refresh checks</button>';
            html += '<button class="btn" onclick="openGuidedPaths()">All paths</button>';
            html += '<button class="btn" onclick="closeStudioModal()">Close</button></div></div>';
            ov.innerHTML = html;
            document.body.appendChild(ov);
        }

        function closeStudioModal() {
            document.getElementById('studioModal')?.remove();
        }

        // ── B2 Python peek ───────────────────────────────────────────
        function updatePythonPeek(blockId) {
            const el = document.getElementById('pythonPeek');
            if (!el) return;
            if (!blockId) {
                el.innerHTML = '';
                return;
            }
            const block = workspace.getBlockById(blockId);
            if (!block) {
                el.innerHTML = '';
                return;
            }
            try {
                let snippet = '';
                if (python.pythonGenerator.forBlock[block.type]) {
                    // Prefer single-block generation via temporary isolation is hard;
                    // use show path: blockToCode
                    const r = python.pythonGenerator.blockToCode(block);
                    snippet = Array.isArray(r) ? r[0] : r;
                }
                snippet = String(snippet || '').replace(/\s+/g, ' ').trim().slice(0, 120);
                if (snippet) {
                    el.innerHTML = '<strong>py</strong>' + escapeHtml(snippet);
                } else {
                    el.innerHTML = '<strong>py</strong>' + escapeHtml(block.type);
                }
            } catch (e) {
                el.innerHTML = '<strong>py</strong>' + escapeHtml(block.type);
            }
        }

        workspace.addChangeListener(function(event) {
            if (event.type === Blockly.Events.SELECTED) {
                updatePythonPeek(event.newElementId || null);
            }
        });

        // ── B3 Favorites ─────────────────────────────────────────────
        function getFavorites() {
            try {
                const a = JSON.parse(localStorage.getItem('pymason_favorites') || '[]');
                return Array.isArray(a) ? a : [];
            } catch (e) { return []; }
        }
        function setFavorites(arr) {
            localStorage.setItem('pymason_favorites', JSON.stringify(arr.slice(0, 40)));
        }

        function registerFavoritesToolbox() {
            if (typeof Blockly === 'undefined' || !Blockly.Variables) return;
            try {
                if (workspace.registerToolboxCategoryCallback) {
                    workspace.registerToolboxCategoryCallback('PYMASON_FAVORITES', function() {
                        const favs = getFavorites();
                        if (!favs.length) {
                            return [{ kind: 'label', text: 'Right-click a block → Add to Favorites' }];
                        }
                        return favs.map(function(type) {
                            return { kind: 'block', type: type };
                        });
                    });
                }
            } catch (e) { console.warn('Favorites toolbox', e); }
        }

        function addBlockToFavorites(block) {
            if (!block || !block.type) return;
            const favs = getFavorites();
            if (favs.indexOf(block.type) >= 0) {
                showToast('Already in Favorites');
                return;
            }
            favs.unshift(block.type);
            setFavorites(favs);
            showToast('Added to Favorites: ' + block.type);
            // Refresh toolbox flyout if open
            try {
                const tb = workspace.getToolbox();
                if (tb && tb.refreshSelection) tb.refreshSelection();
            } catch (e) { /* ok */ }
        }

        function registerFavoriteContextMenu() {
            try {
                Blockly.ContextMenuRegistry.registry.register({
                    displayText: function() { return 'Add to Favorites'; },
                    preconditionFn: function(scope) { return scope.block ? 'enabled' : 'hidden'; },
                    callback: function(scope) { addBlockToFavorites(scope.block); },
                    scopeType: Blockly.ContextMenuRegistry.ScopeType.BLOCK,
                    id: 'pymason_add_favorite',
                    weight: 12,
                });
            } catch (e) { /* already registered */ }
        }

        // ── B4 Diff workspaces ───────────────────────────────────────
        function openWorkspaceDiff() {
            const list = getWorkspaceList();
            if (list.length < 1) {
                showToast('Save at least one named workspace first');
                return;
            }
            closeStudioModal();
            const ov = document.createElement('div');
            ov.className = 'studio-modal-overlay';
            ov.id = 'studioModal';
            ov.onclick = function(e) { if (e.target === ov) closeStudioModal(); };
            let opts = list.map(function(item, i) {
                return '<option value="' + i + '">' + escapeHtml(item.name || 'Untitled') + '</option>';
            }).join('');
            opts += '<option value="current">— Current workspace —</option>';
            ov.innerHTML =
                '<div class="studio-modal"><h2>Diff workspaces</h2>' +
                '<div class="row"><label>A</label><select id="diffA">' + opts + '</select></div>' +
                '<div class="row"><label>B</label><select id="diffB">' + opts + '</select></div>' +
                '<div class="row"><button class="btn btn-accent" onclick="runWorkspaceDiff()">Compare</button>' +
                '<button class="btn" onclick="closeStudioModal()">Close</button></div>' +
                '<div id="diffOut" class="diff-pre muted">Pick two slots and compare generated Python.</div></div>';
            document.body.appendChild(ov);
        }

        function workspaceStateToPython(state) {
            // Load into a temporary headless approach: use serialization on main workspace is destructive.
            // Snapshot current, load, codegen, restore.
            const snap = Blockly.serialization.workspaces.save(workspace);
            try {
                workspace.clear();
                Blockly.serialization.workspaces.load(state, workspace);
                return python.pythonGenerator.workspaceToCode(workspace);
            } finally {
                workspace.clear();
                Blockly.serialization.workspaces.load(snap, workspace);
                updateCode();
            }
        }

        function simpleLineDiff(a, b) {
            const al = a.split('\n');
            const bl = b.split('\n');
            const max = Math.max(al.length, bl.length);
            const out = [];
            for (let i = 0; i < max; i++) {
                const L = al[i];
                const R = bl[i];
                if (L === R) {
                    if (L !== undefined) out.push('<span class="diff-same">  ' + escapeHtml(L) + '</span>');
                } else {
                    if (L !== undefined) out.push('<span class="diff-del">- ' + escapeHtml(L) + '</span>');
                    if (R !== undefined) out.push('<span class="diff-add">+ ' + escapeHtml(R) + '</span>');
                }
            }
            return out.join('\n');
        }

        function runWorkspaceDiff() {
            const list = getWorkspaceList();
            const aVal = document.getElementById('diffA')?.value;
            const bVal = document.getElementById('diffB')?.value;
            function loadCode(val) {
                if (val === 'current') return python.pythonGenerator.workspaceToCode(workspace);
                const idx = parseInt(val, 10);
                if (isNaN(idx) || !list[idx]) return '';
                return workspaceStateToPython(list[idx].data);
            }
            try {
                const ca = loadCode(aVal);
                const cb = loadCode(bVal);
                const out = document.getElementById('diffOut');
                if (out) {
                    out.innerHTML = '<div class="muted">Line-oriented diff (A vs B)</div>\n' + simpleLineDiff(ca, cb);
                }
            } catch (e) {
                showToast('Diff failed: ' + (e.message || e));
            }
        }

        // ── C1 Minimap ───────────────────────────────────────────────
        let minimapVisible = localStorage.getItem('pymason_minimap') === '1';
        function toggleMinimap() {
            minimapVisible = !minimapVisible;
            localStorage.setItem('pymason_minimap', minimapVisible ? '1' : '0');
            const c = document.getElementById('minimapCanvas');
            if (!c) return;
            c.classList.toggle('hidden', !minimapVisible);
            if (minimapVisible) updateMinimap();
            showToast(minimapVisible ? 'Minimap on' : 'Minimap off');
        }
        function updateMinimap() {
            const canvas = document.getElementById('minimapCanvas');
            if (!canvas || canvas.classList.contains('hidden') || !workspace) return;
            const ctx = canvas.getContext('2d');
            const W = canvas.width, H = canvas.height;
            ctx.clearRect(0, 0, W, H);
            ctx.fillStyle = '#0A0807';
            ctx.fillRect(0, 0, W, H);
            const blocks = workspace.getAllBlocks(false).filter(function(b) { return !b.getParent(); });
            if (!blocks.length) {
                ctx.fillStyle = '#A89078';
                ctx.font = '10px sans-serif';
                ctx.fillText('empty', 50, 52);
                return;
            }
            let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
            const rects = blocks.map(function(b) {
                const r = b.getBoundingRectangle ? b.getBoundingRectangle() : null;
                if (r) {
                    minX = Math.min(minX, r.left); minY = Math.min(minY, r.top);
                    maxX = Math.max(maxX, r.right); maxY = Math.max(maxY, r.bottom);
                    return r;
                }
                const xy = b.getRelativeToSurfaceXY();
                minX = Math.min(minX, xy.x); minY = Math.min(minY, xy.y);
                maxX = Math.max(maxX, xy.x + 120); maxY = Math.max(maxY, xy.y + 40);
                return { left: xy.x, top: xy.y, right: xy.x + 120, bottom: xy.y + 40 };
            });
            const bw = Math.max(1, maxX - minX);
            const bh = Math.max(1, maxY - minY);
            const scale = Math.min((W - 8) / bw, (H - 8) / bh);
            ctx.fillStyle = '#FF7A26';
            rects.forEach(function(r) {
                const x = 4 + (r.left - minX) * scale;
                const y = 4 + (r.top - minY) * scale;
                const w = Math.max(3, (r.right - r.left) * scale);
                const h = Math.max(2, (r.bottom - r.top) * scale);
                ctx.globalAlpha = 0.75;
                ctx.fillRect(x, y, w, h);
            });
            ctx.globalAlpha = 1;
            // viewport approx
            try {
                const m = workspace.getMetrics();
                if (m) {
                    ctx.strokeStyle = '#E8DCC8';
                    ctx.lineWidth = 1;
                    const vx = 4 + (m.viewLeft - minX) * scale;
                    const vy = 4 + (m.viewTop - minY) * scale;
                    const vw = m.viewWidth * scale;
                    const vh = m.viewHeight * scale;
                    ctx.strokeRect(vx, vy, vw, vh);
                }
            } catch (e) { /* ok */ }
        }

        (function initMinimap() {
            const c = document.getElementById('minimapCanvas');
            if (!c) return;
            if (minimapVisible) c.classList.remove('hidden');
            c.addEventListener('click', function(ev) {
                // Center workspace roughly
                try {
                    if (workspace.scrollCenter) workspace.scrollCenter();
                    zoomToFitWorkspace();
                } catch (e) { /* ok */ }
            });
            workspace.addChangeListener(function(e) {
                if (!minimapVisible) return;
                if (e.type === Blockly.Events.BLOCK_MOVE ||
                    e.type === Blockly.Events.BLOCK_CREATE ||
                    e.type === Blockly.Events.BLOCK_DELETE ||
                    e.type === Blockly.Events.VIEWPORT_CHANGE) {
                    requestAnimationFrame(updateMinimap);
                }
            });
            setTimeout(updateMinimap, 500);
        })();

        // ── C2 Collapse / expand all ─────────────────────────────────
        function collapseExpandAll(collapse) {
            workspace.getAllBlocks(false).forEach(function(b) {
                try {
                    if (b.isCollapsible && b.isCollapsible()) b.setCollapsed(!!collapse);
                    else if (typeof b.setCollapsed === 'function') b.setCollapsed(!!collapse);
                } catch (e) { /* ok */ }
            });
            updateCode();
            updateMinimap();
            showToast(collapse ? 'Collapsed collapsible blocks' : 'Expanded blocks');
        }

        // ── C3 Snap selected to grid ─────────────────────────────────
        function snapSelectedToGrid() {
            const sel = Blockly.getSelected && Blockly.getSelected();
            if (!sel || !sel.getRelativeToSurfaceXY) {
                showToast('Select a block first');
                return;
            }
            const sp = 22; // match inject grid spacing
            const xy = sel.getRelativeToSurfaceXY();
            const nx = Math.round(xy.x / sp) * sp;
            const ny = Math.round(xy.y / sp) * sp;
            sel.moveBy(nx - xy.x, ny - xy.y);
            showToast('Snapped to grid');
        }

        // ── C4 Soft type / connection warnings ───────────────────────
        function softValidateWorkspace() {
            const issues = [];
            workspace.getAllBlocks(false).forEach(function(b) {
                if (b.disabled || (b.isEnabled && !b.isEnabled())) return;
                // Unconnected top-level non-hat that looks like statement orphan already handled
                b.inputList.forEach(function(input) {
                    if (input.type === Blockly.INPUT_VALUE && input.connection && !input.connection.targetBlock()) {
                        if (input.name && !input.connection.isConnected()) {
                            // only flag if check expects number-like on math
                            const checks = input.connection.getCheck && input.connection.getCheck();
                            if (checks && checks.indexOf('Number') >= 0 && (b.type || '').indexOf('math_') === 0) {
                                issues.push({ block: b, msg: 'Missing number input on ' + b.type });
                            }
                        }
                    }
                });
            });
            return issues;
        }

        workspace.addChangeListener(function(event) {
            if (event.type === Blockly.Events.BLOCK_MOVE ||
                event.type === Blockly.Events.BLOCK_CREATE ||
                event.type === Blockly.Events.BLOCK_CHANGE) {
                // Lightweight — no toast spam; status only when many issues
                setTimeout(function() {
                    const issues = softValidateWorkspace();
                    if (issues.length >= 3 && statusText) {
                        statusText.textContent = issues.length + ' soft input warnings';
                    }
                }, 200);
            }
        });

        // ── C5 Lua in getGeneratedCode ───────────────────────────────
        // Patch onOutputLangChange titles
        const _origGetGeneratedCode = getGeneratedCode;
        getGeneratedCode = function() {
            if (outputLang === 'lua' && typeof lua !== 'undefined' && lua.luaGenerator) {
                try {
                    return lua.luaGenerator.workspaceToCode(workspace);
                } catch (e) {
                    const py = python.pythonGenerator.workspaceToCode(workspace);
                    return '-- Lua generation partial for custom PyMason blocks.\n-- Python fallback:\n\n' +
                        py.split('\n').map(function(l) { return '-- ' + l; }).join('\n');
                }
            }
            return _origGetGeneratedCode();
        };
        const _origOnLang = onOutputLangChange;
        onOutputLangChange = function() {
            outputLang = document.getElementById('langSelect')?.value || 'python';
            localStorage.setItem('pymason_output_lang', outputLang);
            const title = document.querySelector('.code-title');
            if (title) {
                title.textContent =
                    outputLang === 'javascript' ? 'Generated JavaScript' :
                    outputLang === 'lua' ? 'Generated Lua' : 'Generated Python';
            }
            updateCode();
            showToast('Output: ' + outputLang);
        };
        (function fixLangTitle() {
            const sel = document.getElementById('langSelect');
            if (sel && outputLang) sel.value = outputLang;
            if (outputLang === 'lua') {
                const title = document.querySelector('.code-title');
                if (title) title.textContent = 'Generated Lua';
            }
        })();

        // ── E1 Format code ───────────────────────────────────────────
        function formatGeneratedCode(code) {
            // Light formatter: normalize newlines, strip trailing spaces, ensure final newline
            let lines = String(code || '').replace(/\r\n/g, '\n').split('\n');
            lines = lines.map(function(l) { return l.replace(/[ \t]+$/g, ''); });
            // Collapse >2 blank lines
            const out = [];
            let blank = 0;
            lines.forEach(function(l) {
                if (l.trim() === '') {
                    blank++;
                    if (blank <= 2) out.push('');
                } else {
                    blank = 0;
                    out.push(l);
                }
            });
            let s = out.join('\n').replace(/^\n+/, '');
            if (s && !s.endsWith('\n')) s += '\n';
            return s;
        }

        function copyFormattedCode() {
            const code = formatGeneratedCode(getGeneratedCode());
            if (!code.trim()) {
                showToast('Nothing to copy');
                return;
            }
            navigator.clipboard.writeText(code).then(function() {
                showToast('Formatted code copied');
            }).catch(function() {
                const ta = document.createElement('textarea');
                ta.value = code;
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
                showToast('Formatted code copied');
            });
        }

        // ── E2 Voice to chat ─────────────────────────────────────────
        function startVoiceToChat() {
            const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SR) {
                showToast('Speech recognition not supported in this browser');
                return;
            }
            const rec = new SR();
            rec.lang = 'en-US';
            rec.interimResults = false;
            rec.maxAlternatives = 1;
            showToast('Listening…');
            rec.onresult = function(ev) {
                const text = ev.results[0][0].transcript;
                const input = document.getElementById('chatInput');
                if (input) {
                    input.value = (input.value ? input.value + ' ' : '') + text;
                    const chat = document.getElementById('chatPanel');
                    if (chat && !chat.classList.contains('open')) toggleChat();
                    input.focus();
                }
                showToast('Voice captured');
            };
            rec.onerror = function() { showToast('Voice input failed'); };
            rec.start();
        }

        // ── Context menu: snap ───────────────────────────────────────
        try {
            Blockly.ContextMenuRegistry.registry.register({
                displayText: function() { return 'Snap to grid'; },
                preconditionFn: function(scope) { return scope.block ? 'enabled' : 'hidden'; },
                callback: function(scope) {
                    const b = scope.block;
                    const sp = 22;
                    const xy = b.getRelativeToSurfaceXY();
                    b.moveBy(Math.round(xy.x / sp) * sp - xy.x, Math.round(xy.y / sp) * sp - xy.y);
                },
                scopeType: Blockly.ContextMenuRegistry.ScopeType.BLOCK,
                id: 'pymason_snap_grid',
                weight: 14,
            });
        } catch (e) { /* ok */ }

        // ── Keyboard extras ──────────────────────────────────────────
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === '0') {
                e.preventDefault();
                zoomToFitWorkspace();
            }
            if (e.ctrlKey && e.shiftKey && (e.key === 'L' || e.key === 'l')) {
                e.preventDefault();
                shareWorkspaceLink();
            }
        });

        // ── Wire favorites + share load after ensure ──────────────────
        registerFavoritesToolbox();
        registerFavoriteContextMenu();
        renderRunHistoryList();

        // Hook enterApp extensions via patch after definition — done at boot below
        const _studioEnterHooks = function() {
            tryLoadSharedWorkspace();
            registerFavoritesToolbox();
            if (minimapVisible) {
                document.getElementById('minimapCanvas')?.classList.remove('hidden');
                setTimeout(updateMinimap, 200);
            }
        };
        // Call once DOM ready after inject
        setTimeout(_studioEnterHooks, 0);

"""

# Insert before VERSION constant
version_anchor = """        // ═══════════════════════════════════════════════════════════════════
        //  VERSION
        // ═══════════════════════════════════════════════════════════════════

        const PYMASON_VERSION = '0.4.0';"""
version_new = js + """
        // ═══════════════════════════════════════════════════════════════════
        //  VERSION
        // ═══════════════════════════════════════════════════════════════════

        const PYMASON_VERSION = '0.5.0';"""
if version_anchor not in text:
    raise SystemExit("version anchor missing")
text = text.replace(version_anchor, version_new, 1)

# Patch getGeneratedCode for lua was done by wrapping later — also patch original getGeneratedCode for early path
# Patch runCode to use appendOutputSmart and pushRunHistory
# Patch enterApp to call share load
# Patch logout to clear history optional — clear run history is aggressive; skip clear on logout for UX

# Patch runCode error paths
old_run_err = """                            case 'error':
                                if (!executionAborted) appendOutput(e.data.text, true);
                                runResolve = null;
                                resolve();
                                break;"""
new_run_err = """                            case 'error':
                                if (!executionAborted) appendOutputSmart(e.data.text, true);
                                runResolve = null;
                                resolve();
                                break;"""
if old_run_err in text:
    text = text.replace(old_run_err, new_run_err, 1)

# After run finishes, record history — find the finished block
old_finish = """            if (!executionAborted) {
                const elapsed = performance.now() - startTime;
                const timeSpan = document.createElement('span');
                timeSpan.className = 'exec-time';
                timeSpan.textContent = '\\n— Finished in ' + (elapsed / 1000).toFixed(2) + 's —\\n';
                outputContent.appendChild(timeSpan);
                showVarInspector(capturedVars);
            }

            btnRun.style.display = '';
            btnStop.style.display = 'none';
        }"""
new_finish = """            if (!executionAborted) {
                const elapsed = performance.now() - startTime;
                const timeSpan = document.createElement('span');
                timeSpan.className = 'exec-time';
                timeSpan.textContent = '\\n— Finished in ' + (elapsed / 1000).toFixed(2) + 's —\\n';
                outputContent.appendChild(timeSpan);
                showVarInspector(capturedVars);
                try {
                    const full = outputContent.innerText || '';
                    const hadErr = !!outputContent.querySelector('.error');
                    if (typeof pushRunHistory === 'function') {
                        pushRunHistory({
                            ok: !hadErr,
                            ms: elapsed,
                            preview: full.slice(0, 200),
                            full: full,
                        });
                    }
                } catch (histErr) { /* ok */ }
            }

            btnRun.style.display = '';
            btnStop.style.display = 'none';
        }"""
if old_finish not in text:
    # try without double escapes - the file has real newlines
    old_finish2 = """            if (!executionAborted) {
                const elapsed = performance.now() - startTime;
                const timeSpan = document.createElement('span');
                timeSpan.className = 'exec-time';
                timeSpan.textContent = '\n— Finished in ' + (elapsed / 1000).toFixed(2) + 's —\n';
                outputContent.appendChild(timeSpan);
                showVarInspector(capturedVars);
            }

            btnRun.style.display = '';
            btnStop.style.display = 'none';
        }"""
    new_finish2 = """            if (!executionAborted) {
                const elapsed = performance.now() - startTime;
                const timeSpan = document.createElement('span');
                timeSpan.className = 'exec-time';
                timeSpan.textContent = '\n— Finished in ' + (elapsed / 1000).toFixed(2) + 's —\n';
                outputContent.appendChild(timeSpan);
                showVarInspector(capturedVars);
                try {
                    const full = outputContent.innerText || '';
                    const hadErr = !!outputContent.querySelector('.error');
                    if (typeof pushRunHistory === 'function') {
                        pushRunHistory({
                            ok: !hadErr,
                            ms: elapsed,
                            preview: full.slice(0, 200),
                            full: full,
                        });
                    }
                } catch (histErr) { /* ok */ }
            }

            btnRun.style.display = '';
            btnStop.style.display = 'none';
        }"""
    if old_finish2 not in text:
        print("WARN: run finish anchor missing — history may not auto-record")
    else:
        text = text.replace(old_finish2, new_finish2, 1)
else:
    text = text.replace(old_finish, new_finish, 1)

# Patch fallback error to appendOutputSmart
old_fb = """                        appendOutput(cleanLines.join('\\n') || msg, true);"""
# file has real \n in source as join('\n')
old_fb2 = """                        appendOutput(cleanLines.join('\n') || msg, true);"""
new_fb2 = """                        appendOutputSmart(cleanLines.join('\n') || msg, true);"""
if old_fb2 in text:
    text = text.replace(old_fb2, new_fb2, 1)

# enterApp: after showWelcome load share
old_enter = """                    loadWorkspace();
                    showWelcome();
                    setTimeout(refreshBlocklyLayout, 100);
                    setTimeout(refreshBlocklyLayout, 350);"""
new_enter = """                    const shared = (typeof tryLoadSharedWorkspace === 'function') && tryLoadSharedWorkspace();
                    if (!shared) loadWorkspace();
                    showWelcome();
                    if (typeof registerFavoritesToolbox === 'function') registerFavoritesToolbox();
                    setTimeout(refreshBlocklyLayout, 100);
                    setTimeout(refreshBlocklyLayout, 350);
                    setTimeout(function(){ if (typeof updateMinimap === 'function') updateMinimap(); }, 400);"""
if old_enter not in text:
    print("WARN: enterApp anchor missing")
else:
    text = text.replace(old_enter, new_enter, 1)

# downloadPython should use format option lightly
old_dl = """            const isJs = outputLang === 'javascript';
            const blob = new Blob([code], { type: isJs ? 'text/javascript' : 'text/x-python' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = isJs ? 'my_program.js' : 'my_program.py';"""
new_dl = """            const formatted = (typeof formatGeneratedCode === 'function') ? formatGeneratedCode(code) : code;
            const isJs = outputLang === 'javascript';
            const isLua = outputLang === 'lua';
            const blob = new Blob([formatted], {
                type: isJs ? 'text/javascript' : (isLua ? 'text/x-lua' : 'text/x-python')
            });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = isJs ? 'my_program.js' : (isLua ? 'my_program.lua' : 'my_program.py');"""
if old_dl in text:
    text = text.replace(old_dl, new_dl, 1)

# CORE_TOOLBOX should keep Favorites visible
old_core = """        const CORE_TOOLBOX_CATEGORIES = new Set([
            'I/O', 'Variables', 'Text', 'Math', 'Logic', 'Loops', 'Lists', 'Functions',
        ]);"""
new_core = """        const CORE_TOOLBOX_CATEGORIES = new Set([
            'Favorites', 'I/O', 'Variables', 'Text', 'Math', 'Logic', 'Loops', 'Lists', 'Functions',
        ]);"""
if old_core in text:
    text = text.replace(old_core, new_core, 1)

INDEX.write_text(text, encoding="utf-8")
print("Injected studio features into", INDEX)
print("Size:", INDEX.stat().st_size)
