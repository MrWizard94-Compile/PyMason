#!/usr/bin/env python3
"""PyMason v1.2 — deep AST emit + worker debugger (clean)."""
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "index.html"
t = INDEX.read_text(encoding="utf-8")

if "PYMASON_V12_ALL" in t:
    print("v1.2 already present")
    raise SystemExit(0)

# ── Deep AST: replace pyProg array body visitors ───────────────────
# Insert FunctionDef etc. into existing pyProg by replacing the short Pass/generic section
old = """                '    def visit_Pass(self, node):',
                '        return None',
                '    def generic_visit(self, node):',
                '        return {"op": "raw", "text": getattr(ast, "unparse", lambda n: type(node).__name__)(node)}',
                '    def _expr(self, node):',
                '        if isinstance(node, ast.Constant):',
                '            return {"t": "const", "v": node.value}',
                '        if isinstance(node, ast.Name):',
                '            return {"t": "name", "v": node.id}',
                '        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "input":',
                '            prompt = ""',
                '            if node.args and isinstance(node.args[0], ast.Constant):',
                '                prompt = str(node.args[0].value)',
                '            return {"t": "input", "prompt": prompt}',
                '        try:',
                '            return {"t": "raw", "v": getattr(ast, "unparse", lambda n: "")(node)}',
                '        except Exception:',
                '            return {"t": "raw", "v": ""}',
                'json.dumps(Emit().visit(ast.parse(src)))',"""

new = """                '    def visit_Pass(self, node):',
                '        return None',
                '    def visit_Return(self, node):',
                '        return {"op": "return", "value": self._expr(node.value) if node.value else None}',
                '    def visit_Break(self, node):',
                '        return {"op": "break"}',
                '    def visit_Continue(self, node):',
                '        return {"op": "continue"}',
                '    def visit_FunctionDef(self, node):',
                '        args = [a.arg for a in node.args.args if a.arg != "self"]',
                '        return {"op": "def", "name": node.name, "args": args, "body": [x for x in (self.visit(s) for s in node.body) if x]}',
                '    def visit_AsyncFunctionDef(self, node):',
                '        r = self.visit_FunctionDef(node)',
                '        if r: r["async"] = True',
                '        return r',
                '    def visit_ClassDef(self, node):',
                '        bases = [b.id for b in node.bases if isinstance(b, ast.Name)]',
                '        return {"op": "class", "name": node.name, "bases": bases, "body": [x for x in (self.visit(s) for s in node.body) if x]}',
                '    def visit_ImportFrom(self, node):',
                '        names = [a.name for a in node.names]',
                '        return {"op": "from_import", "module": node.module or "", "name": names[0] if names else "*"}',
                '    def visit_Try(self, node):',
                '        hs = []',
                '        for h in node.handlers:',
                '            tn = h.type.id if isinstance(h.type, ast.Name) else "Exception"',
                '            hs.append({"type": tn, "body": [x for x in (self.visit(s) for s in h.body) if x]})',
                '        return {"op": "try", "body": [x for x in (self.visit(s) for s in node.body) if x], "handlers": hs}',
                '    def generic_visit(self, node):',
                '        return {"op": "raw", "text": getattr(ast, "unparse", lambda n: type(node).__name__)(node)}',
                '    def _expr(self, node):',
                '        if node is None: return None',
                '        if isinstance(node, ast.Constant):',
                '            return {"t": "const", "v": node.value}',
                '        if isinstance(node, ast.Name):',
                '            return {"t": "name", "v": node.id}',
                '        if isinstance(node, ast.List):',
                '            return {"t": "list", "elts": [self._expr(x) for x in node.elts]}',
                '        if isinstance(node, ast.BinOp):',
                '            return {"t": "binop", "left": self._expr(node.left), "right": self._expr(node.right)}',
                '        if isinstance(node, ast.Compare) and node.ops and node.comparators:',
                '            return {"t": "compare", "left": self._expr(node.left), "right": self._expr(node.comparators[0])}',
                '        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "input":',
                '            prompt = ""',
                '            if node.args and isinstance(node.args[0], ast.Constant):',
                '                prompt = str(node.args[0].value)',
                '            return {"t": "input", "prompt": prompt}',
                '        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):',
                '            return {"t": "call", "name": node.func.id, "args": [self._expr(a) for a in node.args]}',
                '        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self":',
                '            return {"t": "self_get", "attr": node.attr}',
                '        try:',
                '            return {"t": "raw", "v": getattr(ast, "unparse", lambda n: "")(node)}',
                '        except Exception:',
                '            return {"t": "raw", "v": ""}',
                'json.dumps(Emit().visit(ast.parse(src)))',"""

