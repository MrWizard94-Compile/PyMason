#!/usr/bin/env python3
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "index.html"
t = INDEX.read_text(encoding="utf-8")
if "Blockly.Blocks['py_assert_true']" in t and "python.pythonGenerator.forBlock['py_assert_true']" in t:
    # may exist only as references
    pass

marker = "python.pythonGenerator.forBlock['py_stage_text']"
idx = t.find(marker)
if idx < 0:
    raise SystemExit("stage_text missing")
# end of that function
end = t.find("};", idx) + 2
# skip following whitespace to keep structure
while end < len(t) and t[end] in "\r\n":
    end += 1

extra = r"""
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
            const body = generator.statementToCode(block, 'DO') || (generator.PREFIX + 'pass\n');
            return 'try:\n' + body + '    raise AssertionError("expected ' + exc + '")\nexcept ' + exc + ':\n    pass\n';
        };

"""

if "Blockly.Blocks['py_assert_true'] = {" in t:
    print("assert blocks already defined")
else:
    INDEX.write_text(t[:end] + "\n" + extra + t[end:], encoding="utf-8")
    print("added assert/circle blocks")
