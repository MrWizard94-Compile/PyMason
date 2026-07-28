import { chromium } from 'playwright';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const server = http.createServer((req, res) => {
  let p = decodeURIComponent((req.url || '/').split('?')[0]);
  if (p === '/') p = '/index.html';
  const fp = path.join(ROOT, path.normalize(p).replace(/^(\.\.[/\\])+/, ''));
  fs.readFile(fp, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end();
      return;
    }
    res.end(data);
  });
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
await page.goto(`http://127.0.0.1:${port}/index.html`, {
  waitUntil: 'domcontentloaded',
  timeout: 90000,
});
await page.fill('#loginUser', 'studio');
await page.fill('#loginPass', 'wpai-forge');
await page.click('#loginForm button[type="submit"]');
await page.waitForTimeout(2000);
await page.locator('#welcomeOverlay button').click({ timeout: 2000 }).catch(() => {});
await page.waitForTimeout(400);

const info = await page.evaluate(async () => {
  const present = {
    pythonToBlocks: typeof pythonToBlocks === 'function',
    pythonToBlocksFromEditor: typeof pythonToBlocksFromEditor === 'function',
    undoWorkspaceSnapshot: typeof undoWorkspaceSnapshot === 'function',
    runAssertTests: typeof runAssertTests === 'function',
    setCodeMode: typeof setCodeMode === 'function',
    exportStagePng: typeof exportStagePng === 'function',
    debugRunToCursor: typeof debugRunToCursor === 'function',
  };
  setCodeMode('free');
  const ed = document.getElementById('codeEditor');
  ed.value = 'print("hello")\nx = 5\nprint(x)\n';
  // subset parser path (skip slow pyodide AST in CI if needed)
  const r = pythonToBlocks(ed.value, { clear: true });
  setCodeMode('dual');
  const dual = document.getElementById('codePanel')?.classList.contains('dual-split');
  return {
    version: PYMASON_VERSION,
    present,
    convertCount: r.count,
    convertOk: r.ok,
    blockCount: workspace.getAllBlocks(false).length,
    dual,
    hasAssert: !!Blockly.Blocks['py_assert_true'],
    hasCircle: !!Blockly.Blocks['py_stage_circle'],
  };
});

console.log(JSON.stringify({ info, errors }, null, 2));
await page.screenshot({ path: path.join(ROOT, 'tests', 'v11-best.png') });
await browser.close();
server.close();

const hard = errors.filter((m) => !/VALUE|ORDER/i.test(m));
const missing = Object.entries(info.present)
  .filter(([, v]) => !v)
  .map(([k]) => k);
if (
  hard.length ||
  missing.length ||
  (info.version !== '1.1.0' && info.version !== '1.2.0') ||
  !info.convertOk ||
  info.blockCount < 2 ||
  !info.hasAssert
) {
  console.error('FAIL', { hard, missing, info });
  process.exit(1);
}
console.log('v1.1 OK');