if old not in t:
    print("WARN: AST block not found exact — checking alternate")
    if "'    def visit_FunctionDef" in t:
        print("already has FunctionDef")
    else:
        raise SystemExit("AST visitor section not found")
else:
    t = t.replace(old, new, 1)
    print("deep AST visitors OK")

# Expand emitNode — insert before raw comment handler
raw_m = "                if (node.op === 'raw' && Blockly.Blocks['py_comment']) {"
if "node.op === 'def'" not in t and raw_m in t:
    t = t.replace(
        raw_m,
        r"""                if (node.op === 'return' && Blockly.Blocks['py_return']) {
                    const b = workspace.newBlock('py_return');
                    b.initSvg(); b.render();
                    if (node.value) {
                        const vb = exprIRToBlock(node.value);
                        try {
                            const inp = b.getInput('VALUE') || b.inputList.find(function(i){return i.connection && i.connection.type === 1;});
                            if (inp && vb) inp.connection.connect(vb.outputConnection);
                        } catch (e) {}
                    }
                    return b;
                }
                if (node.op === 'def') {
                    let b = null;
                    const hasRet = (node.body || []).some(function(s) { return s && s.op === 'return' && s.value; });
                    try {
                        if (hasRet && Blockly.Blocks['procedures_defreturn']) b = workspace.newBlock('procedures_defreturn');
                        else if (Blockly.Blocks['procedures_defnoreturn']) b = workspace.newBlock('procedures_defnoreturn');
                    } catch (e) { b = null; }
                    if (b) {
                        try { if (b.getField('NAME')) b.setFieldValue(node.name || 'func', 'NAME'); } catch (e) {}
                        b.initSvg(); b.render();
                        try {
                            if (Array.isArray(b.arguments_) && node.args) {
                                node.args.forEach(function(a) { if (b.arguments_.indexOf(a) < 0) b.arguments_.push(a); });
                                if (b.updateShape_) b.updateShape_();
                            }
                        } catch (e) {}
                        const stack = b.getInput('STACK') || b.getInput('DO');
                        if (stack) emitList(node.body, stack);
                        return b;
                    }
                    if (Blockly.Blocks['py_comment']) {
                        const c = workspace.newBlock('py_comment');
                        c.setFieldValue('def ' + (node.name || 'f') + '(' + (node.args || []).join(',') + ')', 'TEXT');
                        c.initSvg(); c.render();
                        return c;
                    }
                }
                if (node.op === 'class' && Blockly.Blocks['py_class']) {
                    const b = workspace.newBlock('py_class');
                    b.initSvg(); b.render();
                    try {
                        if (b.getField('NAME')) b.setFieldValue(node.name || 'MyClass', 'NAME');
                        if (b.getField('PARENT') && node.bases && node.bases[0]) b.setFieldValue(node.bases[0], 'PARENT');
                    } catch (e) {}
                    const stack = b.getInput('BODY') || b.getInput('DO') || b.getInput('STACK');
                    if (stack) emitList(node.body, stack);
                    return b;
                }
                if (node.op === 'from_import' && Blockly.Blocks['py_from_import']) {
                    const b = workspace.newBlock('py_from_import');
                    try {
                        b.setFieldValue(node.module || 'os', 'MODULE');
                        b.setFieldValue(node.name || 'path', 'NAME');
                    } catch (e) {}
                    b.initSvg(); b.render();
                    return b;
                }
                if (node.op === 'try' && Blockly.Blocks['py_try_except']) {
                    const b = workspace.newBlock('py_try_except');
                    b.initSvg(); b.render();
                    try {
                        emitList(node.body, b.getInput('TRY') || b.getInput('DO'));
                        const h = node.handlers && node.handlers[0];
                        if (h) emitList(h.body, b.getInput('EXCEPT') || b.getInput('DO2'));
                    } catch (e) {}
                    return b;
                }
                if (node.op === 'break' || node.op === 'continue') {
                    if (Blockly.Blocks['controls_flow_statements']) {
                        const b = workspace.newBlock('controls_flow_statements');
                        try { b.setFieldValue(node.op === 'break' ? 'BREAK' : 'CONTINUE', 'FLOW'); } catch (e) {}
                        b.initSvg(); b.render();
                        return b;
                    }
                }
                if (node.op === 'raw' && Blockly.Blocks['py_comment']) {
""",
        1,
    )
    print("emitNode expanded")
