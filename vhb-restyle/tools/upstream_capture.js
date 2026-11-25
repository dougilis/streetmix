// Records everything the running app requests while loading a street, so a single offline HTML can replay it.
const { chromium } = require('playwright')
const fs = require('fs')

async function main () {
  const out = process.argv[2]
  const browser = await chromium.launch({ args: ['--no-proxy-server'] })
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } })
  const recs = []
  page.on('response', async (res) => {
    const req = res.request()
    const url = new URL(res.url())
    if (url.origin !== 'http://localhost:8000') { recs.push({ external: res.url(), method: req.method() }); return }
    let body = null
    try { body = (await res.body()).toString('base64') } catch (e) {}
    recs.push({ method: req.method(), path: url.pathname + url.search, status: res.status(), type: res.headers()['content-type'] || '', body })
  })
  await page.goto('http://localhost:8000/new', { waitUntil: 'load', timeout: 60000 })
  await page.waitForTimeout(9000)
  const finalPath = new URL(page.url()).pathname
  fs.writeFileSync(out, JSON.stringify({ finalPath, recs }))
  for (const r of recs) console.log(r.external ? 'EXT ' + r.method + ' ' + r.external : r.method + ' ' + r.status + ' ' + r.path.slice(0, 90) + '  [' + (r.type || '').split(';')[0] + '] ' + (r.body ? Math.round(r.body.length * 0.75 / 1024) + 'k' : '-'))
  await browser.close()
}

main()
