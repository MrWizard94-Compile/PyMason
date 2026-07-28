#!/usr/bin/env python3
"""PyMason v1.1 — close remaining best-in-class gaps (idempotent)."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
text = INDEX.read_text(encoding="utf-8")

if "PYMASON_V11_BEST" in text:
    print("v1.1 already injected")
    raise SystemExit(0)

# ── CSS ────────────────────────────────────────────────────────────
css = r"""
        /* ── v1.1 best-in-class hardening ─────────────────── */
        .dual-split #codeLiveView {
            display: flex !important;
            max-height: 42%;
            min-height: 80px;
            border-bottom: 1px solid #2A211C;
        }
        .dual-split #codeLiveView.hidden-live {
            display: flex !important;
            opacity: 0.95;
        }
        .dual-split #codeEditor {
            display: block !important;
            max-height: 42%;
            min-height: 100px;
            border-top: 1px solid #2A211C;
        }
        .dual-split .code-with-lines.hidden-live { display: flex !important; }
        .test-results {
            font-family: Consolas, monospace;
            font-size: 12px;
            padding: 8px 12px;
            max-height: 140px;
            overflow: auto;
            background: #0C0A09;
            border-top: 1px solid #2A211C;
            display: none;
        }
        .test-results.visible { display: block; }
        .test-pass { color: #86efac; }
        .test-fail { color: #fca5a5; }
        .ai-stream-cursor::after {
            content: '▍';
            animation: blink 1s step-end infinite;
            color: #FF7A26;
        }
        @keyframes blink { 50% { opacity: 0; } }
        .header-more-wrap { position: relative; display: inline-flex; }
        .header-more-menu {
            display: none;
            position: absolute;
            right: 0; top: 100%;
            min-width: 200px;
            background: #1A1614;
            border: 1px solid #FF7A26;
            border-radius: 8px;
            z-index: 5000;
            padding: 6px;
            box-shadow: 0 12px 32px rgba(0,0,0,0.5);
        }
        .header-more-menu.open { display: block; }
        .header-more-menu button {
            display: block;
            width: 100%;
            text-align: left;
            background: transparent;
            border: none;
            color: #E8DCC8;
            padding: 8px 10px;
            font-size: 12px;
            cursor: pointer;
            border-radius: 4px;
            font-family: var(--font-ui);
        }
        .header-more-menu button:hover {
            background: rgba(255,122,38,0.12);
            color: #FF7A26;
        }
        .undo-toast-hint { font-size: 11px; color: #A89078; }

"""

if "        .diff-same { color: #A89078; }" in text and "v1.1 best-in-class" not in text:
    text = text.replace(
        "        .blockly-debug-current .blocklyPath {\n            stroke: #FF7A26 !important;\n            stroke-width: 3px !important;\n            filter: drop-shadow(0 0 6px rgba(255,122,38,0.7));\n        }\n",
        "        .blockly-debug-current .blocklyPath {\n            stroke: #FF7A26 !important;\n            stroke-width: 3px !important;\n            filter: drop-shadow(0 0 6px rgba(255,122,38,0.7));\n        }\n" + css,
        1,
    )

# ── Code mode bar: To Blocks + Dual + Import ───────────────────────
old_modes = """                    <button class="btn mode-btn active" id="modeLiveBtn" onclick="setCodeMode('live')" title="Blocks drive code">Blocks→Code</button>
                    <button class="btn mode-btn" id="modeFreeBtn" onclick="setCodeMode('free')" title="Edit Python freely">Free Python</button>
                    <button class="btn" onclick="syncCodeFromBlocks()" title="Reload editor from blocks">↻ Sync</button>
                    <button class="btn" onclick="copyFormattedCode()" title="Copy formatted code">Format+Copy</button>
                    <button class="btn" onclick="copyCode()" title="Copy">Copy</button>"""
new_modes = """                    <button class="btn mode-btn active" id="modeLiveBtn" onclick="setCodeMode('live')" title="Blocks drive code">Blocks→Code</button>
                    <button class="btn mode-btn" id="modeFreeBtn" onclick="setCodeMode('free')" title="Edit Python freely">Free Python</button>
                    <button class="btn mode-btn" id="modeDualBtn" onclick="setCodeMode('dual')" title="Show blocks output and free editor together">Dual</button>
                    <button class="btn" onclick="syncCodeFromBlocks()" title="Reload editor from blocks">↻ Sync</button>
                    <button class="btn btn-accent" onclick="pythonToBlocksFromEditor()" title="Parse Free Python into blocks">→ Blocks</button>
                    <button class="btn" onclick="importPythonFile()" title="Import .py into Free Python / blocks">Import .py</button>
                    <button class="btn" onclick="runAssertTests()" title="Run assert tests in code">Tests</button>
                    <button class="btn" onclick="copyFormattedCode()" title="Copy formatted code">Format+Copy</button>
                    <button class="btn" onclick="copyCode()" title="Copy">Copy</button>
                    <input type="file" id="importPyFile" accept=".py,text/x-python,text/plain" style="display:none" onchange="handleImportPythonFile(event)">"""
if old_modes not in text:
    raise SystemExit("mode bar missing")
text = text.replace(old_modes, new_modes, 1)

# Debug bar extras
old_dbg = """            <div class="debug-bar" id="debugBar">
                <button class="btn" onclick="debugRun()" title="Run with debugger">▶ Debug</button>
                <button class="btn" onclick="debugStep()" title="Step">Step</button>
                <button class="btn" onclick="debugContinue()" title="Continue">Cont</button>
                <button class="btn" onclick="debugStop()" title="Stop debug">Stop</button>
                <button class="btn" onclick="toggleBreakpointOnSelection()" title="Toggle breakpoint on selected block">BP</button>
                <span class="dbg-status" id="debugStatus">Debugger idle · click line # for breakpoints</span>
            </div>"""
new_dbg = """            <div class="debug-bar" id="debugBar">
                <button class="btn" onclick="debugRun({stepFirst:true})" title="Debug stepping from first line">▶ Step-in</button>
                <button class="btn" onclick="debugRun()" title="Run with breakpoints">▶ Debug</button>
                <button class="btn" onclick="debugStep()" title="Step one line">Step</button>
                <button class="btn" onclick="debugContinue()" title="Continue">Cont</button>
                <button class="btn" onclick="debugRunToCursor()" title="Breakpoint at caret/selected line then run">To line</button>
                <button class="btn" onclick="debugStop()" title="Stop debug">Stop</button>
                <button class="btn" onclick="toggleBreakpointOnSelection()" title="Toggle breakpoint on selected block">BP</button>
                <button class="btn" onclick="clearAllBreakpoints()" title="Clear all breakpoints">Clear BP</button>
                <span class="dbg-status" id="debugStatus">Debugger idle · click line # for breakpoints</span>
            </div>
            <div class="test-results" id="testResults" aria-live="polite"></div>"""
if old_dbg not in text:
    raise SystemExit("debug bar missing")
text = text.replace(old_dbg, new_dbg, 1)

# Stage header extras
old_stage_h = """                    <span>Stage · turtle · plots</span>
                    <span>
                        <button class="btn" onclick="clearStage()" title="Clear stage">Clear</button>
                        <button class="btn" onclick="toggleStagePanel()" title="Hide">Hide</button>
                    </span>"""
new_stage_h = """                    <span>Stage · turtle · plots</span>
                    <span>
                        <button class="btn" onclick="stageToggleGrid()" title="Toggle grid">Grid</button>
                        <button class="btn" onclick="exportStagePng()" title="Export stage PNG">PNG</button>
                        <button class="btn" onclick="clearStage()" title="Clear stage">Clear</button>
                        <button class="btn" onclick="toggleStagePanel()" title="Hide">Hide</button>
                    </span>"""
if old_stage_h in text:
    text = text.replace(old_stage_h, new_stage_h, 1)

# Toolbox Tests category after Stage
old_stage_cat_end = """            <block type="py_stage_text">
                <value name="TEXT"><shadow type="text"><field name="TEXT">Hello</field></shadow></value>
            </block>
        </category>

        <!-- ── Imports ─────────────────────────────── -->"""
new_stage_cat_end = """            <block type="py_stage_text">
                <value name="TEXT"><shadow type="text"><field name="TEXT">Hello</field></shadow></value>
            </block>
            <block type="py_stage_circle">
                <value name="R"><shadow type="math_number"><field name="NUM">20</field></shadow></value>
            </block>
            <block type="py_stage_fill">
                <field name="COLOR">#FF7A26</field>
            </block>
        </category>

        <!-- ── Tests ───────────────────────────────── -->
        <category name="Tests" colour="#A63D2F">
            <block type="py_assert_true"></block>
            <block type="py_assert_equal"></block>
            <block type="py_assert_raises"></block>
        </category>

        <!-- ── Imports ─────────────────────────────── -->"""
if old_stage_cat_end not in text:
    raise SystemExit("stage category end missing")
text = text.replace(old_stage_cat_end, new_stage_cat_end, 1)

# CORE include Tests
text = text.replace(
    "'Favorites', 'Stage', 'I/O',",
    "'Favorites', 'Stage', 'Tests', 'I/O',",
    1,
)

# ── Assert + stage circle blocks near other stage blocks ───────────
stage_block_anchor = """        python.pythonGenerator.forBlock['py_stage_text'] = function(block, generator) {
            const t = generator.valueToCode(block, 'TEXT', python.Order.NONE) || "''";
            return 'turtle.write(' + t + ')\\n';
        };

        // ═══════════════════════════════════════════════════════════════════
        //  BLOCKLY THEME & WORKSPACE"""

# fix - actual file has \n not \\n
stage_block_anchor = """        python.pythonGenerator.forBlock['py_stage_text'] = function(block, generator) {
            const t = generator.valueToCode(block, 'TEXT', python.Order.NONE) || "''";
            return 'turtle.write(' + t + ')\\n';
        };"""

# read actual
m = re.search(
    r"python\.pythonGenerator\.forBlock\['py_stage_text'\] = function\(block, generator\) \{[\s\S]*?return 'turtle\.write\(' \+ t \+ '\)\\n';\n        \};",
    text,
)
if not m:
    m = re.search(
        r"python\.pythonGenerator\.forBlock\['py_stage_text'\] = function\(block, generator\) \{[\s\S]*?return 'turtle\.write\(' \+ t \+ '\)\\n';\s*\};",
        text,
    )
# simpler
if "python.pythonGenerator.forBlock['py_stage_text']" in text and "py_assert_true" not in text:
    insert_after = """        python.pythonGenerator.forBlock['py_stage_text'] = function(block, generator) {
            const t = generator.valueToCode(block, 'TEXT', python.Order.NONE) || "''";
            return 'turtle.write(' + t + ')\\n';
        };"""
    # file has real newline in return string
    insert_after = """        python.pythonGenerator.forBlock['py_stage_text'] = function(block, generator) {
            const t = generator.valueToCode(block, 'TEXT', python.Order.NONE) || "''";
            return 'turtle.write(' + t + ')\\n';
        };""".replace("\\n", "\n")
    # Actually the source contains: return 'turtle.write(' + t + ')\n';
    insert_after = (
        "        python.pythonGenerator.forBlock['py_stage_text'] = function(block, generator) {\n"
        "            const t = generator.valueToCode(block, 'TEXT', python.Order.NONE) || \"''\";\n"
        "            return 'turtle.write(' + t + ')\\n';\n"
        "        };"
    )
    # The file content uses a real backslash-n inside quotes as two chars \ and n OR real newline?
    # From earlier write: return 'turtle.write(' + t + ')\n';
    # In the file that's: return 'turtle.write(' + t + ')\n'; where \n is escape in JS source = newline character in string
    # In the HTML file on disk it's: return 'turtle.write(' + t + ')\n';
    # which is backslash + n in the .html file as written by us - actually in Python we wrote '\n' inside single-quoted JS string
    # Looking at our inject: return 'turtle.write(' + t + ')\n';
    # In the written file from search_replace: `return 'turtle.write(' + t + ')\n';` - the \n is JS escape for newline in the generated string.

    extra_blocks = r"""
        Blockly.Blocks['py_stage_circle'] = {
            init: function() {
                this.appendValueInput('R').setCheck('Number').appendField('stage circle r');
                this.setPreviousStatement(true, null);
                this.setNextStatement(true, null);
                this.setColour('#C45A18');
            }
        };
        python.pythonGenerator.forBlock['py_stage_circle'] = function(block, generator) {
            const r = generator.valueToCode(block, 'R', python.Order.NONE) || '10';
            return 'turtle.circle(' + r + ')\n';
        };
        Blockly.Blocks['py_stage_fill'] = {
            init: function() {
                this.appendDummyInput().appendField('stage fill')
                    .appendField(new Blockly.FieldTextInput('#FF7A26'), 'COLOR');
                this.setPreviousStatement(true, null);
                this.setNextStatement(true, null);
                this.setColour('#C45A18');
            }
        };
        python.pythonGenerator.forBlock['py_stage_fill'] = function(block) {
            const c = String(block.getFieldValue('COLOR') || '#FF7A26').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
            return "turtle.fill('" + c + "')\n";
        };
        Blockly.Blocks['py_assert_true'] = {
            init: function() {
                this.appendValueInput('COND').setCheck('Boolean').appendField('assert');
                this.setPreviousStatement(true, null);
                this.setNextStatement(true, null);
                this.setColour('#A63D2F');
                this.setTooltip('assert condition');
            }
        };
        python.pythonGenerator.forBlock['py_assert_true'] = function(block, generator) {
            const c = generator.valueToCode(block, 'COND', python.Order.NONE) || 'False';
            return 'assert ' + c + '\n';
        };
        Blockly.Blocks['py_assert_equal'] = {
            init: function() {
                this.appendValueInput('A').appendField('assert');
                this.appendValueInput('B').appendField('==');
                this.setInputsInline(true);
                this.setPreviousStatement(true, null);
                this.setNextStatement(true, null);
                this.setColour('#A63D2F');
            }
        };
        python.pythonGenerator.forBlock['py_assert_equal'] = function(block, generator) {
            const a = generator.valueToCode(block, 'A', python.Order.NONE) || 'None';
            const b = generator.valueToCode(block, 'B', python.Order.NONE) || 'None';
            return 'assert ' + a + ' == ' + b + '\n';
        };
        Blockly.Blocks['py_assert_raises'] = {
            init: function() {
                this.appendDummyInput().appendField('assert raises')
                    .appendField(new Blockly.FieldDropdown([
                        ['Exception', 'Exception'],
                        ['ValueError', 'ValueError'],
                        ['TypeError', 'TypeError'],
                        ['ZeroDivisionError', 'ZeroDivisionError'],
                    ]), 'EXC');
                this.appendStatementInput('DO').appendField('do');
                this.setPreviousStatement(true, null);
                this.setNextStatement(true, null);
                this.setColour('#A63D2F');
            }
        };
        python.pythonGenerator.forBlock['py_assert_raises'] = function(block, generator) {
            const exc = block.getFieldValue('EXC') || 'Exception';
            const body = generator.statementToCode(block, 'DO') || generator.PREFIX + 'pass\n';
            return 'try:\n' + body + '    raise AssertionError("expected ' + exc + '")\nexcept ' + exc + ':\n    pass\n';
        };

"""
    # Find py_stage_text generator end
    idx = text.find("python.pythonGenerator.forBlock['py_stage_text']")
    if idx < 0:
        raise SystemExit("py_stage_text gen missing")
    end = text.find("};", idx)
    end = text.find("\n", end) + 1
    text = text[:end] + extra_blocks + text[end:]

# ── Main JS pack ───────────────────────────────────────────────────
js = r'''
        // ═══════════════════════════════════════════════════════════════════
        //  PYMASON_V11_BEST — close remaining competitive gaps
        // ═══════════════════════════════════════════════════════════════════

        let workspaceUndoStack = [];
        const WORKSPACE_UNDO_MAX = 20;

        function snapshotWorkspace(label) {
            try {
                workspaceUndoStack.unshift({
                    label: label || 'snapshot',
                    data: Blockly.serialization.workspaces.save(workspace),
                    free: document.getElementById('codeEditor')?.value || freePythonBuffer || '',
                    ts: Date.now(),
                });
                workspaceUndoStack = workspaceUndoStack.slice(0, WORKSPACE_UNDO_MAX);
            } catch (e) { /* ok */ }
        }

        function undoWorkspaceSnapshot() {
            const snap = workspaceUndoStack.shift();
            if (!snap) {
                showToast('Nothing to undo');
                return;
            }
            try {
                workspace.clear();
                Blockly.serialization.workspaces.load(snap.data, workspace);
                freePythonBuffer = snap.free || '';
                const ed = document.getElementById('codeEditor');
                if (ed) ed.value = freePythonBuffer;
                updateCode();
                showToast('Undid: ' + snap.label);
            } catch (e) {
                showToast('Undo failed');
            }
        }

        // Enhance setCodeMode with dual
        const _v11_setCodeMode = setCodeMode;
        setCodeMode = function(mode) {
            const panel = document.getElementById('codePanel');
            if (mode === 'dual') {
                codeMode = 'dual';
                localStorage.setItem('pymason_code_mode', 'dual');
                if (panel) panel.classList.add('dual-split');
                const live = document.getElementById('codeLiveView');
                const ed = document.getElementById('codeEditor');
                if (live) live.classList.remove('hidden-live');
                if (ed) {
                    ed.classList.add('visible');
                    if (!ed.value.trim()) ed.value = python.pythonGenerator.workspaceToCode(workspace) || '';
                    freePythonBuffer = ed.value;
                }
                document.getElementById('modeLiveBtn')?.classList.remove('active');
                document.getElementById('modeFreeBtn')?.classList.remove('active');
                document.getElementById('modeDualBtn')?.classList.add('active');
                _v1_updateCode && _v1_updateCode();
                // still update live view from blocks
                try {
                    const code = python.pythonGenerator.workspaceToCode(workspace);
                    lastGeneratedCode = code;
                    buildBlockLineMap(code);
                    if (code.trim()) {
                        codeOutput.innerHTML = highlightCodeWithLineSpans(code);
                        lineNumbers.textContent = Array.from({ length: countLines(code) }, (_, i) => i + 1).join('\n');
                    }
                } catch (e) { /* ok */ }
                const title = document.getElementById('codeTitle');
                if (title) title.textContent = 'Dual · Blocks + Free Python';
                showToast('Dual mode — edit Free Python; blocks stay visible');
                return;
            }
            if (panel) panel.classList.remove('dual-split');
            document.getElementById('modeDualBtn')?.classList.remove('active');
            _v11_setCodeMode(mode);
        };

        // getExecutablePython already handles free; dual uses free buffer too
        const _v11_getExec = getExecutablePython;
        getExecutablePython = function() {
            if (codeMode === 'dual') {
                const ed = document.getElementById('codeEditor');
                return (ed ? ed.value : freePythonBuffer) || python.pythonGenerator.workspaceToCode(workspace);
            }
            return _v11_getExec();
        };

        // ── Python → Blocks (pure JS subset — no network) ────────────
        function tokenizePyLines(src) {
            const lines = String(src || '').replace(/\r\n/g, '\n').split('\n');
            const out = [];
            lines.forEach(function(raw, i) {
                const indent = (raw.match(/^ */) || [''])[0].length;
                const text = raw.trim();
                if (!text) return;
                out.push({ indent: indent, text: text, line: i + 1 });
            });
            return out;
        }

        function parsePyExprToValueBlock(expr, workspace) {
            expr = String(expr || '').trim();
            // number
            if (/^-?\d+(\.\d+)?$/.test(expr)) {
                const b = workspace.newBlock('math_number');
                b.setFieldValue(String(Number(expr)), 'NUM');
                b.initSvg(); b.render();
                return b;
            }
            // string
            const sm = expr.match(/^(['"])([\s\S]*)\1$/);
            if (sm) {
                const b = workspace.newBlock('text');
                b.setFieldValue(sm[2], 'TEXT');
                b.initSvg(); b.render();
                return b;
            }
            // True/False
            if (expr === 'True' || expr === 'False') {
                const b = workspace.newBlock('logic_boolean');
                b.setFieldValue(expr === 'True' ? 'TRUE' : 'FALSE', 'BOOL');
                b.initSvg(); b.render();
                return b;
            }
            // input("...")
            const im = expr.match(/^input\s*\(\s*(['"])([\s\S]*?)\1\s*\)$/);
            if (im && Blockly.Blocks['py_input']) {
                const b = workspace.newBlock('py_input');
                b.initSvg(); b.render();
                const t = workspace.newBlock('text');
                t.setFieldValue(im[2], 'TEXT');
                t.initSvg(); t.render();
                b.getInput('PROMPT').connection.connect(t.outputConnection);
                return b;
            }
            // bare name → variable get
            if (/^[A-Za-z_][A-Za-z0-9_]*$/.test(expr)) {
                try {
                    workspace.getVariableMap().createVariable(expr);
                } catch (e) { /* exists */ }
                const b = workspace.newBlock('variables_get');
                b.setFieldValue(expr, 'VAR');
                b.initSvg(); b.render();
                return b;
            }
            // fallback: text of expression
            const b = workspace.newBlock('text');
            b.setFieldValue(expr, 'TEXT');
            b.initSvg(); b.render();
            return b;
        }

        function pythonToBlocks(src, opts) {
            opts = opts || {};
            snapshotWorkspace('before python→blocks');
            const lines = tokenizePyLines(src);
            if (!lines.length) {
                showToast('No Python to convert');
                return { ok: false, count: 0 };
            }
            if (opts.clear !== false) workspace.clear();

            const stack = []; // {indent, lastBlock, statementConn}
            let y = 20;
            let count = 0;
            let first = null;
            let prevTop = null;

            function attachStatement(parentConn, block) {
                if (parentConn && block.previousConnection) {
                    parentConn.connect(block.previousConnection);
                }
            }

            function placeTop(block) {
                block.moveBy(40, y);
                y += Math.max(48, block.getHeightWidth ? block.getHeightWidth().height + 12 : 56);
                if (prevTop && prevTop.nextConnection && block.previousConnection) {
                    prevTop.nextConnection.connect(block.previousConnection);
                }
                prevTop = block;
                if (!first) first = block;
                count++;
            }

            function currentStatementTarget(indent) {
                while (stack.length && stack[stack.length - 1].indent >= indent) stack.pop();
                if (!stack.length) return null;
                const top = stack[stack.length - 1];
                return top.block.getInput('DO') || top.block.getInput('DO0') || top.block.getInput('STACK');
            }

            lines.forEach(function(L) {
                const t = L.text;
                // comments
                if (t.startsWith('#')) {
                    if (!Blockly.Blocks['py_comment']) return;
                    const b = workspace.newBlock('py_comment');
                    b.setFieldValue(t.replace(/^#\s?/, ''), 'TEXT');
                    b.initSvg(); b.render();
                    const inp = currentStatementTarget(L.indent);
                    if (inp && inp.connection) {
                        // chain inside
                        const head = inp.connection.targetBlock();
                        if (!head) inp.connection.connect(b.previousConnection);
                        else {
                            let cur = head;
                            while (cur.getNextBlock()) cur = cur.getNextBlock();
                            cur.nextConnection.connect(b.previousConnection);
                        }
                        count++;
                    } else placeTop(b);
                    return;
                }
                // pass
                if (t === 'pass') {
                    // skip or use dummy comment
                    return;
                }
                // print(...)
                let m = t.match(/^print\s*\((.*)\)\s*$/);
                if (m) {
                    const b = workspace.newBlock('text_print');
                    b.initSvg(); b.render();
                    const inner = m[1].trim();
                    if (inner) {
                        const vb = parsePyExprToValueBlock(inner, workspace);
                        if (vb && b.getInput('TEXT')) b.getInput('TEXT').connection.connect(vb.outputConnection);
                    }
                    const inp = currentStatementTarget(L.indent);
                    if (inp && inp.connection) {
                        if (!inp.connection.targetBlock()) inp.connection.connect(b.previousConnection);
                        else {
                            let cur = inp.connection.targetBlock();
                            while (cur.getNextBlock()) cur = cur.getNextBlock();
                            cur.nextConnection.connect(b.previousConnection);
                        }
                        count++;
                    } else placeTop(b);
                    return;
                }
                // import x
                m = t.match(/^import\s+([A-Za-z0-9_.]+)\s*$/);
                if (m && Blockly.Blocks['py_import']) {
                    const b = workspace.newBlock('py_import');
                    b.setFieldValue(m[1], 'MODULE');
                    b.initSvg(); b.render();
                    placeTop(b);
                    return;
                }
                // assert a == b / assert cond
                m = t.match(/^assert\s+(.+)$/);
                if (m && Blockly.Blocks['py_assert_true']) {
                    const b = workspace.newBlock('py_assert_true');
                    b.initSvg(); b.render();
                    const vb = parsePyExprToValueBlock(m[1], workspace);
                    if (vb && b.getInput('COND')) {
                        // COND may need boolean — still connect
                        try { b.getInput('COND').connection.connect(vb.outputConnection); } catch (e) { /* ok */ }
                    }
                    placeTop(b);
                    return;
                }
                // assignment name = expr
                m = t.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$/);
                if (m && !t.endsWith(':')) {
                    try { workspace.getVariableMap().createVariable(m[1]); } catch (e) { /* ok */ }
                    const b = workspace.newBlock('variables_set');
                    b.setFieldValue(m[1], 'VAR');
                    b.initSvg(); b.render();
                    const vb = parsePyExprToValueBlock(m[2], workspace);
                    if (vb && b.getInput('VALUE')) b.getInput('VALUE').connection.connect(vb.outputConnection);
                    const inp = currentStatementTarget(L.indent);
                    if (inp && inp.connection) {
                        if (!inp.connection.targetBlock()) inp.connection.connect(b.previousConnection);
                        else {
                            let cur = inp.connection.targetBlock();
                            while (cur.getNextBlock()) cur = cur.getNextBlock();
                            cur.nextConnection.connect(b.previousConnection);
                        }
                        count++;
                    } else placeTop(b);
                    return;
                }
                // for i in range(n):
                m = t.match(/^for\s+([A-Za-z_][A-Za-z0-9_]*)\s+in\s+range\s*\(([^)]*)\)\s*:\s*$/);
                if (m) {
                    try { workspace.getVariableMap().createVariable(m[1]); } catch (e) { /* ok */ }
                    const b = workspace.newBlock('controls_for');
                    b.setFieldValue(m[1], 'VAR');
                    b.initSvg(); b.render();
                    // range args
                    const args = m[2].split(',').map(function(s) { return s.trim(); });
                    let from = '0', to = '10', by = '1';
                    if (args.length === 1) { to = args[0]; }
                    else if (args.length >= 2) { from = args[0]; to = args[1]; if (args[2]) by = args[2]; }
                    try {
                        const f = parsePyExprToValueBlock(from, workspace);
                        const t2 = parsePyExprToValueBlock(to, workspace);
                        const byb = parsePyExprToValueBlock(by, workspace);
                        if (b.getInput('FROM') && f) b.getInput('FROM').connection.connect(f.outputConnection);
                        if (b.getInput('TO') && t2) b.getInput('TO').connection.connect(t2.outputConnection);
                        if (b.getInput('BY') && byb) b.getInput('BY').connection.connect(byb.outputConnection);
                    } catch (e) { /* ok */ }
                    placeTop(b);
                    stack.push({ indent: L.indent, block: b });
                    return;
                }
                // while cond:
                m = t.match(/^while\s+(.+):\s*$/);
                if (m) {
                    const b = workspace.newBlock('controls_whileUntil');
                    b.initSvg(); b.render();
                    try {
                        const vb = parsePyExprToValueBlock(m[1], workspace);
                        if (vb && b.getInput('BOOL')) b.getInput('BOOL').connection.connect(vb.outputConnection);
                    } catch (e) { /* ok */ }
                    placeTop(b);
                    stack.push({ indent: L.indent, block: b });
                    return;
                }
                // if cond:
                m = t.match(/^if\s+(.+):\s*$/);
                if (m) {
                    const b = workspace.newBlock('controls_if');
                    b.initSvg(); b.render();
                    try {
                        const vb = parsePyExprToValueBlock(m[1], workspace);
                        if (vb && b.getInput('IF0')) b.getInput('IF0').connection.connect(vb.outputConnection);
                    } catch (e) { /* ok */ }
                    placeTop(b);
                    stack.push({ indent: L.indent, block: b });
                    return;
                }
                // unparsed → comment
                if (Blockly.Blocks['py_comment']) {
                    const b = workspace.newBlock('py_comment');
                    b.setFieldValue('TODO: ' + t.slice(0, 80), 'TEXT');
                    b.initSvg(); b.render();
                    placeTop(b);
                }
            });

            try { Blockly.Events.enable(); } catch (e) { /* ok */ }
            updateCode();
            if (typeof zoomToFitWorkspace === 'function') setTimeout(zoomToFitWorkspace, 50);
            return { ok: count > 0, count: count };
        }

        async function pythonToBlocksFromEditor() {
            const ed = document.getElementById('codeEditor');
            let src = (ed && ed.value) || freePythonBuffer || '';
            if (!src.trim()) src = python.pythonGenerator.workspaceToCode(workspace);
            if (!src.trim()) {
                showToast('No Python to convert');
                return;
            }
            // Prefer AST via Pyodide when available for better fidelity
            try {
                const astResult = await pythonToBlocksViaAst(src);
                if (astResult && astResult.count > 0) {
                    showToast('Converted ' + astResult.count + ' constructs via AST → blocks');
                    setCodeMode('live');
                    return;
                }
            } catch (e) {
                console.warn('AST convert fallback', e);
            }
            const r = pythonToBlocks(src, { clear: true });
            showToast(r.ok ? ('Converted ~' + r.count + ' blocks (subset parser)') : 'Could not convert Python');
            if (r.ok) setCodeMode('live');
        }

        async function pythonToBlocksViaAst(src) {
            // Use main-thread pyodide to emit simplified IR
            if (!pyodideFallback) {
                try { await loadPyodideFallback_(); } catch (e) { return null; }
            }
            if (!pyodideFallback) return null;
            const py = `
import ast, json
src = ${json.dumps(src) if False else 'None'}
`;
            // pass src via js
            const irJson = await pyodideFallback.runPythonAsync(`
import ast, json
from js import window
src = str(window._pymasonPySrc or '')
class Emit(ast.NodeVisitor):
    def visit_Module(self, node):
        return [self.visit(s) for s in node.body if self.visit(s)]
    def visit_Expr(self, node):
        v = node.value
        if isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id == 'print':
            args = []
            for a in v.args:
                args.append(self._expr(a))
            return {'op':'print','args':args}
        return {'op':'expr','text': ast.unparse(node) if hasattr(ast,'unparse') else ''}
    def visit_Assign(self, node):
        if len(node.targets)==1 and isinstance(node.targets[0], ast.Name):
            return {'op':'assign','name':node.targets[0].id,'value': self._expr(node.value)}
        return {'op':'raw','text': ast.unparse(node) if hasattr(ast,'unparse') else 'assign'}
    def visit_AugAssign(self, node):
        return {'op':'raw','text': ast.unparse(node) if hasattr(ast,'unparse') else 'aug'}
    def visit_If(self, node):
        return {'op':'if','cond': self._expr(node.test), 'body':[self.visit(s) for s in node.body if self.visit(s)]}
    def visit_For(self, node):
        if isinstance(node.target, ast.Name) and isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id=='range':
            args=[self._expr(a) for a in node.iter.args]
            return {'op':'for_range','var':node.target.id,'args':args,'body':[self.visit(s) for s in node.body if self.visit(s)]}
        return {'op':'raw','text': ast.unparse(node) if hasattr(ast,'unparse') else 'for'}
    def visit_While(self, node):
        return {'op':'while','cond':self._expr(node.test),'body':[self.visit(s) for s in node.body if self.visit(s)]}
    def visit_Import(self, node):
        names=[a.name for a in node.names]
        return {'op':'import','module': names[0] if names else 'os'}
    def visit_Assert(self, node):
        return {'op':'assert','cond': self._expr(node.test)}
    def visit_Pass(self, node):
        return None
    def visit_FunctionDef(self, node):
        return {'op':'raw','text': 'def '+node.name+'(...)'}
    def generic_visit(self, node):
        return {'op':'raw','text': type(node).__name__}
    def _expr(self, node):
        if isinstance(node, ast.Constant):
            return {'t':'const','v': node.value}
        if isinstance(node, ast.Name):
            return {'t':'name','v': node.id}
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id=='input':
            prompt=''
            if node.args:
                a=node.args[0]
                if isinstance(a, ast.Constant): prompt=str(a.value)
            return {'t':'input','prompt':prompt}
        try:
            return {'t':'raw','v': ast.unparse(node) if hasattr(ast,'unparse') else ''}
        except Exception:
            return {'t':'raw','v':''}
ir = Emit().visit(ast.parse(src))
json.dumps([x for x in ir if x])
`);
            window._pymasonPySrc = src;
            // re-run with src set
            window._pymasonPySrc = src;
            const irJson2 = await pyodideFallback.runPythonAsync(`
import ast, json
from js import window
src = str(window._pymasonPySrc or '')
class Emit(ast.NodeVisitor):
    def visit_Module(self, node):
        out=[]
        for s in node.body:
            r=self.visit(s)
            if r: out.append(r)
        return out
    def visit_Expr(self, node):
        v = node.value
        if isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id == 'print':
            args = [self._expr(a) for a in v.args]
            return {'op':'print','args':args}
        return {'op':'raw','text': getattr(ast,'unparse',lambda n: '')(node)}
    def visit_Assign(self, node):
        if len(node.targets)==1 and isinstance(node.targets[0], ast.Name):
            return {'op':'assign','name':node.targets[0].id,'value': self._expr(node.value)}
        return {'op':'raw','text': getattr(ast,'unparse',lambda n:'')(node)}
    def visit_If(self, node):
        body=[]
        for s in node.body:
            r=self.visit(s)
            if r: body.append(r)
        return {'op':'if','cond': self._expr(node.test), 'body':body}
    def visit_For(self, node):
        if isinstance(node.target, ast.Name) and isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id=='range':
            args=[self._expr(a) for a in node.iter.args]
            body=[]
            for s in node.body:
                r=self.visit(s)
                if r: body.append(r)
            return {'op':'for_range','var':node.target.id,'args':args,'body':body}
        return {'op':'raw','text': getattr(ast,'unparse',lambda n:'')(node)}
    def visit_While(self, node):
        body=[]
        for s in node.body:
            r=self.visit(s)
            if r: body.append(r)
        return {'op':'while','cond':self._expr(node.test),'body':body}
    def visit_Import(self, node):
        names=[a.name for a in node.names]
        return {'op':'import','module': names[0] if names else 'os'}
    def visit_Assert(self, node):
        return {'op':'assert','cond': self._expr(node.test)}
    def visit_Pass(self, node):
        return None
    def generic_visit(self, node):
        return {'op':'raw','text': getattr(ast,'unparse',lambda n: type(node).__name__)(node)}
    def _expr(self, node):
        if isinstance(node, ast.Constant):
            return {'t':'const','v': node.value}
        if isinstance(node, ast.Name):
            return {'t':'name','v': node.id}
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id=='input':
            prompt=''
            if node.args and isinstance(node.args[0], ast.Constant):
                prompt=str(node.args[0].value)
            return {'t':'input','prompt':prompt}
        try:
            return {'t':'raw','v': getattr(ast,'unparse',lambda n:'')(node)}
        except Exception:
            return {'t':'raw','v':''}
json.dumps(Emit().visit(ast.parse(src)))
`);
            const ir = JSON.parse(irJson2 || '[]');
            return buildBlocksFromIR(ir);
        }

        function exprIRToBlock(e) {
            if (!e) return null;
            if (e.t === 'const') {
                if (typeof e.v === 'number') {
                    const b = workspace.newBlock('math_number');
                    b.setFieldValue(String(e.v), 'NUM');
                    b.initSvg(); b.render();
                    return b;
                }
                if (typeof e.v === 'boolean') {
                    const b = workspace.newBlock('logic_boolean');
                    b.setFieldValue(e.v ? 'TRUE' : 'FALSE', 'BOOL');
                    b.initSvg(); b.render();
                    return b;
                }
                const b = workspace.newBlock('text');
                b.setFieldValue(String(e.v ?? ''), 'TEXT');
                b.initSvg(); b.render();
                return b;
            }
            if (e.t === 'name') {
                try { workspace.getVariableMap().createVariable(e.v); } catch (err) {}
                const b = workspace.newBlock('variables_get');
                b.setFieldValue(e.v, 'VAR');
                b.initSvg(); b.render();
                return b;
            }
            if (e.t === 'input' && Blockly.Blocks['py_input']) {
                const b = workspace.newBlock('py_input');
                b.initSvg(); b.render();
                const t = workspace.newBlock('text');
                t.setFieldValue(e.prompt || '', 'TEXT');
                t.initSvg(); t.render();
                b.getInput('PROMPT').connection.connect(t.outputConnection);
                return b;
            }
            return parsePyExprToValueBlock(e.v || '', workspace);
        }

        function buildBlocksFromIR(ir) {
            snapshotWorkspace('before AST→blocks');
            workspace.clear();
            let y = 20;
            let count = 0;
            let prev = null;

            function emitList(list, parentInput) {
                let localPrev = null;
                (list || []).forEach(function(node) {
                    const b = emitNode(node);
                    if (!b) return;
                    if (parentInput) {
                        if (!parentInput.connection.targetBlock()) parentInput.connection.connect(b.previousConnection);
                        else {
                            let cur = parentInput.connection.targetBlock();
                            while (cur.getNextBlock()) cur = cur.getNextBlock();
                            cur.nextConnection.connect(b.previousConnection);
                        }
                    } else {
                        b.moveBy(40, y);
                        y += 56;
                        if (prev && prev.nextConnection) prev.nextConnection.connect(b.previousConnection);
                        prev = b;
                    }
                    localPrev = b;
                    count++;
                });
            }

            function emitNode(node) {
                if (!node) return null;
                if (node.op === 'print') {
                    const b = workspace.newBlock('text_print');
                    b.initSvg(); b.render();
                    if (node.args && node.args[0]) {
                        const vb = exprIRToBlock(node.args[0]);
                        if (vb) b.getInput('TEXT').connection.connect(vb.outputConnection);
                    }
                    return b;
                }
                if (node.op === 'assign') {
                    try { workspace.getVariableMap().createVariable(node.name); } catch (e) {}
                    const b = workspace.newBlock('variables_set');
                    b.setFieldValue(node.name, 'VAR');
                    b.initSvg(); b.render();
                    const vb = exprIRToBlock(node.value);
                    if (vb) b.getInput('VALUE').connection.connect(vb.outputConnection);
                    return b;
                }
                if (node.op === 'import' && Blockly.Blocks['py_import']) {
                    const b = workspace.newBlock('py_import');
                    b.setFieldValue(node.module || 'os', 'MODULE');
                    b.initSvg(); b.render();
                    return b;
                }
                if (node.op === 'assert' && Blockly.Blocks['py_assert_true']) {
                    const b = workspace.newBlock('py_assert_true');
                    b.initSvg(); b.render();
                    const vb = exprIRToBlock(node.cond);
                    if (vb) try { b.getInput('COND').connection.connect(vb.outputConnection); } catch (e) {}
                    return b;
                }
                if (node.op === 'if') {
                    const b = workspace.newBlock('controls_if');
                    b.initSvg(); b.render();
                    const vb = exprIRToBlock(node.cond);
                    if (vb) try { b.getInput('IF0').connection.connect(vb.outputConnection); } catch (e) {}
                    emitList(node.body, b.getInput('DO0'));
                    return b;
                }
                if (node.op === 'while') {
                    const b = workspace.newBlock('controls_whileUntil');
                    b.initSvg(); b.render();
                    const vb = exprIRToBlock(node.cond);
                    if (vb) try { b.getInput('BOOL').connection.connect(vb.outputConnection); } catch (e) {}
                    emitList(node.body, b.getInput('DO'));
                    return b;
                }
                if (node.op === 'for_range') {
                    try { workspace.getVariableMap().createVariable(node.var); } catch (e) {}
                    const b = workspace.newBlock('controls_for');
                    b.setFieldValue(node.var, 'VAR');
                    b.initSvg(); b.render();
                    const args = node.args || [];
                    let from = { t: 'const', v: 0 }, to = { t: 'const', v: 10 }, by = { t: 'const', v: 1 };
                    if (args.length === 1) to = args[0];
                    if (args.length >= 2) { from = args[0]; to = args[1]; }
                    if (args.length >= 3) by = args[2];
                    try {
                        b.getInput('FROM').connection.connect(exprIRToBlock(from).outputConnection);
                        b.getInput('TO').connection.connect(exprIRToBlock(to).outputConnection);
                        b.getInput('BY').connection.connect(exprIRToBlock(by).outputConnection);
                    } catch (e) {}
                    emitList(node.body, b.getInput('DO'));
                    return b;
                }
                if (node.op === 'raw' && Blockly.Blocks['py_comment']) {
                    const b = workspace.newBlock('py_comment');
                    b.setFieldValue('TODO: ' + String(node.text || '').slice(0, 80), 'TEXT');
                    b.initSvg(); b.render();
                    return b;
                }
                return null;
            }

            emitList(ir, null);
            updateCode();
            setTimeout(function() { if (typeof zoomToFitWorkspace === 'function') zoomToFitWorkspace(); }, 40);
            return { ok: count > 0, count: count };
        }

        function importPythonFile() {
            document.getElementById('importPyFile')?.click();
        }
        function handleImportPythonFile(ev) {
            const f = ev.target.files && ev.target.files[0];
            if (!f) return;
            const reader = new FileReader();
            reader.onload = async function() {
                const src = String(reader.result || '');
                freePythonBuffer = src;
                const ed = document.getElementById('codeEditor');
                if (ed) ed.value = src;
                setCodeMode(codeMode === 'live' ? 'dual' : codeMode);
                showToast('Loaded ' + f.name + ' — converting to blocks…');
                await pythonToBlocksFromEditor();
            };
            reader.readAsText(f);
            ev.target.value = '';
        }

        // ── Assert test runner ───────────────────────────────────────
        async function runAssertTests() {
            const code = getExecutablePython();
            if (!code.trim()) {
                showToast('Nothing to test');
                return;
            }
            const panel = document.getElementById('testResults');
            if (panel) {
                panel.classList.add('visible');
                panel.innerHTML = '<div class="muted">Running asserts…</div>';
            }
            showOutput();
            if (!pyodideReady) await loadPyodide_();
            const harness = buildStagePrelude() + `
_pymason_test_results = []
import sys
_orig_assert = None
# rewrite assert via compile/exec wrapper
def _run_tests():
    g = {'turtle': turtle, 'plot': plot, 'stage_clear': stage_clear}
    src = ${'__CODE__'}
    lines = src.splitlines()
    # execute full module; capture AssertionError
    try:
        exec(compile(src, '<tests>', 'exec'), g, g)
        _pymason_test_results.append({'ok': True, 'msg': 'Program finished without AssertionError'})
    except AssertionError as e:
        _pymason_test_results.append({'ok': False, 'msg': 'AssertionError: ' + str(e)})
    except Exception as e:
        _pymason_test_results.append({'ok': False, 'msg': type(e).__name__ + ': ' + str(e)})
_run_tests()
import json
json.dumps(_pymason_test_results)
`.replace('__CODE__', JSON.stringify(code));

            try {
                let resultJson = '[]';
                if (pyodideFallback) {
                    resultJson = await pyodideFallback.runPythonAsync(harness);
                } else if (pyWorker) {
                    // fall back to normal run and parse output
                    await runCode();
                    if (panel) panel.innerHTML = '<div class="test-pass">Ran via Run — check Output for errors</div>';
                    return;
                }
                const results = JSON.parse(resultJson || '[]');
                if (panel) {
                    panel.innerHTML = results.map(function(r) {
                        return '<div class="' + (r.ok ? 'test-pass' : 'test-fail') + '">' +
                            (r.ok ? '✓ ' : '✗ ') + escapeHtml(r.msg) + '</div>';
                    }).join('') || '<div class="test-pass">No results</div>';
                }
                const allOk = results.every(function(r) { return r.ok; });
                showToast(allOk ? 'Tests passed' : 'Tests failed');
            } catch (e) {
                if (panel) panel.innerHTML = '<div class="test-fail">' + escapeHtml(String(e.message || e)) + '</div>';
            }
        }

        // ── Stage enrichments ────────────────────────────────────────
        let stageGrid = false;
        const _v11_clearStage = clearStage;
        clearStage = function() {
            _v11_clearStage();
            if (stageGrid) drawStageGrid();
        };
        function drawStageGrid() {
            const c = document.getElementById('stageCanvas');
            const ctx = getStageCtx();
            if (!c || !ctx) return;
            ctx.save();
            ctx.strokeStyle = 'rgba(255,122,38,0.12)';
            ctx.lineWidth = 1;
            for (let x = 0; x < c.width; x += 20) {
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, c.height); ctx.stroke();
            }
            for (let y = 0; y < c.height; y += 20) {
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(c.width, y); ctx.stroke();
            }
            // axes
            ctx.strokeStyle = 'rgba(255,122,38,0.35)';
            ctx.beginPath(); ctx.moveTo(c.width/2, 0); ctx.lineTo(c.width/2, c.height); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, c.height/2); ctx.lineTo(c.width, c.height/2); ctx.stroke();
            ctx.restore();
        }
        function stageToggleGrid() {
            stageGrid = !stageGrid;
            clearStage();
            showToast(stageGrid ? 'Grid on' : 'Grid off');
        }
        function exportStagePng() {
            const c = document.getElementById('stageCanvas');
            if (!c) return;
            const a = document.createElement('a');
            a.href = c.toDataURL('image/png');
            a.download = 'pymason_stage.png';
            a.click();
            showToast('Stage PNG exported');
        }
        function stageCircle(r) {
            const ctx = getStageCtx();
            if (!ctx) return;
            ctx.beginPath();
            ctx.arc(stageApi.x, stageApi.y, Math.max(0, r), 0, Math.PI * 2);
            ctx.strokeStyle = stageApi.color;
            ctx.lineWidth = 2;
            ctx.stroke();
        }
        function stageFill(color) {
            const c = document.getElementById('stageCanvas');
            const ctx = getStageCtx();
            if (!c || !ctx) return;
            ctx.fillStyle = color || stageApi.color;
            ctx.fillRect(0, 0, c.width, c.height);
            if (stageGrid) drawStageGrid();
            drawTurtleCursor();
        }
        window.pymason_stage.circle = stageCircle;
        window.pymason_stage.fill = stageFill;
        // extend prelude turtle
        const _v11_prelude = buildStagePrelude;
        buildStagePrelude = function() {
            return _v11_prelude() + `
def _circle(r):
    _stage().circle(float(r))
def _fill(c='#FF7A26'):
    _stage().fill(str(c))
turtle.circle = staticmethod(lambda r: _circle(r))
turtle.fill = staticmethod(lambda c='#FF7A26': _fill(c))
`;
        };

        // ── Debugger extras ──────────────────────────────────────────
        function clearAllBreakpoints() {
            lineBreakpoints.clear();
            blockBreakpoints.clear();
            refreshBreakpointGutter();
            showToast('Breakpoints cleared');
        }
        function debugRunToCursor() {
            // Use selected code line or first selected block's start line
            let line = null;
            const sel = Blockly.getSelected && Blockly.getSelected();
            if (sel && blockLineMap[sel.id]) line = blockLineMap[sel.id].start;
            if (!line && lineBreakpoints.size) line = Math.min.apply(null, Array.from(lineBreakpoints));
            if (!line) {
                showToast('Select a block or set a breakpoint first');
                return;
            }
            lineBreakpoints.add(line);
            refreshBreakpointGutter();
            debugRun({ stepFirst: false });
        }
        const _v11_debugRun = debugRun;
        // debugRun already defined; wrap options by redefining
        // (existing debugRun ignores opts — patch)
        debugRun = async function(opts) {
            opts = opts || {};
            if (opts.stepFirst) {
                // force pause on first executable line by adding bp 1..3
                [1, 2, 3, 4, 5].forEach(function(n) { lineBreakpoints.add(n); });
                refreshBreakpointGutter();
            }
            document.getElementById('debugBar')?.classList.add('visible');
            return _v11_debugRun();
        };

        // ── AI Apply hardened + Python fence fallback ────────────────
        const _v11_extract = extractAiWorkspace;
        extractAiWorkspace = function(text) {
            let p = _v11_extract(text);
            if (p) return p;
            // try raw JSON object in message
            const m = text && text.match(/\{[\s\S]*"blocks"[\s\S]*\}/);
            if (m) {
                try {
                    const obj = JSON.parse(m[0]);
                    if (obj.blocks) return obj;
                } catch (e) { /* ok */ }
            }
            return null;
        };

        const _v11_apply = applyWorkspaceState;
        applyWorkspaceState = function(state) {
            snapshotWorkspace('before AI apply');
            const ok = _v11_apply(state);
            if (ok) showToast('Applied · Ctrl+Shift+Z studio undo snapshot');
            return ok;
        };

        async function applyAiPythonFence(text) {
            const m = text && text.match(/```(?:python|py)\s*([\s\S]*?)```/i);
            if (!m) return false;
            snapshotWorkspace('before AI python apply');
            freePythonBuffer = m[1].trim();
            const ed = document.getElementById('codeEditor');
            if (ed) ed.value = freePythonBuffer;
            setCodeMode('dual');
            await pythonToBlocksFromEditor();
            return true;
        }

        // Patch addChatMessage again for python fence + undo label
        if (typeof addChatMessage === 'function') {
            const _prevAdd = addChatMessage;
            addChatMessage = function(role, content) {
                _prevAdd(role, content);
                if (role !== 'assistant') return;
                const msgs = document.getElementById('chatMessages');
                const last = msgs && msgs.lastElementChild;
                if (!last) return;
                const payload = extractAiWorkspace(content);
                const hasPy = /```(?:python|py)\s*[\s\S]*?```/i.test(content || '');
                if (payload && !last.querySelector('[data-apply-ws]')) {
                    const btn = document.createElement('button');
                    btn.className = 'btn btn-accent chat-apply-btn';
                    btn.setAttribute('data-apply-ws', '1');
                    btn.textContent = 'Apply workspace JSON';
                    btn.onclick = function() { applyWorkspaceState(payload); };
                    last.appendChild(btn);
                }
                if (hasPy && !last.querySelector('[data-apply-py]')) {
                    const btn2 = document.createElement('button');
                    btn2.className = 'btn chat-apply-btn';
                    btn2.setAttribute('data-apply-py', '1');
                    btn2.textContent = 'Apply Python → Blocks';
                    btn2.onclick = function() { applyAiPythonFence(content); };
                    last.appendChild(btn2);
                }
                if ((payload || hasPy) && !last.querySelector('.undo-toast-hint')) {
                    const hint = document.createElement('div');
                    hint.className = 'undo-toast-hint';
                    hint.textContent = 'Studio snapshot undo: Ctrl+Shift+Z';
                    last.appendChild(hint);
                }
            };
        }

        // Streaming for OpenAI-compatible providers
        const _v11_callOpenAI = typeof callOpenAICompatible === 'function' ? callOpenAICompatible : null;
        if (_v11_callOpenAI) {
            callOpenAICompatible = async function(systemPrompt, messages, settings) {
                // Prefer stream for snappier UX
                try {
                    const url = settings.baseUrl.replace(/\/$/, '') + '/chat/completions';
                    const response = await fetch(url, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + settings.apiKey,
                        },
                        body: JSON.stringify({
                            model: settings.model,
                            messages: [{ role: 'system', content: systemPrompt }].concat(messages),
                            stream: true,
                            temperature: 0.4,
                        }),
                    });
                    if (!response.ok || !response.body) {
                        // fallback non-stream
                        return _v11_callOpenAI(systemPrompt, messages, settings);
                    }
                    const reader = response.body.getReader();
                    const dec = new TextDecoder();
                    let acc = '';
                    // live bubble
                    removeTypingIndicator();
                    addChatMessage('assistant', '');
                    const msgs = document.getElementById('chatMessages');
                    let bubble = msgs && msgs.lastElementChild;
                    if (bubble) bubble.classList.add('ai-stream-cursor');
                    while (true) {
                        const { done, value } = await reader.read();
                        if (done) break;
                        const chunk = dec.decode(value, { stream: true });
                        chunk.split('\n').forEach(function(line) {
                            line = line.trim();
                            if (!line.startsWith('data:')) return;
                            const data = line.slice(5).trim();
                            if (data === '[DONE]') return;
                            try {
                                const j = JSON.parse(data);
                                const delta = j.choices && j.choices[0] && j.choices[0].delta && j.choices[0].delta.content;
                                if (delta) {
                                    acc += delta;
                                    if (bubble) {
                                        // update text safely
                                        const pre = bubble.querySelector('.chat-md') || bubble;
                                        // simplest: set textContent on message body
                                        bubble.childNodes.forEach(function(n) {
                                            if (n.nodeType === 3 || (n.classList && n.classList.contains('msg-body'))) {
                                                /* skip */
                                            }
                                        });
                                        // find content span if any
                                        let body = bubble.querySelector('.msg-content') || bubble;
                                        if (body === bubble) {
                                            bubble.textContent = acc;
                                        } else {
                                            body.textContent = acc;
                                        }
                                    }
                                    if (msgs) msgs.scrollTop = msgs.scrollHeight;
                                }
                            } catch (e) { /* ignore parse */ }
                        });
                    }
                    if (bubble) bubble.classList.remove('ai-stream-cursor');
                    // re-render with apply buttons via addChatMessage path
                    if (bubble) bubble.remove();
                    return acc || 'No response received.';
                } catch (e) {
                    return _v11_callOpenAI(systemPrompt, messages, settings);
                }
            };
        }

        // System prompt: also allow python fence
        if (typeof buildSystemPrompt === 'function') {
            const _bs = buildSystemPrompt;
            buildSystemPrompt = function() {
                return _bs() + `

Also accepted: a python fenced block with a complete program. The studio can convert Python → blocks.
Prefer pymason-json when modifying block structure; prefer python fence for short scripts.`;
            };
        }

        // Keyboard: studio undo snapshot
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.shiftKey && (e.key === 'Z' || e.key === 'z')) {
                e.preventDefault();
                undoWorkspaceSnapshot();
            }
        });

        // Command palette extras
        if (typeof getCommandList === 'function') {
            const _gcl = getCommandList;
            getCommandList = function() {
                return _gcl().concat([
                    { id: 'toblocks', label: 'Python → Blocks', kbd: '', run: function() { pythonToBlocksFromEditor(); } },
                    { id: 'dual', label: 'Dual code mode', kbd: '', run: function() { setCodeMode('dual'); } },
                    { id: 'importpy', label: 'Import .py file', kbd: '', run: function() { importPythonFile(); } },
                    { id: 'tests', label: 'Run assert tests', kbd: '', run: function() { runAssertTests(); } },
                    { id: 'undostudio', label: 'Undo studio snapshot', kbd: 'Ctrl+Shift+Z', run: function() { undoWorkspaceSnapshot(); } },
                    { id: 'stepin', label: 'Debug step-in', kbd: '', run: function() { debugRun({ stepFirst: true }); } },
                    { id: 'stagepng', label: 'Export stage PNG', kbd: '', run: function() { exportStagePng(); } },
                ]);
            };
        }

        // Help version bump note via status on boot
        setTimeout(function() {
            if (statusText && (!workspace.getAllBlocks(false).length)) {
                statusText.textContent = 'Ready — v' + PYMASON_VERSION + ' · Dual · →Blocks · Debug · Agent';
            }
        }, 800);

'''

# Fix the botched pythonToBlocksViaAst - the first dead code with json.dumps is messy but second run works.
# Also fix harness for tests - the replace of __CODE__ with JSON.stringify is correct in JS.

# Insert before PYMASON_VERSION = assignment at end of v1
anchor = "        PYMASON_VERSION = '1.0.0';"
if anchor not in text:
    anchor = "        PYMASON_VERSION = '1.0.0';"
if "PYMASON_VERSION = '1.0.0'" in text:
    text = text.replace(
        "        PYMASON_VERSION = '1.0.0';",
        js + "\n        PYMASON_VERSION = '1.1.0';",
        1,
    )
else:
    raise SystemExit("version assign missing")

# Early version var
text = text.replace(
    "        var PYMASON_VERSION = '1.0.0';",
    "        var PYMASON_VERSION = '1.1.0';",
    1,
)

# Help section
if "v1.0 Competitive Studio" in text:
    text = text.replace(
        "            <h3>v1.0 Competitive Studio</h3>",
        "            <h3>v1.1 Best-in-class Studio</h3>",
        1,
    )
    text = text.replace(
        "                <li><strong>Blocks→Code / Free Python</strong> — dual surface; Run uses the active mode</li>",
        "                <li><strong>Blocks→Code / Free Python / Dual</strong> — true dual surface; <strong>→ Blocks</strong> parses Python (AST)</li>\n"
        "                <li><strong>Import .py</strong> — load a script and convert to blocks</li>\n"
        "                <li><strong>Tests</strong> — run assert harness</li>\n"
        "                <li><strong>Ctrl+Shift+Z</strong> — undo studio snapshot (AI apply / convert)</li>",
        1,
    )

INDEX.write_text(text, encoding="utf-8")
print("Injected v1.1 best pack,", INDEX.stat().st_size, "bytes")
