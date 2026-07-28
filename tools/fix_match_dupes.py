#!/usr/bin/env python3
from pathlib import Path
import re

p = Path(__file__).resolve().parents[1] / "index.html"
t = p.read_text(encoding="utf-8")

start = t.find("        // match/case — free-form cases for flexibility")
end = t.find("        Blockly.Blocks['py_getitem']")
if start < 0 or end < 0:
    raise SystemExit(f"markers {start} {end}")
t = t[:start] + t[end:]

# Fix Advanced toolbox entry for match/walrus
t2, n = re.subn(
    r'            <block type="py_match">\s*'
    r'<field name="SUBJECT">value</field>\s*'
    r'<field name="CASES">[^<]*</field>\s*'
    r'</block>\s*'
    r'<block type="py_walrus">\s*'
    r'<field name="VAR">n</field>\s*'
    r'</block>',
    """            <block type="py_match"></block>
            <block type="py_case">
                <field name="PATTERN">_</field>
            </block>
            <block type="py_walrus"></block>""",
    t,
    count=1,
)
print("toolbox replacements", n)
p.write_text(t2 if n else t, encoding="utf-8")
print("ok")
