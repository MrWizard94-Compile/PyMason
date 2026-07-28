#!/usr/bin/env python3
"""Inject additional PyMason blocks + toolbox categories (idempotent)."""
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "index.html"
t = INDEX.read_text(encoding="utf-8")

if "py_random_randint" in t and "category name=\"Time\"" in t:
    print("More blocks already present")
    raise SystemExit(0)

TOOLBOX = r'''
        <!-- ── Time ─────────────────────────────────── -->
        <category name="Time" colour="#6B8A9A">
            <block type="py_time_sleep">
                <value name="SEC"><shadow type="math_number"><field name="NUM">1</field></shadow></value>
            </block>
            <block type="py_time_time"></block>
            <block type="py_datetime_now"></block>
            <block type="py_datetime_strftime">
                <field name="FMT">%Y-%m-%d %H:%M:%S</field>
            </block>
            <block type="py_datetime_strptime">
                <field name="FMT">%Y-%m-%d</field>
            </block>
        </category>

        <!-- ── Random ───────────────────────────────── -->
        <category name="Random" colour="#9A6B8A">
            <block type="py_random_seed">
                <value name="SEED"><shadow type="math_number"><field name="NUM">42</field></shadow></value>
            </block>
            <block type="py_random_random"></block>
            <block type="py_random_randint">
                <value name="A"><shadow type="math_number"><field name="NUM">1</field></shadow></value>
                <value name="B"><shadow type="math_number"><field name="NUM">10</field></shadow></value>
            </block>
            <block type="py_random_choice"></block>
            <block type="py_random_sample">
                <value name="K"><shadow type="math_number"><field name="NUM">2</field></shadow></value>
            </block>
            <block type="py_random_shuffle"></block>
            <block type="py_random_uniform">
                <value name="A"><shadow type="math_number"><field name="NUM">0</field></shadow></value>
                <value name="B"><shadow type="math_number"><field name="NUM">1</field></shadow></value>
            </block>
        </category>

        <!-- ── Path & OS ────────────────────────────── -->
        <category name="Path &amp; OS" colour="#6B9A7A">
            <block type="py_os_getcwd"></block>
            <block type="py_os_listdir">
                <value name="PATH"><shadow type="text"><field name="TEXT">.</field></shadow></value>
            </block>
            <block type="py_os_path_join">
                <value name="A"><shadow type="text"><field name="TEXT">folder</field></shadow></value>
                <value name="B"><shadow type="text"><field name="TEXT">file.txt</field></shadow></value>
            </block>
            <block type="py_os_path_exists">
                <value name="PATH"><shadow type="text"><field name="TEXT">file.txt</field></shadow></value>
            </block>
            <block type="py_os_path_basename">
                <value name="PATH"><shadow type="text"><field name="TEXT">/a/b/c.txt</field></shadow></value>
            </block>
            <block type="py_os_makedirs">
                <value name="PATH"><shadow type="text"><field name="TEXT">out/data</field></shadow></value>
            </block>
            <block type="py_pathlib_path">
                <value name="PATH"><shadow type="text"><field name="TEXT">.</field></shadow></value>
            </block>
        </category>

        <!-- ── Regex ────────────────────────────────── -->
        <category name="Regex" colour="#9A8A6B">
            <block type="py_re_search">
                <value name="PATTERN"><shadow type="text"><field name="TEXT">\\d+</field></shadow></value>
            </block>
            <block type="py_re_findall">
                <value name="PATTERN"><shadow type="text"><field name="TEXT">\\w+</field></shadow></value>
            </block>
            <block type="py_re_sub">
                <value name="PATTERN"><shadow type="text"><field name="TEXT">\\s+</field></shadow></value>
                <value name="REPL"><shadow type="text"><field name="TEXT"> </field></shadow></value>
            </block>
            <block type="py_re_split">
                <value name="PATTERN"><shadow type="text"><field name="TEXT">,</field></shadow></value>
            </block>
            <block type="py_re_match">
                <value name="PATTERN"><shadow type="text"><field name="TEXT">^hello</field></shadow></value>
            </block>
        </category>

        <!-- ── Bitwise &amp; more Math ──────────────── -->
        <category name="Bitwise" colour="#5B67A5">
            <block type="py_bitwise">
                <value name="A"><shadow type="math_number"><field name="NUM">5</field></shadow></value>
                <value name="B"><shadow type="math_number"><field name="NUM">3</field></shadow></value>
            </block>
            <block type="py_bit_not">
                <value name="A"><shadow type="math_number"><field name="NUM">0</field></shadow></value>
            </block>
            <block type="py_pow">
                <value name="A"><shadow type="math_number"><field name="NUM">2</field></shadow></value>
                <value name="B"><shadow type="math_number"><field name="NUM">10</field></shadow></value>
            </block>
            <block type="py_round">
                <value name="A"><shadow type="math_number"><field name="NUM">3.14159</field></shadow></value>
                <value name="NDIGITS"><shadow type="math_number"><field name="NUM">2</field></shadow></value>
            </block>
            <block type="py_divmod">
                <value name="A"><shadow type="math_number"><field name="NUM">17</field></shadow></value>
                <value name="B"><shadow type="math_number"><field name="NUM">5</field></shadow></value>
            </block>
        </category>

        <!-- ── Advanced control ─────────────────────── -->
        <category name="Advanced" colour="#8A6B9A">
            <block type="py_match">
                <field name="SUBJECT">value</field>
                <field name="CASES">case 1:\n    print("one")\ncase _:\n    print("other")</field>
            </block>
            <block type="py_walrus">
                <field name="VAR">n</field>
            </block>
            <block type="py_getitem"></block>
            <block type="py_setitem"></block>
            <block type="py_delitem"></block>
            <block type="py_bool_op"></block>
            <block type="py_is_none"></block>
            <block type="py_hasattr"></block>
            <block type="py_getattr_default"></block>
            <block type="py_next"></block>
            <block type="py_iter"></block>
            <block type="py_enumerate_val"></block>
            <block type="py_zip_val"></block>
            <block type="py_copy"></block>
            <block type="py_breakpoint"></block>
            <block type="py_repr"></block>
            <block type="py_id_hash"></block>
            <block type="py_bytes_encode"></block>
            <block type="py_bytes_decode"></block>
            <block type="py_dict_merge"></block>
            <block type="py_list_repeat">
                <value name="N"><shadow type="math_number"><field name="NUM">3</field></shadow></value>
            </block>
            <block type="py_async_for"></block>
            <block type="py_async_with"></block>
            <block type="py_staticmethod"></block>
            <block type="py_classmethod"></block>
            <block type="py_property_def"></block>
        </category>

'''

