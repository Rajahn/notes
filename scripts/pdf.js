// 把 mdBook 生成的 print.html 打印成 PDF：A4、页眉书名、页脚页码、PDF 书签。
// 用法：node scripts/pdf.js INPUT_PRINT_HTML OUTPUT_PDF
// 需要 playwright（npm install playwright）及其 Chromium。
// 公式样式来自 KaTeX 的 CDN；没有网络时，可以把 KATEX_DIST 设为本地 katex/dist 目录。
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

async function main() {
  const [input, output] = process.argv.slice(2);
  if (!input || !output) {
    console.error('usage: node scripts/pdf.js INPUT_PRINT_HTML OUTPUT_PDF');
    process.exit(2);
  }
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    // print.html 加载后会调用 window.print()，这里改成空操作。
    await page.addInitScript(() => { window.print = () => {}; });
    if (process.env.KATEX_DIST) {
      const dist = path.resolve(process.env.KATEX_DIST);
      await page.route(/cdn\.jsdelivr\.net\/npm\/katex@[^/]+\/dist\//, (route) => {
        const rel = route.request().url().split('/dist/')[1];
        return route.fulfill({ path: path.join(dist, rel) });
      });
    }
    await page.goto(pathToFileURL(path.resolve(input)).href, { waitUntil: 'networkidle', timeout: 600000 });
    const title = await page.evaluate(() => {
      const name = document.title;
      const cover = document.createElement('section');
      cover.className = 'pdf-cover';
      cover.innerHTML =
        '<h1></h1><p class="pdf-cover-note"></p>';
      cover.querySelector('h1').textContent = name;
      cover.querySelector('.pdf-cover-note').textContent =
        '离线 PDF 版　·　生成于 ' + new Date().toISOString().slice(0, 10);
      const style = document.createElement('style');
      style.textContent = `
        .pdf-cover { break-after: page; min-height: 230mm; display: flex;
          flex-direction: column; justify-content: center; text-align: center; }
        .pdf-cover h1 { font-size: 26pt; line-height: 1.4; margin: 0 0 12mm; }
        .pdf-cover-note { color: #555; font-size: 11pt; }
        details > *:not(summary) { display: block; }
        pre { white-space: pre-wrap; word-break: break-all; }
      `;
      document.head.appendChild(style);
      const main = document.querySelector('main') || document.body;
      main.insertBefore(cover, main.firstChild);
      // 打印版展开全部折叠块（练习答案等）。
      document.querySelectorAll('details').forEach((d) => { d.open = true; });
      return name;
    });
    await page.evaluate(() => document.fonts.ready);
    const small = 'font-size:8pt;color:#777;width:100%;padding:0 15mm;font-family:sans-serif;';
    await page.pdf({
      path: output,
      format: 'A4',
      margin: { top: '20mm', bottom: '20mm', left: '18mm', right: '18mm' },
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: `<div style="${small}text-align:right;"><span class="title"></span></div>`,
      footerTemplate: `<div style="${small}text-align:center;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>`,
      outline: true,
      tagged: true,
    });
    console.log(`pdf: ${output} (${title})`);
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