else:
    print("emitNode expand skipped")

# exprIRToBlock extras
ea = "            return parsePyExprToValueBlock(e.v || '', workspace);\n        }\n\n        function buildBlocksFromIR(ir) {"
if "e.t === 'binop'" not in t and ea in t:
    t = t.replace(
        ea,
        """            if (e.t === 'binop' || e.t === 'compare') {
                try {
                    const b = workspace.newBlock(e.t === 'compare' ? 'logic_compare' : 'math_arithmetic');
                    b.initSvg(); b.render();
                    const L = exprIRToBlock(e.left), R = exprIRToBlock(e.right);
                    if (L && b.getInput('A')) b.getInput('A').connection.connect(L.outputConnection);
                    if (R && b.getInput('B')) b.getInput('B').connection.connect(R.outputConnection);
                    return b;
                } catch (err) {}
            }
            if (e.t === 'self_get' && Blockly.Blocks['py_self_get']) {
                const b = workspace.newBlock('py_self_get');
                try { b.setFieldValue(e.attr || 'name', 'ATTR'); } catch (err) {}
                b.initSvg(); b.render();
                return b;
            }
            if (e.t === 'call') {
                return parsePyExprToValueBlock((e.name || 'f') + '()', workspace);
            }
            return parsePyExprToValueBlock(e.v || '', workspace);
        }

        function buildBlocksFromIR(ir) {""",
        1,
    )
    print("exprIR expanded")

