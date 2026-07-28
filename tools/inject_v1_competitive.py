#!/usr/bin/env python3
"""Inject PyMason v1.0 competitive best-in-class pack (idempotent)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
text = INDEX.read_text(encoding="utf-8")

if "PYMASON_V1_COMPETITIVE" in text:
    print("Already injected v1 competitive — skipping")
    raise SystemExit(0)

# ── CSS ────────────────────────────────────────────────────────────
css = r"""
        /* ── v1.0 Competitive surfaces ───────────────────── */
        .code-mode-bar {
            display: flex; gap: 4px; align-items: center; flex-wrap: wrap;
        }
        .code-mode-bar .mode-btn.active {
            background: rgba(255,122,38,0.22);
            border-color: #FF7A26;
            color: #FF7A26;
        }
        #codeEditor {
            display: none;
            flex: 1;
            width: 100%;
            min-height: 120px;
            border: none;
            resize: none;
            background: #0C0A09;
            color: #F5E6D3;
            font-family: 'Cascadia Code', 'Fira Code', Consolas, monospace;
            font-size: 13px;
            line-height: 1.55;
            padding: 12px 14px;
            tab-size: 4;
            outline: none;
        }
        #codeEditor.visible { display: block; }
        .code-with-lines.hidden-live { display: none !important; }
        .debug-bar {
            display: none;
            gap: 6px;
            align-items: center;
            padding: 6px 10px;
            background: #1A1614;
            border-bottom: 1px solid #2A211C;
            flex-wrap: wrap;
        }
        .debug-bar.visible { display: flex; }
        .debug-bar .dbg-status {
            font-size: 11px; color: #A89078; margin-left: auto;
        }
        .stage-panel {
            display: none;
            border-top: 1px solid var(--panel-border);
            background: #0C0A09;
            flex-shrink: 0;
        }
        .stage-panel.visible { display: block; }
        .stage-header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 4px 10px; font-size: 10px; color: var(--brass-dim);
            text-transform: uppercase; letter-spacing: 0.06em;
        }
        #stageCanvas {
            display: block;
            width: 100%;
            height: 180px;
            background: #0A0807;
            cursor: crosshair;
        }
        .cmd-palette-overlay {
            position: fixed; inset: 0; z-index: 40000;
            background: rgba(0,0,0,0.65);
            display: flex; justify-content: center; padding-top: 12vh;
        }
        .cmd-palette {
            width: min(520px, 94vw);
            background: #1A1614;
            border: 2px solid #FF7A26;
            border-radius: 10px;
            box-shadow: 0 16px 48px rgba(0,0,0,0.6);
            overflow: hidden;
        }
        .cmd-palette input {
            width: 100%; border: none; background: #0A0807; color: #E8DCC8;
            padding: 14px 16px; font-size: 15px; outline: none;
            border-bottom: 1px solid #2A211C; font-family: var(--font-ui);
        }
        .cmd-palette-list { max-height: 320px; overflow: auto; }
        .cmd-item {
            padding: 10px 16px; cursor: pointer; font-size: 13px; color: #E8DCC8;
            display: flex; justify-content: space-between; gap: 12px;
        }
        .cmd-item:hover, .cmd-item.active {
            background: rgba(255,122,38,0.12); color: #FF7A26;
        }
        .cmd-item kbd {
            font-size: 10px; color: #A89078; border: 1px solid #2A211C;
            padding: 2px 6px; border-radius: 4px;
        }
        .module-tabs {
            display: flex; gap: 4px; flex-wrap: wrap; align-items: center;
            padding: 4px 8px; background: #110F0D; border-bottom: 1px solid #2A211C;
        }
        .module-tab {
            font-size: 11px; padding: 4px 10px; border-radius: 999px;
            border: 1px solid #2A211C; background: transparent; color: #A89078;
            cursor: pointer; font-family: var(--font-ui);
        }
        .module-tab.active {
            border-color: #FF7A26; color: #FF7A26;
            background: rgba(255,122,38,0.1);
        }
        .chat-apply-btn {
            margin-top: 8px;
        }
        .bp-line {
            cursor: pointer;
        }
        .bp-line.has-bp {
            color: #FF7A26 !important;
            font-weight: 700;
        }
        .blockly-debug-current .blocklyPath {
            stroke: #FF7A26 !important;
            stroke-width: 3px !important;
            filter: drop-shadow(0 0 6px rgba(255,122,38,0.7));
        }