# Insert toolbox before Functions category (after Errors is fine - before closing xml after Classes)
anchor = '        <!-- ── Functions ───────────────────────────── -->'
if anchor not in t:
    raise SystemExit("toolbox anchor missing")
t = t.replace(anchor, TOOLBOX + "\n" + anchor, 1)

# Block definitions before THEME
defs = r'''
        // ═══════════════════════════════════════════════════════════════
        //  MORE BLOCKS pack — Time, Random, Path, Regex, Bitwise, Advanced
        // ═══════════════════════════════════════════════════════════════

        Blockly.Blocks['py_time_sleep'] = {
            init: function() {
                this.appendValueInput('SEC').setCheck('Number').appendField('sleep seconds');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#6B8A9A');
                this.setTooltip('time.sleep(sec) — pause. Requires: import time');
            }
        };
        python.pythonGenerator.forBlock['py_time_sleep'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEC', python.Order.NONE) || '1';
            return 'time.sleep(' + s + ')\n';
        };

        Blockly.Blocks['py_time_time'] = {
            init: function() {
                this.appendDummyInput().appendField('time.time()');
                this.setOutput(true, 'Number');
                this.setColour('#6B8A9A');
                this.setTooltip('Seconds since epoch. Requires: import time');
            }
        };
        python.pythonGenerator.forBlock['py_time_time'] = function() {
            return ['time.time()', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_datetime_now'] = {
            init: function() {
                this.appendDummyInput().appendField('datetime.now()');
                this.setOutput(true);
                this.setColour('#6B8A9A');
                this.setTooltip('Current local datetime. Requires: from datetime import datetime');
            }
        };
        python.pythonGenerator.forBlock['py_datetime_now'] = function() {
            return ['datetime.now()', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_datetime_strftime'] = {
            init: function() {
                this.appendValueInput('DT').appendField('strftime');
                this.appendDummyInput().appendField(new Blockly.FieldTextInput('%Y-%m-%d %H:%M:%S'), 'FMT');
                this.setInputsInline(true);
                this.setOutput(true, 'String');
                this.setColour('#6B8A9A');
            }
        };
        python.pythonGenerator.forBlock['py_datetime_strftime'] = function(block, generator) {
            const dt = generator.valueToCode(block, 'DT', python.Order.MEMBER) || 'datetime.now()';
            const fmt = (block.getFieldValue('FMT') || '%Y-%m-%d').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
            return [dt + '.strftime(\'' + fmt + '\')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_datetime_strptime'] = {
            init: function() {
                this.appendValueInput('TEXT').setCheck('String').appendField('strptime');
                this.appendDummyInput().appendField(new Blockly.FieldTextInput('%Y-%m-%d'), 'FMT');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#6B8A9A');
                this.setTooltip('Parse date string. Requires: from datetime import datetime');
            }
        };
        python.pythonGenerator.forBlock['py_datetime_strptime'] = function(block, generator) {
            const text = generator.valueToCode(block, 'TEXT', python.Order.NONE) || "''";
            const fmt = (block.getFieldValue('FMT') || '%Y-%m-%d').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
            return ['datetime.strptime(' + text + ', \'' + fmt + '\')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_random_seed'] = {
            init: function() {
                this.appendValueInput('SEED').setCheck('Number').appendField('random.seed');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#9A6B8A');
                this.setTooltip('Requires: import random');
            }
        };
        python.pythonGenerator.forBlock['py_random_seed'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEED', python.Order.NONE) || 'None';
            return 'random.seed(' + s + ')\n';
        };

        Blockly.Blocks['py_random_random'] = {
            init: function() {
                this.appendDummyInput().appendField('random.random()');
                this.setOutput(true, 'Number');
                this.setColour('#9A6B8A');
            }
        };
        python.pythonGenerator.forBlock['py_random_random'] = function() {
            return ['random.random()', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_random_randint'] = {
            init: function() {
                this.appendValueInput('A').setCheck('Number').appendField('random.randint');
                this.appendValueInput('B').setCheck('Number').appendField('to');
                this.setInputsInline(true);
                this.setOutput(true, 'Number');
                this.setColour('#9A6B8A');
            }
        };
        python.pythonGenerator.forBlock['py_random_randint'] = function(block, generator) {
            const a = generator.valueToCode(block, 'A', python.Order.NONE) || '1';
            const b = generator.valueToCode(block, 'B', python.Order.NONE) || '10';
            return ['random.randint(' + a + ', ' + b + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_random_choice'] = {
            init: function() {
                this.appendValueInput('SEQ').appendField('random.choice');
                this.setOutput(true);
                this.setColour('#9A6B8A');
            }
        };
        python.pythonGenerator.forBlock['py_random_choice'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEQ', python.Order.NONE) || '[]';
            return ['random.choice(' + s + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_random_sample'] = {
            init: function() {
                this.appendValueInput('SEQ').appendField('random.sample');
                this.appendValueInput('K').setCheck('Number').appendField('k');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#9A6B8A');
            }
        };
        python.pythonGenerator.forBlock['py_random_sample'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEQ', python.Order.NONE) || '[]';
            const k = generator.valueToCode(block, 'K', python.Order.NONE) || '1';
            return ['random.sample(' + s + ', ' + k + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_random_shuffle'] = {
            init: function() {
                this.appendValueInput('SEQ').appendField('random.shuffle');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#9A6B8A');
                this.setTooltip('Shuffle list in place');
            }
        };
        python.pythonGenerator.forBlock['py_random_shuffle'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEQ', python.Order.NONE) || '[]';
            return 'random.shuffle(' + s + ')\n';
        };

        Blockly.Blocks['py_random_uniform'] = {
            init: function() {
                this.appendValueInput('A').setCheck('Number').appendField('random.uniform');
                this.appendValueInput('B').setCheck('Number').appendField('to');
                this.setInputsInline(true);
                this.setOutput(true, 'Number');
                this.setColour('#9A6B8A');
            }
        };
        python.pythonGenerator.forBlock['py_random_uniform'] = function(block, generator) {
            const a = generator.valueToCode(block, 'A', python.Order.NONE) || '0';
            const b = generator.valueToCode(block, 'B', python.Order.NONE) || '1';
            return ['random.uniform(' + a + ', ' + b + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_os_getcwd'] = {
            init: function() {
                this.appendDummyInput().appendField('os.getcwd()');
                this.setOutput(true, 'String');
                this.setColour('#6B9A7A');
                this.setTooltip('Requires: import os');
            }
        };
        python.pythonGenerator.forBlock['py_os_getcwd'] = function() {
            return ['os.getcwd()', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_os_listdir'] = {
            init: function() {
                this.appendValueInput('PATH').setCheck('String').appendField('os.listdir');
                this.setOutput(true);
                this.setColour('#6B9A7A');
            }
        };
        python.pythonGenerator.forBlock['py_os_listdir'] = function(block, generator) {
            const p = generator.valueToCode(block, 'PATH', python.Order.NONE) || "'.'";
            return ['os.listdir(' + p + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_os_path_join'] = {
            init: function() {
                this.appendValueInput('A').appendField('os.path.join');
                this.appendValueInput('B');
                this.setInputsInline(true);
                this.setOutput(true, 'String');
                this.setColour('#6B9A7A');
            }
        };
        python.pythonGenerator.forBlock['py_os_path_join'] = function(block, generator) {
            const a = generator.valueToCode(block, 'A', python.Order.NONE) || "''";
            const b = generator.valueToCode(block, 'B', python.Order.NONE) || "''";
            return ['os.path.join(' + a + ', ' + b + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_os_path_exists'] = {
            init: function() {
                this.appendValueInput('PATH').setCheck('String').appendField('os.path.exists');
                this.setOutput(true, 'Boolean');
                this.setColour('#6B9A7A');
            }
        };
        python.pythonGenerator.forBlock['py_os_path_exists'] = function(block, generator) {
            const p = generator.valueToCode(block, 'PATH', python.Order.NONE) || "''";
            return ['os.path.exists(' + p + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_os_path_basename'] = {
            init: function() {
                this.appendValueInput('PATH').setCheck('String').appendField('os.path.basename');
                this.setOutput(true, 'String');
                this.setColour('#6B9A7A');
            }
        };
        python.pythonGenerator.forBlock['py_os_path_basename'] = function(block, generator) {
            const p = generator.valueToCode(block, 'PATH', python.Order.NONE) || "''";
            return ['os.path.basename(' + p + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_os_makedirs'] = {
            init: function() {
                this.appendValueInput('PATH').setCheck('String').appendField('os.makedirs');
                this.appendDummyInput().appendField('exist_ok=True');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#6B9A7A');
            }
        };
        python.pythonGenerator.forBlock['py_os_makedirs'] = function(block, generator) {
            const p = generator.valueToCode(block, 'PATH', python.Order.NONE) || "''";
            return 'os.makedirs(' + p + ', exist_ok=True)\n';
        };

        Blockly.Blocks['py_pathlib_path'] = {
            init: function() {
                this.appendValueInput('PATH').setCheck('String').appendField('Path');
                this.setOutput(true);
                this.setColour('#6B9A7A');
                this.setTooltip('pathlib.Path(...). Requires: from pathlib import Path');
            }
        };
        python.pythonGenerator.forBlock['py_pathlib_path'] = function(block, generator) {
            const p = generator.valueToCode(block, 'PATH', python.Order.NONE) || "'.'";
            return ['Path(' + p + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_re_search'] = {
            init: function() {
                this.appendValueInput('PATTERN').setCheck('String').appendField('re.search');
                this.appendValueInput('TEXT').setCheck('String').appendField('in');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#9A8A6B');
                this.setTooltip('Requires: import re');
            }
        };
        python.pythonGenerator.forBlock['py_re_search'] = function(block, generator) {
            const p = generator.valueToCode(block, 'PATTERN', python.Order.NONE) || "''";
            const s = generator.valueToCode(block, 'TEXT', python.Order.NONE) || "''";
            return ['re.search(' + p + ', ' + s + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_re_match'] = {
            init: function() {
                this.appendValueInput('PATTERN').setCheck('String').appendField('re.match');
                this.appendValueInput('TEXT').setCheck('String').appendField('in');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#9A8A6B');
            }
        };
        python.pythonGenerator.forBlock['py_re_match'] = function(block, generator) {
            const p = generator.valueToCode(block, 'PATTERN', python.Order.NONE) || "''";
            const s = generator.valueToCode(block, 'TEXT', python.Order.NONE) || "''";
            return ['re.match(' + p + ', ' + s + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_re_findall'] = {
            init: function() {
                this.appendValueInput('PATTERN').setCheck('String').appendField('re.findall');
                this.appendValueInput('TEXT').setCheck('String').appendField('in');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#9A8A6B');
            }
        };
        python.pythonGenerator.forBlock['py_re_findall'] = function(block, generator) {
            const p = generator.valueToCode(block, 'PATTERN', python.Order.NONE) || "''";
            const s = generator.valueToCode(block, 'TEXT', python.Order.NONE) || "''";
            return ['re.findall(' + p + ', ' + s + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_re_sub'] = {
            init: function() {
                this.appendValueInput('PATTERN').setCheck('String').appendField('re.sub');
                this.appendValueInput('REPL').setCheck('String').appendField('→');
                this.appendValueInput('TEXT').setCheck('String').appendField('in');
                this.setInputsInline(true);
                this.setOutput(true, 'String');
                this.setColour('#9A8A6B');
            }
        };
        python.pythonGenerator.forBlock['py_re_sub'] = function(block, generator) {
            const p = generator.valueToCode(block, 'PATTERN', python.Order.NONE) || "''";
            const r = generator.valueToCode(block, 'REPL', python.Order.NONE) || "''";
            const s = generator.valueToCode(block, 'TEXT', python.Order.NONE) || "''";
            return ['re.sub(' + p + ', ' + r + ', ' + s + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_re_split'] = {
            init: function() {
                this.appendValueInput('PATTERN').setCheck('String').appendField('re.split');
                this.appendValueInput('TEXT').setCheck('String').appendField('on');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#9A8A6B');
            }
        };
        python.pythonGenerator.forBlock['py_re_split'] = function(block, generator) {
            const p = generator.valueToCode(block, 'PATTERN', python.Order.NONE) || "''";
            const s = generator.valueToCode(block, 'TEXT', python.Order.NONE) || "''";
            return ['re.split(' + p + ', ' + s + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_bitwise'] = {
            init: function() {
                this.appendValueInput('A').setCheck('Number');
                this.appendDummyInput().appendField(new Blockly.FieldDropdown([
                    ['&', '&'], ['|', '|'], ['^', '^'], ['<<', '<<'], ['>>', '>>'],
                ]), 'OP');
                this.appendValueInput('B').setCheck('Number');
                this.setInputsInline(true);
                this.setOutput(true, 'Number');
                this.setColour('#5B67A5');
            }
        };
        python.pythonGenerator.forBlock['py_bitwise'] = function(block, generator) {
            const op = block.getFieldValue('OP') || '&';
            const a = generator.valueToCode(block, 'A', python.Order.BITWISE_AND) || '0';
            const b = generator.valueToCode(block, 'B', python.Order.BITWISE_AND) || '0';
            return ['(' + a + ' ' + op + ' ' + b + ')', python.Order.BITWISE_AND];
        };

        Blockly.Blocks['py_bit_not'] = {
            init: function() {
                this.appendValueInput('A').setCheck('Number').appendField('~');
                this.setOutput(true, 'Number');
                this.setColour('#5B67A5');
            }
        };
        python.pythonGenerator.forBlock['py_bit_not'] = function(block, generator) {
            const a = generator.valueToCode(block, 'A', python.Order.BITWISE_NOT) || '0';
            return ['(~' + a + ')', python.Order.BITWISE_NOT];
        };

        Blockly.Blocks['py_pow'] = {
            init: function() {
                this.appendValueInput('A').setCheck('Number').appendField('pow');
                this.appendValueInput('B').setCheck('Number').appendField('**');
                this.setInputsInline(true);
                this.setOutput(true, 'Number');
                this.setColour('#5B67A5');
            }
        };
        python.pythonGenerator.forBlock['py_pow'] = function(block, generator) {
            const a = generator.valueToCode(block, 'A', python.Order.NONE) || '0';
            const b = generator.valueToCode(block, 'B', python.Order.NONE) || '1';
            return ['pow(' + a + ', ' + b + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_round'] = {
            init: function() {
                this.appendValueInput('A').setCheck('Number').appendField('round');
                this.appendValueInput('NDIGITS').setCheck('Number').appendField('digits');
                this.setInputsInline(true);
                this.setOutput(true, 'Number');
                this.setColour('#5B67A5');
            }
        };
        python.pythonGenerator.forBlock['py_round'] = function(block, generator) {
            const a = generator.valueToCode(block, 'A', python.Order.NONE) || '0';
            const n = generator.valueToCode(block, 'NDIGITS', python.Order.NONE) || '0';
            return ['round(' + a + ', ' + n + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_divmod'] = {
            init: function() {
                this.appendValueInput('A').setCheck('Number').appendField('divmod');
                this.appendValueInput('B').setCheck('Number');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#5B67A5');
            }
        };
        python.pythonGenerator.forBlock['py_divmod'] = function(block, generator) {
            const a = generator.valueToCode(block, 'A', python.Order.NONE) || '0';
            const b = generator.valueToCode(block, 'B', python.Order.NONE) || '1';
            return ['divmod(' + a + ', ' + b + ')', python.Order.FUNCTION_CALL];
        };

        // match/case — free-form cases for flexibility
        Blockly.Blocks['py_match'] = {
            init: function() {
                this.appendDummyInput()
                    .appendField('match')
                    .appendField(new Blockly.FieldTextInput('value'), 'SUBJECT');
                this.appendDummyInput()
                    .appendField(new Blockly.FieldMultilineInput('case 1:\\n    print("one")\\ncase _:\\n    print("other")'), 'CASES');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#8A6B9A');
                this.setTooltip('Python 3.10+ match/case. Edit cases as text; subject is an expression.');
            }
        };
        python.pythonGenerator.forBlock['py_match'] = function(block) {
            const subj = pySanitizeExprList(block.getFieldValue('SUBJECT') || 'value') || 'value';
            let cases = String(block.getFieldValue('CASES') || 'case _:\\n    pass');
            // normalize newlines from field
            cases = cases.replace(/\\r\\n/g, '\\n');
            const indented = cases.split('\\n').map(function(l) {
                return l.trim() === '' ? '' : (generatorIndent() + l);
            }).join('\\n');
            return 'match ' + subj + ':\\n' + indented + (indented.endsWith('\\n') ? '' : '\\n');
        };
        function generatorIndent() {
            try { return python.pythonGenerator.INDENT || '    '; } catch (e) { return '    '; }
        }
        // Fix py_match generator to not use broken escaping
        python.pythonGenerator.forBlock['py_match'] = function(block) {
            const subj = pySanitizeExprList(block.getFieldValue('SUBJECT') || 'value') || 'value';
            let cases = String(block.getFieldValue('CASES') || 'case _:\\n    pass');
            cases = cases.replace(/\\r\\n/g, '\\n');
            const ind = python.pythonGenerator.INDENT || '    ';
            const body = cases.split('\\n').map(function(l) {
                return ind + l;
            }).join('\\n');
            return 'match ' + subj + ':\\n' + body + '\\n';
        };

        Blockly.Blocks['py_walrus'] = {
            init: function() {
                this.appendValueInput('VALUE')
                    .appendField(new Blockly.FieldTextInput('n'), 'VAR')
                    .appendField(':=');
                this.setOutput(true);
                this.setColour('#8A6B9A');
                this.setTooltip('Walrus operator (assignment expression)');
            }
        };
        python.pythonGenerator.forBlock['py_walrus'] = function(block, generator) {
            const v = pySanitizeIdentifier(block.getFieldValue('VAR'), 'n');
            const val = generator.valueToCode(block, 'VALUE', python.Order.NONE) || 'None';
            return ['(' + v + ' := ' + val + ')', python.Order.NONE];
        };

        Blockly.Blocks['py_getitem'] = {
            init: function() {
                this.appendValueInput('OBJ');
                this.appendValueInput('KEY').appendField('[');
                this.appendDummyInput().appendField(']');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_getitem'] = function(block, generator) {
            const o = generator.valueToCode(block, 'OBJ', python.Order.MEMBER) || 'obj';
            const k = generator.valueToCode(block, 'KEY', python.Order.NONE) || '0';
            return [o + '[' + k + ']', python.Order.MEMBER];
        };

        Blockly.Blocks['py_setitem'] = {
            init: function() {
                this.appendValueInput('OBJ');
                this.appendValueInput('KEY').appendField('[');
                this.appendValueInput('VALUE').appendField('] =');
                this.setInputsInline(true);
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_setitem'] = function(block, generator) {
            const o = generator.valueToCode(block, 'OBJ', python.Order.MEMBER) || 'obj';
            const k = generator.valueToCode(block, 'KEY', python.Order.NONE) || '0';
            const v = generator.valueToCode(block, 'VALUE', python.Order.NONE) || 'None';
            return o + '[' + k + '] = ' + v + '\\n';
        };

        Blockly.Blocks['py_delitem'] = {
            init: function() {
                this.appendValueInput('OBJ').appendField('del');
                this.appendValueInput('KEY').appendField('[');
                this.appendDummyInput().appendField(']');
                this.setInputsInline(true);
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_delitem'] = function(block, generator) {
            const o = generator.valueToCode(block, 'OBJ', python.Order.MEMBER) || 'obj';
            const k = generator.valueToCode(block, 'KEY', python.Order.NONE) || '0';
            return 'del ' + o + '[' + k + ']\\n';
        };

        Blockly.Blocks['py_bool_op'] = {
            init: function() {
                this.appendValueInput('A');
                this.appendDummyInput().appendField(new Blockly.FieldDropdown([
                    ['and', 'and'], ['or', 'or'],
                ]), 'OP');
                this.appendValueInput('B');
                this.setInputsInline(true);
                this.setOutput(true, 'Boolean');
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_bool_op'] = function(block, generator) {
            const op = block.getFieldValue('OP') || 'and';
            const order = op === 'and' ? python.Order.LOGICAL_AND : python.Order.LOGICAL_OR;
            const a = generator.valueToCode(block, 'A', order) || 'False';
            const b = generator.valueToCode(block, 'B', order) || 'False';
            return [a + ' ' + op + ' ' + b, order];
        };

        Blockly.Blocks['py_is_none'] = {
            init: function() {
                this.appendValueInput('VALUE');
                this.appendDummyInput().appendField(new Blockly.FieldDropdown([
                    ['is None', 'is None'],
                    ['is not None', 'is not None'],
                ]), 'OP');
                this.setInputsInline(true);
                this.setOutput(true, 'Boolean');
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_is_none'] = function(block, generator) {
            const v = generator.valueToCode(block, 'VALUE', python.Order.RELATIONAL) || 'None';
            const op = block.getFieldValue('OP') || 'is None';
            return [v + ' ' + op, python.Order.RELATIONAL];
        };

        Blockly.Blocks['py_hasattr'] = {
            init: function() {
                this.appendValueInput('OBJ').appendField('hasattr');
                this.appendDummyInput().appendField(new Blockly.FieldTextInput('name'), 'ATTR');
                this.setInputsInline(true);
                this.setOutput(true, 'Boolean');
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_hasattr'] = function(block, generator) {
            const o = generator.valueToCode(block, 'OBJ', python.Order.NONE) || 'obj';
            const a = (block.getFieldValue('ATTR') || 'name').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
            return ['hasattr(' + o + ', \'' + a + '\')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_getattr_default'] = {
            init: function() {
                this.appendValueInput('OBJ').appendField('getattr');
                this.appendDummyInput().appendField(new Blockly.FieldTextInput('name'), 'ATTR');
                this.appendValueInput('DEFAULT').appendField('default');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_getattr_default'] = function(block, generator) {
            const o = generator.valueToCode(block, 'OBJ', python.Order.NONE) || 'obj';
            const a = (block.getFieldValue('ATTR') || 'name').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
            const d = generator.valueToCode(block, 'DEFAULT', python.Order.NONE) || 'None';
            return ['getattr(' + o + ', \'' + a + '\', ' + d + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_next'] = {
            init: function() {
                this.appendValueInput('ITER').appendField('next');
                this.appendValueInput('DEFAULT').appendField('default');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_next'] = function(block, generator) {
            const it = generator.valueToCode(block, 'ITER', python.Order.NONE) || 'iter([])';
            const d = generator.valueToCode(block, 'DEFAULT', python.Order.NONE);
            if (d) return ['next(' + it + ', ' + d + ')', python.Order.FUNCTION_CALL];
            return ['next(' + it + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_iter'] = {
            init: function() {
                this.appendValueInput('SEQ').appendField('iter');
                this.setOutput(true);
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_iter'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEQ', python.Order.NONE) || '[]';
            return ['iter(' + s + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_enumerate_val'] = {
            init: function() {
                this.appendValueInput('SEQ').appendField('enumerate');
                this.setOutput(true);
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_enumerate_val'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEQ', python.Order.NONE) || '[]';
            return ['enumerate(' + s + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_zip_val'] = {
            init: function() {
                this.appendValueInput('A').appendField('zip');
                this.appendValueInput('B');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_zip_val'] = function(block, generator) {
            const a = generator.valueToCode(block, 'A', python.Order.NONE) || '[]';
            const b = generator.valueToCode(block, 'B', python.Order.NONE) || '[]';
            return ['zip(' + a + ', ' + b + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_copy'] = {
            init: function() {
                this.appendValueInput('OBJ')
                    .appendField(new Blockly.FieldDropdown([
                        ['copy.copy', 'copy.copy'],
                        ['copy.deepcopy', 'copy.deepcopy'],
                    ]), 'FUNC');
                this.setOutput(true);
                this.setColour('#8A6B9A');
                this.setTooltip('Requires: import copy');
            }
        };
        python.pythonGenerator.forBlock['py_copy'] = function(block, generator) {
            const f = block.getFieldValue('FUNC') || 'copy.copy';
            const o = generator.valueToCode(block, 'OBJ', python.Order.NONE) || 'None';
            return [f + '(' + o + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_breakpoint'] = {
            init: function() {
                this.appendDummyInput().appendField('breakpoint()');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#8A6B9A');
                this.setTooltip('Python debugger breakpoint (may be limited in browser)');
            }
        };
        python.pythonGenerator.forBlock['py_breakpoint'] = function() {
            return 'breakpoint()\\n';
        };

        Blockly.Blocks['py_repr'] = {
            init: function() {
                this.appendValueInput('VALUE').appendField('repr');
                this.setOutput(true, 'String');
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_repr'] = function(block, generator) {
            const v = generator.valueToCode(block, 'VALUE', python.Order.NONE) || 'None';
            return ['repr(' + v + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_id_hash'] = {
            init: function() {
                this.appendValueInput('VALUE')
                    .appendField(new Blockly.FieldDropdown([
                        ['id', 'id'], ['hash', 'hash'], ['dir', 'dir'],
                    ]), 'FUNC');
                this.setOutput(true);
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_id_hash'] = function(block, generator) {
            const f = block.getFieldValue('FUNC') || 'id';
            const v = generator.valueToCode(block, 'VALUE', python.Order.NONE) || 'None';
            return [f + '(' + v + ')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_bytes_encode'] = {
            init: function() {
                this.appendValueInput('TEXT').setCheck('String').appendField('encode');
                this.appendDummyInput().appendField(new Blockly.FieldDropdown([
                    ['utf-8', 'utf-8'], ['ascii', 'ascii'], ['latin-1', 'latin-1'],
                ]), 'ENC');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_bytes_encode'] = function(block, generator) {
            const t = generator.valueToCode(block, 'TEXT', python.Order.MEMBER) || "''";
            const e = block.getFieldValue('ENC') || 'utf-8';
            return [t + '.encode(\'' + e + '\')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_bytes_decode'] = {
            init: function() {
                this.appendValueInput('DATA').appendField('decode');
                this.appendDummyInput().appendField(new Blockly.FieldDropdown([
                    ['utf-8', 'utf-8'], ['ascii', 'ascii'], ['latin-1', 'latin-1'],
                ]), 'ENC');
                this.setInputsInline(true);
                this.setOutput(true, 'String');
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_bytes_decode'] = function(block, generator) {
            const t = generator.valueToCode(block, 'DATA', python.Order.MEMBER) || "b''";
            const e = block.getFieldValue('ENC') || 'utf-8';
            return [t + '.decode(\'' + e + '\')', python.Order.FUNCTION_CALL];
        };

        Blockly.Blocks['py_dict_merge'] = {
            init: function() {
                this.appendValueInput('A').appendField('merge dicts');
                this.appendValueInput('B').appendField('|');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B9A');
                this.setTooltip('Python 3.9+ dict merge: a | b');
            }
        };
        python.pythonGenerator.forBlock['py_dict_merge'] = function(block, generator) {
            const a = generator.valueToCode(block, 'A', python.Order.NONE) || '{}';
            const b = generator.valueToCode(block, 'B', python.Order.NONE) || '{}';
            return ['(' + a + ' | ' + b + ')', python.Order.NONE];
        };

        Blockly.Blocks['py_list_repeat'] = {
            init: function() {
                this.appendValueInput('LIST').appendField('list *');
                this.appendValueInput('N').setCheck('Number');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_list_repeat'] = function(block, generator) {
            const l = generator.valueToCode(block, 'LIST', python.Order.MULTIPLICATIVE) || '[]';
            const n = generator.valueToCode(block, 'N', python.Order.MULTIPLICATIVE) || '1';
            return ['(' + l + ' * ' + n + ')', python.Order.MULTIPLICATIVE];
        };

        Blockly.Blocks['py_async_for'] = {
            init: function() {
                this.appendValueInput('LIST').appendField('async for')
                    .appendField(new Blockly.FieldVariable('item'), 'VAR')
                    .appendField('in');
                this.appendStatementInput('DO').appendField('do');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_async_for'] = function(block, generator) {
            const v = generator.getVariableName(block.getFieldValue('VAR'));
            const list = generator.valueToCode(block, 'LIST', python.Order.NONE) || '[]';
            const body = generator.statementToCode(block, 'DO') || generator.INDENT + 'pass\\n';
            return 'async for ' + v + ' in ' + list + ':\\n' + body;
        };

        Blockly.Blocks['py_async_with'] = {
            init: function() {
                this.appendValueInput('EXPR').appendField('async with');
                this.appendDummyInput().appendField('as')
                    .appendField(new Blockly.FieldVariable('ctx'), 'VAR');
                this.appendStatementInput('DO').appendField('do');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#8A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_async_with'] = function(block, generator) {
            const e = generator.valueToCode(block, 'EXPR', python.Order.NONE) || 'None';
            const v = generator.getVariableName(block.getFieldValue('VAR'));
            const body = generator.statementToCode(block, 'DO') || generator.INDENT + 'pass\\n';
            return 'async with ' + e + ' as ' + v + ':\\n' + body;
        };

        Blockly.Blocks['py_staticmethod'] = {
            init: function() {
                this.appendDummyInput().appendField('@staticmethod');
                this.appendStatementInput('DO');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#4A8A8A');
            }
        };
        python.pythonGenerator.forBlock['py_staticmethod'] = function(block, generator) {
            const body = generator.statementToCode(block, 'DO') || '';
            // decorate first def line if present
            if (!body.trim()) return '@staticmethod\\n';
            const lines = body.split('\\n');
            // statementToCode is already indented one level — strip one for decorator placement inside class
            return '@staticmethod\\n' + body;
        };

        Blockly.Blocks['py_classmethod'] = {
            init: function() {
                this.appendDummyInput().appendField('@classmethod');
                this.appendStatementInput('DO');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#4A8A8A');
            }
        };
        python.pythonGenerator.forBlock['py_classmethod'] = function(block, generator) {
            const body = generator.statementToCode(block, 'DO') || '';
            return '@classmethod\\n' + body;
        };

        Blockly.Blocks['py_property_def'] = {
            init: function() {
                this.appendDummyInput().appendField('@property');
                this.appendStatementInput('DO');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#4A8A8A');
            }
        };
        python.pythonGenerator.forBlock['py_property_def'] = function(block, generator) {
            const body = generator.statementToCode(block, 'DO') || '';
            return '@property\\n' + body;
        };

'''

