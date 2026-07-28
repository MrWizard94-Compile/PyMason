#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "index.html"
t = p.read_text(encoding="utf-8")
# Safer Order enums — some Blockly builds lack BITWISE_* / LOGICAL_*
for name in (
    "BITWISE_AND",
    "BITWISE_NOT",
    "BITWISE_OR",
    "LOGICAL_AND",
    "LOGICAL_OR",
    "RELATIONAL",
):
    t = t.replace(f"python.Order.{name}", "python.Order.NONE")
p.write_text(t, encoding="utf-8")
print("Order enum fallbacks applied")
