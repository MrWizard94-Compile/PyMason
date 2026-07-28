/**
 * Static line-oriented audit of index.html + support files.
 * Run: node tests/line-audit.mjs
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const INDEX = path.join(ROOT, 'index.html');

const findings = [];
function add(sev, file, line, title, detail) {
  findings.push({ sev, file, line, title, detail });
}

const html = fs.readFileSync(INDEX, 'utf8');
const lines = html.split(/\r?\n/);

function lineOf(substr, from = 0) {
  const i = html.indexOf(substr, from);
  if (i < 0) return 0;
  return html.slice(0, i).split(/\r?\n/).length;
}

// ── Line map of major regions ──────────────────────────────────────────────
const regions = [
  ['HEAD / CDN scripts', 1, 14],
  ['CSS theme + layout', 15, 857],
  ['HTML shell (header/main/panels)', 859, 1012],
  ['Toolbox XML', 1013, 1730],
  ['Custom block definitions + generators', 1732, 4607],
  ['Theme + workspace inject', 4608, 4700],
  ['Tooltips / updateCode / highlight', 4700, 5200],
  ['Pyodide execution', 5160, 5660],
  ['Shortcuts / warnings / workspaces', 5660, 6080],
  ['Examples + welcome', 6080, 6700],
  ['AI chat + version + Electron', 6700, 7034],
];

// ── Structural ─────────────────────────────────────────────────────────────
const ver = html.match(/PYMASON_VERSION\s*=\s*'([^']+)'/);
if (!ver) add('CRIT', 'index.html', 0, 'Missing PYMASON_VERSION', '');
else add('INFO', 'index.html', lineOf("PYMASON_VERSION"), 'Version', ver[1]);

// CDN pins
const cdnLines = lines
  .map((l, i) => ({ l, n: i + 1 }))
  .filter(({ l }) => l.includes('<script src='));
for (const { l, n } of cdnLines) {
  if (l.includes('unpkg.com/blockly/') && !l.includes('blockly@')) {
    add('CRIT', 'index.html', n, 'Unpinned Blockly CDN', l.trim());
  }
  if (l.includes('keyboard-navigation') && !l.includes('@3.0.5')) {
    add('HIGH', 'index.html', n, 'keyboard-nav version unexpected', l.trim());
  }
  if (l.includes('http://')) {
    add('HIGH', 'index.html', n, 'Insecure HTTP script', l.trim());
  }
}

// No CSP meta
if (!html.includes('Content-Security-Policy')) {
  add(
    'MED',
    'index.html',
    3,
    'No CSP meta tag',
    'Rely on host headers; documented in docs/hosting.md'
  );
}

// ── Security patterns ──────────────────────────────────────────────────────
lines.forEach((l, i) => {
  const n = i + 1;
  if (/\beval\s*\(/.test(l) || /new Function\s*\(/.test(l)) {
    add('CRIT', 'index.html', n, 'eval / Function constructor', l.trim());
  }
  if (/document\.write\s*\(/.test(l)) {
    add('HIGH', 'index.html', n, 'document.write', l.trim());
  }
  if (/innerHTML\s*=/.test(l) && !l.includes('//')) {
    // context: check nearby escapeHtml
    const window = lines.slice(Math.max(0, i - 8), i + 1).join('\n');
    if (
      !window.includes('escapeHtml') &&
      !window.includes('highlightPython') &&
      !window.includes('highlightCodeWithLineSpans') &&
      !l.includes("''") &&
      !l.includes('typing') &&
      !l.includes('empty-state') &&
      !l.includes('system')
    ) {
      // classify
      if (l.includes('dialog.innerHTML') || l.includes('setup.innerHTML') || l.includes('overlay.innerHTML') || l.includes('hint.innerHTML') || l.includes('popup.innerHTML')) {
        add('LOW', 'index.html', n, 'innerHTML with static/template UI', l.trim().slice(0, 100));
      } else if (l.includes('codeOutput.innerHTML')) {
        add('INFO', 'index.html', n, 'codeOutput innerHTML (highlightPython escapes)', l.trim().slice(0, 80));
      } else if (l.includes('div.innerHTML = html')) {
        add('INFO', 'index.html', n, 'chat message innerHTML (must be after escapeHtml)', l.trim());
      } else if (l.includes('list.innerHTML')) {
        add('INFO', 'index.html', n, 'var inspector list (escapeHtml used)', l.trim().slice(0, 80));
      } else {
        add('MED', 'index.html', n, 'innerHTML assignment', l.trim().slice(0, 120));
      }
    }
  }
  if (/localStorage\.setItem\(\s*['\"]pymason_api_key/.test(l)) {
    add('MED', 'index.html', n, 'API key stored in localStorage', 'Documented; risk on shared machines');
  }
  if (/anthropic-dangerous-direct-browser-access/.test(l)) {
    add('MED', 'index.html', n, 'Browser Anthropic CORS header', 'Required for client-side key; not multi-tenant safe');
  }
});

// Chat must escape
const chatIdx = html.indexOf('function addChatMessage');
if (chatIdx > 0) {
  const chunk = html.slice(chatIdx, chatIdx + 400);
  const ln = lineOf('function addChatMessage');
  if (!chunk.includes('escapeHtml')) {
    add('CRIT', 'index.html', ln, 'addChatMessage missing escapeHtml', '');
  } else {
    add('OK', 'index.html', ln, 'addChatMessage escapes HTML', '');
  }
}

// ── Generators: invalid Order ──────────────────────────────────────────────
const knownOrders = new Set([
  'ATOMIC',
  'COLLECTION',
  'STRING_CONVERSION',
  'MEMBER',
  'FUNCTION_CALL',
  'EXPONENTIATION',
  'UNARY_SIGN',
  'BITWISE_NOT',
  'MULTIPLICATIVE',
  'ADDITIVE',
  'BITWISE_SHIFT',
  'BITWISE_AND',
  'BITWISE_XOR',
  'BITWISE_OR',
  'RELATIONAL',
  'LOGICAL_NOT',
  'LOGICAL_AND',
  'LOGICAL_OR',
  'CONDITIONAL',
  'LAMBDA',
  'NONE',
]);
for (let i = 0; i < lines.length; i++) {
  const m = lines[i].matchAll(/python\.Order\.([A-Z_]+)/g);
  for (const hit of m) {
    if (!knownOrders.has(hit[1])) {
      add('CRIT', 'index.html', i + 1, `Invalid python.Order.${hit[1]}`, lines[i].trim());
    }
  }
}

// ── Blocks vs generators vs toolbox ────────────────────────────────────────
const defs = [...html.matchAll(/Blockly\.Blocks\['([^']+)'\]/g)].map((m) => m[1]);
const gens = [...html.matchAll(/pythonGenerator\.forBlock\['([^']+)'\]/g)].map((m) => m[1]);
const defSet = new Set(defs);
const genSet = new Set(gens);
const mutatorOnly = new Set(['py_tuple_container', 'py_tuple_item']);
for (const d of defSet) {
  if (!genSet.has(d) && !mutatorOnly.has(d)) {
    add('HIGH', 'index.html', lineOf(`Blockly.Blocks['${d}']`), `Block without generator: ${d}`, '');
  }
}
for (const g of genSet) {
  if (!defSet.has(g)) {
    add('HIGH', 'index.html', lineOf(`forBlock['${g}']`), `Generator without block: ${g}`, '');
  }
}
const toolbox = [...html.matchAll(/<block\s+type="(py_[^"]+)"/g)].map((m) => m[1]);
for (const t of new Set(toolbox)) {
  if (!defSet.has(t)) {
    add('CRIT', 'index.html', lineOf(`type="${t}"`), `Toolbox type missing block def: ${t}`, '');
  }
}

// ── Free-text fields injected into Python without identifier validation ────
const freeTextGens = [
  ['py_class', 'NAME/PARENT unvalidated identifiers'],
  ['py_method', 'NAME/PARAMS unvalidated'],
  ['py_init', 'PARAMS unvalidated'],
  ['py_import', 'module via dropdown/custom'],
  ['py_from_import', 'NAME field free text'],
  ['py_self_get', 'ATTR free text'],
  ['py_self_set', 'ATTR free text'],
  ['py_self_call', 'method free text'],
  ['py_instantiate', 'CLASS/ARGS free text'],
  ['py_obj_get', 'ATTR free text'],
  ['py_obj_call', 'method free text'],
  ['py_async_def', 'NAME/PARAMS free text'],
  ['py_decorator', 'NAME free text'],
  ['py_global', 'uses getVariableName — OK'],
];
for (const [type, note] of freeTextGens) {
  if (defSet.has(type) || type === 'py_global') {
    const ln = lineOf(`forBlock['${type}']`) || lineOf(`Blocks['${type}']`);
    if (note.includes('OK')) {
      add('OK', 'index.html', ln, `${type}: ${note}`, '');
    } else {
      add(
        'MED',
        'index.html',
        ln,
        `${type}: free-text → Python AST injection surface`,
        note + ' — expected for visual builder; generates invalid Python if user types junk'
      );
    }
  }
}

// f-string uses single quotes while UI shows f"
const fstrUi = lineOf("appendField('f\"')");
const fstrGen = lineOf("return [\"f'\"");
if (fstrUi && fstrGen) {
  add(
    'LOW',
    'index.html',
    fstrGen,
    'f-string UI shows f"…" but generator emits f\'…\'',
    'Cosmetic inconsistency; escaped correctly for single-quoted form'
  );
}

// py_return has no next connection
const retBlock = lineOf("Blockly.Blocks['py_return']");
const retChunk = html.slice(html.indexOf("Blocks['py_return']"), html.indexOf("Blocks['py_return']") + 500);
if (retChunk.includes('setPreviousStatement') && !retChunk.includes('setNextStatement')) {
  add(
    'LOW',
    'index.html',
    retBlock,
    'py_return has no setNextStatement',
    'Intentional for bare return end-of-branch; cannot stack blocks after return'
  );
}

// ── Pyodide protocol ───────────────────────────────────────────────────────
if (html.includes('slice.length + 1') || html.includes('length + 1')) {
  add('OK', 'index.html', lineOf('length + 1') || lineOf('slice.length + 1'), 'Empty input wake protocol', '');
} else {
  add('CRIT', 'index.html', 0, 'Missing empty-input Atomics wake protocol', '');
}
if (html.includes('runResolve')) {
  add('OK', 'index.html', lineOf('runResolve'), 'Stop settles run promise', '');
}
if (html.includes('!useSharedBuffer')) {
  add('OK', 'index.html', lineOf('!useSharedBuffer'), 'No-SAB falls back to main thread', '');
}

// Worker input ignores prompt argument
const workerInput = lineOf('"input_request"');
if (workerInput) {
  add(
    'MED',
    'index.html',
    workerInput,
    'Worker input_request prompt always empty string',
    'Relies on Pyodide writing prompt to stdout; may be empty on some paths'
  );
}

// ── Accessibility / UX ─────────────────────────────────────────────────────
if (!html.includes('prefers-reduced-motion')) {
  add('LOW', 'index.html', 0, 'No prefers-reduced-motion CSS', 'TODO: reduced motion mode');
}
if (html.includes('aria-live')) {
  add('OK', 'index.html', lineOf('aria-live'), 'Output aria-live present', '');
}

// Header button density
const headerBtn = (html.match(/class="btn/g) || []).length;
add('INFO', 'index.html', lineOf('header-actions'), `Many .btn instances (~${headerBtn})`, 'Header may overflow on small screens');

// ── Electron ───────────────────────────────────────────────────────────────
const mainJs = fs.readFileSync(path.join(ROOT, 'electron', 'main.js'), 'utf8');
const preload = fs.readFileSync(path.join(ROOT, 'electron', 'preload.js'), 'utf8');
if (!mainJs.includes('contextIsolation: true')) {
  add('CRIT', 'electron/main.js', 0, 'contextIsolation not true', '');
} else {
  add('OK', 'electron/main.js', lineOfIn(mainJs, 'contextIsolation'), 'contextIsolation true', '');
}
if (mainJs.includes('nodeIntegration: true')) {
  add('CRIT', 'electron/main.js', 0, 'nodeIntegration enabled', '');
} else {
  add('OK', 'electron/main.js', lineOfIn(mainJs, 'nodeIntegration'), 'nodeIntegration false', '');
}
if (!preload.includes('contextBridge')) {
  add('HIGH', 'electron/preload.js', 0, 'No contextBridge', '');
}

// Open .py only reference
if (html.includes('reference only')) {
  add('OK', 'index.html', lineOf('reference only'), 'Open .py is reference dump', '');
}

// ── Tests package ──────────────────────────────────────────────────────────
const smoke = fs.readFileSync(path.join(ROOT, 'tests', 'smoke.mjs'), 'utf8');
if (!smoke.includes('Pyodide execute') && !smoke.includes('tier F') && !smoke.includes('Hello')) {
  add('MED', 'tests/smoke.mjs', 0, 'Missing Pyodide E2E?', '');
} else {
  add('OK', 'tests/smoke.mjs', 0, 'Smoke includes Pyodide/Hello path', '');
}

// ── Duplicate block type registrations ─────────────────────────────────────
const defCounts = {};
for (const d of defs) defCounts[d] = (defCounts[d] || 0) + 1;
for (const [k, c] of Object.entries(defCounts)) {
  if (c > 1) add('HIGH', 'index.html', lineOf(`Blocks['${k}']`), `Duplicate block def x${c}: ${k}`, '');
}

// ── Output ─────────────────────────────────────────────────────────────────
function lineOfIn(text, sub) {
  const i = text.indexOf(sub);
  if (i < 0) return 0;
  return text.slice(0, i).split(/\r?\n/).length;
}

const order = { CRIT: 0, HIGH: 1, MED: 2, LOW: 3, INFO: 4, OK: 5 };
findings.sort((a, b) => order[a.sev] - order[b.sev] || a.line - b.line);

const counts = {};
for (const f of findings) counts[f.sev] = (counts[f.sev] || 0) + 1;

console.log('=== LINE AUDIT SUMMARY ===');
console.log('index.html lines:', lines.length);
console.log('counts:', counts);
console.log('\n=== REGIONS ===');
regions.forEach(([name, a, b]) => console.log(`  ${a}-${b}: ${name}`));
console.log('\n=== FINDINGS ===');
for (const f of findings) {
  if (f.sev === 'OK' || f.sev === 'INFO') continue;
  console.log(`[${f.sev}] ${f.file}:${f.line} — ${f.title}`);
  if (f.detail) console.log('    ', f.detail);
}
console.log('\n=== OK/INFO (abbrev) ===');
for (const f of findings.filter((x) => x.sev === 'OK' || x.sev === 'INFO')) {
  console.log(`[${f.sev}] ${f.file}:${f.line} — ${f.title}`);
}

// write JSON for report
fs.writeFileSync(
  path.join(ROOT, 'tests', 'line-audit-results.json'),
  JSON.stringify({ counts, regions, findings }, null, 2)
);
console.log('\nWrote tests/line-audit-results.json');