# Fix escaped newlines in generators - in the file we need actual \n in JS strings
# The raw string above uses \\n which becomes \n in file = correct for JS string containing backslash-n
# For return '...\n' we need the JS source to have \n escape

theme = "        // ═══════════════════════════════════════════════════════════════════\n        //  BLOCKLY THEME & WORKSPACE"
# find first THEME marker after blocks
idx = t.find("//  BLOCKLY THEME & WORKSPACE")
if idx < 0:
    raise SystemExit("theme marker missing")
# go to line start
line_start = t.rfind("\n", 0, idx) + 1
# include the comment banner before theme if present
banner = t.rfind("═══════════════════════════════════════════════════════════════════", 0, idx)
if banner > 0:
    line_start = t.rfind("\n", 0, banner) + 1

# Clean defs: fix double-escaped issues in match and async generators
# Use proper JS \n in return statements by post-processing
defs_clean = defs.replace("return 'match ' + subj + ':\\n' + body + '\\n';",
                          "return 'match ' + subj + ':\\n' + body + (body.endsWith('\\n') ? '' : '\\n');")

# Actually in Python raw string, \\n in the output file is \n which is what we want for JS.

t = t[:line_start] + defs + "\n" + t[line_start:]

# Fix py_match generator - FieldMultilineInput might not exist in Blockly 12
# Use FieldTextInput multiline alternative - Blockly has FieldMultilineInput in recent versions
# Fallback: FieldTextInput with long string