# ── Worker debugger pack ───────────────────────────────────────────
v12 = r"""
        // ═══════════════════════════════════════════════════════════════════
        //  PYMASON_V12_ALL — worker SAB debugger
        // ═══════════════════════════════════════════════════════════════════

        let debugSharedBuffer = null;
        let debugSharedInt32 = null;
        if (typeof useSharedBuffer !== 'undefined' && useSharedBuffer) {
            try {
                debugSharedBuffer = new SharedArrayBuffer(16);
                debugSharedInt32 = new Int32Array(debugSharedBuffer);
            } catch (e) {
                debugSharedBuffer = null;
            }
        }

        // Replace worker factory with debug-capable version
        createPyWorker = function() {
            const lines = [];
            lines.push('let pyodide=null;');
            lines.push('self.onmessage=async function(e){');
            lines.push('const msg=e.data||{},type=msg.type;');
            lines.push('if(type==="init"){try{');
            lines.push('importScripts("https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js");');
            lines.push('pyodide=await loadPyodide({stdout:(t)=>self.postMessage({type:"stdout",text:t+"\\n"}),stderr:(t)=>self.postMessage({type:"stderr",text:t+"\\n"})});');
            lines.push('self.postMessage({type:"ready"});');
            lines.push('}catch(err){self.postMessage({type:"error",text:String(err.message||err)});}return;}');
            lines.push('if(type==="run"||type==="debug_run"){try{');
            lines.push('if(msg.sharedBuffer){const s=new Int32Array(msg.sharedBuffer);self._pymason_shared_int32=s;try{pyodide.pyimport("js")._pymason_shared_int32=s;}catch(x){}}');
            lines.push('if(msg.debugBuffer){const d=new Int32Array(msg.debugBuffer);self._pymason_debug_i32=d;try{pyodide.pyimport("js")._pymason_debug_i32=d;}catch(x){}}');
            lines.push('await pyodide.runPythonAsync("import sys,json,builtins\\n"');
            lines.push('+ "def _pymason_read_shared():\\n import js\\n js.Atomics.wait(js._pymason_shared_int32,0,0)\\n flag=int(js._pymason_shared_int32[0])\\n length=max(0,flag-1)\\n chars=[chr(int(js._pymason_shared_int32[1+i])) for i in range(length)]\\n js._pymason_shared_int32[0]=0\\n return \\\"\\\".join(chars)\\n"');
            lines.push('+ "def _pymason_input(prompt=\\\"\\\"):\\n import js\\n p=\\\"\\\" if prompt is None else str(prompt)\\n js.self.postMessage(js.JSON.parse(json.dumps({\\\"type\\\":\\\"input_request\\\",\\\"prompt\\\":p})))\\n return _pymason_read_shared()\\n"');
            lines.push('+ "builtins.input=_pymason_input\\n"');
            lines.push('+ "class _PyMasonInput:\\n def readline(self,size=-1):\\n  import js\\n  js.self.postMessage(js.JSON.parse(json.dumps({\\\"type\\\":\\\"input_request\\\",\\\"prompt\\\":\\\"\\\"})))\\n  return _pymason_read_shared()+\\\"\\\\n\\\"\\n"');
            lines.push('+ "sys.stdin=_PyMasonInput()");');
            lines.push('let codeToRun=msg.code||"";');
            lines.push('if(type==="debug_run"){');
            lines.push('const bps=(msg.breakpoints||[]).filter(n=>n>0);');
            lines.push('const indented=(msg.code||"").split("\\n").map(l=>"    "+l).join("\\n");');
            lines.push('codeToRun=["import sys,json","_pymason_bps=set(["+bps.join(",")+"])","_pymason_debug_mode={\'mode\':\'run\'}",');
            lines.push('"def _pymason_dbg_wait():"," import js"," js.Atomics.store(js._pymason_debug_i32,0,0)"," js.Atomics.wait(js._pymason_debug_i32,0,0)"," cmd=int(js._pymason_debug_i32[0])",');
            lines.push('" if cmd==1: _pymason_debug_mode[\\'mode\\']=\\'step\\'"," elif cmd==2: _pymason_debug_mode[\\'mode\\']=\\'run\\'"," elif cmd==3: _pymason_debug_mode[\\'mode\\']=\\'stop\\'",');
            lines.push('"def _pymason_trace(frame,event,arg):"," if event!=\\'line\\': return _pymason_trace"," fn=frame.f_code.co_filename or \\\"\\\"",');
            lines.push('" if \\\'<exec>\\\' not in fn and fn!=\\\'<string>\\\': return _pymason_trace"," line=int(frame.f_lineno)",');
            lines.push('" try:","  import js","  locs={}","  for k,v in list(frame.f_locals.items()):","   if str(k).startswith(\\\'_\\\'): continue","   try: locs[str(k)]=repr(v)[:140]","   except Exception: locs[str(k)]=\\\'?\\\'",');
            lines.push('"  js.self.postMessage(js.JSON.parse(json.dumps({\\\"type\\\":\\\"debug_line\\\",\\\"line\\\":line,\\\"vars\\\":locs})))"," except Exception:","  pass",');
            lines.push('" if (line in _pymason_bps) or (_pymason_debug_mode.get(\\\'mode\\\')==\\\'step\\\'):","  _pymason_debug_mode[\\\'mode\\\']=\\\'wait\\\'","  _pymason_dbg_wait()","  if _pymason_debug_mode.get(\\\'mode\\\')==\\\'stop\\\':","   raise SystemExit(\\\'Debug stopped\\\')"," return _pymason_trace",');
            lines.push('"sys.settrace(_pymason_trace)","try:",indented,"finally:"," sys.settrace(None)"].join("\\n");');
            lines.push('}');
            lines.push('await pyodide.runPythonAsync(codeToRun);');
            lines.push('let varsJson="{}";try{varsJson=await pyodide.runPythonAsync("import json as _json\\n_skip={\\\'__builtins__\\\',\\\'__name__\\\',\\\'__doc__\\\',\\\'__package__\\\',\\\'__loader__\\\',\\\'__spec__\\\',\\\'sys\\\',\\\'json\\\'}\\n_vars={}\\nfor _k,_v in list(globals().items()):\\n if _k in _skip or str(_k).startswith(\\\'_\\\'): continue\\n try:\\n  _s=repr(_v)\\n  if len(_s)>180: _s=_s[:177]+\\\'...\\\'\\n  _vars[_k]=_s\\n except Exception:\\n  _vars[_k]=\\\'<unprintable>\\\'\\n_json.dumps(_vars)");}catch(ve){}');
            lines.push('self.postMessage({type:"done",vars:varsJson});');
            lines.push('}catch(err){const msg=err.message||String(err);if(!/Debug stopped|SystemExit/i.test(msg))self.postMessage({type:"error",text:msg});else self.postMessage({type:"done",vars:"{}"});}return;}');
            lines.push('};');
            const blob = new Blob([lines.join("\n")], { type: "application/javascript" });
            return new Worker(URL.createObjectURL(blob));
        };

        const _v12_mainDebug = debugRun;
        debugRun = async function(opts) {
            opts = opts || {};
            document.getElementById("debugBar")?.classList.add("visible");
            const userCode = getExecutablePython();
            if (!userCode.trim()) { showToast("Nothing to debug"); return; }
            if (outputLang !== "python") { showToast("Debugger is Python-only"); return; }
            if (opts.stepFirst) {
                [1,2,3,4,5].forEach(function(n){ lineBreakpoints.add(n); });
                if (typeof refreshBreakpointGutter === "function") refreshBreakpointGutter();
            }
            const canWorker = useSharedBuffer && debugSharedBuffer && debugSharedInt32;
            if (!canWorker) {
                setDebugStatus("No SAB — main-thread debug");
                return _v12_mainDebug(opts);
            }
            showOutput(); clearOutput();
            setDebugStatus("Worker debug…");
            debugState.active = true;
            executionAborted = false;
            btnRun.style.display = "none";
            btnStop.style.display = "";
            if (!pyodideReady || !pyWorker) await loadPyodide_();
            // Recreate worker with new factory if old worker lacks debug_run
            try { if (pyWorker) { pyWorker.terminate(); } } catch(e){}
            pyWorker = createPyWorker();
            await new Promise(function(resolve, reject) {
                const t = setTimeout(function(){ reject(new Error("Timeout")); }, 60000);
                pyWorker.onmessage = function(e) {
                    if (e.data.type === "ready") { clearTimeout(t); resolve(); }
                    else if (e.data.type === "error") { clearTimeout(t); reject(new Error(e.data.text)); }
                };
                pyWorker.postMessage({ type: "init" });
            });
            pyodideReady = true;
            Atomics.store(debugSharedInt32, 0, 0);
            debugStep = function(){ Atomics.store(debugSharedInt32,0,1); Atomics.notify(debugSharedInt32,0); setDebugStatus("Step…"); };
            debugContinue = function(){ Atomics.store(debugSharedInt32,0,2); Atomics.notify(debugSharedInt32,0); setDebugStatus("Continue…"); };
            debugStop = function(){
                Atomics.store(debugSharedInt32,0,3); Atomics.notify(debugSharedInt32,0);
                debugState.active=false; clearDebugHighlight(); setDebugStatus("Stopped");
                executionAborted=true;
                try{ pyWorker.terminate(); }catch(e){}
                pyWorker=null; pyodideReady=false;
            };
            const fullCode = (typeof buildStagePrelude==="function"?buildStagePrelude()+"\\n":"") + userCode;
            const bps = Array.from(lineBreakpoints);
            await new Promise(function(resolve){
                runResolve = resolve;
                pyWorker.onmessage = async function(e){
                    if (executionAborted) {
                        if (e.data.type==="done"||e.data.type==="error"){ runResolve=null; resolve(); }
                        return;
                    }
                    switch(e.data.type){
                        case "stdout": appendOutput(e.data.text); break;
                        case "stderr": appendOutput(e.data.text,true); break;
                        case "debug_line":
                            if (typeof highlightDebugLine==="function") highlightDebugLine(e.data.line);
                            if (e.data.vars && typeof showVarInspector==="function") showVarInspector(e.data.vars);
                            setDebugStatus("Paused @ "+e.data.line+" (worker SAB)");
                            break;
                        case "input_request": {
                            const val = await showInlineInput(e.data.prompt||"");
                            if (sharedInt32) {
                                const max=sharedInt32.length-1, slice=val.slice(0,max);
                                for(let i=0;i<slice.length;i++) sharedInt32[1+i]=slice.charCodeAt(i);
                                sharedInt32[0]=slice.length+1; Atomics.notify(sharedInt32,0);
                            }
                            break;
                        }
                        case "error":
                            if (typeof appendOutputSmart==="function") appendOutputSmart(e.data.text,true);
                            else appendOutput(e.data.text,true);
                            runResolve=null; resolve(); break;
                        case "done":
                            if (typeof showVarInspector==="function") showVarInspector(parseVarsPayload(e.data.vars));
                            runResolve=null; resolve(); break;
                    }
                };
                pyWorker.postMessage({
                    type: "debug_run",
                    code: fullCode,
                    sharedBuffer: sharedBuffer,
                    debugBuffer: debugSharedBuffer,
                    breakpoints: bps
                });
            });
            clearDebugHighlight();
            debugState.active=false;
            setDebugStatus("Worker debug finished");
            btnRun.style.display="";
            btnStop.style.display="none";
        };

"""

# place before version assign
for ver in ["1.1.0", "1.0.0", "1.2.0"]:
    marker = f"        PYMASON_VERSION = '{ver}';"
    if marker in t and "PYMASON_V12_ALL" not in t:
        t = t.replace(marker, v12 + f"\n        PYMASON_VERSION = '1.2.0';", 1)
        print("injected v12 before", ver)
        break
else:
    if "PYMASON_V12_ALL" not in t:
        # after var PYMASON
        t = t.replace(
            "var PYMASON_VERSION = '1.1.0';",
            "var PYMASON_VERSION = '1.2.0';\n",
            1,
        )
        boot = t.rfind("        bootWPAI();")
        if boot > 0:
            t = t[:boot] + v12 + "\n" + t[boot:]
            print("injected v12 before bootWPAI")
        else:
            raise SystemExit("could not place v12")

t = t.replace("var PYMASON_VERSION = '1.1.0';", "var PYMASON_VERSION = '1.2.0';")
t = t.replace("var PYMASON_VERSION = '1.0.0';", "var PYMASON_VERSION = '1.2.0';")

INDEX.write_text(t, encoding="utf-8")
print("done", INDEX.stat().st_size)
