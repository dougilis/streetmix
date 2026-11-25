// Rasterises every SVG under ../vhb to a PNG beside it (transparent background, 1:1 pixels).
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path')
const probe = process.argv[2] === '--probe'; const root = probe ? path.join(__dirname, '.probe') : path.join(__dirname, '..', (process.env.VHB_VARIANT || 'classic') === 'classic' ? 'vhb' : 'vhb-' + process.env.VHB_VARIANT); const only = probe ? null : process.argv[2]
function walk (d) { return fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]) }
;(async () => {
  const browser = await chromium.launch(); const page = await browser.newPage()
  for (const file of walk(root).filter(f => f.endsWith('.svg') && (!only || f.includes(only)))) {
    const src = fs.readFileSync(file, 'utf8'); const m = src.match(/width="([\d.]+)" height="([\d.]+)"/)
    await page.setViewportSize({ width: Math.ceil(+m[1]), height: Math.ceil(+m[2]) })
    await page.setContent(`<body style="margin:0;background:transparent">${src}</body>`)
    await page.screenshot({ path: file.replace(/\.svg$/, '.png'), omitBackground: true })
  }
  await browser.close()
})()
