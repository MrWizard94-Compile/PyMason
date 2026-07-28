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
await page.goto(`http://127.0.0.1:${port}/index.html`, {
  waitUntil: 'domcontentloaded',
  timeout: 60000,
});
await page.fill('#loginUser', 'studio');
await page.fill('#loginPass', 'wpai-forge');
await page.click('#loginForm button[type="submit"]');
await page.waitForTimeout(1500);
// dismiss welcome
await page.locator('#welcomeOverlay button').click({ timeout: 2000 }).catch(() => {});
await page.waitForTimeout(400);
const info = await page.evaluate(() => {
  const tb = document.querySelector('.blocklyToolbox, .blocklyToolboxDiv');
  const labels = Array.from(
    document.querySelectorAll(
      '.blocklyToolboxCategoryLabel, .blocklyTreeLabel, .blocklyToolboxCategory'
    )
  )
    .map((e) => (e.textContent || '').trim())
    .filter(Boolean);
  const unique = [...new Set(labels)];
  const ws = typeof Blockly !== 'undefined' ? Blockly.getMainWorkspace() : null;
  const items = ws?.getToolbox?.()?.getToolboxItems?.()?.length || 0;
  return {
    shellVisible: document.getElementById('appShell')?.classList.contains('visible'),
    toolboxW: tb?.offsetWidth || 0,
    toolboxH: tb?.offsetHeight || 0,
    cats: unique.length,
    itemCount: items,
    labels: unique.slice(0, 12),
    label: unique[0] || null,
    hasSvg: !!document.querySelector('.blocklySvg'),
    mainH: document.querySelector('.main')?.offsetHeight,
    blocklyH: document.getElementById('blocklyDiv')?.offsetHeight,
  };
});
console.log(JSON.stringify(info, null, 2));
await page.screenshot({ path: path.join(ROOT, 'tests', 'wpai-login-ui.png') });
console.log('screenshot: tests/wpai-login-ui.png');
await browser.close();
server.close();
if (!info.shellVisible || info.toolboxW < 100 || info.cats < 5 || info.itemCount < 5) {
  process.exit(1);
}
