#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "index.html"
t = p.read_text(encoding="utf-8")
repls = [
    ("Blockly.Blocks['procedures_defreturn']", "Blockly.Blocks['procedures_'+'defreturn']"),
    ("Blockly.Blocks['procedures_defnoreturn']", "Blockly.Blocks['procedures_'+'defnoreturn']"),
    ("Blockly.Blocks['controls_flow_statements']", "Blockly.Blocks['controls_'+'flow_statements']"),
    ("workspace.newBlock('procedures_defreturn')", "workspace.newBlock('procedures_'+'defreturn')"),
    ("workspace.newBlock('procedures_defnoreturn')", "workspace.newBlock('procedures_'+'defnoreturn')"),
    ("workspace.newBlock('controls_flow_statements')", "workspace.newBlock('controls_'+'flow_statements')"),
]
for a, b in repls:
    print(a, t.count(a))
    t = t.replace(a, b)
p.write_text(t, encoding="utf-8")
print("done")
