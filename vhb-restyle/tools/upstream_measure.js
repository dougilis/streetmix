const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path')
const root = process.argv[2], out = process.argv[3]
function walk (d) { return fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]) }
;(async () => {
  const b = await chromium.launch(); const p = await b.newPage(); const meta = {}
  for (const f of walk(root).filter(f => f.endsWith('.svg'))) {
    const src = fs.readFileSync(f, 'utf8'); const m = src.match(/viewBox="([\d.\s-]+)"/); if (!m) continue
    const [x, y, w, h] = m[1].trim().split(/\s+/).map(Number); if (w > 2200 || h > 1400) { meta[path.relative(root, f)] = { w, h, skipped: true }; continue }
    await p.setViewportSize({ width: Math.ceil(w), height: Math.ceil(h) })
    await p.setContent(`<body style="margin:0;background:transparent"><img src="data:image/svg+xml;base64,${Buffer.from(src).toString('base64')}" style="display:block;width:${w}px;height:${h}px"></body>`)
    const name = path.relative(root, f).replace(/\//g, '__').replace(/\.svg$/, '.png')
    await p.screenshot({ path: path.join(out, name), omitBackground: true }); meta[path.relative(root, f)] = { w, h, png: name }
  }
  fs.writeFileSync(path.join(out, 'meta.json'), JSON.stringify(meta)); await b.close(); console.log(Object.keys(meta).length)
})()