if "FieldMultilineInput" in t:
    # replace with safer field if needed - keep and polyfill
    pass

# Polyfill FieldMultilineInput if missing - inject near block defs start
poly = r'''
        // Multiline field fallback for older Blockly builds
        if (typeof Blockly.FieldMultilineInput === 'undefined' && Blockly.FieldTextInput) {
            Blockly.FieldMultilineInput = Blockly.FieldTextInput;
        }

'''
if "FieldMultilineInput = Blockly.FieldTextInput" not in t:
    t = t.replace(
        "        // Soft-sanitize free-text fields",
        poly + "        // Soft-sanitize free-text fields",
        1,
    )

# Bump version
t = t.replace("var PYMASON_VERSION = '1.3.1';", "var PYMASON_VERSION = '1.4.0';")
t = t.replace("PYMASON_VERSION = '1.3.1';", "PYMASON_VERSION = '1.4.0';")

INDEX.write_text(t, encoding="utf-8")
print("Added toolbox + block defs, size", INDEX.stat().st_size)

# Quick count
import re
blocks = set(re.findall(r"Blockly\.Blocks\['(py_[^']+)'\]", t))
gens = set(re.findall(r"pythonGenerator\.forBlock\['(py_[^']+)'\]", t))
print("blocks", len(blocks), "gens", len(gens), "missing", sorted(blocks - gens)[:15])
