#!/usr/bin/env python3
"""Add another pack of PyMason blocks (idempotent)."""
from pathlib import Path
import re

INDEX = Path(__file__).resolve().parents[1] / "index.html"
t = INDEX.read_text(encoding="utf-8")

if "py_collections_counter" in t and 'category name="Collections"' in t:
    print("Even more blocks already present")
    raise SystemExit(0)

TOOLBOX = r'''
        <!-- ── Collections ──────────────────────────── -->
        <category name="Collections" colour="#7A6B9A">
            <block type="py_collections_counter"></block>
            <block type="py_collections_defaultdict">
                <field name="FACTORY">list</field>
            </block>
            <block type="py_collections_deque"></block>
            <block type="py_collections_namedtuple">
                <field name="NAME">Point</field>
                <field name="FIELDS">x y</field>
            </block>
            <block type="py_heapq_heappush"></block>
            <block type="py_heapq_heappop"></block>
            <block type="py_bisect_insort"></block>
        </category>

        <!-- ── Stats &amp; Math+ ────────────────────── -->
        <category name="Stats" colour="#5B8A9A">
            <block type="py_statistics_mean"></block>
            <block type="py_statistics_median"></block>
            <block type="py_statistics_mode"></block>
            <block type="py_statistics_stdev"></block>
            <block type="py_math_floor_ceil"></block>
            <block type="py_math_sqrt">
                <value name="X"><shadow type="math_number"><field name="NUM">9</field></shadow></value>
            </block>
            <block type="py_math_log">
                <value name="X"><shadow type="math_number"><field name="NUM">2.718</field></shadow></value>
            </block>
            <block type="py_math_trig">
                <value name="X"><shadow type="math_number"><field name="NUM">0</field></shadow></value>
            </block>
            <block type="py_math_degrees">
                <value name="X"><shadow type="math_number"><field name="NUM">3.14159</field></shadow></value>
            </block>
            <block type="py_math_clamp">
                <value name="X"><shadow type="math_number"><field name="NUM">5</field></shadow></value>
                <value name="LO"><shadow type="math_number"><field name="NUM">0</field></shadow></value>
                <value name="HI"><shadow type="math_number"><field name="NUM">10</field></shadow></value>
            </block>
        </category>

        <!-- ── Encode ───────────────────────────────── -->
        <category name="Encode" colour="#9A7A5B">
            <block type="py_base64_encode"></block>
            <block type="py_base64_decode"></block>
            <block type="py_json_pretty"></block>
            <block type="py_json_load_file"></block>
            <block type="py_json_dump_file"></block>
            <block type="py_csv_reader"></block>
            <block type="py_csv_writerow"></block>
            <block type="py_urllib_quote"></block>
            <block type="py_urllib_parse_qs"></block>
            <block type="py_hashlib_digest">
                <field name="ALG">sha256</field>
            </block>
            <block type="py_uuid4"></block>
            <block type="py_secrets_token"></block>
        </category>

        <!-- ── Text+ ────────────────────────────────── -->
        <category name="Text+" colour="#5BA58C">
            <block type="py_str_partition"></block>
            <block type="py_str_zfill">
                <value name="WIDTH"><shadow type="math_number"><field name="NUM">5</field></shadow></value>
            </block>
            <block type="py_str_removeprefix"></block>
            <block type="py_str_removesuffix"></block>
            <block type="py_str_expandtabs"></block>
            <block type="py_str_translate_simple"></block>
            <block type="py_chr"></block>
            <block type="py_ord"></block>
            <block type="py_str_mul">
                <value name="N"><shadow type="math_number"><field name="NUM">3</field></shadow></value>
            </block>
            <block type="py_str_center">
                <value name="WIDTH"><shadow type="math_number"><field name="NUM">20</field></shadow></value>
            </block>
            <block type="py_fstring_expr">
                <field name="EXPR">name</field>
                <field name="FMT"></field>
            </block>
        </category>

        <!-- ── Itertools ────────────────────────────── -->
        <category name="Itertools" colour="#8A6B7A">
            <block type="py_itertools_chain"></block>
            <block type="py_itertools_cycle"></block>
            <block type="py_itertools_repeat">
                <value name="N"><shadow type="math_number"><field name="NUM">3</field></shadow></value>
            </block>
            <block type="py_itertools_count">
                <value name="START"><shadow type="math_number"><field name="NUM">0</field></shadow></value>
            </block>
            <block type="py_itertools_islice">
                <value name="STOP"><shadow type="math_number"><field name="NUM">5</field></shadow></value>
            </block>
            <block type="py_itertools_product"></block>
            <block type="py_itertools_combinations">
                <value name="R"><shadow type="math_number"><field name="NUM">2</field></shadow></value>
            </block>
            <block type="py_itertools_permutations">
                <value name="R"><shadow type="math_number"><field name="NUM">2</field></shadow></value>
            </block>
            <block type="py_itertools_groupby"></block>
            <block type="py_functools_reduce"></block>
            <block type="py_functools_partial">
                <field name="FUNC">print</field>
            </block>
        </category>

        <!-- ── Web sketch ───────────────────────────── -->
        <category name="Web sketch" colour="#6B7A9A">
            <block type="py_http_get_sketch">
                <value name="URL"><shadow type="text"><field name="TEXT">https://example.com</field></shadow></value>
            </block>
            <block type="py_url_join">
                <value name="BASE"><shadow type="text"><field name="TEXT">https://api.example.com</field></shadow></value>
                <value name="PATH"><shadow type="text"><field name="TEXT">/v1/items</field></shadow></value>
            </block>
            <block type="py_html_escape"></block>
            <block type="py_query_build"></block>
            <block type="py_user_agent_header"></block>
        </category>

        <!-- ── Concurrency sketch ───────────────────── -->
        <category name="Concurrency" colour="#9A5B6B">
            <block type="py_threading_thread">
                <field name="TARGET">worker</field>
            </block>
            <block type="py_threading_start"></block>
            <block type="py_threading_join"></block>
            <block type="py_queue_queue"></block>
            <block type="py_queue_put"></block>
            <block type="py_queue_get"></block>
            <block type="py_asyncio_run"></block>
            <block type="py_asyncio_gather"></block>
            <block type="py_asyncio_sleep">
                <value name="SEC"><shadow type="math_number"><field name="NUM">0.1</field></shadow></value>
            </block>
        </category>

'''

