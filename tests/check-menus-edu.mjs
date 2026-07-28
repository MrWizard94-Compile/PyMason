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
await page.evaluate(() => {
  localStorage.setItem('pymason_welcomed', '1');
  localStorage.setItem('pymason_tour_done', '1');
});
await page.fill('#loginUser', 'studio');
await page.fill('#loginPass', 'wpai-forge');
await page.click('#loginForm button[type="submit"]');
await page.waitForTimeout(1500);
await page.locator('#welcomeOverlay button').click({ timeout: 1500 }).catch(() => {});

const header = await page.evaluate(() => {
  const menus = ['menuFile', 'menuEdit', 'menuView', 'menuLearn', 'menuEducate'];
  return {
    menus: menus.map((id) => !!document.getElementById(id)),
    rawButtons: document.querySelectorAll('.header-actions > .btn').length,
    menuTriggers: document.querySelectorAll('.menu-trigger').length,
    hasRun: !!document.getElementById('btnRun'),
    hasChat: !!document.getElementById('btnChat'),
  };
});

// Open File menu
await page.click('#menuFile > .menu-trigger');
await page.waitForTimeout(100);
const fileOpen = await page.evaluate(() =>
  document.getElementById('menuFile')?.classList.contains('open')
);

// Educator dashboard
await page.evaluate(() => openEducatorDashboard());
await page.waitForTimeout(200);
const dash = await page.evaluate(() => !!document.getElementById('studioModal'));
await page.evaluate(() => closeStudioModal());

// Add roster + assignment
await page.evaluate(() => {
  setRoster([{ id: 's1', name: 'Ada' }]);
  // minimal assignment with print check
  const starter = Blockly.serialization.workspaces.save(workspace);
  setAssignments([
    {
      id: 'a1',
      title: 'Print lab',
      blurb: 'Print hello',
      checks: [{ id: 'print', label: 'Has print()', type: 'code_regex', pattern: 'print\\s*\\(' }],
      starter,
      createdAt: new Date().toISOString(),
    },
  ]);
  localStorage.setItem('pymason_edu_active_assign', 'a1');
  // add a print block
  const b = workspace.newBlock('text_print');
  b.initSvg();
  b.render();
  const t = workspace.newBlock('text');
  t.setFieldValue('hi', 'TEXT');
  t.initSvg();
  t.render();
  b.getInput('TEXT').connection.connect(t.outputConnection);
  updateCode();
});

await page.evaluate(() => runClassroomAutograde());
await page.waitForTimeout(200);
const auto = await page.evaluate(() => {
  const text = document.getElementById('studioModal')?.innerText || '';
  return { open: !!document.getElementById('studioModal'), pass: /1\s*\/\s*1/.test(text) || /✓/.test(text) };
});
await page.evaluate(() => {
  const sel = document.getElementById('gradeStudentSelect');
  if (sel) sel.value = 's1';
  saveAutogradeResult();
});
const grades = await page.evaluate(() => getGradebook().length);

// Student mode hides educate
await page.evaluate(() => setStudentMode(true));
const hidden = await page.evaluate(
  () => getComputedStyle(document.getElementById('menuEducate')).display === 'none'
);
await page.evaluate(() => setStudentMode(false));

console.log(
  JSON.stringify({ header, fileOpen, dash, auto, grades, hidden, errors }, null, 2)
);
await browser.close();
server.close();

const hard = errors.filter((m) => !/VALUE|ORDER/i.test(m));
if (
  hard.length ||
  !header.menus.every(Boolean) ||
  !fileOpen ||
  !dash ||
  grades < 1 ||
  !hidden
) {
  console.error('FAIL');
  process.exit(1);
}
console.log('menus+edu OK');
