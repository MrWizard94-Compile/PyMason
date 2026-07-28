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
await page.waitForTimeout(500);

const info = await page.evaluate(() => {
  const fns = [
    'setCodeMode',
    'getExecutablePython',
    'debugRun',
    'toggleStagePanel',
    'openCommandPalette',
    'openCurriculumHub',
    'downloadProjectFiles',
    'applyWorkspaceState',
    'extractAiWorkspace',
    'chatAgentBuild',
    'stageForward',
    'clearStage',
  ];
  const present = {};
  fns.forEach((f) => {
    present[f] = typeof window[f] === 'function';
  });

  // Dual mode
  setCodeMode('free');
  const ed = document.getElementById('codeEditor');
  const freeVisible = ed && ed.classList.contains('visible');
  setCodeMode('live');

  // Stage
  toggleStagePanel();
  clearStage();
  stageForward(20);
  const stageOn = document.getElementById('stagePanel')?.classList.contains('visible');

  // Stage block exists
  const hasStageBlock = !!Blockly.Blocks['py_turtle_forward'];

  // Command palette
  openCommandPalette();
  const palette = !!document.getElementById('cmdPalette');
  closeCommandPalette();

  // Curriculum
  openCurriculumHub();
  const curr = !!document.getElementById('studioModal');
  closeStudioModal();

  // AI extract
  const sample =
    'Here you go:\n```pymason-json\n{"blocks":{"languageVersion":0,"blocks":[]}}\n```\n';
  const extracted = extractAiWorkspace(sample);

  // Modules
  renderModuleTabs();
  const tabs = document.querySelectorAll('.module-tab').length;

  // Toolbox stage
  const names = (workspace.getToolbox()?.getToolboxItems?.() || []).map((i) =>
    i.getName?.()
  );

  return {
    version: PYMASON_VERSION,
    present,
    freeVisible,
    stageOn,
    hasStageBlock,
    palette,
    curr,
    extracted: !!extracted,
    tabs,
    names: names.slice(0, 8),
    cats: names.length,
  };
});

console.log(JSON.stringify({ info, errors }, null, 2));
await page.screenshot({ path: path.join(ROOT, 'tests', 'v1-competitive.png') });
await browser.close();
server.close();

const hard = errors.filter((m) => !/VALUE|ORDER/i.test(m));
const missing = Object.entries(info.present)
  .filter(([, v]) => !v)
  .map(([k]) => k);
if (
  hard.length ||
  missing.length ||
  info.version !== '1.0.0' ||
  !info.hasStageBlock ||
  !info.palette ||
  !info.extracted
) {
  console.error('FAIL', { hard, missing });
  process.exit(1);
}
console.log('v1 competitive OK');
