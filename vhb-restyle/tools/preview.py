#!/usr/bin/env python3
"""Composes a mock street section from the new art so the style can be judged in context (not the app's own renderer)."""
import generate as G
from svgkit import *
import art_street as S

def art(name):
    o = G.byname[name]; return G.fitted(o), o['bbox'][2], o['bbox'][3]
def put(name, cx, gy, dy=0):
    a, w, h = art(name); return g(a, f'translate({f(cx - w / 2)} {f(gy - h + dy)})')
def stack(kind, side, x, gy, floors):
    a, w, h = art(f'building-{kind}-{side}-ground-floor'); ua, uw, uh = art(f'building-{kind}-{side}-upper-floor'); ra, rw, rh = art(f'building-{kind}-{side}-roof')
    ux = x if side == 'left' else x + (w - uw)
    s = g(a, f'translate({x} {gy - h})')
    for i in range(floors): s += g(ua, f'translate({ux} {gy - h - uh * (i + 1)})')
    return s + g(ra, f'translate({ux - (rw - uw if side == "right" else 0)} {gy - h - uh * floors - rh})')

W, H, GY = 3042, 1180, 930; SW = GY - 14
segs = [('sidewalk', 192), ('sidewalk', 96), ('bike', 144), ('asphalt', 192), ('asphalt', 240), ('bus', 288), ('median', 96), ('rail', 288), ('sidewalk', 216), ('sidewalk', 144)]
COL = dict(sidewalk=lgrey, bike=leaf, asphalt=dgrey, bus=berry, median=concrete, rail='#7B7C7E')
s = f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{cobalt}"/><stop offset=".55" stop-color="{aqua}"/><stop offset="1" stop-color="#7FC1CD"/></linearGradient></defs>'
s += f'<rect width="{W}" height="{GY}" fill="url(#sky)"/>'
for x in range(0, W, 500): s += g(S.clouds(500, 240, 11, 5, .35), f'translate({x} 60)') + g(S.clouds(500, 560, 23, 7, .5), f'translate({x} 250)')
s += rr(0, GY, W, H - GY, espresso)
s += stack('wide', 'left', 0, SW, 2)
x = 736; cx = {}
for i, (k, w) in enumerate(segs):
    top = SW if k in ('sidewalk', 'median') else GY
    s += rr(x, top, w, 104 if top == SW else 90, COL[k]); cx[i] = x + w / 2; x += w
s += stack('narrow', 'right', x - 28, SW, 3)
for i, p in enumerate((3, 14, 23)): s += g(S.person(p), f'translate({cx[0] - 150 + i * 75} {SW - 190})')
s += put('tree-big', cx[1] + 10, SW) + put('lamp-traditional-both', cx[1] - 30, SW)
s += put('arrow-inbound-grey', cx[2], GY, 70) + put('cyclist-a-front', cx[2], GY)
s += put('car-front-parked', cx[3], GY) + put('parking-stall-line-right', cx[3] + 80, GY, 80)
s += put('arrow-outbound-straight', cx[4], GY, 75) + put('car-rear', cx[4], GY) + put('lane-edge-line-left', cx[4] + 116, GY, 85)
s += put('bus-front-shared-lane', cx[5], GY)
s += put('planter-box', cx[6], SW) + put('lamp-modern-both', cx[6] + 40, SW)
s += put('rail-tracks-dark', cx[7], GY, 85) + put('light-rail-front', cx[7], GY)
s += put('transit-shelter-light-rail-left', cx[8], SW)
s += put('bench-left', cx[9] - 30, SW) + g(S.person(19), f'translate({cx[9] - 10} {SW - 190})') + g(S.person(28), f'translate({cx[8] - 130} {SW - 190})')
G.write(G.OUT + '/preview/street-scene.svg', svg(W, H, s))
print('preview written')