anchor = '        <!-- ── Functions ───────────────────────────── -->'
if anchor not in t:
    # try after Advanced category - find last category before Functions
    if "<!-- ── Advanced" in t:
        # insert before Functions still
        pass
    if anchor not in t:
        raise SystemExit("Functions category anchor missing")
t = t.replace(anchor, TOOLBOX + "\n" + anchor, 1)

DEFS = r'''
        // ═══════════════════════════════════════════════════════════════
        //  EVEN MORE BLOCKS — Collections, Stats, Encode, Text+, Itertools
        // ═══════════════════════════════════════════════════════════════

        function _pyStrField(block, name, fallback) {
            return String(block.getFieldValue(name) || fallback || '')
                .replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        }
        function _pyOrderNone() {
            try { return python.Order.NONE; } catch (e) { return 99; }
        }
        function _pyOrderCall() {
            try { return python.Order.FUNCTION_CALL; } catch (e) { return 2; }
        }

        Blockly.Blocks['py_collections_counter'] = {
            init: function() {
                this.appendValueInput('SEQ').appendField('Counter');
                this.setOutput(true);
                this.setColour('#7A6B9A');
                this.setTooltip('collections.Counter(seq). Requires: from collections import Counter');
            }
        };
        python.pythonGenerator.forBlock['py_collections_counter'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEQ', _pyOrderNone()) || '[]';
            return ['Counter(' + s + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_collections_defaultdict'] = {
            init: function() {
                this.appendDummyInput()
                    .appendField('defaultdict')
                    .appendField(new Blockly.FieldDropdown([
                        ['list', 'list'], ['int', 'int'], ['set', 'set'], ['dict', 'dict'],
                    ]), 'FACTORY');
                this.setOutput(true);
                this.setColour('#7A6B9A');
                this.setTooltip('Requires: from collections import defaultdict');
            }
        };
        python.pythonGenerator.forBlock['py_collections_defaultdict'] = function(block) {
            const f = block.getFieldValue('FACTORY') || 'list';
            return ['defaultdict(' + f + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_collections_deque'] = {
            init: function() {
                this.appendValueInput('SEQ').appendField('deque');
                this.setOutput(true);
                this.setColour('#7A6B9A');
                this.setTooltip('Requires: from collections import deque');
            }
        };
        python.pythonGenerator.forBlock['py_collections_deque'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEQ', _pyOrderNone()) || '[]';
            return ['deque(' + s + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_collections_namedtuple'] = {
            init: function() {
                this.appendDummyInput()
                    .appendField('namedtuple')
                    .appendField(new Blockly.FieldTextInput('Point'), 'NAME')
                    .appendField(new Blockly.FieldTextInput('x y'), 'FIELDS');
                this.setOutput(true);
                this.setColour('#7A6B9A');
                this.setTooltip('Requires: from collections import namedtuple');
            }
        };
        python.pythonGenerator.forBlock['py_collections_namedtuple'] = function(block) {
            const n = _pyStrField(block, 'NAME', 'Point');
            const f = _pyStrField(block, 'FIELDS', 'x y');
            return ["namedtuple('" + n + "', '" + f + "')", _pyOrderCall()];
        };

        Blockly.Blocks['py_heapq_heappush'] = {
            init: function() {
                this.appendValueInput('HEAP').appendField('heappush');
                this.appendValueInput('ITEM').appendField('item');
                this.setInputsInline(true);
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#7A6B9A');
                this.setTooltip('Requires: import heapq');
            }
        };
        python.pythonGenerator.forBlock['py_heapq_heappush'] = function(block, generator) {
            const h = generator.valueToCode(block, 'HEAP', _pyOrderNone()) || '[]';
            const i = generator.valueToCode(block, 'ITEM', _pyOrderNone()) || '0';
            return 'heapq.heappush(' + h + ', ' + i + ')\n';
        };

        Blockly.Blocks['py_heapq_heappop'] = {
            init: function() {
                this.appendValueInput('HEAP').appendField('heappop');
                this.setOutput(true);
                this.setColour('#7A6B9A');
            }
        };
        python.pythonGenerator.forBlock['py_heapq_heappop'] = function(block, generator) {
            const h = generator.valueToCode(block, 'HEAP', _pyOrderNone()) || '[]';
            return ['heapq.heappop(' + h + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_bisect_insort'] = {
            init: function() {
                this.appendValueInput('LIST').appendField('bisect.insort');
                this.appendValueInput('ITEM').appendField('item');
                this.setInputsInline(true);
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#7A6B9A');
                this.setTooltip('Requires: import bisect');
            }
        };
        python.pythonGenerator.forBlock['py_bisect_insort'] = function(block, generator) {
            const l = generator.valueToCode(block, 'LIST', _pyOrderNone()) || '[]';
            const i = generator.valueToCode(block, 'ITEM', _pyOrderNone()) || '0';
            return 'bisect.insort(' + l + ', ' + i + ')\n';
        };

        Blockly.Blocks['py_statistics_mean'] = {
            init: function() {
                this.appendValueInput('DATA').appendField('statistics.mean');
                this.setOutput(true, 'Number');
                this.setColour('#5B8A9A');
                this.setTooltip('Requires: import statistics');
            }
        };
        python.pythonGenerator.forBlock['py_statistics_mean'] = function(block, generator) {
            const d = generator.valueToCode(block, 'DATA', _pyOrderNone()) || '[]';
            return ['statistics.mean(' + d + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_statistics_median'] = {
            init: function() {
                this.appendValueInput('DATA').appendField('statistics.median');
                this.setOutput(true, 'Number');
                this.setColour('#5B8A9A');
            }
        };
        python.pythonGenerator.forBlock['py_statistics_median'] = function(block, generator) {
            const d = generator.valueToCode(block, 'DATA', _pyOrderNone()) || '[]';
            return ['statistics.median(' + d + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_statistics_mode'] = {
            init: function() {
                this.appendValueInput('DATA').appendField('statistics.mode');
                this.setOutput(true);
                this.setColour('#5B8A9A');
            }
        };
        python.pythonGenerator.forBlock['py_statistics_mode'] = function(block, generator) {
            const d = generator.valueToCode(block, 'DATA', _pyOrderNone()) || '[]';
            return ['statistics.mode(' + d + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_statistics_stdev'] = {
            init: function() {
                this.appendValueInput('DATA').appendField('statistics.stdev');
                this.setOutput(true, 'Number');
                this.setColour('#5B8A9A');
            }
        };
        python.pythonGenerator.forBlock['py_statistics_stdev'] = function(block, generator) {
            const d = generator.valueToCode(block, 'DATA', _pyOrderNone()) || '[]';
            return ['statistics.stdev(' + d + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_math_floor_ceil'] = {
            init: function() {
                this.appendValueInput('X').setCheck('Number')
                    .appendField(new Blockly.FieldDropdown([
                        ['math.floor', 'math.floor'],
                        ['math.ceil', 'math.ceil'],
                        ['math.trunc', 'math.trunc'],
                    ]), 'FUNC');
                this.setOutput(true, 'Number');
                this.setColour('#5B8A9A');
                this.setTooltip('Requires: import math');
            }
        };
        python.pythonGenerator.forBlock['py_math_floor_ceil'] = function(block, generator) {
            const f = block.getFieldValue('FUNC') || 'math.floor';
            const x = generator.valueToCode(block, 'X', _pyOrderNone()) || '0';
            return [f + '(' + x + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_math_sqrt'] = {
            init: function() {
                this.appendValueInput('X').setCheck('Number').appendField('math.sqrt');
                this.setOutput(true, 'Number');
                this.setColour('#5B8A9A');
            }
        };
        python.pythonGenerator.forBlock['py_math_sqrt'] = function(block, generator) {
            const x = generator.valueToCode(block, 'X', _pyOrderNone()) || '0';
            return ['math.sqrt(' + x + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_math_log'] = {
            init: function() {
                this.appendValueInput('X').setCheck('Number')
                    .appendField(new Blockly.FieldDropdown([
                        ['math.log', 'math.log'],
                        ['math.log10', 'math.log10'],
                        ['math.log2', 'math.log2'],
                        ['math.exp', 'math.exp'],
                    ]), 'FUNC');
                this.setOutput(true, 'Number');
                this.setColour('#5B8A9A');
            }
        };
        python.pythonGenerator.forBlock['py_math_log'] = function(block, generator) {
            const f = block.getFieldValue('FUNC') || 'math.log';
            const x = generator.valueToCode(block, 'X', _pyOrderNone()) || '1';
            return [f + '(' + x + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_math_trig'] = {
            init: function() {
                this.appendValueInput('X').setCheck('Number')
                    .appendField(new Blockly.FieldDropdown([
                        ['math.sin', 'math.sin'],
                        ['math.cos', 'math.cos'],
                        ['math.tan', 'math.tan'],
                        ['math.asin', 'math.asin'],
                        ['math.acos', 'math.acos'],
                        ['math.atan', 'math.atan'],
                    ]), 'FUNC');
                this.setOutput(true, 'Number');
                this.setColour('#5B8A9A');
            }
        };
        python.pythonGenerator.forBlock['py_math_trig'] = function(block, generator) {
            const f = block.getFieldValue('FUNC') || 'math.sin';
            const x = generator.valueToCode(block, 'X', _pyOrderNone()) || '0';
            return [f + '(' + x + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_math_degrees'] = {
            init: function() {
                this.appendValueInput('X').setCheck('Number')
                    .appendField(new Blockly.FieldDropdown([
                        ['math.degrees', 'math.degrees'],
                        ['math.radians', 'math.radians'],
                    ]), 'FUNC');
                this.setOutput(true, 'Number');
                this.setColour('#5B8A9A');
            }
        };
        python.pythonGenerator.forBlock['py_math_degrees'] = function(block, generator) {
            const f = block.getFieldValue('FUNC') || 'math.degrees';
            const x = generator.valueToCode(block, 'X', _pyOrderNone()) || '0';
            return [f + '(' + x + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_math_clamp'] = {
            init: function() {
                this.appendValueInput('X').setCheck('Number').appendField('clamp');
                this.appendValueInput('LO').setCheck('Number').appendField('lo');
                this.appendValueInput('HI').setCheck('Number').appendField('hi');
                this.setInputsInline(true);
                this.setOutput(true, 'Number');
                this.setColour('#5B8A9A');
                this.setTooltip('min(max(x, lo), hi)');
            }
        };
        python.pythonGenerator.forBlock['py_math_clamp'] = function(block, generator) {
            const x = generator.valueToCode(block, 'X', _pyOrderNone()) || '0';
            const lo = generator.valueToCode(block, 'LO', _pyOrderNone()) || '0';
            const hi = generator.valueToCode(block, 'HI', _pyOrderNone()) || '1';
            return ['min(max(' + x + ', ' + lo + '), ' + hi + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_base64_encode'] = {
            init: function() {
                this.appendValueInput('DATA').appendField('base64.b64encode');
                this.setOutput(true);
                this.setColour('#9A7A5B');
                this.setTooltip('Requires: import base64 — input should be bytes');
            }
        };
        python.pythonGenerator.forBlock['py_base64_encode'] = function(block, generator) {
            const d = generator.valueToCode(block, 'DATA', _pyOrderNone()) || "b''";
            return ['base64.b64encode(' + d + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_base64_decode'] = {
            init: function() {
                this.appendValueInput('DATA').appendField('base64.b64decode');
                this.setOutput(true);
                this.setColour('#9A7A5B');
            }
        };
        python.pythonGenerator.forBlock['py_base64_decode'] = function(block, generator) {
            const d = generator.valueToCode(block, 'DATA', _pyOrderNone()) || "b''";
            return ['base64.b64decode(' + d + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_json_pretty'] = {
            init: function() {
                this.appendValueInput('OBJ').appendField('json.dumps pretty');
                this.setOutput(true, 'String');
                this.setColour('#9A7A5B');
                this.setTooltip('json.dumps(obj, indent=2). Requires: import json');
            }
        };
        python.pythonGenerator.forBlock['py_json_pretty'] = function(block, generator) {
            const o = generator.valueToCode(block, 'OBJ', _pyOrderNone()) || '{}';
            return ['json.dumps(' + o + ', indent=2)', _pyOrderCall()];
        };

        Blockly.Blocks['py_json_load_file'] = {
            init: function() {
                this.appendValueInput('PATH').setCheck('String').appendField('json.load file');
                this.setOutput(true);
                this.setColour('#9A7A5B');
            }
        };
        python.pythonGenerator.forBlock['py_json_load_file'] = function(block, generator) {
            const p = generator.valueToCode(block, 'PATH', _pyOrderNone()) || "'data.json'";
            return ['json.load(open(' + p + ', encoding="utf-8"))', _pyOrderCall()];
        };

        Blockly.Blocks['py_json_dump_file'] = {
            init: function() {
                this.appendValueInput('OBJ').appendField('json.dump');
                this.appendValueInput('PATH').setCheck('String').appendField('to file');
                this.setInputsInline(true);
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#9A7A5B');
            }
        };
        python.pythonGenerator.forBlock['py_json_dump_file'] = function(block, generator) {
            const o = generator.valueToCode(block, 'OBJ', _pyOrderNone()) || '{}';
            const p = generator.valueToCode(block, 'PATH', _pyOrderNone()) || "'out.json'";
            return 'json.dump(' + o + ', open(' + p + ', "w", encoding="utf-8"), indent=2)\n';
        };

        Blockly.Blocks['py_csv_reader'] = {
            init: function() {
                this.appendValueInput('PATH').setCheck('String').appendField('csv.reader file');
                this.setOutput(true);
                this.setColour('#9A7A5B');
                this.setTooltip('list(csv.reader(...)). Requires: import csv');
            }
        };
        python.pythonGenerator.forBlock['py_csv_reader'] = function(block, generator) {
            const p = generator.valueToCode(block, 'PATH', _pyOrderNone()) || "'data.csv'";
            return ['list(csv.reader(open(' + p + ', newline="", encoding="utf-8")))', _pyOrderCall()];
        };

        Blockly.Blocks['py_csv_writerow'] = {
            init: function() {
                this.appendValueInput('PATH').setCheck('String').appendField('csv.writerow to');
                this.appendValueInput('ROW').appendField('row');
                this.setInputsInline(true);
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#9A7A5B');
            }
        };
        python.pythonGenerator.forBlock['py_csv_writerow'] = function(block, generator) {
            const p = generator.valueToCode(block, 'PATH', _pyOrderNone()) || "'out.csv'";
            const r = generator.valueToCode(block, 'ROW', _pyOrderNone()) || '[]';
            return 'csv.writer(open(' + p + ', "a", newline="", encoding="utf-8")).writerow(' + r + ')\n';
        };

        Blockly.Blocks['py_urllib_quote'] = {
            init: function() {
                this.appendValueInput('TEXT').setCheck('String').appendField('urllib.parse.quote');
                this.setOutput(true, 'String');
                this.setColour('#9A7A5B');
                this.setTooltip('Requires: from urllib.parse import quote');
            }
        };
        python.pythonGenerator.forBlock['py_urllib_quote'] = function(block, generator) {
            const s = generator.valueToCode(block, 'TEXT', _pyOrderNone()) || "''";
            return ['quote(' + s + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_urllib_parse_qs'] = {
            init: function() {
                this.appendValueInput('TEXT').setCheck('String').appendField('parse_qs');
                this.setOutput(true);
                this.setColour('#9A7A5B');
                this.setTooltip('Requires: from urllib.parse import parse_qs');
            }
        };
        python.pythonGenerator.forBlock['py_urllib_parse_qs'] = function(block, generator) {
            const s = generator.valueToCode(block, 'TEXT', _pyOrderNone()) || "''";
            return ['parse_qs(' + s + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_hashlib_digest'] = {
            init: function() {
                this.appendValueInput('DATA').appendField(
                    new Blockly.FieldDropdown([
                        ['sha256', 'sha256'],
                        ['md5', 'md5'],
                        ['sha1', 'sha1'],
                        ['sha512', 'sha512'],
                    ]), 'ALG'
                ).appendField('hexdigest');
                this.setOutput(true, 'String');
                this.setColour('#9A7A5B');
                this.setTooltip('Requires: import hashlib — DATA should be bytes');
            }
        };
        python.pythonGenerator.forBlock['py_hashlib_digest'] = function(block, generator) {
            const alg = block.getFieldValue('ALG') || 'sha256';
            const d = generator.valueToCode(block, 'DATA', _pyOrderNone()) || "b''";
            return ['hashlib.' + alg + '(' + d + ').hexdigest()', _pyOrderCall()];
        };

        Blockly.Blocks['py_uuid4'] = {
            init: function() {
                this.appendDummyInput().appendField('uuid.uuid4()');
                this.setOutput(true);
                this.setColour('#9A7A5B');
                this.setTooltip('Requires: import uuid');
            }
        };
        python.pythonGenerator.forBlock['py_uuid4'] = function() {
            return ['uuid.uuid4()', _pyOrderCall()];
        };

        Blockly.Blocks['py_secrets_token'] = {
            init: function() {
                this.appendDummyInput()
                    .appendField(new Blockly.FieldDropdown([
                        ['secrets.token_hex', 'token_hex'],
                        ['secrets.token_urlsafe', 'token_urlsafe'],
                    ]), 'FUNC')
                    .appendField(new Blockly.FieldNumber(16, 1, 128), 'N');
                this.setOutput(true, 'String');
                this.setColour('#9A7A5B');
                this.setTooltip('Requires: import secrets');
            }
        };
        python.pythonGenerator.forBlock['py_secrets_token'] = function(block) {
            const f = block.getFieldValue('FUNC') || 'token_hex';
            const n = block.getFieldValue('N') || 16;
            return ['secrets.' + f + '(' + n + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_str_partition'] = {
            init: function() {
                this.appendValueInput('TEXT').setCheck('String');
                this.appendDummyInput()
                    .appendField(new Blockly.FieldDropdown([
                        ['.partition', 'partition'],
                        ['.rpartition', 'rpartition'],
                    ]), 'METH');
                this.appendValueInput('SEP').setCheck('String');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#5BA58C');
            }
        };
        python.pythonGenerator.forBlock['py_str_partition'] = function(block, generator) {
            const t = generator.valueToCode(block, 'TEXT', python.Order.MEMBER || _pyOrderNone()) || "''";
            const m = block.getFieldValue('METH') || 'partition';
            const s = generator.valueToCode(block, 'SEP', _pyOrderNone()) || "' '";
            return [t + '.' + m + '(' + s + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_str_zfill'] = {
            init: function() {
                this.appendValueInput('TEXT').setCheck('String').appendField('zfill');
                this.appendValueInput('WIDTH').setCheck('Number');
                this.setInputsInline(true);
                this.setOutput(true, 'String');
                this.setColour('#5BA58C');
            }
        };
        python.pythonGenerator.forBlock['py_str_zfill'] = function(block, generator) {
            const t = generator.valueToCode(block, 'TEXT', python.Order.MEMBER || _pyOrderNone()) || "''";
            const w = generator.valueToCode(block, 'WIDTH', _pyOrderNone()) || '0';
            return [t + '.zfill(' + w + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_str_removeprefix'] = {
            init: function() {
                this.appendValueInput('TEXT').setCheck('String')
                    .appendField(new Blockly.FieldDropdown([
                        ['.removeprefix', 'removeprefix'],
                        ['.removesuffix', 'removesuffix'],
                    ]), 'METH');
                this.appendValueInput('FIX').setCheck('String');
                this.setInputsInline(true);
                this.setOutput(true, 'String');
                this.setColour('#5BA58C');
            }
        };
        python.pythonGenerator.forBlock['py_str_removeprefix'] = function(block, generator) {
            const t = generator.valueToCode(block, 'TEXT', python.Order.MEMBER || _pyOrderNone()) || "''";
            const m = block.getFieldValue('METH') || 'removeprefix';
            const f = generator.valueToCode(block, 'FIX', _pyOrderNone()) || "''";
            return [t + '.' + m + '(' + f + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_str_removesuffix'] = {
            init: function() {
                this.appendValueInput('TEXT').setCheck('String').appendField('.removesuffix');
                this.appendValueInput('FIX').setCheck('String');
                this.setInputsInline(true);
                this.setOutput(true, 'String');
                this.setColour('#5BA58C');
            }
        };
        python.pythonGenerator.forBlock['py_str_removesuffix'] = function(block, generator) {
            const t = generator.valueToCode(block, 'TEXT', python.Order.MEMBER || _pyOrderNone()) || "''";
            const f = generator.valueToCode(block, 'FIX', _pyOrderNone()) || "''";
            return [t + '.removesuffix(' + f + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_str_expandtabs'] = {
            init: function() {
                this.appendValueInput('TEXT').setCheck('String').appendField('expandtabs');
                this.setOutput(true, 'String');
                this.setColour('#5BA58C');
            }
        };
        python.pythonGenerator.forBlock['py_str_expandtabs'] = function(block, generator) {
            const t = generator.valueToCode(block, 'TEXT', python.Order.MEMBER || _pyOrderNone()) || "''";
            return [t + '.expandtabs()', _pyOrderCall()];
        };

        Blockly.Blocks['py_str_translate_simple'] = {
            init: function() {
                this.appendValueInput('TEXT').setCheck('String').appendField('replace all');
                this.appendValueInput('OLD').setCheck('String').appendField('of');
                this.appendValueInput('NEW').setCheck('String').appendField('with');
                this.setInputsInline(true);
                this.setOutput(true, 'String');
                this.setColour('#5BA58C');
                this.setTooltip('str.replace (global)');
            }
        };
        python.pythonGenerator.forBlock['py_str_translate_simple'] = function(block, generator) {
            const t = generator.valueToCode(block, 'TEXT', python.Order.MEMBER || _pyOrderNone()) || "''";
            const o = generator.valueToCode(block, 'OLD', _pyOrderNone()) || "''";
            const n = generator.valueToCode(block, 'NEW', _pyOrderNone()) || "''";
            return [t + '.replace(' + o + ', ' + n + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_chr'] = {
            init: function() {
                this.appendValueInput('N').setCheck('Number').appendField('chr');
                this.setOutput(true, 'String');
                this.setColour('#5BA58C');
            }
        };
        python.pythonGenerator.forBlock['py_chr'] = function(block, generator) {
            const n = generator.valueToCode(block, 'N', _pyOrderNone()) || '65';
            return ['chr(' + n + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_ord'] = {
            init: function() {
                this.appendValueInput('C').setCheck('String').appendField('ord');
                this.setOutput(true, 'Number');
                this.setColour('#5BA58C');
            }
        };
        python.pythonGenerator.forBlock['py_ord'] = function(block, generator) {
            const c = generator.valueToCode(block, 'C', _pyOrderNone()) || "'A'";
            return ['ord(' + c + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_str_mul'] = {
            init: function() {
                this.appendValueInput('TEXT').setCheck('String').appendField('str *');
                this.appendValueInput('N').setCheck('Number');
                this.setInputsInline(true);
                this.setOutput(true, 'String');
                this.setColour('#5BA58C');
            }
        };
        python.pythonGenerator.forBlock['py_str_mul'] = function(block, generator) {
            const t = generator.valueToCode(block, 'TEXT', _pyOrderNone()) || "''";
            const n = generator.valueToCode(block, 'N', _pyOrderNone()) || '1';
            return ['(' + t + ' * ' + n + ')', _pyOrderNone()];
        };

        Blockly.Blocks['py_str_center'] = {
            init: function() {
                this.appendValueInput('TEXT').setCheck('String').appendField('center');
                this.appendValueInput('WIDTH').setCheck('Number');
                this.setInputsInline(true);
                this.setOutput(true, 'String');
                this.setColour('#5BA58C');
            }
        };
        python.pythonGenerator.forBlock['py_str_center'] = function(block, generator) {
            const t = generator.valueToCode(block, 'TEXT', python.Order.MEMBER || _pyOrderNone()) || "''";
            const w = generator.valueToCode(block, 'WIDTH', _pyOrderNone()) || '10';
            return [t + '.center(' + w + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_fstring_expr'] = {
            init: function() {
                this.appendDummyInput()
                    .appendField('f"{')
                    .appendField(new Blockly.FieldTextInput('name'), 'EXPR')
                    .appendField(':')
                    .appendField(new Blockly.FieldTextInput(''), 'FMT')
                    .appendField('}"');
                this.setOutput(true, 'String');
                this.setColour('#5BA58C');
                this.setTooltip('Simple f-string fragment');
            }
        };
        python.pythonGenerator.forBlock['py_fstring_expr'] = function(block) {
            const e = pySanitizeExprList(block.getFieldValue('EXPR') || 'x') || 'x';
            const f = String(block.getFieldValue('FMT') || '').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
            if (f) return ["f'{" + e + ':' + f + "}'", _pyOrderNone()];
            return ["f'{" + e + "}'", _pyOrderNone()];
        };

        Blockly.Blocks['py_itertools_chain'] = {
            init: function() {
                this.appendValueInput('A').appendField('itertools.chain');
                this.appendValueInput('B');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B7A');
                this.setTooltip('Requires: import itertools');
            }
        };
        python.pythonGenerator.forBlock['py_itertools_chain'] = function(block, generator) {
            const a = generator.valueToCode(block, 'A', _pyOrderNone()) || '[]';
            const b = generator.valueToCode(block, 'B', _pyOrderNone()) || '[]';
            return ['itertools.chain(' + a + ', ' + b + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_itertools_cycle'] = {
            init: function() {
                this.appendValueInput('SEQ').appendField('itertools.cycle');
                this.setOutput(true);
                this.setColour('#8A6B7A');
            }
        };
        python.pythonGenerator.forBlock['py_itertools_cycle'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEQ', _pyOrderNone()) || '[]';
            return ['itertools.cycle(' + s + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_itertools_repeat'] = {
            init: function() {
                this.appendValueInput('VAL').appendField('itertools.repeat');
                this.appendValueInput('N').setCheck('Number').appendField('times');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B7A');
            }
        };
        python.pythonGenerator.forBlock['py_itertools_repeat'] = function(block, generator) {
            const v = generator.valueToCode(block, 'VAL', _pyOrderNone()) || 'None';
            const n = generator.valueToCode(block, 'N', _pyOrderNone()) || 'None';
            return ['itertools.repeat(' + v + ', ' + n + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_itertools_count'] = {
            init: function() {
                this.appendValueInput('START').setCheck('Number').appendField('itertools.count');
                this.setOutput(true);
                this.setColour('#8A6B7A');
            }
        };
        python.pythonGenerator.forBlock['py_itertools_count'] = function(block, generator) {
            const s = generator.valueToCode(block, 'START', _pyOrderNone()) || '0';
            return ['itertools.count(' + s + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_itertools_islice'] = {
            init: function() {
                this.appendValueInput('SEQ').appendField('itertools.islice');
                this.appendValueInput('STOP').setCheck('Number').appendField('stop');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B7A');
            }
        };
        python.pythonGenerator.forBlock['py_itertools_islice'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEQ', _pyOrderNone()) || '[]';
            const n = generator.valueToCode(block, 'STOP', _pyOrderNone()) || '5';
            return ['itertools.islice(' + s + ', ' + n + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_itertools_product'] = {
            init: function() {
                this.appendValueInput('A').appendField('itertools.product');
                this.appendValueInput('B');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B7A');
            }
        };
        python.pythonGenerator.forBlock['py_itertools_product'] = function(block, generator) {
            const a = generator.valueToCode(block, 'A', _pyOrderNone()) || '[]';
            const b = generator.valueToCode(block, 'B', _pyOrderNone()) || '[]';
            return ['itertools.product(' + a + ', ' + b + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_itertools_combinations'] = {
            init: function() {
                this.appendValueInput('SEQ').appendField('itertools.combinations');
                this.appendValueInput('R').setCheck('Number').appendField('r');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B7A');
            }
        };
        python.pythonGenerator.forBlock['py_itertools_combinations'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEQ', _pyOrderNone()) || '[]';
            const r = generator.valueToCode(block, 'R', _pyOrderNone()) || '2';
            return ['itertools.combinations(' + s + ', ' + r + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_itertools_permutations'] = {
            init: function() {
                this.appendValueInput('SEQ').appendField('itertools.permutations');
                this.appendValueInput('R').setCheck('Number').appendField('r');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B7A');
            }
        };
        python.pythonGenerator.forBlock['py_itertools_permutations'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEQ', _pyOrderNone()) || '[]';
            const r = generator.valueToCode(block, 'R', _pyOrderNone()) || '2';
            return ['itertools.permutations(' + s + ', ' + r + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_itertools_groupby'] = {
            init: function() {
                this.appendValueInput('SEQ').appendField('itertools.groupby');
                this.setOutput(true);
                this.setColour('#8A6B7A');
            }
        };
        python.pythonGenerator.forBlock['py_itertools_groupby'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEQ', _pyOrderNone()) || '[]';
            return ['itertools.groupby(' + s + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_functools_reduce'] = {
            init: function() {
                this.appendValueInput('FUNC').appendField('functools.reduce');
                this.appendValueInput('SEQ').appendField('over');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B7A');
                this.setTooltip('Requires: import functools — FUNC should be a 2-arg callable');
            }
        };
        python.pythonGenerator.forBlock['py_functools_reduce'] = function(block, generator) {
            const f = generator.valueToCode(block, 'FUNC', _pyOrderNone()) || 'lambda a, b: a';
            const s = generator.valueToCode(block, 'SEQ', _pyOrderNone()) || '[]';
            return ['functools.reduce(' + f + ', ' + s + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_functools_partial'] = {
            init: function() {
                this.appendDummyInput()
                    .appendField('functools.partial')
                    .appendField(new Blockly.FieldTextInput('print'), 'FUNC');
                this.appendValueInput('ARG').appendField('arg');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#8A6B7A');
            }
        };
        python.pythonGenerator.forBlock['py_functools_partial'] = function(block, generator) {
            const f = pySanitizeExprList(block.getFieldValue('FUNC') || 'print') || 'print';
            const a = generator.valueToCode(block, 'ARG', _pyOrderNone()) || 'None';
            return ['functools.partial(' + f + ', ' + a + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_http_get_sketch'] = {
            init: function() {
                this.appendValueInput('URL').setCheck('String').appendField('HTTP GET sketch');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#6B7A9A');
                this.setTooltip('Sketch only — prints intent. Use requests outside browser sandbox.');
            }
        };
        python.pythonGenerator.forBlock['py_http_get_sketch'] = function(block, generator) {
            const u = generator.valueToCode(block, 'URL', _pyOrderNone()) || "''";
            return 'print("GET", ' + u + ')  # sketch: replace with requests.get in desktop Python\\n';
        };

        Blockly.Blocks['py_url_join'] = {
            init: function() {
                this.appendValueInput('BASE').setCheck('String').appendField('urljoin');
                this.appendValueInput('PATH').setCheck('String');
                this.setInputsInline(true);
                this.setOutput(true, 'String');
                this.setColour('#6B7A9A');
                this.setTooltip('Requires: from urllib.parse import urljoin');
            }
        };
        python.pythonGenerator.forBlock['py_url_join'] = function(block, generator) {
            const a = generator.valueToCode(block, 'BASE', _pyOrderNone()) || "''";
            const b = generator.valueToCode(block, 'PATH', _pyOrderNone()) || "''";
            return ['urljoin(' + a + ', ' + b + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_html_escape'] = {
            init: function() {
                this.appendValueInput('TEXT').setCheck('String').appendField('html.escape');
                this.setOutput(true, 'String');
                this.setColour('#6B7A9A');
                this.setTooltip('Requires: import html');
            }
        };
        python.pythonGenerator.forBlock['py_html_escape'] = function(block, generator) {
            const s = generator.valueToCode(block, 'TEXT', _pyOrderNone()) || "''";
            return ['html.escape(' + s + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_query_build'] = {
            init: function() {
                this.appendValueInput('DICT').appendField('urlencode');
                this.setOutput(true, 'String');
                this.setColour('#6B7A9A');
                this.setTooltip('Requires: from urllib.parse import urlencode');
            }
        };
        python.pythonGenerator.forBlock['py_query_build'] = function(block, generator) {
            const d = generator.valueToCode(block, 'DICT', _pyOrderNone()) || '{}';
            return ['urlencode(' + d + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_user_agent_header'] = {
            init: function() {
                this.appendDummyInput().appendField('headers User-Agent PyMason');
                this.setOutput(true);
                this.setColour('#6B7A9A');
            }
        };
        python.pythonGenerator.forBlock['py_user_agent_header'] = function() {
            return ['{"User-Agent": "PyMason/1.4"}', _pyOrderNone()];
        };

        Blockly.Blocks['py_threading_thread'] = {
            init: function() {
                this.appendDummyInput()
                    .appendField('Thread target=')
                    .appendField(new Blockly.FieldTextInput('worker'), 'TARGET');
                this.setOutput(true);
                this.setColour('#9A5B6B');
                this.setTooltip('Requires: import threading — target is a function name');
            }
        };
        python.pythonGenerator.forBlock['py_threading_thread'] = function(block) {
            const t = pySanitizeIdentifier(block.getFieldValue('TARGET'), 'worker');
            return ['threading.Thread(target=' + t + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_threading_start'] = {
            init: function() {
                this.appendValueInput('THREAD').appendField('thread.start');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#9A5B6B');
            }
        };
        python.pythonGenerator.forBlock['py_threading_start'] = function(block, generator) {
            const t = generator.valueToCode(block, 'THREAD', python.Order.MEMBER || _pyOrderNone()) || 't';
            return t + '.start()\\n';
        };

        Blockly.Blocks['py_threading_join'] = {
            init: function() {
                this.appendValueInput('THREAD').appendField('thread.join');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#9A5B6B');
            }
        };
        python.pythonGenerator.forBlock['py_threading_join'] = function(block, generator) {
            const t = generator.valueToCode(block, 'THREAD', python.Order.MEMBER || _pyOrderNone()) || 't';
            return t + '.join()\\n';
        };

        Blockly.Blocks['py_queue_queue'] = {
            init: function() {
                this.appendDummyInput().appendField('queue.Queue()');
                this.setOutput(true);
                this.setColour('#9A5B6B');
                this.setTooltip('Requires: import queue');
            }
        };
        python.pythonGenerator.forBlock['py_queue_queue'] = function() {
            return ['queue.Queue()', _pyOrderCall()];
        };

        Blockly.Blocks['py_queue_put'] = {
            init: function() {
                this.appendValueInput('Q').appendField('queue.put');
                this.appendValueInput('ITEM').appendField('item');
                this.setInputsInline(true);
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#9A5B6B');
            }
        };
        python.pythonGenerator.forBlock['py_queue_put'] = function(block, generator) {
            const q = generator.valueToCode(block, 'Q', python.Order.MEMBER || _pyOrderNone()) || 'q';
            const i = generator.valueToCode(block, 'ITEM', _pyOrderNone()) || 'None';
            return q + '.put(' + i + ')\\n';
        };

        Blockly.Blocks['py_queue_get'] = {
            init: function() {
                this.appendValueInput('Q').appendField('queue.get');
                this.setOutput(true);
                this.setColour('#9A5B6B');
            }
        };
        python.pythonGenerator.forBlock['py_queue_get'] = function(block, generator) {
            const q = generator.valueToCode(block, 'Q', python.Order.MEMBER || _pyOrderNone()) || 'q';
            return [q + '.get()', _pyOrderCall()];
        };

        Blockly.Blocks['py_asyncio_run'] = {
            init: function() {
                this.appendValueInput('CORO').appendField('asyncio.run');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#9A5B6B');
                this.setTooltip('Requires: import asyncio');
            }
        };
        python.pythonGenerator.forBlock['py_asyncio_run'] = function(block, generator) {
            const c = generator.valueToCode(block, 'CORO', _pyOrderNone()) || 'None';
            return 'asyncio.run(' + c + ')\\n';
        };

        Blockly.Blocks['py_asyncio_gather'] = {
            init: function() {
                this.appendValueInput('A').appendField('asyncio.gather');
                this.appendValueInput('B');
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour('#9A5B6B');
            }
        };
        python.pythonGenerator.forBlock['py_asyncio_gather'] = function(block, generator) {
            const a = generator.valueToCode(block, 'A', _pyOrderNone()) || 'None';
            const b = generator.valueToCode(block, 'B', _pyOrderNone()) || 'None';
            return ['asyncio.gather(' + a + ', ' + b + ')', _pyOrderCall()];
        };

        Blockly.Blocks['py_asyncio_sleep'] = {
            init: function() {
                this.appendValueInput('SEC').setCheck('Number').appendField('await asyncio.sleep');
                this.setPreviousStatement(true); this.setNextStatement(true);
                this.setColour('#9A5B6B');
            }
        };
        python.pythonGenerator.forBlock['py_asyncio_sleep'] = function(block, generator) {
            const s = generator.valueToCode(block, 'SEC', _pyOrderNone()) || '0';
            return 'await asyncio.sleep(' + s + ')\\n';
        };

'''

# Insert defs before theme
marker = "//  BLOCKLY THEME & WORKSPACE"
idx = t.find(marker)
if idx < 0:
    raise SystemExit("theme marker missing")
line_start = t.rfind("\n", 0, idx)
# include banner lines
banner = t.rfind("════", 0, idx)
if banner > 0:
    line_start = t.rfind("\n", 0, banner)

t = t[: line_start + 1] + DEFS + "\n" + t[line_start + 1 :]

t = t.replace("var PYMASON_VERSION = '1.4.0';", "var PYMASON_VERSION = '1.5.0';")
t = t.replace("PYMASON_VERSION = '1.4.0';", "PYMASON_VERSION = '1.5.0';")

INDEX.write_text(t, encoding="utf-8")
blocks = set(re.findall(r"Blockly\.Blocks\['(py_[^']+)'\]", t))
gens = set(re.findall(r"pythonGenerator\.forBlock\['(py_[^']+)'\]", t))
print("blocks", len(blocks), "gens", len(gens))
print("missing gens", sorted(blocks - gens)[:20])
print("written", INDEX.stat().st_size)
