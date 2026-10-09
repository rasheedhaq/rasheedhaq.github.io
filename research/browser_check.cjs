const { chromium } = require('C:/Users/rashe/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const { pathToFileURL } = require('url');
const path = require('path');
const os = require('os');
(async () => {
  const browser = await chromium.launch({channel:'msedge', headless:true});
  const failures=[];
  for (const width of [390,1440]) {
    const page=await browser.newPage({viewport:{width,height:900}});
    page.on('pageerror', e=>failures.push(e.message));
    for (const name of ['../index.html','../index_ats.html','index.html','thesis.html','publications.html','patents.html']) {
      await page.goto(pathToFileURL(path.resolve(__dirname,name)).href);
      await page.waitForTimeout(300);
      const result=await page.evaluate(()=>({title:document.title,overflow:document.documentElement.scrollWidth>innerWidth+1,h1:document.querySelectorAll('h1').length,brokenAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash)}));
      if(result.overflow||result.brokenAnchors.length) failures.push({width,name,...result});
      if(name==='publications.html') await page.screenshot({path:path.join(os.tmpdir(),`nitpy-papers-${width}.png`),fullPage:true});
      console.log(JSON.stringify({width,name,...result}));
    }
    await page.close();
  }
  await browser.close();
  console.log('Failures:',JSON.stringify(failures));
  if(failures.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
