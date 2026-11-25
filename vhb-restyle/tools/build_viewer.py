#!/usr/bin/env python3
"""Builds vhb-streetmix-sketch.html: one self-contained page that draws a live, editable street from the sketch sheets,
using the segment definitions in assets/scripts/segments/info.js and the same placement maths as the app."""
import base64, json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.dirname(HERE); ROOT = os.path.dirname(BASE)
JS = r"""
const fs = require('fs'); let src = fs.readFileSync(process.argv[1], 'utf8').replace(/^export /gm, '').replace(/^import .*$/gm, '')
const S = new Function(src + '\nreturn SEGMENT_INFO')(); const out = {}
for (const [k, v] of Object.entries(S)) { out[k] = { name: v.name, zIndex: v.zIndex, defaultWidth: v.defaultWidth, variants: v.variants, secret: !!v.secret, details: {} }
  for (const [d, x] of Object.entries(v.details)) out[k].details[d] = { name: x.name, graphics: x.graphics } }
console.log(JSON.stringify(out))
"""
seginfo = subprocess.check_output(['node', '-e', JS, ROOT + '/assets/scripts/segments/info.js']).decode().strip()
def uri(path, mime): return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()
art = {'sketch': {str(i): uri(f'{BASE}/vhb-sketch/sheets/tiles-{i}.png', 'image/png') for i in (1, 2, 3)},
       'original': {str(i): uri(f'{BASE}/original/sheets/tiles-{i}.png', 'image/png') for i in (1, 2, 3)}}
for k, d in (('sketch', 'vhb-sketch/sky'), ('original', 'original/sky')):
    art[k]['skyFront'] = uri(f'{BASE}/{d}/sky-front.png', 'image/png'); art[k]['skyRear'] = uri(f'{BASE}/{d}/sky-rear.png', 'image/png')
people = [uri(f'{BASE}/vhb-sketch/people/people-{i:02d}.svg', 'image/svg+xml') for i in range(1, 32)]
html = open(HERE + '/viewer_template.html').read().replace('__SEGINFO__', seginfo).replace('__ART__', json.dumps(art)).replace('__PEOPLE__', json.dumps(people))
open(BASE + '/vhb-streetmix-sketch.html', 'w').write(html); print('wrote', round(len(html) / 1e6, 2), 'MB')