"""

css_anchor = "        .diff-same { color: #A89078; }\n\n\n    </style>"
if css_anchor not in text:
    css_anchor = "        .diff-same { color: #A89078; }\n\n    </style>"
if css_anchor not in text:
    raise SystemExit("css anchor missing")
text = text.replace(css_anchor, "        .diff-same { color: #A89078; }\n" + css + "\n    </style>", 1)

# ── Header buttons ─────────────────────────────────────────────────
old_h = """            <button class="btn" onclick="collapseExpandAll(true)" title="Collapse all blocks">Collapse</button>
            <button class="btn" onclick="collapseExpandAll(false)" title="Expand all blocks">Expand</button>
            <button class="btn btn-accent" onclick="downloadPython()" title="Download as .py file (Ctrl+D)">Download .py</button>"""
new_h = """            <button class="btn" onclick="collapseExpandAll(true)" title="Collapse all blocks">Collapse</button>
            <button class="btn" onclick="collapseExpandAll(false)" title="Expand all blocks">Expand</button>
            <button class="btn" onclick="openCommandPalette()" title="Command palette (Ctrl+K)">⌘K</button>
            <button class="btn" onclick="openProjectModules()" title="Multi-module project">Project</button>
            <button class="btn" onclick="openCurriculumHub()" title="Curriculum packs &amp; autograde">Curriculum</button>
            <button class="btn" onclick="toggleStagePanel()" title="Stage / turtle / plots">Stage</button>
            <button class="btn" onclick="toggleDebugBar()" title="Debugger controls">Debug</button>
            <button class="btn btn-accent" onclick="downloadPython()" title="Download as .py file (Ctrl+D)">Download .py</button>"""
if old_h not in text:
    raise SystemExit("header anchor missing")
text = text.replace(old_h, new_h, 1)

# ── Code panel dual mode + debug + stage ───────────────────────────
old_panel = """        <div class="code-panel" id="codePanel" role="region" aria-label="Generated Python code">
            <div class="code-header">
                <div class="code-title">Generated Python</div>
                <div class="code-actions">
                    <button class="btn" onclick="copyFormattedCode()" title="Copy formatted code">Format+Copy</button>
                    <button class="btn" onclick="copyCode()" title="Copy">Copy</button>
                </div>
            </div>
            <div class="code-with-lines">
                <div class="line-numbers" id="lineNumbers"></div>
                <div class="code-output" id="codeOutput">
                    <span class="empty-state">Drag blocks from the toolbox to start building.<br>Your Python code will appear here in real time.</span>
                </div>
            </div>
            <div class="output-panel collapsed" id="outputPanel" role="region" aria-label="Program output" aria-live="polite">
                <div class="output-header">
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
                <div class="output-content" id="outputContent"></div>
                <div class="var-inspector" id="varInspector" aria-label="Variable inspector">
                    <div class="var-inspector-title">Variables after run</div>
                    <div class="var-inspector-list" id="varInspectorList"></div>
                </div>
            </div>
        </div>"""

new_panel = """        <div class="code-panel" id="codePanel" role="region" aria-label="Generated Python code">
            <div class="module-tabs" id="moduleTabs" aria-label="Project modules"></div>
            <div class="code-header">
                <div class="code-title" id="codeTitle">Generated Python</div>
                <div class="code-actions code-mode-bar">
                    <button class="btn mode-btn active" id="modeLiveBtn" onclick="setCodeMode('live')" title="Blocks drive code">Blocks→Code</button>
                    <button class="btn mode-btn" id="modeFreeBtn" onclick="setCodeMode('free')" title="Edit Python freely">Free Python</button>
                    <button class="btn" onclick="syncCodeFromBlocks()" title="Reload editor from blocks">↻ Sync</button>
                    <button class="btn" onclick="copyFormattedCode()" title="Copy formatted code">Format+Copy</button>
                    <button class="btn" onclick="copyCode()" title="Copy">Copy</button>
                </div>
            </div>
            <div class="debug-bar" id="debugBar">
                <button class="btn" onclick="debugRun()" title="Run with debugger">▶ Debug</button>
                <button class="btn" onclick="debugStep()" title="Step">Step</button>
                <button class="btn" onclick="debugContinue()" title="Continue">Cont</button>
                <button class="btn" onclick="debugStop()" title="Stop debug">Stop</button>
                <button class="btn" onclick="toggleBreakpointOnSelection()" title="Toggle breakpoint on selected block">BP</button>
                <span class="dbg-status" id="debugStatus">Debugger idle · click line # for breakpoints</span>
            </div>
            <div class="code-with-lines" id="codeLiveView">
                <div class="line-numbers" id="lineNumbers"></div>
                <div class="code-output" id="codeOutput">
                    <span class="empty-state">Drag blocks from the toolbox to start building.<br>Your Python code will appear here in real time.</span>
                </div>
            </div>
            <textarea id="codeEditor" spellcheck="false" aria-label="Free Python editor" placeholder="# Free Python mode — edit code directly. Run uses this buffer. Sync reloads from blocks."></textarea>
            <div class="stage-panel" id="stagePanel">
                <div class="stage-header">
                    <span>Stage · turtle · plots</span>
                    <span>
                        <button class="btn" onclick="clearStage()" title="Clear stage">Clear</button>
                        <button class="btn" onclick="toggleStagePanel()" title="Hide">Hide</button>
                    </span>
                </div>
                <canvas id="stageCanvas" width="640" height="180" aria-label="Graphics stage"></canvas>
            </div>
            <div class="output-panel collapsed" id="outputPanel" role="region" aria-label="Program output" aria-live="polite">
                <div class="output-header">
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
                <div class="output-content" id="outputContent"></div>
                <div class="var-inspector" id="varInspector" aria-label="Variable inspector">
                    <div class="var-inspector-title">Variables after run</div>
                    <div class="var-inspector-list" id="varInspectorList"></div>
                </div>
            </div>
        </div>"""

if old_panel not in text:
    raise SystemExit("code panel anchor missing")
text = text.replace(old_panel, new_panel, 1)

# Toolbox stage category before Imports favorites section already has Favorites
old_tb = """        <!-- ── Favorites (populated dynamically) ───── -->
        <category name="Favorites" colour="#FF7A26" custom="PYMASON_FAVORITES"></category>

        <!-- ── Imports ─────────────────────────────── -->"""
new_tb = """        <!-- ── Favorites (populated dynamically) ───── -->
        <category name="Favorites" colour="#FF7A26" custom="PYMASON_FAVORITES"></category>

        <!-- ── Stage / turtle / plots ──────────────── -->
        <category name="Stage" colour="#C45A18">
            <block type="py_stage_clear"></block>
            <block type="py_turtle_forward">
                <value name="DIST"><shadow type="math_number"><field name="NUM">50</field></shadow></value>
            </block>
            <block type="py_turtle_turn">
                <value name="DEG"><shadow type="math_number"><field name="NUM">90</field></shadow></value>
            </block>
            <block type="py_turtle_goto">
                <value name="X"><shadow type="math_number"><field name="NUM">0</field></shadow></value>
                <value name="Y"><shadow type="math_number"><field name="NUM">0</field></shadow></value>
            </block>
            <block type="py_turtle_pen">
                <field name="MODE">down</field>
            </block>
            <block type="py_turtle_color">
                <field name="COLOR">#FF7A26</field>
            </block>
            <block type="py_plot_list"></block>
            <block type="py_stage_text">
                <value name="TEXT"><shadow type="text"><field name="TEXT">Hello</field></shadow></value>
            </block>
        </category>

        <!-- ── Imports ─────────────────────────────── -->"""
if old_tb not in text:
    raise SystemExit("toolbox favorites anchor missing")
text = text.replace(old_tb, new_tb, 1)

# CORE categories include Stage
text = text.replace(
    "'Favorites', 'I/O', 'Variables', 'Text', 'Math', 'Logic', 'Loops', 'Lists', 'Functions',",
    "'Favorites', 'Stage', 'I/O', 'Variables', 'Text', 'Math', 'Logic', 'Loops', 'Lists', 'Functions',",
    1,
)

# ── JS pack ────────────────────────────────────────────────────────
js = r'''
        // ═══════════════════════════════════════════════════════════════════
        //  PYMASON_V1_COMPETITIVE — best-in-class Target 1.0+
        // ═══════════════════════════════════════════════════════════════════

        // ── Dual code surface ────────────────────────────────────────
        let codeMode = localStorage.getItem('pymason_code_mode') || 'live'; // live | free
        let freePythonBuffer = '';
        let lineBreakpoints = new Set(); // 1-based line numbers
        let blockBreakpoints = new Set(); // block ids
        let debugState = { active: false, paused: false, line: 0, resolveStep: null };

        function setCodeMode(mode) {
            codeMode = mode === 'free' ? 'free' : 'live';
            localStorage.setItem('pymason_code_mode', codeMode);
            const live = document.getElementById('codeLiveView');
            const ed = document.getElementById('codeEditor');
            const bL = document.getElementById('modeLiveBtn');
            const bF = document.getElementById('modeFreeBtn');
            if (bL) bL.classList.toggle('active', codeMode === 'live');
            if (bF) bF.classList.toggle('active', codeMode === 'free');
            if (codeMode === 'free') {
                if (live) live.classList.add('hidden-live');
                if (ed) {
                    ed.classList.add('visible');
                    if (!ed.value.trim()) ed.value = getGeneratedCode() || freePythonBuffer || '';
                    freePythonBuffer = ed.value;
                }
                showToast('Free Python — Run uses the editor buffer');
            } else {
                if (live) live.classList.remove('hidden-live');
                if (ed) {
                    freePythonBuffer = ed.value;
                    ed.classList.remove('visible');
                }
                updateCode();
                showToast('Blocks→Code live sync');
            }
            const title = document.getElementById('codeTitle') || document.querySelector('.code-title');
            if (title && outputLang === 'python') {
                title.textContent = codeMode === 'free' ? 'Free Python (editable)' : 'Generated Python';
            }
        }

        function syncCodeFromBlocks() {
            const code = python.pythonGenerator.workspaceToCode(workspace);
            freePythonBuffer = code;
            const ed = document.getElementById('codeEditor');
            if (ed) ed.value = code;
            if (codeMode === 'live') updateCode();
            showToast('Synced from blocks');
        }

        function getExecutablePython() {
            if (outputLang !== 'python' && outputLang !== 'lua' && outputLang !== 'javascript') {
                /* keep */
            }
            if (codeMode === 'free') {
                const ed = document.getElementById('codeEditor');
                const v = ed ? ed.value : freePythonBuffer;
                return v || '';
            }
            return python.pythonGenerator.workspaceToCode(workspace);
        }

        // Patch updateCode to respect free mode
        const _v1_updateCode = updateCode;
        updateCode = function(event) {
            if (codeMode === 'free') {
                // Still update maps from blocks for debug jump, but don't clobber editor
                try {
                    const code = python.pythonGenerator.workspaceToCode(workspace);
                    lastGeneratedCode = code;
                    buildBlockLineMap(code);
                    const blocks = workspace.getAllBlocks(false);
                    blockCount.textContent = blocks.length + ' block' + (blocks.length !== 1 ? 's' : '');
                    updateCategoryCounts();
                } catch (e) { /* ok */ }
                return;
            }
            _v1_updateCode(event);
            // Line number breakpoint clicks
            setTimeout(wireLineBreakpointClicks, 0);
        };

        function wireLineBreakpointClicks() {
            const ln = document.getElementById('lineNumbers');
            if (!ln || ln._bpWired) return;
            ln._bpWired = true;
            ln.style.cursor = 'pointer';
            ln.title = 'Click a line number to toggle breakpoint';
            ln.addEventListener('click', function(ev) {
                const text = ln.textContent || '';
                const lines = text.split('\n');
                const rect = ln.getBoundingClientRect();
                const y = ev.clientY - rect.top;
                const lineH = rect.height / Math.max(1, lines.length);
                const idx = Math.min(lines.length - 1, Math.max(0, Math.floor(y / lineH)));
                const lineNum = idx + 1;
                toggleLineBreakpoint(lineNum);
            });
        }

        function toggleLineBreakpoint(lineNum) {
            if (lineBreakpoints.has(lineNum)) lineBreakpoints.delete(lineNum);
            else lineBreakpoints.add(lineNum);
            refreshBreakpointGutter();
            showToast('Breakpoint line ' + lineNum + (lineBreakpoints.has(lineNum) ? ' on' : ' off'));
        }

        function refreshBreakpointGutter() {
            const ln = document.getElementById('lineNumbers');
            if (!ln || !lastGeneratedCode) return;
            const n = countLines(lastGeneratedCode || getGeneratedCode());
            ln.innerHTML = Array.from({ length: n }, function(_, i) {
                const line = i + 1;
                const cls = lineBreakpoints.has(line) ? 'bp-line has-bp' : 'bp-line';
                return '<span class="' + cls + '" data-bp-line="' + line + '">' + line + '</span>';
            }).join('\n');
            ln._bpWired = false;
            wireLineBreakpointClicks();
        }

        function toggleBreakpointOnSelection() {
            const sel = Blockly.getSelected && Blockly.getSelected();
            if (!sel) {
                showToast('Select a block first');
                return;
            }
            if (blockBreakpoints.has(sel.id)) {
                blockBreakpoints.delete(sel.id);
                showToast('Block breakpoint off');
            } else {
                blockBreakpoints.add(sel.id);
                showToast('Block breakpoint on');
            }
            // Map to lines
            const range = blockLineMap[sel.id];
            if (range) {
                for (let l = range.start; l <= range.end; l++) {
                    if (blockBreakpoints.has(sel.id)) lineBreakpoints.add(l);
                    else lineBreakpoints.delete(l);
                }
                refreshBreakpointGutter();
            }
        }

        // ── Stage / turtle / plots ───────────────────────────────────
        const stageApi = {
            x: 320, y: 90, angle: 0, pen: true, color: '#FF7A26', path: [],
        };

        function getStageCtx() {
            const c = document.getElementById('stageCanvas');
            if (!c) return null;
            return c.getContext('2d');
        }

        function clearStage() {
            const c = document.getElementById('stageCanvas');
            const ctx = getStageCtx();
            if (!c || !ctx) return;
            ctx.fillStyle = '#0A0807';
            ctx.fillRect(0, 0, c.width, c.height);
            stageApi.x = c.width / 2;
            stageApi.y = c.height / 2;
            stageApi.angle = 0;
            stageApi.path = [];
            drawTurtleCursor();
        }

        function drawTurtleCursor() {
            const ctx = getStageCtx();
            const c = document.getElementById('stageCanvas');
            if (!ctx || !c) return;
            const rad = (stageApi.angle - 90) * Math.PI / 180;
            ctx.save();
            ctx.translate(stageApi.x, stageApi.y);
            ctx.rotate(rad);
            ctx.fillStyle = stageApi.color;
            ctx.beginPath();
            ctx.moveTo(0, -8);
            ctx.lineTo(6, 6);
            ctx.lineTo(-6, 6);
            ctx.closePath();
            ctx.fill();
            ctx.restore();
        }

        function stageForward(dist) {
            const ctx = getStageCtx();
            if (!ctx) return;
            const rad = (stageApi.angle - 90) * Math.PI / 180;
            const nx = stageApi.x + Math.cos(rad) * dist;
            const ny = stageApi.y + Math.sin(rad) * dist;
            if (stageApi.pen) {
                ctx.strokeStyle = stageApi.color;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(stageApi.x, stageApi.y);
                ctx.lineTo(nx, ny);
                ctx.stroke();
            }
            stageApi.x = nx;
            stageApi.y = ny;
            drawTurtleCursor();
        }

        function stageTurn(deg) {
            stageApi.angle = (stageApi.angle + deg) % 360;
            // redraw cursor only — leave trails
            const c = document.getElementById('stageCanvas');
            const ctx = getStageCtx();
            // soft redraw cursor by not clearing trails
            drawTurtleCursor();
        }

        function stageGoto(x, y) {
            const ctx = getStageCtx();
            if (!ctx) return;
            // canvas y: invert so math y-up feels natural relative center
            const c = document.getElementById('stageCanvas');
            const cx = c.width / 2 + x;
            const cy = c.height / 2 - y;
            if (stageApi.pen) {
                ctx.strokeStyle = stageApi.color;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(stageApi.x, stageApi.y);
                ctx.lineTo(cx, cy);
                ctx.stroke();
            }
            stageApi.x = cx;
            stageApi.y = cy;
            drawTurtleCursor();
        }

        function stagePlot(values) {
            const ctx = getStageCtx();
            const c = document.getElementById('stageCanvas');
            if (!ctx || !c || !values || !values.length) return;
            const nums = values.map(Number).filter(function(n) { return !isNaN(n); });
            if (!nums.length) return;
            const min = Math.min.apply(null, nums);
            const max = Math.max.apply(null, nums);
            const span = Math.max(1e-9, max - min);
            ctx.strokeStyle = stageApi.color;
            ctx.lineWidth = 2;
            ctx.beginPath();
            nums.forEach(function(v, i) {
                const x = (i / Math.max(1, nums.length - 1)) * (c.width - 20) + 10;
                const y = c.height - 15 - ((v - min) / span) * (c.height - 30);
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            });
            ctx.stroke();
        }

        function stageText(text) {
            const ctx = getStageCtx();
            if (!ctx) return;
            ctx.fillStyle = stageApi.color;
            ctx.font = '14px Inter, sans-serif';
            ctx.fillText(String(text), stageApi.x, stageApi.y);
        }

        function toggleStagePanel() {
            const p = document.getElementById('stagePanel');
            if (!p) return;
            p.classList.toggle('visible');
            if (p.classList.contains('visible')) {
                clearStage();
                showToast('Stage ready — use Stage blocks or pymason_stage in free Python');
            }
        }

        // Bridge for Python / free code
        window.pymason_stage = {
            clear: clearStage,
            forward: stageForward,
            turn: stageTurn,
            left: function(d) { stageTurn(-d); },
            right: function(d) { stageTurn(d); },
            goto: stageGoto,
            pen: function(down) { stageApi.pen = !!down; },
            color: function(c) { stageApi.color = c || '#FF7A26'; },
            plot: stagePlot,
            text: stageText,
        };

        function buildStagePrelude() {
            return `
import js
def _stage():
    return js.pymason_stage
class turtle:
    @staticmethod
    def forward(d): _stage().forward(float(d))
    @staticmethod
    def fd(d): turtle.forward(d)
    @staticmethod
    def right(d): _stage().right(float(d))
    @staticmethod
    def left(d): _stage().left(float(d))
    @staticmethod
    def goto(x,y): _stage().goto(float(x), float(y))
    @staticmethod
    def pendown(): _stage().pen(True)
    @staticmethod
    def penup(): _stage().pen(False)
    @staticmethod
    def pencolor(c): _stage().color(str(c))
    @staticmethod
    def clear(): _stage().clear()
    @staticmethod
    def write(t): _stage().text(str(t))
def plot(values):
    _stage().plot(list(values))
def stage_clear():
    _stage().clear()
`;
        }

        // Stage blocks
        (function registerStageBlocks() {
            function stmt(init, gen) {
                Blockly.Blocks[init.type] = {
                    init: function() {
                        init.build(this);
                        this.setPreviousStatement(true, null);
                        this.setNextStatement(true, null);
                        this.setColour('#C45A18');
                    }
                };
                python.pythonGenerator.forBlock[init.type] = gen;
            }
            Blockly.Blocks['py_stage_clear'] = {
                init: function() {
                    this.appendDummyInput().appendField('stage clear');
                    this.setPreviousStatement(true, null);
                    this.setNextStatement(true, null);
                    this.setColour('#C45A18');
                    this.setTooltip('Clear the graphics stage');
                }
            };
            python.pythonGenerator.forBlock['py_stage_clear'] = function() {
                return 'stage_clear()\n';
            };
            Blockly.Blocks['py_turtle_forward'] = {
                init: function() {
                    this.appendValueInput('DIST').setCheck('Number').appendField('turtle forward');
                    this.setPreviousStatement(true, null);
                    this.setNextStatement(true, null);
                    this.setColour('#C45A18');
                }
            };
            python.pythonGenerator.forBlock['py_turtle_forward'] = function(block) {
                const d = python.pythonGenerator.valueToCode(block, 'DIST', python.Order.NONE) || '0';
                return 'turtle.forward(' + d + ')\n';
            };
            Blockly.Blocks['py_turtle_turn'] = {
                init: function() {
                    this.appendValueInput('DEG').setCheck('Number').appendField('turtle turn °');
                    this.setPreviousStatement(true, null);
                    this.setNextStatement(true, null);
                    this.setColour('#C45A18');
                }
            };
            python.pythonGenerator.forBlock['py_turtle_turn'] = function(block) {
                const d = python.pythonGenerator.valueToCode(block, 'DEG', python.Order.NONE) || '0';
                return 'turtle.right(' + d + ')\n';
            };
            Blockly.Blocks['py_turtle_goto'] = {
                init: function() {
                    this.appendValueInput('X').setCheck('Number').appendField('turtle goto x');
                    this.appendValueInput('Y').setCheck('Number').appendField('y');
                    this.setPreviousStatement(true, null);
                    this.setNextStatement(true, null);
                    this.setColour('#C45A18');
                }
            };
            python.pythonGenerator.forBlock['py_turtle_goto'] = function(block) {
                const x = python.pythonGenerator.valueToCode(block, 'X', python.Order.NONE) || '0';
                const y = python.pythonGenerator.valueToCode(block, 'Y', python.Order.NONE) || '0';
                return 'turtle.goto(' + x + ', ' + y + ')\n';
            };
            Blockly.Blocks['py_turtle_pen'] = {
                init: function() {
                    this.appendDummyInput()
                        .appendField('pen')
                        .appendField(new Blockly.FieldDropdown([['down','down'],['up','up']]), 'MODE');
                    this.setPreviousStatement(true, null);
                    this.setNextStatement(true, null);
                    this.setColour('#C45A18');
                }
            };
            python.pythonGenerator.forBlock['py_turtle_pen'] = function(block) {
                const m = block.getFieldValue('MODE');
                return m === 'up' ? 'turtle.penup()\n' : 'turtle.pendown()\n';
            };
            Blockly.Blocks['py_turtle_color'] = {
                init: function() {
                    this.appendDummyInput()
                        .appendField('pen color')
                        .appendField(new Blockly.FieldTextInput('#FF7A26'), 'COLOR');
                    this.setPreviousStatement(true, null);
                    this.setNextStatement(true, null);
                    this.setColour('#C45A18');
                }
            };
            python.pythonGenerator.forBlock['py_turtle_color'] = function(block) {
                const c = (block.getFieldValue('COLOR') || '#FF7A26').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
                return "turtle.pencolor('" + c + "')\n";
            };
            Blockly.Blocks['py_plot_list'] = {
                init: function() {
                    this.appendValueInput('LIST').appendField('plot list');
                    this.setPreviousStatement(true, null);
                    this.setNextStatement(true, null);
                    this.setColour('#C45A18');
                    this.setTooltip('Plot a list of numbers on the stage');
                }
            };
            python.pythonGenerator.forBlock['py_plot_list'] = function(block) {
                const L = python.pythonGenerator.valueToCode(block, 'LIST', python.Order.NONE) || '[]';
                return 'plot(' + L + ')\n';
            };
            Blockly.Blocks['py_stage_text'] = {
                init: function() {
                    this.appendValueInput('TEXT').appendField('stage text');
                    this.setPreviousStatement(true, null);
                    this.setNextStatement(true, null);
                    this.setColour('#C45A18');
                }
            };
            python.pythonGenerator.forBlock['py_stage_text'] = function(block) {
                const t = python.pythonGenerator.valueToCode(block, 'TEXT', python.Order.NONE) || "''";
                return 'turtle.write(' + t + ')\n';
            };
        })();

        // ── Debugger ─────────────────────────────────────────────────
        function toggleDebugBar() {
            const b = document.getElementById('debugBar');
            if (!b) return;
            b.classList.toggle('visible');
        }

        function setDebugStatus(msg) {
            const el = document.getElementById('debugStatus');
            if (el) el.textContent = msg;
        }

        function clearDebugHighlight() {
            document.querySelectorAll('.blockly-debug-current').forEach(function(el) {
                el.classList.remove('blockly-debug-current');
            });
        }

        function highlightDebugLine(line) {
            clearDebugHighlight();
            highlightBlockForLine(line);
            const blockId = lineBlockMap[line];
            if (blockId) {
                const block = workspace.getBlockById(blockId);
                if (block && block.pathObject && block.pathObject.svgRoot) {
                    block.pathObject.svgRoot.classList.add('blockly-debug-current');
                }
            }
            document.querySelectorAll('.code-line-highlight').forEach(function(el) {
                el.classList.remove('code-line-highlight');
            });
            const lineEl = codeOutput.querySelector('[data-line="' + line + '"]');
            if (lineEl) {
                lineEl.classList.add('code-line-highlight');
                lineEl.scrollIntoView({ block: 'nearest' });
            }
            setDebugStatus('Paused at line ' + line + (blockId ? ' · block ' + blockId.slice(0, 8) : ''));
        }

        function buildDebugWrapper(userCode, breakpoints) {
            const bps = Array.from(breakpoints || lineBreakpoints).filter(function(n) { return n > 0; });
            const bpPy = '[' + bps.join(', ') + ']';
            const indented = userCode.split('\n').map(function(l) { return '    ' + l; }).join('\n');
            return buildStagePrelude() + `
import sys, json
_pymason_bps = set(${'__BP__'})
_pymason_debug_step = {'mode': 'run'}

def _pymason_trace(frame, event, arg):
    if event != 'line':
        return _pymason_trace
    fn = frame.f_code.co_filename or ''
    if '<exec>' not in fn and fn != '<string>':
        return _pymason_trace
    line = int(frame.f_lineno)
    try:
        import js
        locs = {}
        for k, v in list(frame.f_locals.items()):
            if str(k).startswith('_'):
                continue
            try:
                locs[str(k)] = repr(v)[:140]
            except Exception:
                locs[str(k)] = '?'
        js._pymasonOnDebugLine(line, json.dumps(locs))
    except Exception:
        pass
    should_pause = (line in _pymason_bps) or (_pymason_debug_step.get('mode') == 'step')
    if should_pause:
        _pymason_debug_step['mode'] = 'wait'
        import js
        while _pymason_debug_step.get('mode') == 'wait':
            js._pymasonDebugWait()
            if _pymason_debug_step.get('mode') == 'stop':
                raise SystemExit('Debug stopped')
        if _pymason_debug_step.get('mode') == 'step':
            pass
    return _pymason_trace

sys.settrace(_pymason_trace)
try:
${'__BODY__'}
finally:
    sys.settrace(None)
`.replace('__BP__', bpPy).replace('__BODY__', indented);
        }

        window._pymasonOnDebugLine = function(line, locsJson) {
            debugState.paused = true;
            debugState.line = line;
            highlightDebugLine(line);
            try {
                showVarInspector(JSON.parse(locsJson || '{}'));
            } catch (e) { /* ok */ }
        };

        window._pymasonDebugWait = function() {
            // Busy-wait is bad on main thread; for worker we'd use Atomics.
            // Main-thread debug: use Atomics.wait if SAB, else short loop with shared flag
            if (debugState.resolveStep) {
                // synchronous wait not possible without blocking — use Atomcs on SAB
            }
            const sab = window._pymasonDebugSab;
            if (sab) {
                const i32 = new Int32Array(sab);
                // 0 = wait, 1 = step, 2 = continue, 3 = stop
                Atomics.store(i32, 0, 0);
                Atomics.wait(i32, 0, 0);
                const cmd = Atomics.load(i32, 0);
                try {
                    // sync into python dict via pyodide — handled differently per path
                    if (window._pymasonDebugCmdHandler) window._pymasonDebugCmdHandler(cmd);
                } catch (e) { /* ok */ }
            }
        };

        function debugSignal(cmd) {
            // 1 step, 2 cont, 3 stop
            const sab = window._pymasonDebugSab;
            if (sab) {
                const i32 = new Int32Array(sab);
                Atomics.store(i32, 0, cmd);
                Atomics.notify(i32, 0);
            }
            if (window._pyodideDebugGlobals) {
                try {
                    const mode = cmd === 1 ? 'step' : cmd === 2 ? 'run' : cmd === 3 ? 'stop' : 'run';
                    window._pyodideDebugGlobals.get('_pymason_debug_step').set('mode', mode === 'run' && cmd === 2 ? 'run' : mode);
                    if (cmd === 2) window._pyodideDebugGlobals.get('_pymason_debug_step').set('mode', 'run');
                    if (cmd === 1) window._pyodideDebugGlobals.get('_pymason_debug_step').set('mode', 'step');
                    if (cmd === 3) window._pyodideDebugGlobals.get('_pymason_debug_step').set('mode', 'stop');
                } catch (e) { /* ok */ }
            }
            debugState.paused = false;
        }

        function debugStep() { debugSignal(1); setDebugStatus('Step…'); }
        function debugContinue() { debugSignal(2); setDebugStatus('Continue…'); }
        function debugStop() {
            debugSignal(3);
            debugState.active = false;
            clearDebugHighlight();
            setDebugStatus('Stopped');
            stopCode();
        }

        async function debugRun() {
            document.getElementById('debugBar')?.classList.add('visible');
            // Force main-thread for interactive debug control
            const code = getExecutablePython();
            if (!code.trim()) {
                showToast('Nothing to debug');
                return;
            }
            if (outputLang !== 'python') {
                showToast('Debugger is Python-only');
                return;
            }
            showOutput();
            clearOutput();
            if (!document.getElementById('stagePanel')?.classList.contains('visible')) {
                // keep stage optional
            }
            setDebugStatus('Starting debug…');
            debugState.active = true;

            // Prefer fallback pyodide for debug
            if (!pyodideFallback) {
                await loadPyodideFallback_();
            }
            if (!pyodideFallback) {
                showToast('Debug needs main-thread Python');
                return;
            }

            // Create debug SAB
            try {
                window._pymasonDebugSab = new SharedArrayBuffer(8);
            } catch (e) {
                window._pymasonDebugSab = null;
            }

            const wrapped = buildDebugWrapper(code, lineBreakpoints);
            // Patch wait to use cooperative yield via pyodide
            // Use polling with time.sleep through pyodide is async — use runPythonAsync with custom wait:

            window._pymasonDebugCmd = 0;
            const waitImpl = `
def _pymason_wait_cmd():
    import time
    import js
    # poll js flag
    while True:
        mode = _pymason_debug_step.get('mode')
        if mode != 'wait':
            return
        # read command from js
        try:
            cmd = int(js._pymasonDebugCmd or 0)
        except Exception:
            cmd = 0
        if cmd == 1:
            js._pymasonDebugCmd = 0
            _pymason_debug_step['mode'] = 'step'
            return
        if cmd == 2:
            js._pymasonDebugCmd = 0
            _pymason_debug_step['mode'] = 'run'
            return
        if cmd == 3:
            js._pymasonDebugCmd = 0
            _pymason_debug_step['mode'] = 'stop'
            return
        time.sleep(0.05)
`;
            // Rebuild wrapper using polling wait instead of Atomics
            const bps = Array.from(lineBreakpoints).filter(function(n) { return n > 0; });
            const indented = code.split('\n').map(function(l) { return '    ' + l; }).join('\n');
            const full = buildStagePrelude() + `
import sys, json, time
_pymason_bps = set([${bps.join(', ') || ''}])
_pymason_debug_step = {'mode': 'run'}

def _pymason_wait_cmd():
    import js
    while _pymason_debug_step.get('mode') == 'wait':
        try:
            cmd = int(getattr(js, '_pymasonDebugCmd', 0) or 0)
        except Exception:
            cmd = 0
        if cmd == 1:
            js._pymasonDebugCmd = 0
            _pymason_debug_step['mode'] = 'step'
            return
        if cmd == 2:
            js._pymasonDebugCmd = 0
            _pymason_debug_step['mode'] = 'run'
            return
        if cmd == 3:
            js._pymasonDebugCmd = 0
            _pymason_debug_step['mode'] = 'stop'
            return
        time.sleep(0.04)

def _pymason_trace(frame, event, arg):
    if event != 'line':
        return _pymason_trace
    fn = frame.f_code.co_filename or ''
    if '<exec>' not in fn and fn != '<string>':
        return _pymason_trace
    line = int(frame.f_lineno)
    try:
        import js
        locs = {}
        for k, v in list(frame.f_locals.items()):
            if str(k).startswith('_'):
                continue
            try:
                locs[str(k)] = repr(v)[:140]
            except Exception:
                locs[str(k)] = '?'
        js._pymasonOnDebugLine(line, json.dumps(locs))
    except Exception:
        pass
    should_pause = (line in _pymason_bps) or (_pymason_debug_step.get('mode') == 'step')
    if should_pause:
        _pymason_debug_step['mode'] = 'wait'
        _pymason_wait_cmd()
        if _pymason_debug_step.get('mode') == 'stop':
            raise SystemExit('Debug stopped')
    return _pymason_trace

sys.settrace(_pymason_trace)
try:
${indented}
finally:
    sys.settrace(None)
`;

            // Redefine signals for polling mode
            debugStep = function() {
                window._pymasonDebugCmd = 1;
                setDebugStatus('Step…');
            };
            debugContinue = function() {
                window._pymasonDebugCmd = 2;
                setDebugStatus('Continue…');
            };
            debugStop = function() {
                window._pymasonDebugCmd = 3;
                debugState.active = false;
                clearDebugHighlight();
                setDebugStatus('Stopped');
                executionAborted = true;
            };

            btnRun.style.display = 'none';
            btnStop.style.display = '';
            executionAborted = false;
            const start = performance.now();
            try {
                // First line pause if any bp, else run; enable step-mode from start if no bps
                if (!bps.length) {
                    // start in step mode for first line
                    // inject initial step by setting mode after first line via bps empty → user Cont
                }
                await pyodideFallback.runPythonAsync(full);
                appendOutput('\n— Debug finished in ' + ((performance.now() - start) / 1000).toFixed(2) + 's —\n');
                setDebugStatus('Finished');
            } catch (err) {
                if (!/Debug stopped|SystemExit/i.test(String(err))) {
                    appendOutputSmart(String(err.message || err), true);
                }
                setDebugStatus('Ended');
            }
            clearDebugHighlight();
            debugState.active = false;
            btnRun.style.display = '';
            btnStop.style.display = 'none';
        }

        // ── Patch runCode for free mode + stage prelude ──────────────
        const _v1_runCode = runCode;
        runCode = async function() {
            if (outputLang === 'javascript' || outputLang === 'lua') {
                showToast('Run uses Pyodide (Python). Switch output to Python.');
                return;
            }
            let code = getExecutablePython();
            if (!code.trim()) {
                showToast('Nothing to run — add blocks or write Python.');
                return;
            }
            // Always inject stage helpers
            code = buildStagePrelude() + '\n' + code;
            // Temporarily swap generator path by monkeypatching python workspaceToCode usage:
            // Inline reimplementation of run using free code
            if (!pyodideReady) {
                await loadPyodide_();
                if (!pyodideReady) {
                    showToast('Python engine failed to load.');
                    return;
                }
            }
            clearOutput();
            showOutput();
            // auto-show stage if turtle/plot in code
            if (/turtle\.|plot\(|stage_clear/.test(code)) {
                document.getElementById('stagePanel')?.classList.add('visible');
                clearStage();
            }
            executionAborted = false;
            btnRun.style.display = 'none';
            btnStop.style.display = '';
            const startTime = performance.now();
            let capturedVars = {};

            if (pyWorker) {
                if (sharedInt32) sharedInt32[0] = 0;
                await new Promise(function(resolve) {
                    runResolve = resolve;
                    pyWorker.onmessage = async function(e) {
                        if (executionAborted) {
                            if (e.data.type === 'done' || e.data.type === 'error') {
                                runResolve = null;
                                resolve();
                            }
                            return;
                        }
                        switch (e.data.type) {
                            case 'stdout':
                                appendOutput(e.data.text);
                                break;
                            case 'stderr':
                                appendOutput(e.data.text, true);
                                break;
                            case 'input_request': {
                                const val = await showInlineInput(e.data.prompt || '');
                                if (executionAborted) break;
                                if (useSharedBuffer && sharedInt32) {
                                    const maxChars = sharedInt32.length - 1;
                                    const slice = val.slice(0, maxChars);
                                    for (let i = 0; i < slice.length; i++) sharedInt32[1 + i] = slice.charCodeAt(i);
                                    sharedInt32[0] = slice.length + 1;
                                    Atomics.notify(sharedInt32, 0);
                                }
                                break;
                            }
                            case 'error':
                                if (!executionAborted) {
                                    if (typeof appendOutputSmart === 'function') appendOutputSmart(e.data.text, true);
                                    else appendOutput(e.data.text, true);
                                }
                                runResolve = null;
                                resolve();
                                break;
                            case 'done':
                                capturedVars = parseVarsPayload(e.data.vars);
                                runResolve = null;
                                resolve();
                                break;
                        }
                    };
                    pyWorker.postMessage({ type: 'run', code: code, sharedBuffer: sharedBuffer });
                });
            } else if (pyodideFallback) {
                try {
                    await pyodideFallback.runPythonAsync(code);
                    try {
                        const varsJson = await pyodideFallback.runPythonAsync(`
import json as _json
_skip = {'__builtins__','__name__','__doc__','__package__','__loader__','__spec__','sys','json','_json','_skip','_vars','_k','_v','_s','turtle','plot','stage_clear','_stage'}
_vars = {}
for _k,_v in list(globals().items()):
    if _k in _skip or _k.startswith('_'):
        continue
    try:
        _s = repr(_v)
        if len(_s) > 180: _s = _s[:177]+'...'
        _vars[_k] = _s
    except Exception:
        _vars[_k] = '<unprintable>'
_json.dumps(_vars)
`);
                        capturedVars = parseVarsPayload(varsJson);
                    } catch (ve) { /* ok */ }
                } catch (err) {
                    if (!executionAborted) {
                        const msg = err.message || String(err);
                        if (typeof appendOutputSmart === 'function') appendOutputSmart(msg, true);
                        else appendOutput(msg, true);
                    }
                }
            }

            if (!executionAborted) {
                const elapsed = performance.now() - startTime;
                const timeSpan = document.createElement('span');
                timeSpan.className = 'exec-time';
                timeSpan.textContent = '\n— Finished in ' + (elapsed / 1000).toFixed(2) + 's —\n';
                outputContent.appendChild(timeSpan);
                showVarInspector(capturedVars);
                if (typeof pushRunHistory === 'function') {
                    const full = outputContent.innerText || '';
                    pushRunHistory({
                        ok: !outputContent.querySelector('.error'),
                        ms: elapsed,
                        preview: full.slice(0, 200),
                        full: full,
                    });
                }
            }
            btnRun.style.display = '';
            btnStop.style.display = 'none';
        };

        // ── AI Apply agent ───────────────────────────────────────────
        function extractAiWorkspace(text) {
            if (!text) return null;
            // fenced pymason-json
            let m = text.match(/```(?:pymason-json|pymason|workspace-json)\s*([\s\S]*?)```/i);
            if (!m) m = text.match(/```json\s*([\s\S]*?)```/i);
            if (!m) return null;
            try {
                const obj = JSON.parse(m[1].trim());
                if (obj.blocks || obj.variables || obj.workspace) return obj;
                // raw serialization
                if (obj.languageVersion != null || obj.blocks) return obj;
            } catch (e) { return null; }
            return null;
        }

        function applyWorkspaceState(state) {
            if (!state) return false;
            try {
                // Accept full serialization or {workspace: ser}
                const ser = state.workspace && state.workspace.blocks ? state.workspace : state;
                workspace.clear();
                Blockly.serialization.workspaces.load(ser, workspace);
                updateCode();
                if (typeof ensureToolboxPopulated === 'function') ensureToolboxPopulated();
                showToast('AI workspace applied (undo via Ctrl+Z if available)');
                return true;
            } catch (e) {
                showToast('Apply failed: ' + (e.message || e));
                return false;
            }
        }

        const _v1_addChat = typeof addChatMessage === 'function' ? addChatMessage : null;
        if (_v1_addChat) {
            addChatMessage = function(role, content) {
                _v1_addChat(role, content);
                if (role === 'assistant') {
                    const payload = extractAiWorkspace(content);
                    if (payload) {
                        const msgs = document.getElementById('chatMessages');
                        const last = msgs && msgs.lastElementChild;
                        if (last) {
                            const btn = document.createElement('button');
                            btn.className = 'btn btn-accent chat-apply-btn';
                            btn.textContent = 'Apply to workspace';
                            btn.onclick = function() { applyWorkspaceState(payload); };
                            last.appendChild(btn);
                        }
                    }
                }
            };
        }

        const _v1_buildSystem = typeof buildSystemPrompt === 'function' ? buildSystemPrompt : null;
        if (_v1_buildSystem) {
            buildSystemPrompt = function() {
                let base = _v1_buildSystem();
                base += `

AGENT MODE (critical):
When the user asks you to build, fix, or modify their program, you MUST end your reply with a fenced block:
\`\`\`pymason-json
{Blockly workspace serialization JSON}
\`\`\`
Use Blockly serialization format with top-level "blocks" (and "variables" if needed) compatible with Blockly.serialization.workspaces.load.
Prefer complete valid workspace JSON for the finished program. Explain briefly, then the fence.
If you only advise without changing blocks, omit the fence.`;
                return base;
            };
        }

        // Quick action: Agent build
        window.chatAgentBuild = function() {
            const chat = document.getElementById('chatPanel');
            if (chat && !chat.classList.contains('open')) toggleChat();
            const input = document.getElementById('chatInput');
            if (input) {
                input.value = 'Build or improve my current program. Return a complete pymason-json workspace serialization I can Apply.';
                sendChat();
            }
        };

        // ── Multi-module projects ────────────────────────────────────
        function getProject() {
            try {
                return JSON.parse(localStorage.getItem('pymason_project') || 'null') || {
                    modules: [{ id: 'main', name: 'main', data: null }],
                    active: 'main',
                };
            } catch (e) {
                return { modules: [{ id: 'main', name: 'main', data: null }], active: 'main' };
            }
        }
        function saveProject(p) {
            localStorage.setItem('pymason_project', JSON.stringify(p));
        }

        function persistActiveModule() {
            const p = getProject();
            const m = p.modules.find(function(x) { return x.id === p.active; });
            if (m) {
                m.data = Blockly.serialization.workspaces.save(workspace);
                m.freePython = document.getElementById('codeEditor')?.value || freePythonBuffer || '';
            }
            saveProject(p);
        }

        function renderModuleTabs() {
            const host = document.getElementById('moduleTabs');
            if (!host) return;
            const p = getProject();
            host.innerHTML = p.modules.map(function(m) {
                return '<button type="button" class="module-tab' + (m.id === p.active ? ' active' : '') +
                    '" onclick="switchProjectModule(\'' + m.id + '\')">' + escapeHtml(m.name) + '.py</button>';
            }).join('') +
                '<button type="button" class="module-tab" onclick="addProjectModule()" title="Add module">+</button>' +
                '<button type="button" class="module-tab" onclick="downloadProjectFiles()" title="Download all modules">⬇ all</button>';
        }

        function switchProjectModule(id) {
            persistActiveModule();
            const p = getProject();
            const m = p.modules.find(function(x) { return x.id === id; });
            if (!m) return;
            p.active = id;
            saveProject(p);
            workspace.clear();
            if (m.data) {
                try { Blockly.serialization.workspaces.load(m.data, workspace); } catch (e) { /* ok */ }
            }
            if (m.freePython != null) {
                freePythonBuffer = m.freePython;
                const ed = document.getElementById('codeEditor');
                if (ed) ed.value = m.freePython;
            }
            updateCode();
            renderModuleTabs();
            showToast('Module: ' + m.name + '.py');
        }

        function addProjectModule() {
            const name = prompt('Module name (without .py):', 'utils');
            if (!name) return;
            const id = name.replace(/[^A-Za-z0-9_]/g, '_').toLowerCase() || 'mod';
            const p = getProject();
            if (p.modules.some(function(m) { return m.id === id; })) {
                showToast('Module exists');
                return;
            }
            persistActiveModule();
            p.modules.push({ id: id, name: id, data: null, freePython: '' });
            p.active = id;
            saveProject(p);
            workspace.clear();
            updateCode();
            renderModuleTabs();
        }

        function openProjectModules() {
            renderModuleTabs();
            showToast('Project modules — use tabs under code header');
        }

        function downloadProjectFiles() {
            persistActiveModule();
            const p = getProject();
            // Save current as data first
            p.modules.forEach(function(m) {
                // generate python for each module
            });
            // Snapshot current, walk modules
            const snap = Blockly.serialization.workspaces.save(workspace);
            const freeSnap = document.getElementById('codeEditor')?.value || '';
            const files = [];
            p.modules.forEach(function(m) {
                let py = '';
                if (m.id === p.active) {
                    py = getExecutablePython();
                } else if (m.data) {
                    try {
                        workspace.clear();
                        Blockly.serialization.workspaces.load(m.data, workspace);
                        py = python.pythonGenerator.workspaceToCode(workspace);
                    } catch (e) {
                        py = m.freePython || '';
                    }
                } else {
                    py = m.freePython || '';
                }
                files.push({ name: m.name + '.py', content: formatGeneratedCode ? formatGeneratedCode(py) : py });
            });
            // restore
            workspace.clear();
            try { Blockly.serialization.workspaces.load(snap, workspace); } catch (e) { /* ok */ }
            if (document.getElementById('codeEditor')) document.getElementById('codeEditor').value = freeSnap;
            updateCode();

            // Multi-file download as one project.json + sequential .py
            const bundle = {
                format: 'pymason-project-v1',
                modules: p.modules,
                files: files,
            };
            const blob = new Blob([JSON.stringify(bundle, null, 2)], { type: 'application/json' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'pymason_project.json';
            a.click();
            URL.revokeObjectURL(a.href);
            // Also download each py
            files.forEach(function(f, i) {
                setTimeout(function() {
                    const b = new Blob([f.content || ''], { type: 'text/x-python' });
                    const link = document.createElement('a');
                    link.href = URL.createObjectURL(b);
                    link.download = f.name;
                    link.click();
                    URL.revokeObjectURL(link.href);
                }, 200 * (i + 1));
            });
            showToast('Downloading ' + files.length + ' module(s)');
        }

        // ── Curriculum + autograde ───────────────────────────────────
        const CURRICULUM_PACKS = [
            {
                id: 'foundations',
                title: 'Foundations',
                units: [
                    {
                        id: 'print_once',
                        title: 'Print once',
                        blurb: 'Print any message.',
                        tests: [
                            { id: 'has_print', label: 'Has print block or print()', check: function() {
                                const code = getExecutablePython();
                                return /print\s*\(/.test(code) || workspace.getAllBlocks(false).some(function(b){ return b.type === 'text_print'; });
                            }},
                        ],
                    },
                    {
                        id: 'loop_three',
                        title: 'Loop thrice',
                        blurb: 'Use a loop that can run 3 times.',
                        tests: [
                            { id: 'has_loop', label: 'Has for/while loop', check: function() {
                                return workspace.getAllBlocks(false).some(function(b) {
                                    const t = b.type || '';
                                    return t.indexOf('controls_') === 0 || t.indexOf('py_for') === 0 || t.indexOf('py_while') === 0;
                                }) || /\bfor\b|\bwhile\b/.test(getExecutablePython());
                            }},
                        ],
                    },
                ],
            },
            {
                id: 'data',
                title: 'Data & structures',
                units: [
                    {
                        id: 'list_plot',
                        title: 'List + plot',
                        blurb: 'Create a list and plot it on the Stage.',
                        tests: [
                            { id: 'has_list', label: 'Uses a list', check: function() {
                                return workspace.getAllBlocks(false).some(function(b) {
                                    return (b.type || '').indexOf('lists_') === 0 || (b.type || '').indexOf('py_list') === 0;
                                }) || /\[.*\]/.test(getExecutablePython());
                            }},
                            { id: 'has_plot', label: 'Plots or uses Stage', check: function() {
                                return /plot\s*\(|turtle\./.test(getExecutablePython()) ||
                                    workspace.getAllBlocks(false).some(function(b){ return (b.type || '').indexOf('py_plot') === 0 || (b.type || '').indexOf('py_turtle') === 0; });
                            }},
                        ],
                    },
                ],
            },
        ];

        function openCurriculumHub() {
            closeStudioModal();
            const ov = document.createElement('div');
            ov.className = 'studio-modal-overlay';
            ov.id = 'studioModal';
            ov.onclick = function(e) { if (e.target === ov) closeStudioModal(); };
            let html = '<div class="studio-modal"><h2>Curriculum</h2><p class="muted">Autograded units — build on the workspace, then grade.</p>';
            CURRICULUM_PACKS.forEach(function(pack, pi) {
                html += '<div style="margin:12px 0;"><strong style="color:#FF7A26">' + escapeHtml(pack.title) + '</strong>';
                pack.units.forEach(function(u, ui) {
                    html += '<div class="path-step"><div>' + escapeHtml(u.title) + '</div>';
                    html += '<div class="muted">' + escapeHtml(u.blurb) + '</div>';
                    html += '<button class="btn" style="margin-top:6px" onclick="gradeCurriculumUnit(' + pi + ',' + ui + ')">Autograde</button></div>';
                });
                html += '</div>';
            });
            html += '<div class="row"><button class="btn" onclick="closeStudioModal()">Close</button></div></div>';
            ov.innerHTML = html;
            document.body.appendChild(ov);
        }

        function gradeCurriculumUnit(pi, ui) {
            const unit = CURRICULUM_PACKS[pi].units[ui];
            const results = unit.tests.map(function(t) {
                let ok = false;
                try { ok = !!t.check(); } catch (e) { ok = false; }
                return { label: t.label, ok: ok };
            });
            const passed = results.filter(function(r) { return r.ok; }).length;
            const all = results.length;
            closeStudioModal();
            const ov = document.createElement('div');
            ov.className = 'studio-modal-overlay';
            ov.id = 'studioModal';
            ov.onclick = function(e) { if (e.target === ov) closeStudioModal(); };
            let html = '<div class="studio-modal"><h2>' + escapeHtml(unit.title) + '</h2>';
            html += '<p style="color:#FF7A26;font-weight:600;">' + passed + ' / ' + all + ' checks passed</p>';
            results.forEach(function(r) {
                html += '<div class="path-step' + (r.ok ? ' done' : '') + '">' + (r.ok ? '✓ ' : '○ ') + escapeHtml(r.label) + '</div>';
            });
            if (passed === all) {
                try {
                    const key = 'pymason_curriculum_done';
                    const done = JSON.parse(localStorage.getItem(key) || '[]');
                    if (done.indexOf(unit.id) < 0) {
                        done.push(unit.id);
                        localStorage.setItem(key, JSON.stringify(done));
                    }
                } catch (e) { /* ok */ }
                html += '<p class="muted">Unit complete — logged locally.</p>';
            }
            html += '<div class="row"><button class="btn" onclick="openCurriculumHub()">Back</button>';
            html += '<button class="btn" onclick="closeStudioModal()">Close</button></div></div>';
            ov.innerHTML = html;
            document.body.appendChild(ov);
        }

        // ── Command palette ──────────────────────────────────────────
        function getCommandList() {
            return [
                { id: 'run', label: 'Run program', kbd: 'Ctrl+Enter', run: function() { runCode(); } },
                { id: 'debug', label: 'Debug run', kbd: '', run: function() { debugRun(); } },
                { id: 'fit', label: 'Zoom to fit', kbd: 'Ctrl+0', run: function() { zoomToFitWorkspace(); } },
                { id: 'share', label: 'Copy share link', kbd: 'Ctrl+Shift+L', run: function() { shareWorkspaceLink(); } },
                { id: 'save', label: 'Save workspace', kbd: 'Ctrl+S', run: function() { saveWorkspace(); } },
                { id: 'search', label: 'Search blocks', kbd: 'Ctrl+F', run: function() { openBlockSearch(); } },
                { id: 'live', label: 'Mode: Blocks→Code', kbd: '', run: function() { setCodeMode('live'); } },
                { id: 'free', label: 'Mode: Free Python', kbd: '', run: function() { setCodeMode('free'); } },
                { id: 'stage', label: 'Toggle stage', kbd: '', run: function() { toggleStagePanel(); } },
                { id: 'debugbar', label: 'Toggle debug bar', kbd: '', run: function() { toggleDebugBar(); } },
                { id: 'paths', label: 'Guided paths', kbd: '', run: function() { openGuidedPaths(); } },
                { id: 'curriculum', label: 'Curriculum packs', kbd: '', run: function() { openCurriculumHub(); } },
                { id: 'packages', label: 'Install packages', kbd: '', run: function() { openPackagesUI(); } },
                { id: 'project', label: 'Project modules', kbd: '', run: function() { openProjectModules(); } },
                { id: 'diff', label: 'Diff workspaces', kbd: '', run: function() { openWorkspaceDiff(); } },
                { id: 'map', label: 'Toggle minimap', kbd: '', run: function() { toggleMinimap(); } },
                { id: 'agent', label: 'AI: apply build request', kbd: '', run: function() { chatAgentBuild(); } },
                { id: 'chat', label: 'Toggle AI chat', kbd: '', run: function() { toggleChat(); } },
                { id: 'help', label: 'Help', kbd: 'F1', run: function() { toggleHelp(); } },
                { id: 'download', label: 'Download project files', kbd: '', run: function() { downloadProjectFiles(); } },
                { id: 'bp', label: 'Toggle breakpoint on selection', kbd: '', run: function() { toggleBreakpointOnSelection(); } },
            ];
        }

        function openCommandPalette() {
            closeCommandPalette();
            const ov = document.createElement('div');
            ov.className = 'cmd-palette-overlay';
            ov.id = 'cmdPalette';
            ov.onclick = function(e) { if (e.target === ov) closeCommandPalette(); };
            ov.innerHTML = '<div class="cmd-palette" role="dialog" aria-label="Command palette">' +
                '<input id="cmdPaletteInput" placeholder="Type a command…" autocomplete="off" />' +
                '<div class="cmd-palette-list" id="cmdPaletteList"></div></div>';
            document.body.appendChild(ov);
            const input = document.getElementById('cmdPaletteInput');
            let active = 0;
            let filtered = getCommandList();
            function render() {
                const q = (input.value || '').toLowerCase().trim();
                filtered = getCommandList().filter(function(c) {
                    return !q || c.label.toLowerCase().indexOf(q) >= 0 || c.id.indexOf(q) >= 0;
                });
                active = Math.min(active, Math.max(0, filtered.length - 1));
                document.getElementById('cmdPaletteList').innerHTML = filtered.map(function(c, i) {
                    return '<div class="cmd-item' + (i === active ? ' active' : '') + '" data-i="' + i + '">' +
                        '<span>' + escapeHtml(c.label) + '</span>' +
                        (c.kbd ? '<kbd>' + escapeHtml(c.kbd) + '</kbd>' : '') + '</div>';
                }).join('') || '<div class="cmd-item">No matches</div>';
                document.querySelectorAll('#cmdPaletteList .cmd-item[data-i]').forEach(function(el) {
                    el.onmouseenter = function() { active = parseInt(el.getAttribute('data-i'), 10); render(); };
                    el.onclick = function() { runActive(); };
                });
            }
            function runActive() {
                const c = filtered[active];
                closeCommandPalette();
                if (c && c.run) c.run();
            }
            input.addEventListener('input', function() { active = 0; render(); });
            input.addEventListener('keydown', function(e) {
                if (e.key === 'ArrowDown') { e.preventDefault(); active = Math.min(filtered.length - 1, active + 1); render(); }
                if (e.key === 'ArrowUp') { e.preventDefault(); active = Math.max(0, active - 1); render(); }
                if (e.key === 'Enter') { e.preventDefault(); runActive(); }
                if (e.key === 'Escape') { e.preventDefault(); closeCommandPalette(); }
            });
            render();
            setTimeout(function() { input.focus(); }, 10);
        }

        function closeCommandPalette() {
            document.getElementById('cmdPalette')?.remove();
        }

        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && (e.key === 'k' || e.key === 'K')) {
                e.preventDefault();
                openCommandPalette();
            }
        });

        // ── Init v1 surfaces ─────────────────────────────────────────
        (function initV1() {
            setCodeMode(codeMode === 'free' ? 'free' : 'live');
            renderModuleTabs();
            const ed = document.getElementById('codeEditor');
            if (ed) {
                ed.addEventListener('input', function() {
                    freePythonBuffer = ed.value;
                });
            }
            // Chat quick agent button
            const chatActions = document.querySelector('.chat-quick-actions');
            if (chatActions && !document.getElementById('btnAgentBuild')) {
                const b = document.createElement('button');
                b.id = 'btnAgentBuild';
                b.className = 'chat-quick-btn';
                b.textContent = 'Agent Apply';
                b.title = 'Ask AI to return applyable workspace JSON';
                b.onclick = function() { chatAgentBuild(); };
                chatActions.appendChild(b);
            }
            setTimeout(function() {
                if (typeof ensureToolboxPopulated === 'function') ensureToolboxPopulated();
            }, 50);
        })();

'''

# Insert before VERSION
old_ver = "        const PYMASON_VERSION = '0.5.0';"
if old_ver not in text:
    old_ver = "        const PYMASON_VERSION = '0.5.0';"
if "const PYMASON_VERSION = '0.5.0'" not in text:
    # try any
    import re
    m = re.search(r"const PYMASON_VERSION = '[^']+';", text)
    if not m:
        raise SystemExit("version not found")
    old_ver = m.group(0)

text = text.replace(
    old_ver,
    js + "\n        const PYMASON_VERSION = '1.0.0';",
    1,
)

# Help blurb
old_help_tips = """            <h3>Tips</h3>
            <ul>
                <li>Select a block to highlight its lines in the code panel</li>"""
new_help_tips = """            <h3>v1.0 Competitive Studio</h3>
            <ul>
                <li><strong>Blocks→Code / Free Python</strong> — dual surface; Run uses the active mode</li>
                <li><strong>Debug</strong> — breakpoints on line numbers, Step / Cont / locals</li>
                <li><strong>Stage</strong> — turtle + plot canvas (Stage category)</li>
                <li><strong>Agent Apply</strong> — AI returns pymason-json; one-click apply</li>
                <li><strong>Project</strong> — multi-module tabs + download all</li>
                <li><strong>Curriculum</strong> — autograded units</li>
                <li><kbd>Ctrl+K</kbd> — command palette</li>
            </ul>
            <h3>Tips</h3>
            <ul>
                <li>Select a block to highlight its lines in the code panel</li>"""
if old_help_tips in text:
    text = text.replace(old_help_tips, new_help_tips, 1)

INDEX.write_text(text, encoding="utf-8")
print("Injected v1 competitive pack →", INDEX)
print("bytes", INDEX.stat().st_size)
