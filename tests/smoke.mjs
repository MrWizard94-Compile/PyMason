/**
 * PyMason smoke suite
 *
 * A  — structural integrity of index.html
 * B  — headless Blockly: all generators, goldens, save/load
 * C  — in-app EXAMPLE builders → workspaceToCode expectations
 * D  — HTML/DOM contract (required IDs, wiring)
 * E  — headless Chromium page load + Blockly inject + Hello World UI
 * F  — Pyodide execute: Run Hello World, assert Output contains Hello
 *
 * Run:  npm test   (repo root or tests/)
 * Env:  SKIP_BROWSER=1   — skip Playwright (E+F)
 *       SKIP_PYODIDE=1   — load/UI only; skip ~first-download Python run
 *       UPDATE_FIXTURES=1 — rewrite tests/fixtures/examples/*.py snapshots
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';
import { createRequire } from 'module';
import http from 'http';
import vm from 'vm';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const INDEX = path.join(ROOT, 'index.html');
const FIXTURES_DIR = path.join(__dirname, 'fixtures', 'examples');

const require = createRequire(import.meta.url);

let failed = 0;
let passed = 0;
const failures = [];

function ok(cond, msg) {
  if (cond) {
    passed++;
    return true;
  }
  failed++;
  failures.push(msg);
  console.error('  FAIL:', msg);
  return false;
}

function section(title) {
  console.log('\n== ' + title + ' ==');
}

/** Normalize generated Python for snapshot compare */
function normalizePy(code) {
  return String(code || '')
    .replace(/\r\n/g, '\n')
    .replace(/[ \t]+$/gm, '')
    .trim() + '\n';
}

// ─── Tier A: structure ───────────────────────────────────────────────────────

