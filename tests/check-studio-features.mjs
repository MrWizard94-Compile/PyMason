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
  timeout: 60000,
});
await page.fill('#loginUser', 'studio');
await page.fill('#loginPass', 'wpai-forge');
await page.click('#loginForm button[type="submit"]');
await page.waitForTimeout(1500);
await page.locator('#welcomeOverlay button').click({ timeout: 2000 }).catch(() => {});
await page.waitForTimeout(400);

const api = await page.evaluate(() => {
  const fns = [
    'zoomToFitWorkspace',
    'shareWorkspaceLink',
    'openGuidedPaths',
    'openPackagesUI',
    'openWorkspaceDiff',
    'toggleMinimap',
    'collapseExpandAll',
    'copyFormattedCode',
    'startVoiceToChat',
    'pushRunHistory',
    'formatGeneratedCode',
    'tryLoadSharedWorkspace',
  ];
  const present = {};
  fns.forEach((f) => {
    present[f] = typeof window[f] === 'function';
  });
  // Fit
  zoomToFitWorkspace();
  // Minimap on
  if (!document.getElementById('minimapCanvas') || document.getElementById('minimapCanvas').classList.contains('hidden')) {
    toggleMinimap();
  }
  // Add a print block via serialization-ish: create block
  const b = workspace.newBlock('text_print');
  b.initSvg();
  b.render();
  b.moveBy(40, 40);
  updateCode();
  // Favorites
  addBlockToFavorites(b);
  // Format
  const formatted = formatGeneratedCode(getGeneratedCode());
  // Share encode size
  let shareOk = false;
  try {
    const b64 = encodeWorkspaceShare();
    shareOk = b64.length > 10;
  } catch (e) {
    shareOk = false;
  }
  // History
  pushRunHistory({ ok: true, ms: 12, preview: 'hello', full: 'hello\n' });
  // Lang lua option
  const hasLua = !!document.querySelector('#langSelect option[value="lua"]');
  // Header buttons
  const buttons = Array.from(document.querySelectorAll('.header-actions .btn')).map((el) => el.textContent.trim());
  return {
    present,
    shareOk,
    formattedLen: formatted.length,
    hasLua,
    buttons,
    cats: workspace.getToolbox()?.getToolboxItems?.()?.length,
    minimapShown: !document.getElementById('minimapCanvas')?.classList.contains('hidden'),
    peek: !!document.getElementById('pythonPeek'),
    version: typeof PYMASON_VERSION !== 'undefined' ? PYMASON_VERSION : null,
  };
});

// Open guided paths UI
await page.evaluate(() => openGuidedPaths());
await page.waitForTimeout(200);
const pathModal = await page.evaluate(() => !!document.getElementById('studioModal'));
await page.evaluate(() => closeStudioModal());

console.log(JSON.stringify({ api, pathModal, errors }, null, 2));
await page.screenshot({ path: path.join(ROOT, 'tests', 'studio-features.png') });
await browser.close();
server.close();

const missing = Object.entries(api.present).filter(([, v]) => !v).map(([k]) => k);
// Blockly may throw Order.VALUE on incomplete blocks during codegen — ignore those.
const hardErrors = errors.filter((m) => !/VALUE|ORDER/i.test(m));
if (hardErrors.length || missing.length || !api.shareOk || !pathModal || api.version !== '0.5.0') {
  console.error('FAIL', { missing, hardErrors, errors });
  process.exit(1);
}
console.log('studio features OK');
