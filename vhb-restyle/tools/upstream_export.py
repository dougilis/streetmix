#!/usr/bin/env python3
"""Redraws current-Streetmix illustrations (packages/illustrations/images/**.svg) in the VHB marker-sketch style.

  node tools/upstream_measure.js <images dir> <tmp dir>     # rasterises the originals and records their content bounds
  python3 tools/upstream_export.py <images dir> <tmp dir>   # overwrites every sprite it knows how to draw

Each output keeps the original viewBox and draws into the original art's footprint, so the app's sprite positions
still line up. Upstream art is 100 units per metre; the sketch drawings were made at 24 px per foot, hence K."""
import json, os, re, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *
import styles, art_modern as M, art_vehicles as V, art_street as S

IMAGES, TMP = sys.argv[1], sys.argv[2]; K = 100 / (24 / .3048)
meta = json.load(open(TMP + '/meta.json')); st = styles.Sketch(); done, skipped = [], []
SURF = {'asphalt': '#6E7085', 'asphalt-gray': '#8C8EA3', 'asphalt-green': '#A9C487', 'asphalt-red': '#A8456A', 'concrete': '#F1EFE7', 'earth': '#9A8F86', 'sand': '#EADDBB', 'wall': '#D9D7CE'}
FLOWERS = {'blue': (cobalt, aqua, cobaltT), 'orange': (papaya, yellow, papaya), 'red': (berry, '#E24C4B', berry), 'white': (white, lgrey, white), 'yellow': (yellow, citron, yellow)}
BLD = {'apartments-narrow': {'left': (teal, deep, citron, 2), 'right': (body, gray, papaya, 2)}, 'apartments-wide': {'left': (aquaT, aqua, leaf, 4), 'right': (aqua, midnight, citron, 4)}}
HOME = {'left': (aqua, deep, midnight), 'right': (leafT, leaf, espresso)}


def png(rel): return Image.open(f"{TMP}/{meta[rel]['png']}").convert('RGBA')
def band(rel, y0, y1):
    im = png(rel).crop((0, int(y0), meta[rel]['w'], int(y1))); b = im.getbbox(); return (b[0], b[2]) if b else (0, meta[rel]['w'])
def boxed(x0, y0, x1, y1, fn):
    """Run a drawing function written for the 24px/ft scale inside an upstream-unit rectangle."""
    return g(fn((x1 - x0) / K, (y1 - y0) / K), f'translate({f(x0)} {f(y0)}) scale({K:.4f})')
def stretched(x0, y0, x1, y1, nw, nh, art): return g(art, f'translate({f(x0)} {f(y0)}) scale({(x1 - x0) / nw:.4f} {(y1 - y0) / nh:.4f})')


def building(rel, kind, side, m):
    W, H = m['w'], m['h']; d = json.load(open(os.path.dirname(os.path.abspath(__file__)) + '/upstream_buildings.json'))[kind]
    roof, floor = d['roof'] * 100, d['floor'] * 100
    if kind == 'residential':
        wall, trim, roofc = HOME[side]; rx = band(rel, 0, roof - 8); mx = band(rel, roof + 4, H)
        s = boxed(rx[0], m['bbox'][1], rx[1], roof, lambda w, h: M.home_roof(st, w, h, roofc, side))
        return s + stretched(mx[0], roof, mx[1], H, 729, 588, M.home(st, 729, 588, wall, trim, roofc, side))
    wall, trim, awn, n = BLD[kind][side]; rx = band(rel, 0, roof - 4); fx = band(rel, roof + 8, roof + floor - 8); gx = band(rel, roof + floor + 4, H)
    s = boxed(rx[0], m['bbox'][1], rx[1], roof, lambda w, h: M.building_roof(st, w, h, trim))
    s += boxed(fx[0], roof, fx[1], roof + floor, lambda w, h: M.building_upper(st, w, h, wall, trim, n))
    return s + boxed(gx[0], roof + floor, gx[1], H, lambda w, h: M.building_ground(st, w, h, (fx[1] - fx[0]) / K, wall, trim, awn, side))


