#!/usr/bin/env python3
"""Replace broken v12 createPyWorker with a syntactically valid implementation."""
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "index.html"
t = INDEX.read_text(encoding="utf-8")

start = t.find("        // Replace worker factory with debug-capable version")
if start < 0:
    start = t.find("        // Clean worker factory (debug_run + run)")
if start < 0:
    start = t.find("        createPyWorker = function() {\n            const lines = [];")
end = t.find("        const _v12_mainDebug = debugRun;")
if start < 0 or end < 0:
    raise SystemExit(f"markers missing start={start} end={end}")

clean = r'''
        // Clean worker factory (debug_run + run) — v1.2
        createPyWorker = function() {
            // Worker source built as one string (avoid quote hell)
            var workerSrc = "";
            workerSrc += "let pyodide=null;\n";
            workerSrc += "self.onmessage=async function(e){\n";
            workerSrc += "const msg=e.data||{},type=msg.type;\n";
            workerSrc += "if(type==='init'){try{\n";
            workerSrc += "importScripts('https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js');\n";
            workerSrc += "pyodide=await loadPyodide({stdout:function(t){self.postMessage({type:'stdout',text:t+'\\n'});},stderr:function(t){self.postMessage({type:'stderr',text:t+'\\n'});}});\n";
            workerSrc += "self.postMessage({type:'ready'});\n";
            workerSrc += "}catch(err){self.postMessage({type:'error',text:String(err.message||err)});}return;}\n";
            workerSrc += "if(type==='run'||type==='debug_run'){try{\n";
            workerSrc += "if(msg.sharedBuffer){var s=new Int32Array(msg.sharedBuffer);self._pymason_shared_int32=s;try{pyodide.pyimport('js')._pymason_shared_int32=s;}catch(x){}}\n";
            workerSrc += "if(msg.debugBuffer){var d=new Int32Array(msg.debugBuffer);self._pymason_debug_i32=d;try{pyodide.pyimport('js')._pymason_debug_i32=d;}catch(x){}}\n";
            workerSrc += "var boot=['import sys,json,builtins',";
            workerSrc += "'def _pymason_read_shared():','    import js','    js.Atomics.wait(js._pymason_shared_int32,0,0)',";
            workerSrc += "'    flag=int(js._pymason_shared_int32[0])','    length=max(0,flag-1)',";
            workerSrc += "'    chars=[chr(int(js._pymason_shared_int32[1+i])) for i in range(length)]',";
            workerSrc += "'    js._pymason_shared_int32[0]=0','    return chr(0).join(chars) if False else \"\".join(chars)',";
            workerSrc += "'def _pymason_input(prompt=\"\"):','    import js','    p=\"\" if prompt is None else str(prompt)',";
            workerSrc += "'    js.self.postMessage(js.JSON.parse(json.dumps({\"type\":\"input_request\",\"prompt\":p})))',";
            workerSrc += "'    return _pymason_read_shared()','builtins.input=_pymason_input',";
            workerSrc += "'class _PyMasonInput:','    def readline(self,size=-1):','        import js',";
            workerSrc += "'        js.self.postMessage(js.JSON.parse(json.dumps({\"type\":\"input_request\",\"prompt\":\"\"})))',";
            workerSrc += "'        return _pymason_read_shared()+\"\\\\n\"','sys.stdin=_PyMasonInput()'].join('\\n');\n";
            workerSrc += "await pyodide.runPythonAsync(boot);\n";
            workerSrc += "var codeToRun=msg.code||'';\n";
            workerSrc += "if(type==='debug_run'){\n";
            workerSrc += "var bps=(msg.breakpoints||[]).filter(function(n){return n>0;});\n";
            workerSrc += "var indented=(msg.code||'').split('\\n').map(function(l){return '    '+l;}).join('\\n');\n";
            workerSrc += "var parts=[];\n";
            workerSrc += "parts.push('import sys,json');\n";
            workerSrc += "parts.push('_pymason_bps=set(['+bps.join(',')+'])');\n";
            workerSrc += "parts.push('_pymason_debug_mode={\"mode\":\"run\"}');\n";
            workerSrc += "parts.push('def _pymason_dbg_wait():');\n";
            workerSrc += "parts.push('    import js');\n";
            workerSrc += "parts.push('    js.Atomics.store(js._pymason_debug_i32,0,0)');\n";
            workerSrc += "parts.push('    js.Atomics.wait(js._pymason_debug_i32,0,0)');\n";
            workerSrc += "parts.push('    cmd=int(js._pymason_debug_i32[0])');\n";
            workerSrc += "parts.push('    if cmd==1: _pymason_debug_mode[\"mode\"]=\"step\"');\n";
            workerSrc += "parts.push('    elif cmd==2: _pymason_debug_mode[\"mode\"]=\"run\"');\n";
            workerSrc += "parts.push('    elif cmd==3: _pymason_debug_mode[\"mode\"]=\"stop\"');\n";
            workerSrc += "parts.push('def _pymason_trace(frame,event,arg):');\n";
            workerSrc += "parts.push('    if event!=\"line\": return _pymason_trace');\n";
            workerSrc += "parts.push('    fn=frame.f_code.co_filename or \"\"');\n";
            workerSrc += "parts.push('    if \"<exec>\" not in fn and fn!=\"<string>\": return _pymason_trace');\n";
            workerSrc += "parts.push('    line=int(frame.f_lineno)');\n";
            workerSrc += "parts.push('    try:');\n";
            workerSrc += "parts.push('        import js');\n";
            workerSrc += "parts.push('        locs={}');\n";
            workerSrc += "parts.push('        for k,v in list(frame.f_locals.items()):');\n";
            workerSrc += "parts.push('            if str(k).startswith(\"_\"): continue');\n";
            workerSrc += "parts.push('            try: locs[str(k)]=repr(v)[:140]');\n";
            workerSrc += "parts.push('            except Exception: locs[str(k)]=\"?\"');\n";
            workerSrc += "parts.push('        js.self.postMessage(js.JSON.parse(json.dumps({\"type\":\"debug_line\",\"line\":line,\"vars\":locs})))');\n";
            workerSrc += "parts.push('    except Exception:');\n";
            workerSrc += "parts.push('        pass');\n";
            workerSrc += "parts.push('    if (line in _pymason_bps) or (_pymason_debug_mode.get(\"mode\")==\"step\"):');\n";
            workerSrc += "parts.push('        _pymason_debug_mode[\"mode\"]=\"wait\"');\n";
            workerSrc += "parts.push('        _pymason_dbg_wait()');\n";
            workerSrc += "parts.push('        if _pymason_debug_mode.get(\"mode\")==\"stop\":');\n";
            workerSrc += "parts.push('            raise SystemExit(\"Debug stopped\")');\n";
            workerSrc += "parts.push('    return _pymason_trace');\n";
            workerSrc += "parts.push('sys.settrace(_pymason_trace)');\n";
            workerSrc += "parts.push('try:');\n";
            workerSrc += "parts.push(indented);\n";
            workerSrc += "parts.push('finally:');\n";
            workerSrc += "parts.push('    sys.settrace(None)');\n";
            workerSrc += "codeToRun=parts.join('\\n');\n";
            workerSrc += "}\n";
            workerSrc += "await pyodide.runPythonAsync(codeToRun);\n";
            workerSrc += "var varsJson='{}';try{\n";
            workerSrc += "varsJson=await pyodide.runPythonAsync('import json as _json\\n_skip={\"__builtins__\",\"__name__\",\"sys\",\"json\"}\\n_vars={}\\nfor _k,_v in list(globals().items()):\\n if _k in _skip or str(_k).startswith(\"_\"): continue\\n try:\\n  _s=repr(_v)\\n  if len(_s)>180: _s=_s[:177]+\"...\"\\n  _vars[_k]=_s\\n except Exception:\\n  _vars[_k]=\"<unprintable>\"\\n_json.dumps(_vars)');\n";
            workerSrc += "}catch(ve){}\n";
            workerSrc += "self.postMessage({type:'done',vars:varsJson});\n";
            workerSrc += "}catch(err){var m=err.message||String(err);if(!/Debug stopped|SystemExit/i.test(m))self.postMessage({type:'error',text:m});else self.postMessage({type:'done',vars:'{}'});}return;}\n";
            workerSrc += "};\n";
            var blob = new Blob([workerSrc], { type: "application/javascript" });
            return new Worker(URL.createObjectURL(blob));
        };

'''

# Fix boot join chars line - the "if False" hack is ugly; use simpler empty join
clean = clean.replace(
    "'    return chr(0).join(chars) if False else \"\".join(chars)',",
    "'    return \"\".join(chars)',",
)

INDEX.write_text(t[:start] + clean + t[end:], encoding="utf-8")
print("fixed worker, size", INDEX.stat().st_size)
