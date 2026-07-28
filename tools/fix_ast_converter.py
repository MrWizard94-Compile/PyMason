#!/usr/bin/env python3
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "index.html"
t = INDEX.read_text(encoding="utf-8")
start = t.find("        async function pythonToBlocksViaAst(src) {")
end = t.find("        function exprIRToBlock(e) {")
if start < 0 or end < 0:
    raise SystemExit(f"markers missing {start} {end}")

new = r"""        async function pythonToBlocksViaAst(src) {
            if (!pyodideFallback) {
                try { await loadPyodideFallback_(); } catch (e) { return null; }
            }
            if (!pyodideFallback) return null;
            window._pymasonPySrc = String(src || '');
            const pyProg = [
                'import ast, json',
                'from js import window',
                'src = str(window._pymasonPySrc or "")',
                'class Emit(ast.NodeVisitor):',
                '    def visit_Module(self, node):',
                '        out = []',
                '        for s in node.body:',
                '            r = self.visit(s)',
                '            if r: out.append(r)',
                '        return out',
                '    def visit_Expr(self, node):',
                '        v = node.value',
                '        if isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id == "print":',
                '            return {"op": "print", "args": [self._expr(a) for a in v.args]}',
                '        return {"op": "raw", "text": getattr(ast, "unparse", lambda n: "")(node)}',
                '    def visit_Assign(self, node):',
                '        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):',
                '            return {"op": "assign", "name": node.targets[0].id, "value": self._expr(node.value)}',
                '        return {"op": "raw", "text": getattr(ast, "unparse", lambda n: "")(node)}',
                '    def visit_If(self, node):',
                '        body = [x for x in (self.visit(s) for s in node.body) if x]',
                '        return {"op": "if", "cond": self._expr(node.test), "body": body}',
                '    def visit_For(self, node):',
                '        if isinstance(node.target, ast.Name) and isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == "range":',
                '            args = [self._expr(a) for a in node.iter.args]',
                '            body = [x for x in (self.visit(s) for s in node.body) if x]',
                '            return {"op": "for_range", "var": node.target.id, "args": args, "body": body}',
                '        return {"op": "raw", "text": getattr(ast, "unparse", lambda n: "")(node)}',
                '    def visit_While(self, node):',
                '        body = [x for x in (self.visit(s) for s in node.body) if x]',
                '        return {"op": "while", "cond": self._expr(node.test), "body": body}',
                '    def visit_Import(self, node):',
                '        names = [a.name for a in node.names]',
                '        return {"op": "import", "module": names[0] if names else "os"}',
                '    def visit_Assert(self, node):',
                '        return {"op": "assert", "cond": self._expr(node.test)}',
                '    def visit_Pass(self, node):',
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
                'json.dumps(Emit().visit(ast.parse(src)))',
            ].join('\n');
            const irJson = await pyodideFallback.runPythonAsync(pyProg);
            const ir = JSON.parse(irJson || '[]');
            return buildBlocksFromIR(ir);
        }

"""
INDEX.write_text(t[:start] + new + t[end:], encoding="utf-8")
print("fixed AST converter")