def art(rel, m):
    d, n = rel[:-4].split('/'); W, H = m['w'], m['h']; b = m.get('bbox'); side = 'left' if n.endswith('left') or '-left-' in n else 'right'
    if not b: return None
    x0, y0, x1, y1 = b; fx = ((m['foot'][0] + m['foot'][1]) / 2 - x0) / K if m.get('foot') else (x1 - x0) / 2 / K
    box = lambda fn: boxed(x0, y0, x1, y1, fn)
    if d == 'ground': return rr(0, 0, W, H, SURF[n]) if n in SURF else None
    if d == 'vehicles':
        mm = re.match(r'(car|taxi|rideshare)-(inbound|outbound)(?:-(turn-signal|door)-(left|right))?$', n)
        if mm:
            kind, dirn, extra, sd = mm.groups(); kw = dict(rear=dirn == 'outbound', cw=184 / K)
            if extra == 'turn-signal': kw['signal'] = sd
            if extra == 'door': kw['door'] = sd
            if kind == 'taxi': kw.update(bodyc=yellow, belt=charcoal, topper=white)
            if kind == 'rideshare': kw.update(belt=aqua, topper=berry)
            return box(lambda w, h: M.car(st, w, h, **kw))
        if n.startswith('car-sideways') or n.startswith('car-angled'): return box(lambda w, h: M.car_side(st, w, h, side))
        if n.startswith('truck'): return box(lambda w, h: M.truck(st, w, h, 'outbound' in n))
    if d == 'transit':
        if re.match(r'bus-(in|out)bound', n): return box(lambda w, h: M.bus(st, w, h, 'outbound' in n))
        if n.startswith('light-rail'): return box(lambda w, h: M.light_rail(st, w, h, 'outbound' in n))
        if n.startswith('streetcar'): return box(lambda w, h: M.streetcar(st, w, h, 'outbound' in n))
        if n.startswith('tracks'): return box(lambda w, h: V.rails(w, h, st.col(charcoal) if 'dark' in n else st.col(gray)))
        if n.startswith('transit-shelter'): return box(lambda w, h: M.shelter(st, w, h, side, teal if '-01-' in n else leaf))
    if d == 'trees': return box(lambda w, h: M.tree_palm(st, w, h, fx) if 'palm' in n else M.tree_big(st, w, h, fx))
    if d == 'bikes':
        if n.startswith('bike-rack-parallel'): return box(lambda w, h: M.bike_rack_front(st, w, h, side))
        if n.startswith('bike-rack-perp'): return box(lambda w, h: M.bike_rack_side(st, w, h, side, False))
        if n.startswith('biker-01'): return box(lambda w, h: M.cyclist(st, w, h, 'outbound' in n, aqua, citron, skin[3], midnight))
        if n.startswith('biker-02'): return box(lambda w, h: M.cyclist(st, w, h, 'outbound' in n, berry, papaya, skin[0], dgrey))
    if d == 'dividers':
        if n in ('bollard', 'dome'): return box(lambda w, h: getattr(M, n)(st, w, h))
        if n == 'planter-box': return box(lambda w, h: M.planter_box(st, w, h))
    if d == 'furniture' and n.startswith('bench'): return box(lambda w, h: M.bench_front(st, w, h) if n.endswith('center') else M.bench_side(st, w, h, side))
    if d == 'parklet': return box(lambda w, h: M.parklet(st, w, h, side))
    if d == 'wayfinding': return box(lambda w, h: M.wayfinding(st, w, h))
    if d == 'secret': return box(lambda w, h: M.train(st, w, h))
    if d == 'lamps':
        if n.startswith('lamp-modern'):
            arms = {'both': lambda w: [(-1, 0, fx), (1, .2, min(w - fx, 210))], 'right': lambda w: [(1, 0, w - fx)], 'left': lambda w: [(-1, 0, fx)]}[n.split('-')[2]]
            return box(lambda w, h: M.lamp_modern(st, w, h, fx, arms(w)))
        if n.startswith('lamp-traditional'):
            arms = {'both': [-1, 1], 'center': [], 'left': [-1], 'right': [1], 'with': [-1, 1]}[n.split('-')[2]]
            return box(lambda w, h: M.lamp_trad(st, w, h, fx, arms))
        if n.startswith('pride-banner'): return box(lambda w, h: M.banner(st, w, h, side, M.PRIDE))
    if d == 'plants':
        if n == 'bush': return box(lambda w, h: M.bush(st, w, h))
        if n == 'grass': return box(lambda w, h: M.tufts(st, w, h, 8))
        if n.startswith('flowers-'): return box(lambda w, h: M.flowers(st, w, h, FLOWERS[n[8:]]))
    if d == 'people':
        mm = re.match(r'people-(\d\d)(-back)?$', n)
        if mm and int(mm.group(1)) <= 31:                      # the 31 figures keep their kinds; scaled so feet land on the original baseline
            k = 220 / 192; return g(M.person(st, int(mm.group(1))), f'translate({f((x0 + x1) / 2 - 60 * k)} {f(y1 - 190 * k)}) scale({k:.4f})')
        if mm:
            i = int(mm.group(1)); r = rng(700 + i); ht = (y1 - y0) / K * .94
            fig = M.figure(st, 60, 190, ht, skin[i % 5], S.HAIR[i % 6], S.TOPS[(i * 5) % 12], S.BOTS[(i * 3) % 7], i % 2 == 0)
            sx = min(1, (W - 8) / (.36 * (y1 - y0)))          # these viewBoxes are narrow: slim the figure rather than shorten it
            return g(fig, f'translate({f((x0 + x1) / 2 - 60 * K * sx)} {f(y1 - 190 * K)}) scale({K * sx:.4f} {K:.4f})')
    if d == 'buildings':
        mm = re.match(r'(apartments-narrow|apartments-wide|residential)-(left|right)$', n)
        if mm: return building(rel, mm.group(1), mm.group(2), m)
    if d == 'boundaries':
        if n.startswith('fenced-lot'): return box(lambda w, h: M.fence(st, w, h))
        if n == 'grass': return box(lambda w, h: M.tufts(st, w, h, 6))
        hw = W / 2
        if n.startswith('parking-lot'):            # one half repeats, the half nearest the street carries the sign
            e, r_ = (hw, 0) if side == 'left' else (0, hw)
            return boxed(e, y0, e + hw, y1, lambda w, h: M.parking_lot(st, w, h, side, True)) + boxed(r_, y0, r_ + hw, y1, lambda w, h: M.parking_lot(st, w, h, side, False))
        if re.match(r'waterfront2?-', n):
            e, r_ = (hw, 0) if side == 'left' else (0, hw); wy = y1 - 105 * K
            return boxed(r_, wy, r_ + hw, y1, lambda w, h: M.water(st, w, h)) + boxed(e, y0, e + hw, y1, lambda w, h: M.waterfront_edge(st, w, h, side))
        if n.startswith('water-'): return boxed(0, y0, hw, y1, lambda w, h: M.water(st, w, h)) + boxed(hw, y0, W, y1, lambda w, h: M.water(st, w, h, 9))
    if d == 'sky' and n in ('sky-front', 'sky-rear'):
        return g(M.clouds(st, 2 * W, 2 * H, 23 if 'front' in n else 11, 7 if 'front' in n else 5, .95), 'scale(.5)')
    return None


for rel, m in sorted(meta.items()):
    if m.get('skipped') or '_retired' in rel or rel == 'missing.svg': skipped.append(rel); continue
    st.seed(rel); a = art(rel, m)
    if a is None: skipped.append(rel); continue
    W, H = m['w'], m['h']
    open(f'{IMAGES}/{rel}', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2">{a}</svg>\n')
    done.append(rel)
json.dump({'redrawn': done, 'untouched': skipped}, open(TMP + '/export-report.json', 'w'), indent=1)
import collections
print(len(done), 'redrawn,', len(skipped), 'left as upstream art')
c = collections.Counter(r.split('/')[0] for r in skipped); print('untouched by folder:', dict(c))
