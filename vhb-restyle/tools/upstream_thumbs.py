#!/usr/bin/env python3
"""Redraws the 38 palette thumbnails (packages/illustrations/images/thumbnails/*.svg, 60 x 80) in the marker-sketch style.

  python3 tools/upstream_thumbs.py <images dir>

Each thumbnail is a strip of ground with the segment's main subject standing on it, like the originals."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *
import styles, art_modern as M, art_street as S

OUT = sys.argv[1] + '/thumbnails'; st = styles.Sketch()
ROAD, WALK, SAND, EARTH = '#6E7085', '#F1EFE7', '#EADDBB', '#9A8F86'
SK = skin


def umbrella(w, h, c=papaya):
    return st.ln(.5 * w, .2 * h, .5 * w, h, midnight, 5) + st.p(f'M0 {f(.3*h)}Q{f(.5*w)} {f(-.28*h)} {f(w)} {f(.3*h)}Z', c)
def dining(w, h):
    s = umbrella(w, h * .62, berry) + st.ln(.5 * w, .5 * h, .5 * w, h, midnight, 5) + st.r(.28 * w, .64 * h, .44 * w, .05 * h, wood, 3)
    for x in (.06, .76): s += st.r(x * w, .56 * h, .16 * w, .26 * h, wood, 4) + st.ln((x + .08) * w, .82 * h, (x + .08) * w, h, midnight, 5)
    return s
def scooter(w, h, rider=False):
    s = (g(M.figure(st, 0, 0, h * .9, SK[1], S.HAIR[0], cobalt, midnight), f'translate({f(.42*w)} {f(.93*h)})') if rider else '')
    s += st.ln(.14 * w, .93 * h, .8 * w, .93 * h, midnight, 7) + st.ln(.8 * w, .93 * h, .7 * w, .36 * h, midnight, 6) + st.ln(.56 * w, .36 * h, .82 * w, .36 * h, midnight, 7)
    return s + st.c(.16 * w, .94 * h, .06 * h, charcoal, ol=False) + st.c(.82 * w, .94 * h, .06 * h, charcoal, ol=False)
def cone(w, h):
    return st.pg([(.4 * w, 0), (.6 * w, 0), (.84 * w, .86 * h), (.16 * w, .86 * h)], papaya) + st.r(.3 * w, .36 * h, .4 * w, .14 * h, white, 0, ol=False) + st.r(.04 * w, .86 * h, .92 * w, .14 * h, papaya, 4)
def utility(w, h):
    s = st.r(.46 * w, 0, .09 * w, h, wood, 2) + st.r(.1 * w, .1 * h, .8 * w, .045 * h, wood, 2) + st.r(.22 * w, .21 * h, .56 * w, .04 * h, wood, 2)
    return s + st.r(.58 * w, .38 * h, .2 * w, .16 * h, gray, 5)
def guardrail(w, h): return st.r(.36 * w, .12 * h, .28 * w, .88 * h, midnight, 5, ol=False) + st.c(.5 * w, .1 * h, .2 * w, midnight, ol=False)
def wall(w, h): return st.r(0, .56 * h, .56 * w, .44 * h, concrete) + st.pg([(.5 * w, h), (.58 * w, 0), (.84 * w, 0), (.92 * w, h)], '#D9D7CE')
def slope(w, h): return st.pg([(0, h), (w, .15 * h), (w, h)], concrete) + path(f'M{f(.1*w)} {f(.86*h)}L{f(.95*w)} {f(.14*h)}', 'none', leaf2, 9)
def bioswale(w, h): return st.p(f'M0 {f(.1*h)}Q{f(.5*w)} {f(1.5*h)} {f(w)} {f(.1*h)}V{f(h)}H0Z', EARTH) + g(M.bush(st, .44 * w, .5 * h), f'translate({f(.28*w)} {f(.12*h)})')
def drainage(w, h): return st.pg([(0, 0), (.26 * w, 0), (.44 * w, .78 * h), (.56 * w, .78 * h), (.74 * w, 0), (w, 0), (w, h), (0, h)], concrete)
def marsh(w, h):
    s = ''
    for i, (x, lean, c) in enumerate(((.1, .25, leaf3), (.3, .3, leaf), (.5, .22, leaf2), (.68, .3, leaf), (.84, .16, leaf3))):
        s += st.p(f'M{f(x*w)} {f(h)}Q{f(x*w)} {f(.3*h)} {f((x+lean)*w)} {f(.05*h + i%2*.12*h)}Q{f((x+.1)*w)} {f(.5*h)} {f((x+.12)*w)} {f(h)}Z', c)
    return s
def vendor(w, h):
    s = g(M.figure(st, 0, 0, h * .95, SK[3], S.HAIR[1], leaf, midnight, True), f'translate({f(.5*w)} {f(h)})')
    s += st.r(.04 * w, .56 * h, .92 * w, .07 * h, wood, 3) + st.r(.1 * w, .63 * h, .07 * w, .37 * h, wood, 0) + st.r(.83 * w, .63 * h, .07 * w, .37 * h, wood, 0)
    return s + st.c(.26 * w, .52 * h, .06 * w, berry, ol=False) + st.c(.4 * w, .52 * h, .06 * w, papaya, ol=False) + st.c(.7 * w, .52 * h, .07 * w, citron, ol=False)
def foodtruck(w, h):
    s = st.r(.14 * w, .9 * h, .16 * w, .1 * h, charcoal, 5, ol=False) + st.r(.7 * w, .9 * h, .16 * w, .1 * h, charcoal, 5, ol=False)
    s += st.r(.06 * w, .12 * h, .88 * w, .8 * h, leaf, 18) + st.glass(.16 * w, .26 * h, .68 * w, .26 * h, 10) + st.r(0, .08 * h, w, .1 * h, citron, 8)
    return s + st.r(.2 * w, .64 * h, .6 * w, .12 * h, midnight, 6, ol=False) + st.r(.14 * w, .8 * h, .16 * w, .05 * h, lamp, 4, ol=False) + st.r(.7 * w, .8 * h, .16 * w, .05 * h, lamp, 4, ol=False)
def carpet(w, h):
    s = st.c(.5 * w, .2 * h, .11 * w, SK[2]) + st.r(.34 * w, .32 * h, .32 * w, .3 * h, aqua, 14)
    s += st.p(f'M0 {f(.7*h)}Q{f(.25*w)} {f(.58*h)} {f(.5*w)} {f(.7*h)}T{f(w)} {f(.7*h)}V{f(.84*h)}Q{f(.75*w)} {f(.96*h)} {f(.5*w)} {f(.84*h)}T0 {f(.84*h)}Z', plum)
    return s + st.r(.1 * w, .72 * h, .8 * w, .04 * h, citron, 2, ol=False)
def curb(w, h):
    s = st.r(.2 * w, .1 * h, 7, .9 * h, gray, 3, ol=False) + st.r(.12 * w, .02 * h, .26 * w, .16 * h, midnight, 5) + st.r(.17 * w, .06 * h, .16 * w, .04 * h, citron, 2, ol=False)
    return s + g(M.figure(st, 0, 0, h * .62, SK[2], S.HAIR[2], teal, midnight), f'translate({f(.68*w)} {f(h)})')
def missing(w, h): return st.ring(w / 2, h / 2, w * .42, berry, 6).replace(st.ink, berry) + line(.2 * w, .2 * h, .8 * w, .8 * h, berry, 12)
def bikeshare(w, h): return st.r(0, 0, .42 * w, h, white, 8) + st.glass(.07 * w, .08 * h, .28 * w, .3 * h, 5) + g(M.bike_side(st, .72 * w, .52 * h, leaf), f'translate({f(.28*w)} {f(.48*h)})')
def people(w, h):
    return ''.join(g(M.figure(st, 0, 0, ht, SK[i], S.HAIR[i], c, midnight, d), f'translate({f(x*w)} {f(h)})') for i, (x, ht, c, d) in enumerate(((.18, h * .92, leaf, True), (.5, h, cobalt, False), (.82, h * .86, papaya, False))))
def beach(w, h): return g(umbrella(.8 * w, h, cobalt), f'translate({f(.02*w)} 0) rotate(-12 {f(.4*w)} {f(h)})') + st.r(.5 * w, .78 * h, .46 * w, .08 * h, aqua, 4) + st.ln(.56 * w, .86 * h, .56 * w, h, midnight, 5) + st.ln(.9 * w, .86 * h, .9 * w, h, midnight, 5)
def brt_station(w, h): return M.shelter(st, w, h, 'left', papaya) + g(M.figure(st, 0, 0, h * .55, SK[4], S.HAIR[1], citron, midnight, True), f'translate({f(.3*w)} {f(h)})')

car = lambda **k: (lambda w, h: M.car(st, w, h, **k))
# name: (ground colour, native width, native height, drawing)
T = {
    'beach': (SAND, 150, 170, beach), 'bike-lane': (ROAD, 55, 137, lambda w, h: M.cyclist(st, w, h, False, aqua, citron, SK[3], midnight)),
    'bikeshare': (ROAD, 170, 170, bikeshare), 'bioswale': (None, 160, 70, bioswale),
    'brt-lane': (ROAD, 251, 241, lambda w, h: M.bus(st, w, h)), 'brt-station': (WALK, 210, 240, brt_station),
    'bus-lane': (ROAD, 251, 241, lambda w, h: M.bus(st, w, h)), 'divider': (WALK, 110, 70, lambda w, h: M.flowers(st, w, h) + g(M.tufts(st, w, h * .3, 6), f'translate(0 {f(h*.7)})')),
    'drainage-channel': (None, 160, 80, drainage), 'drive-lane': (ROAD, 145, 120, car()),
    'flex-zone-curb': (WALK, 130, 240, curb), 'flex-zone': (ROAD, 210, 132, car(bodyc=yellow, belt=charcoal, topper=white, door='left', cw=145)),
    'food-truck': (ROAD, 200, 210, foodtruck), 'guardrail': (WALK, 50, 160, guardrail),
    'light-rail': (ROAD, 192, 383, lambda w, h: M.light_rail(st, w, h)), 'magic-carpet': (ROAD, 170, 130, carpet),
    'marsh': (EARTH, 160, 120, marsh), 'missing': (None, 100, 100, missing), 'outdoor-dining': (WALK, 180, 210, dining),
    'parking-lane': (ROAD, 145, 120, car()), 'parklet': (ROAD, 191, 145, lambda w, h: M.parklet(st, w, h, 'right')),
    'scooter-drop-zone': (WALK, 120, 110, scooter), 'scooter': (ROAD, 110, 200, lambda w, h: scooter(w, h, True)),
    'sidewalk-bench': (WALK, 100, 94, lambda w, h: M.bench_side(st, w, h, 'left')), 'sidewalk-bike-rack': (WALK, 137, 81, lambda w, h: M.bike_rack_side(st, w, h, 'right', False)),
    'sidewalk-lamp': (None, 80, 240, lambda w, h: M.lamp_trad(st, w, h, w / 2, [])), 'sidewalk-tree': (None, 150, 300, lambda w, h: M.tree_big(st, w, h, w / 2)),
    'sidewalk-wayfinding': (WALK, 96, 198, lambda w, h: M.wayfinding(st, w, h)), 'sidewalk': (WALK, 190, 170, people),
    'slope': (None, 160, 90, slope), 'street-vendor': (WALK, 170, 190, vendor), 'streetcar': (ROAD, 249, 317, lambda w, h: M.streetcar(st, w, h)),
    'temporary': (ROAD, 80, 110, cone), 'train': (ROAD, 311, 361, lambda w, h: M.train(st, w, h)),
    'transit-shelter': (WALK, 207, 282, lambda w, h: M.shelter(st, w, h, 'left', teal)), 'turn-lane': (ROAD, 158, 120, car(rear=True, signal='left')),
    'utilities': (None, 120, 300, utility), 'wall': (None, 160, 190, wall),
}
for name, (ground, w, h, fn) in T.items():
    st.seed('thumb-' + name); base = 72 if ground else 80
    s = min(54 / w, (base - 6) / h); art = g(fn(w, h), f'translate({f((60 - w * s) / 2)} {f(base - h * s)}) scale({s:.4f})')
    strip = rr(0, 72, 60, 8, ground) if ground else ''
    open(f'{OUT}/{name}.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 80" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2">{strip}{art}</svg>\n')
print(len(T), 'thumbnails written')
