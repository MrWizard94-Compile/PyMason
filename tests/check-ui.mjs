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
      res.end('no');
      return;
    }
    const ext = path.extname(fp);
    const ct =
      ext === '.html'
        ? 'text/html'
        : ext === '.js'
          ? 'application/javascript'
          : 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': ct });
    res.end(data);
  });
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
await page.goto(`http://127.0.0.1:${port}/index.html`, {
  waitUntil: 'domcontentloaded',
  timeout: 90000,
});
await page.waitForTimeout(4000);
const info = await page.evaluate(() => {
  const inj = document.getElementById('blocklyDiv');
  const classes = [...document.querySelectorAll('*')]
    .map((e) => e.className)
    .filter((c) => typeof c === 'string' && c.includes('blockly'))
    .slice(0, 50);
  const tb = document.querySelector('.blocklyToolbox, .blocklyToolboxDiv');
  const label = document.querySelector('.blocklyToolboxCategoryLabel, .blocklyTreeLabel');
  const cs = tb ? getComputedStyle(tb) : null;
  const lcs = label ? getComputedStyle(label) : null;
  return {
    hasBlockly: typeof Blockly !== 'undefined',
    hasSvg: !!document.querySelector('.blocklySvg'),
    toolbox: !!tb,
    toolboxW: tb?.offsetWidth || 0,
    toolboxH: tb?.offsetHeight || 0,
    toolboxBg: cs?.backgroundColor,
    toolboxColor: cs?.color,
    labelText: label?.textContent,
    labelColor: lcs?.color,
    flyout: !!document.querySelector('.blocklyFlyout'),
    injKids: inj ? inj.children.length : -1,
    categoryCount: document.querySelectorAll('.blocklyToolboxCategory').length,
    status: document.getElementById('statusText')?.textContent,
  };
});
console.log(JSON.stringify({ info, errors }, null, 2));
await browser.close();
server.close();