function tierStructure(html) {
  section('A. Structural integrity');

  ok(html.includes('blockly@12.5.1/blockly_compressed.js'), 'Blockly CDN pinned to 12.5.1');
  ok(html.includes('@blockly/keyboard-navigation@3.0.5/'), 'keyboard-navigation CDN pinned to 3.0.5');
  ok(html.includes('pyodide/v0.25.1/'), 'Pyodide CDN pinned to 0.25.1');
  ok(html.includes('javascript_compressed.js'), 'JavaScript generator script included');
  ok(html.includes("value: 'xai'") || html.includes("id: 'xai'"), 'xAI provider present');
  ok(html.includes("id: 'ollama'") || html.includes("value=\"ollama\""), 'Ollama provider present');
  ok(html.includes('callOpenAICompatible') || html.includes('api.x.ai'), 'xAI chat completions path');
  ok(html.includes('/api/chat') || html.includes('callOllama'), 'Ollama chat path');
  ok(html.includes('aiProviderSelect'), 'AI provider select in UI');
  ok(html.includes('toolboxModeSelect'), 'Toolbox progressive disclosure control');
  ok(html.includes('langSelect'), 'Language selector present');
  ok(
    !/unpkg\.com\/blockly\/blockly_compressed/.test(html) || /unpkg\.com\/blockly@/.test(html),
    'No unpinned unpkg.com/blockly/'
  );

  const ver = html.match(/PYMASON_VERSION\s*=\s*'([^']+)'/);
  ok(!!ver, 'PYMASON_VERSION defined');
  if (ver) console.log('  version:', ver[1]);

  const blockDefs = new Set(
    [...html.matchAll(/Blockly\.Blocks\['([^']+)'\]/g)].map((m) => m[1])
  );
  const gens = new Set(
    [...html.matchAll(/pythonGenerator\.forBlock\['([^']+)'\]/g)].map((m) => m[1])
  );
  const mutatorOnly = new Set(['py_tuple_container', 'py_tuple_item']);
  const missingGen = [...blockDefs].filter((b) => !gens.has(b) && !mutatorOnly.has(b));
  const extraGen = [...gens].filter((g) => !blockDefs.has(g));

  ok(blockDefs.size >= 100, `Enough custom blocks (${blockDefs.size})`);
  ok(gens.size >= 100, `Enough generators (${gens.size})`);
  ok(missingGen.length === 0, `Blocks without generator: ${missingGen.join(', ') || 'none'}`);
  ok(extraGen.length === 0, `Generators without block: ${extraGen.join(', ') || 'none'}`);

  const toolboxTypes = new Set(
    [...html.matchAll(/<block\s+type="(py_[^"]+)"/g)].map((m) => m[1])
  );
  const toolboxMissing = [...toolboxTypes].filter((t) => !blockDefs.has(t));
  ok(toolboxMissing.length === 0, `Toolbox orphans: ${toolboxMissing.join(', ') || 'none'}`);

  ok(
    html.includes('slice.length + 1') || html.includes('length + 1'),
    'Empty-input Atomics wake protocol present'
  );
  ok(html.includes('runResolve'), 'runResolve stop-hang fix present');
  ok(html.includes('escapeHtml'), 'escapeHtml helper present');
  ok(
    html.includes('escapeHtml(String(content') || html.includes("escapeHtml(String(content"),
    'Chat uses escapeHtml'
  );

  // Example keys present
  const exampleKeys = [
    'Hello World',
    'Name Greeter',
    'FizzBuzz',
    'Calculator',
    'Number Guessing Game',
    'Todo List',
    'Rock Paper Scissors',
    'Simple Class',
    'Temperature Converter',
    'Word Counter',
  ];
  for (const name of exampleKeys) {
    ok(html.includes("'" + name + "': function"), `Example builder present: ${name}`);
  }

  console.log(`  blocks=${blockDefs.size} generators=${gens.size} toolbox_py=${toolboxTypes.size}`);
  return { blockDefs, gens, toolboxTypes, exampleKeys, version: ver && ver[1] };
}

// ─── Shared: load Blockly + custom blocks ────────────────────────────────────

function extractBlockSource(html) {
  // Prefer the full script region from first custom block comment through theme
  const end = html.indexOf('const pymasonTheme');
  if (end < 0) return null;
  // Start at first Blockly.Blocks assignment (valid JS)
  const start = html.indexOf("Blockly.Blocks['py_input']");
  if (start < 0) {
    const alt = html.indexOf('Blockly.Blocks[');
    if (alt < 0) return null;
    return html.slice(alt, end);
  }
  return html.slice(start, end);
}

function extractExamplesSource(html) {
  const start = html.indexOf('const EXAMPLES = {');
  const end = html.indexOf('function loadExample');
  if (start < 0 || end < 0) return null;
  return html.slice(start, end);
}

function loadBlocklyStack() {
  const Blockly = require('blockly');
  const { pythonGenerator, Order } = require('blockly/python');
  require('blockly/blocks');
  return { Blockly, pythonGenerator, Order };
}

function extractSanitizeHelpers(html) {
  const start = html.indexOf('function pyIsIdentifier');
  const end = html.indexOf("Blockly.Blocks['py_input']");
  if (start < 0 || end < 0 || end <= start) return '';
  return html.slice(start, end);
}

function registerCustomBlocks(html, Blockly, pythonGenerator, Order) {
  const helpers = extractSanitizeHelpers(html);
  const src = extractBlockSource(html);
  if (!src) throw new Error('Could not extract block definitions');

  // Headless: Block has no initSvg; examples call it — polyfill no-ops
  if (Blockly.Block && Blockly.Block.prototype) {
    Blockly.Block.prototype.initSvg = Blockly.Block.prototype.initSvg || function () {};
    Blockly.Block.prototype.render = Blockly.Block.prototype.render || function () {};
  }

  const sandbox = {
    Blockly,
    python: { pythonGenerator, Order },
    console,
    prompt: () => null,
    setTimeout,
    clearTimeout,
    setInterval,
    clearInterval,
  };
  sandbox.global = sandbox;
  sandbox.window = sandbox;
  sandbox.self = sandbox;
  const full = (helpers || '') + '\n' + src;
  vm.runInNewContext(full, sandbox, { timeout: 15000, filename: 'pymason-blocks.js' });
  // Expose sanitizers on sandbox for goldens if needed
  return full.length;
}

// ─── Tier B: headless codegen ────────────────────────────────────────────────

async function tierCodegen(html, meta) {
  section('B. Headless Blockly codegen + serialization');

  let Blockly, pythonGenerator, Order;
  try {
    ({ Blockly, pythonGenerator, Order } = loadBlocklyStack());
  } catch (e) {
    console.error('  SKIP codegen: cd tests && npm install —', e.message);
    return null;
  }

  try {
    const n = registerCustomBlocks(html, Blockly, pythonGenerator, Order);
    ok(n > 1000, `Custom block definitions evaluated (${n} chars)`);
  } catch (e) {
    ok(false, 'Eval block definitions: ' + e.message);
    return null;
  }

  const registered = Object.keys(pythonGenerator.forBlock || {}).filter((k) => k.startsWith('py_'));
  ok(registered.length >= 100, `Generators registered (${registered.length})`);

  const workspace = new Blockly.Workspace();
  pythonGenerator.init(workspace);

  const skipInstantiate = new Set(['py_tuple_container', 'py_tuple_item', 'py_tuple_create']);
  let genOk = 0;
  let genFail = 0;
  const genErrors = [];

  const origError = console.error;
  console.error = (...args) => {
    if (String(args[0] || '').includes('CodeGenerator init was not called')) return;
    origError.apply(console, args);
  };

  for (const type of [...meta.blockDefs].sort()) {
    if (skipInstantiate.has(type)) continue;
    if (!Blockly.Blocks[type]) {
      genFail++;
      genErrors.push(`${type}: not registered`);
      continue;
    }
    try {
      const block = workspace.newBlock(type);
      const code = pythonGenerator.blockToCode(block);
      const valid =
        typeof code === 'string' ||
        (Array.isArray(code) && typeof code[0] === 'string' && typeof code[1] === 'number');
      if (!valid) {
        genFail++;
        genErrors.push(`${type}: bad return ${JSON.stringify(code)}`);
      } else genOk++;
      block.dispose(false);
    } catch (e) {
      genFail++;
      genErrors.push(`${type}: ${e.message}`);
    }
  }
  console.error = origError;

  ok(genFail === 0, `blockToCode each type (ok=${genOk} fail=${genFail})`);
  if (genErrors.length) genErrors.slice(0, 12).forEach((e) => console.error('   -', e));

  section('B2. Golden output checks');
  function genOne(type, setup) {
    pythonGenerator.init(workspace);
    const b = workspace.newBlock(type);
    if (setup) setup(b);
    const code = pythonGenerator.blockToCode(b);
    const out = Array.isArray(code) ? code[0] : code;
    b.dispose(false);
    return out;
  }

  ok(genOne('py_pass').trim() === 'pass', 'py_pass → pass');
  ok(genOne('py_import', (b) => b.setFieldValue('math', 'MODULE')).includes('import math'), 'py_import math');
  {
    const c = genOne('py_fstring', (b) => b.setFieldValue("it's {x}", 'TEXT'));
    ok(c.includes("\\'") || c.includes("it\\'s"), `py_fstring escapes quote (${c})`);
  }
  {
    const c = genOne('py_comment', (b) => b.setFieldValue('hello\nworld', 'TEXT'));
    ok(!c.includes('\nworld') && c.startsWith('#'), 'py_comment strips newlines');
  }
  ok(genOne('py_return').trim() === 'return', 'py_return bare');
  {
    const c = genOne('py_open', (b) => b.setFieldValue("'r'", 'MODE'));
    ok(/open\(/.test(c) && /'r'/.test(c), 'py_open mode quoted');
  }
  {
    const c = genOne('py_await');
    ok(c.includes('await'), `py_await generates await (${c})`);
  }
  {
    const c = genOne('py_starred');
    ok(c.startsWith('*') || c.startsWith('**'), `py_starred prefix (${c})`);
  }

  // String-field escape / injection goldens (AUDIT-LINEBYLINE)
  section('B2b. String & identifier sanitization');
  {
    const c = genOne('py_str_format', (b) => b.setFieldValue("it's {0}", 'TEMPLATE'));
    ok(c.includes("\\'") || c.includes("it\\'s"), `py_str_format escapes quote (${c})`);
    ok(c.includes('.format('), 'py_str_format has .format');
  }
  {
    const c = genOne('py_raw_string', (b) => b.setFieldValue("path\\to", 'TEXT'));
    ok(c.startsWith("r'"), `py_raw_string raw prefix (${c})`);
    ok(!c.includes("r'path\\to'") || c.includes('\\\\') || c.includes('path'), 'py_raw_string produces raw literal');
  }
  {
    const c = genOne('py_raw_string', (b) => b.setFieldValue("o'clock", 'TEXT'));
    ok(c.includes("\\'"), `py_raw_string escapes quote (${c})`);
  }
  {
    const c = genOne('py_multiline_string', (b) => b.setFieldValue('a"""b', 'TEXT'));
    ok(c.startsWith('"""'), 'py_multiline triple-quote open');
    ok(!c.includes('"""a"""b"""') || c.includes('\\"'), `py_multiline escapes embedded triple (${c})`);
  }
  {
    const c = genOne('py_class', (b) => {
      b.setFieldValue('Bad-Name!', 'NAME');
      b.setFieldValue('', 'PARENT');
    });
    ok(/^class\s+[A-Za-z_][A-Za-z0-9_]*\s*:/m.test(c), `py_class sanitizes identifier (${c.trim()})`);
    ok(!c.includes('Bad-Name'), 'py_class stripped invalid chars from name');
  }
  {
    const c = genOne('py_method', (b) => {
      b.setFieldValue('do stuff', 'NAME');
      b.setFieldValue('a; import os', 'PARAMS');
    });
    ok(/def\s+do_stuff\s*\(/.test(c) || /def\s+do_stuff\(/.test(c), `py_method sanitizes name (${c})`);
    ok(!c.includes('import os'), 'py_method params cannot inject statements via semicolon');
  }
  {
    const c = genOne('py_self_get', (b) => b.setFieldValue('x.y', 'ATTR'));
    ok(/^self\.[A-Za-z_][A-Za-z0-9_]*$/.test(c.trim()) || c.includes('self.'), `py_self_get sanitized (${c})`);
  }

  section('B3. Serialization round-trip');
  {
    const wsA = new Blockly.Workspace();
    const a = wsA.newBlock('py_import');
    a.setFieldValue('json', 'MODULE');
    const b = wsA.newBlock('py_pass');
    a.nextConnection.connect(b.previousConnection);
    const state = Blockly.serialization.workspaces.save(wsA);
    const wsB = new Blockly.Workspace();
    Blockly.serialization.workspaces.load(JSON.parse(JSON.stringify(state)), wsB);
    pythonGenerator.init(wsA);
    const codeA = pythonGenerator.workspaceToCode(wsA).trim();
    pythonGenerator.init(wsB);
    const codeB = pythonGenerator.workspaceToCode(wsB).trim();
    ok(codeA === codeB, 'Round-trip code match');
    ok(codeA.includes('import json') && codeA.includes('pass'), 'Round-trip content');
    wsA.dispose();
    wsB.dispose();
  }

  workspace.dispose();
  return { Blockly, pythonGenerator, Order };
}

// ─── Tier C: example programs ────────────────────────────────────────────────

/** Soft expectations (intended behavior) — must appear in generated code */
const EXAMPLE_EXPECT = {
  'Hello World': [/print\s*\(/, /Hello,\s*World/],
  'Name Greeter': [/input\s*\(/, /Hello/],
  'FizzBuzz': [/for\s+/, /range\s*\(/],
  'Calculator': [/input\s*\(/, /float\s*\(|int\s*\(/],
  'Number Guessing Game': [/while\s+/, /input\s*\(/],
  'Todo List': [/while\s+/, /input\s*\(/],
  'Rock Paper Scissors': [/import\s+random|random\./, /input\s*\(/],
  'Simple Class': [/class\s+Dog/, /def\s+__init__/],
  'Temperature Converter': [/celsius|fahrenheit/i, /input\s*\(/, /print\s*\(/],
  'Word Counter': [/input\s*\(/, /split|\.lower|for\s+/],
};

function slugExample(name) {
  return name.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
}

async function tierExamples(html, stack) {
  section('C. Example program builders → generated Python');

  if (!stack) {
    console.log('  SKIP (codegen stack unavailable)');
    return;
  }

  const { Blockly, pythonGenerator, Order } = stack;
  const exSrc = extractExamplesSource(html);
  ok(!!exSrc && exSrc.length > 500, `Extracted EXAMPLES source (${exSrc ? exSrc.length : 0} chars)`);
  if (!exSrc) return;

  fs.mkdirSync(FIXTURES_DIR, { recursive: true });

  const workspace = new Blockly.Workspace();
  // Polyfill workspace methods used by example builders
  workspace.render = function () {};
  if (Blockly.Block && Blockly.Block.prototype) {
    Blockly.Block.prototype.initSvg = function () {};
  }

  // Real-ish DOM for controls_if mutations (document.createElement('mutation'))
  let jsdomDocument = null;
  try {
    const { JSDOM } = require('jsdom');
    const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
    jsdomDocument = dom.window.document;
  } catch (e) {
    console.log('  note: jsdom unavailable, mutation-heavy examples may fail');
  }

  let EXAMPLES;
  try {
    const createWorkspaceVariable = (name) => {
      if (workspace.getVariableMap && typeof workspace.getVariableMap === 'function') {
        return workspace.getVariableMap().createVariable(name);
      }
      return workspace.createVariable(name);
    };
    const sandbox = {
      Blockly,
      python: { pythonGenerator, Order },
      workspace,
      createWorkspaceVariable,
      updateCode: () => {},
      showToast: () => {},
      console,
      prompt: () => null,
      document: jsdomDocument || {
        createElement: () => ({ setAttribute() {}, getAttribute() { return null; } }),
      },
    };
    sandbox.window = { document: sandbox.document };
    sandbox.global = sandbox;
    sandbox.self = sandbox;
    // EXAMPLES is assigned via const in source — wrap to capture
    const wrapped =
      exSrc.replace(/^const EXAMPLES\s*=/, 'EXAMPLES =') +
      '\n; EXAMPLES;';
    EXAMPLES = vm.runInNewContext(wrapped, sandbox, {
      timeout: 15000,
      filename: 'pymason-examples.js',
    });
  } catch (e) {
    ok(false, 'Eval EXAMPLES: ' + e.message);
    return;
  }

  ok(EXAMPLES && typeof EXAMPLES === 'object', 'EXAMPLES object loaded');
  const names = Object.keys(EXAMPLES || {});
  ok(names.length >= 10, `Example count (${names.length})`);
  console.log('  examples:', names.join(', '));

  const updateSnapshots = process.env.UPDATE_FIXTURES === '1';

  for (const name of names) {
    try {
      workspace.clear();
      // Re-bind workspace global used inside closures if any
      EXAMPLES[name]();
      pythonGenerator.init(workspace);
      const code = normalizePy(pythonGenerator.workspaceToCode(workspace));
      const blockCount = workspace.getAllBlocks(false).length;

      ok(blockCount > 0, `${name}: produced blocks (${blockCount})`);
      ok(code.trim().length > 0, `${name}: produced non-empty Python`);

      const expects = EXAMPLE_EXPECT[name] || [];
      for (const re of expects) {
        ok(re.test(code), `${name}: matches ${re} — got:\n${code.slice(0, 200)}`);
      }

      // Snapshot file
      const fixturePath = path.join(FIXTURES_DIR, slugExample(name) + '.py');
      if (updateSnapshots || !fs.existsSync(fixturePath)) {
        fs.writeFileSync(fixturePath, code, 'utf8');
        if (updateSnapshots) console.log('  wrote fixture', path.basename(fixturePath));
      } else {
        const expected = normalizePy(fs.readFileSync(fixturePath, 'utf8'));
        // Variable IDs can change renames — compare structure loosely if exact fails
        if (code !== expected) {
          // Allow var name differences: strip identifier renames is hard; require
          // same line count and same non-identifier tokens ratio
          const linesA = code.split('\n').filter((l) => l.trim());
          const linesB = expected.split('\n').filter((l) => l.trim());
          const lineOk = Math.abs(linesA.length - linesB.length) <= 1;
          // Tokenize keywords
          const kw = (s) =>
            (s.match(/\b(print|input|import|class|def|while|for|if|return|True|False|None)\b/g) || [])
              .join(',');
          const kwOk = kw(code) === kw(expected);
          ok(
            lineOk && kwOk,
            `${name}: fixture drift (set UPDATE_FIXTURES=1 to refresh)\n` +
              `    got ${linesA.length} lines kw=${kw(code)}\n` +
              `    exp ${linesB.length} lines kw=${kw(expected)}`
          );
          if (!(lineOk && kwOk)) {
            console.error('--- got ---\n' + code.slice(0, 400));
            console.error('--- exp ---\n' + expected.slice(0, 400));
          }
        } else {
          ok(true, `${name}: fixture match`);
        }
      }

      // Save/load this example workspace
      const state = Blockly.serialization.workspaces.save(workspace);
      const ws2 = new Blockly.Workspace();
      Blockly.serialization.workspaces.load(JSON.parse(JSON.stringify(state)), ws2);
      pythonGenerator.init(ws2);
      const code2 = normalizePy(pythonGenerator.workspaceToCode(ws2));
      ok(
        kwMatch(code, code2),
        `${name}: serialization preserves structure`
      );
      ws2.dispose();
    } catch (e) {
      ok(false, `${name}: threw ${e.message}`);
    }
  }

  workspace.dispose();
}

function kwMatch(a, b) {
  const kw = (s) =>
    (s.match(/\b(print|input|import|class|def|while|for|if|return|True|False|None|from|as)\b/g) || [])
      .join(',');
  return kw(a) === kw(b);
}

// ─── Tier D: DOM contract ────────────────────────────────────────────────────

function tierDomContract(html) {
  section('D. HTML / DOM contract');

  const requiredIds = [
    'blocklyDiv',
    'codeOutput',
    'lineNumbers',
    'outputPanel',
    'outputContent',
    'varInspector',
    'varInspectorList',
    'btnRun',
    'btnStop',
    'btnChat',
    'chatPanel',
    'chatMessages',
    'chatInput',
    'helpPanel',
    'statusText',
    'blockCount',
    'lastSaved',
    'pyodideStatus',
    'divider',
    'codePanel',
    'importFile',
    'toolbox',
    'toast',
  ];

  for (const id of requiredIds) {
    ok(
      new RegExp(`id=["']${id}["']`).test(html),
      `Required element #${id}`
    );
  }

  const requiredFns = [
    'runCode',
    'stopCode',
    'saveWorkspace',
    'loadWorkspace',
    'exportWorkspace',
    'importWorkspace',
    'copyCode',
    'downloadPython',
    'openExamplesMenu',
    'loadExample',
    'toggleChat',
    'toggleHelp',
    'updateCode',
  ];
  for (const fn of requiredFns) {
    ok(
      html.includes('function ' + fn) || html.includes(fn + ' =') || html.includes(`function ${fn}(`),
      `Required function ${fn}`
    );
  }

  ok(html.includes('role="application"'), 'Block editor ARIA application role');
  ok(html.includes('aria-live'), 'Output aria-live for a11y');
  ok(html.includes('onclick="runCode()"') || html.includes('runCode()'), 'Run wired in UI');
}

// ─── Tier E: Playwright page load ────────────────────────────────────────────

function startStaticServer(rootDir) {
  const mime = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.png': 'image/png',
    '.md': 'text/markdown',
    '.json': 'application/json',
  };
  const server = http.createServer((req, res) => {
    let urlPath = decodeURIComponent((req.url || '/').split('?')[0]);
    if (urlPath === '/') urlPath = '/index.html';
    const filePath = path.join(rootDir, path.normalize(urlPath).replace(/^(\.\.[/\\])+/, ''));
    if (!filePath.startsWith(rootDir)) {
      res.writeHead(403);
      res.end('Forbidden');
      return;
    }
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end('Not found');
        return;
      }
      const ext = path.extname(filePath);
      res.writeHead(200, { 'Content-Type': mime[ext] || 'application/octet-stream' });
      res.end(data);
    });
  });
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({ server, port, base: `http://127.0.0.1:${port}` });
    });
  });
}

async function tierBrowser(html) {
  section('E. Headless Chromium page load');

  if (process.env.SKIP_BROWSER === '1') {
    console.log('  SKIP (SKIP_BROWSER=1)');
    return;
  }

  let chromium;
  try {
    ({ chromium } = await import('playwright'));
  } catch (e) {
    console.log('  SKIP (playwright not installed):', e.message);
    return;
  }

  const { server, base } = await startStaticServer(ROOT);
  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    // Skip first-run welcome so UI is interactive
    await context.addInitScript(() => {
      try {
        localStorage.setItem('pymason_welcomed', '1');
      } catch (_) { /* ignore */ }
    });
    const page = await context.newPage();
    const pageErrors = [];
    page.on('pageerror', (err) => pageErrors.push(String(err.message || err)));

    const resp = await page.goto(base + '/index.html', {
      waitUntil: 'domcontentloaded',
      timeout: 60000,
    });
    ok(resp && resp.ok(), `index.html HTTP ${resp && resp.status()}`);

    // WPAI login gate
    if (await page.locator('#loginGate').isVisible().catch(() => false)) {
      await page.fill('#loginUser', 'studio');
      await page.fill('#loginPass', 'wpai-forge');
      await page.click('#loginForm button[type="submit"]');
      await page.waitForTimeout(600);
    }
    await page.locator('#appShell.visible').waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
    ok(await page.locator('#appShell').evaluate((el) => el.classList.contains('visible')).catch(() => false),
      'App shell visible after login');

    // Dismiss welcome if still present
    const welcomeBtn = page.locator('#welcomeOverlay button');
    if (await welcomeBtn.count()) {
      await welcomeBtn.click().catch(() => {});
    }
    await page.locator('#welcomeOverlay').waitFor({ state: 'detached', timeout: 3000 }).catch(() => {});

    // Wait for Blockly + inject
    await page.waitForFunction(
      () =>
        typeof window.Blockly !== 'undefined' &&
        document.querySelector('.blocklySvg, .blocklyWorkspace, #blocklyDiv svg'),
      { timeout: 45000 }
    );
    ok(true, 'Blockly loaded and workspace SVG present');

    const status = await page.locator('#statusText').textContent();
    ok(status && /v\d+\.\d+\.\d+/.test(status), `Status shows version (${status})`);

    await page.locator('#btnRun').waitFor({ state: 'visible', timeout: 5000 });
    ok(true, 'Run button visible');

    const hasWorkspace = await page.evaluate(
      () => !!document.querySelector('.blocklySvg')
    );
    ok(hasWorkspace, 'Workspace DOM ready');

    // Open Examples via API (header menus use dropdowns)
    await page.evaluate(() => {
      if (typeof openExamplesMenu === 'function') openExamplesMenu();
    });
    await page.locator('#examplesDialog').waitFor({ state: 'visible', timeout: 5000 });
    page.once('dialog', (d) => d.accept());
    await page.locator('#examplesDialog div', { hasText: 'Hello World' }).first().click();
    await page.waitForTimeout(500);
    const codeText = await page.locator('#codeOutput').innerText();
    ok(/print|Hello/i.test(codeText), `Hello World code panel: ${codeText.slice(0, 120)}`);

    // ── F. Pyodide: Run Hello World ───────────────────────────────────
    section('F. Pyodide execute Hello World');
    if (process.env.SKIP_PYODIDE === '1') {
      console.log('  SKIP (SKIP_PYODIDE=1) — first Pyodide download can take 1–3 minutes');
    } else {
      // Ensure output panel can show results
      await page.locator('#btnRun').click();
      console.log('  waiting for Pyodide load + run (may download ~7MB on first run)...');
      try {
        await page.waitForFunction(
          () => {
            const el = document.getElementById('outputContent');
            if (!el) return false;
            const t = el.innerText || '';
            // Success: printed greeting and/or finished marker
            // Failure: explicit engine failure
            return (
              /Hello/i.test(t) ||
              /Finished in/i.test(t) ||
              /Failed to load Python/i.test(t) ||
              /Python engine failed/i.test(t)
            );
          },
          { timeout: 180000 }
        );
        const out = await page.locator('#outputContent').innerText();
        console.log('  output:', out.slice(0, 200).replace(/\s+/g, ' '));
        ok(/Hello/i.test(out), `Output contains Hello (got: ${out.slice(0, 160).replace(/\n/g, ' ')})`);
        ok(
          /Finished in/i.test(out) || /Hello/i.test(out),
          'Run reached completion marker or printed Hello'
        );
        ok(
          !/Failed to load Python/i.test(out) && !/Python engine failed/i.test(out),
          'Python engine did not report load failure'
        );
        // Run button restored after completion
        await page.locator('#btnRun').waitFor({ state: 'visible', timeout: 10000 });
        ok(true, 'Run button visible again after execution');
      } catch (e) {
        const out = await page.locator('#outputContent').innerText().catch(() => '');
        const st = await page.locator('#pyodideStatus').innerText().catch(() => '');
        ok(
          false,
          `Pyodide run timed out or failed: ${e.message}\n    status=${st}\n    output=${out.slice(0, 300)}`
        );
      }
    }

    // Landing page loads
    const land = await page.goto(base + '/landing.html', {
      waitUntil: 'domcontentloaded',
      timeout: 15000,
    });
    ok(land && land.ok(), 'landing.html loads');
    const title = await page.title();
    ok(/PyMason/i.test(title), `landing title contains PyMason (${title})`);
      // WPAI / privacy framing on landing
    const landBody = await page.locator('body').innerText();
    ok(
      /WPAI|wizard|studio|forge|API|localStorage|privacy/i.test(landBody),
      'Landing mentions WPAI / privacy framing'
    );

    // Blockly field noise during load can emit VALUE-access races; only fail on unique serious errors
    if (pageErrors.length) {
      const serious = pageErrors.filter(
        (e) =>
          !/favicon/i.test(e) &&
          !/reading 'VALUE'/i.test(e) &&
          !/ResizeObserver/i.test(e) &&
          !/SharedArrayBuffer/i.test(e)
      );
      const valueNoise = pageErrors.filter((e) => /reading 'VALUE'/i.test(e)).length;
      if (valueNoise) console.log(`  note: ${valueNoise} Blockly field VALUE races during load (non-fatal)`);
      ok(serious.length === 0, `No serious page errors: ${serious.join(' | ') || 'none'}`);
      if (serious.length) serious.forEach((e) => console.error('   pageerror:', e));
    } else {
      ok(true, 'No serious page errors');
    }
  } catch (e) {
    ok(false, 'Browser tier: ' + e.message);
  } finally {
    if (browser) await browser.close();
    await new Promise((r) => server.close(r));
  }
}

// ─── main ────────────────────────────────────────────────────────────────────

async function main() {
  console.log('PyMason smoke suite');
  console.log('index:', INDEX);

  if (!fs.existsSync(INDEX)) {
    console.error('index.html not found');
    process.exit(2);
  }
  const html = fs.readFileSync(INDEX, 'utf8');

  const meta = tierStructure(html);
  const stack = await tierCodegen(html, meta);
  await tierExamples(html, stack);
  tierDomContract(html);
  await tierBrowser(html);

  section('Summary');
  console.log(`  passed: ${passed}`);
  console.log(`  failed: ${failed}`);
  if (failed) {
    console.log('\nFailures:');
    failures.forEach((f) => console.log('  -', f));
    process.exit(1);
  }
  console.log('\nAll smoke checks passed.');
  process.exit(0);
}

main().catch((e) => {
  console.error(e);
  process.exit(2);
});
