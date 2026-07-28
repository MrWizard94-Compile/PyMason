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
// Clear tour/welcome flags so we can test
await page.evaluate(() => {
  localStorage.removeItem('pymason_welcomed');
  localStorage.removeItem('pymason_tour_done');
  sessionStorage.clear();
});
await page.reload({ waitUntil: 'domcontentloaded' });
await page.fill('#loginUser', 'studio');
await page.fill('#loginPass', 'wpai-forge');
await page.click('#loginForm button[type="submit"]');
await page.waitForTimeout(1500);

// Welcome → Take the tour
const welcome = page.locator('#welcomeStartTour');
if (await welcome.count()) {
  await welcome.click();
} else {
  await page.evaluate(() => startStudioTour(true));
}
await page.waitForTimeout(400);

let step1 = await page.evaluate(() => ({
  active: isStudioTourActive(),
  card: !!document.getElementById('tourCard'),
  title: document.querySelector('#tourCard h3')?.textContent,
  index: typeof tourState !== 'undefined' ? tourState.index : -1,
}));

// Advance a few steps
await page.click('#tourNext');
await page.waitForTimeout(200);
await page.click('#tourNext');
await page.waitForTimeout(200);
await page.keyboard.press('ArrowRight');
await page.waitForTimeout(200);

const mid = await page.evaluate(() => ({
  active: isStudioTourActive(),
  index: tourState.index,
  highlight: document.getElementById('tourHighlight')?.style?.display !== 'none',
  title: document.querySelector('#tourCard h3')?.textContent,
}));

// Replay from button
await page.keyboard.press('Escape');
await page.waitForTimeout(200);
await page.click('#btnTour');
await page.waitForTimeout(300);
const replay = await page.evaluate(() => ({
  active: isStudioTourActive(),
  index: tourState.index,
  title: document.querySelector('#tourCard h3')?.textContent,
}));

// Finish last step quickly
await page.evaluate(() => {
  tourState.index = STUDIO_TOUR_STEPS.length - 1;
  renderTourStep();
});
await page.waitForTimeout(150);
await page.click('#tourFinish');
await page.waitForTimeout(200);
const done = await page.evaluate(() => ({
  active: isStudioTourActive(),
  stored: localStorage.getItem('pymason_tour_done'),
}));

console.log(JSON.stringify({ step1, mid, replay, done, errors }, null, 2));
await page.screenshot({ path: path.join(ROOT, 'tests', 'tour-ui.png') });
await browser.close();
server.close();

const hard = errors.filter((m) => !/VALUE|ORDER/i.test(m));
if (
  hard.length ||
  !step1.active ||
  !mid.active ||
  mid.index < 1 ||
  !replay.active ||
  replay.index !== 0 ||
  done.active ||
  done.stored !== '1'
) {
  console.error('FAIL tour');
  process.exit(1);
}
console.log('tour OK');
