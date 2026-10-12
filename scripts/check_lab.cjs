// Run with Playwright and its Chromium browser available in the Node environment.
const { chromium } = require('playwright');
const { resolve } = require('node:path');
const { pathToFileURL } = require('node:url');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  try {
    for (const width of [320, 390, 768, 1440]) {
      const page = await browser.newPage({ viewport: { width, height: 1000 } });
      for (const name of ['index', 'virtual-sensing', 'water-quality-prediction', 'monitoring-prototype', 'nammaopen', 'vlc-playlists']) {
        await page.goto(pathToFileURL(resolve(__dirname, '../lab', name + '.html')).href);
        await page.evaluate(() => document.fonts.ready);
        const result = await page.evaluate(() => ({
          overflow: document.documentElement.scrollWidth > innerWidth,
          hiddenNavigation: [...document.querySelectorAll('nav a')].some(a => {
            const rect = a.getBoundingClientRect();
            return rect.left < 0 || rect.right > innerWidth;
          }),
          currentPages: document.querySelectorAll('[aria-current="page"]').length,
          sections: document.querySelectorAll('.story section').length,
          unsafeLinks: document.querySelectorAll('a[target="_blank"]:not([rel~="noopener"])').length
        }));
        assert.equal(result.overflow, false, name + ': page overflow');
        assert.equal(result.hiddenNavigation, false, name + ': hidden navigation');
        assert.equal(result.currentPages, name === 'index' ? 1 : 0);
        assert.equal(result.sections, name === 'index' ? 0 : 4);
        assert.equal(result.unsafeLinks, 0);
        console.log(width, name, 'PASS');
        if (process.env.LAB_SCREENSHOTS && ['index', 'virtual-sensing'].includes(name)) {
          await page.screenshot({ path: resolve(process.env.LAB_SCREENSHOTS, `lab-${name}-${width}.png`), fullPage: true });
        }
      }
      await page.close();
    }
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
