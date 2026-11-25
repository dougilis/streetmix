#!/usr/bin/env python3
"""Regenerates every Streetmix sprite in the VHB style, at the exact pixel positions the app already reads.

  python3 tools/generate.py        -> vhb/sheets/tiles-{1,2,3}.svg, vhb/sprites/**, vhb/people/**, vhb/sky/**, vhb/preview/**
  node tools/render.js             -> PNGs next to each SVG

Inputs: ../manifest.json + ../art-objects.json (from the original sheets) and ../original/sheets/*.png (for anchor positions)."""
import json, os, re, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *
import art_vehicles as V, art_street as S

HERE = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.dirname(HERE); OUT = BASE + '/vhb'
man = json.load(open(BASE + '/manifest.json')); objs = json.load(open(BASE + '/art-objects.json'))
sheets = {f'tiles-{i}.png': Image.open(f'{BASE}/original/sheets/tiles-{i}.png').convert('RGBA') for i in (1, 2, 3)}
bymanifest = {m['name']: m for m in man}
byname = {n: o for o in objs for n in o['names']}
SURF = {'surface-bike-lane-green': leaf, 'surface-divider-median': concrete, 'surface-asphalt': dgrey, 'surface-bus-lane-red': berry,
        'surface-light-rail-grey': '#7B7C7E', 'surface-sidewalk-concrete': lgrey, 'surface-transit-platform-raised': lgrey}
BLD = {'narrow-left': (teal, deep, citron, white, 2), 'narrow-right': (body, gray, papaya, gray, 2),
       'wide-left': (aquaT, aqua, leaf, white, 4), 'wide-right': (cobalt, midnight, lgrey, white, 4)}
HOME = {'left': (aqua, deep, midnight, white), 'right': (leafT, leaf, espresso, leaf3)}
PRIDE = ['#E24C4B', papaya, yellow, leaf, cobalt, plum]


def content_bbox(sheet, x, y, w, h):
    b = sheets[sheet].crop((x, y, x + w, y + h)).getbbox()
    return None if not b else (x + b[0], y + b[1], b[2] - b[0], b[3] - b[1])


def foot(o):
    """Centre x (local) of whatever touches the ground in the original art, so poles and trunks land on the same spot."""
    x, y, w, h = o['bbox']; im = sheets[o['sheet']].crop((x, y + h - 6, x + w, y + h)); b = im.getbbox()
    return (b[0] + b[2]) / 2 if b else w / 2


def draw(o):
    n = o['names'][0]; x, y, w, h = o['bbox']; side = 'left' if n.endswith('left') or '-left-' in n else 'right'
    if n in SURF: return rr(0, 0, w, h, SURF[n])
    if n.startswith('lot-fence'): return S.fence(w, h)
    if n == 'lot-grass': return S.lot_grass(w, h)
    if n.startswith('wayfinding'): return S.wayfinding(w, h)
    if n.startswith('bike-rack-parallel'): return S.bike_rack_front(w, h, side)
    if n.startswith('bike-rack'): return S.bike_rack_side(w, h, side, 'road' in n)
    if n == 'bench-center': return S.bench_front(w, h)
    if n.startswith('bench'): return S.bench_side(w, h, side)
    m = re.match(r'arrow-(inbound|outbound)-(.+)', n)
    if m:
        grey = m.group(2).startswith('grey')
        return V.arrow(w, h, 'straight' if grey else m.group(2), m.group(1) == 'inbound', white, .45 if grey else None)
    if n.startswith('waterfront'): return S.waterfront_edge(w, h, side) if n.endswith('edge') else S.water(w, h)
    if n.startswith('parking-stall'): return V.stall_line(w, h, side)
    if n.startswith('lamp-modern'):
        px = foot(o)
        arms = {'both': [(-1, 0, px), (1, .2, min(w - px, 210))], 'right': [(1, 0, w - px)], 'left': [(-1, 0, px)]}[n.split('-')[-1]]
        return S.lamp_modern(w, h, px, arms)
    if n.startswith('lamp-traditional'):
        px = foot(o); return S.lamp_trad(w, h, px, {'both': [], 'left': [-1], 'right': [1]}[n.split('-')[-1]] if n.split('-')[-1] != 'both' else [])
    if n.startswith('bus-'): return V.bus(w, h, 'rear' in n)
    if n.startswith('car-side'): return V.car_side(w, h, side)
    if n.startswith('car-'):
        sig = 'left' if 'signal-left' in n else 'right' if 'signal-right' in n else None
        return V.car(w, h, 'rear' in n, sig)
    if n == 'tree-palm': return S.tree_palm(w, h, foot(o))
    if n == 'tree-big': return S.tree_big(w, h, foot(o))
    if n.startswith('light-rail'): return V.light_rail(w, h, 'rear' in n)
    if n.startswith('streetcar'): return V.streetcar(w, h, 'rear' in n)
    if n.startswith('cyclist-a'): return V.cyclist(w, h, 'rear' in n, aqua, citron, skin[3], midnight)
    if n.startswith('cyclist-b'): return V.cyclist(w, h, 'rear' in n, berry, papaya, skin[0], dgrey)
    if n.startswith('rail-tracks'): return V.rails(w, h, charcoal if 'dark' in n else gray)
    if n.startswith('truck'): return V.truck(w, h, 'rear' in n)
    if n.startswith('train'): return V.train(w, h)
    if n.startswith('center-line'): return V.center_line(w, h, side)
    if n.startswith('lane-edge'): return V.bar(w, h)
    if n.startswith('sharrow'): return V.sharrow(w, h, 'inbound' in n)
    if n == 'striped-buffer-hatching': return S.hatching(w, h)
    if n.startswith('parklet'): return S.parklet(w, h, side)
    if n == 'flowers': return S.flowers(w, h)
    if n == 'bollard': return S.bollard(w, h)
    if n == 'planter-box': return S.planter_box(w, h)
    if n == 'divider-dome': return S.dome(w, h)
    if n.startswith('transit-shelter'): return S.shelter(w, h, side, leaf if 'light-rail' in n else teal, citron)
    if n.startswith('banner'): return S.banner(w, h, side, PRIDE)
    if n.startswith('parking-lot'): return S.parking_lot(w, h, side, n.endswith('edge'))
    if n == 'ground-cover-grass':
        s = ''
        for part, fn in (('ground-cover-grass', S.grass_strip), ('bush', S.bush)):
            mm = bymanifest[part]
            bx, by, bw, bh = content_bbox(mm['sheet'], mm['px'], mm['py'], mm['pw'], 40 if part == 'ground-cover-grass' else mm['ph'])
            s += g(fn(bw, bh), f'translate({bx - x} {by - y})')
        return s
    m = re.match(r'building-(narrow|wide)-(left|right)-(roof|upper-floor|ground-floor)', n)
    if m:
        wall, trim, awn, frame, nwin = BLD[m.group(1) + '-' + m.group(2)]
        if m.group(3) == 'roof': return S.building_roof(w, h, trim)
        if m.group(3) == 'upper-floor': return S.building_upper(w, h, wall, trim, nwin, frame)
        ww = byname[n.replace('ground-floor', 'upper-floor')]['bbox'][2]
        return S.building_ground(w, h, ww, wall, trim, awn, m.group(2), frame)
    m = re.match(r'building-home-(left|right)-(roof|ground-floor)', n)
    if m:
        wall, trim, roofc, frame = HOME[m.group(1)]
        return S.home_roof(w, h, roofc, m.group(1)) if m.group(2) == 'roof' else S.home(w, h, wall, trim, roofc, m.group(1), frame)
    raise KeyError(n)


FITS = json.load(open(HERE + '/fit.json')) if os.path.exists(HERE + '/fit.json') else {}
PAD = 40


def fitted(o):
    """Art nudged/scaled (see fit.py) so nothing spills outside the footprint the app crops for this sprite."""
    art = draw(o); t = FITS.get(o['names'][0])
    return g(art, t) if t else art


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True); open(path, 'w').write(content)


def main():
    cat = {m['name']: m['category'] for m in man}; layers = {k: [] for k in sheets}; index = []
    for o in objs:
        x, y, w, h = o['bbox']; art = fitted(o); n = o['names'][0]
        layers[o['sheet']].append(g(art, f'translate({x} {y})', n))
        write(f'{OUT}/sprites/{cat[n]}/{n}.svg', svg(w, h, art))
        write(f'{HERE}/.probe/{n}.svg', svg(w + 2 * PAD, h + 2 * PAD, g(draw(o), f'translate({PAD} {PAD})')))
        index.append(dict(name=n, alsoCoveredCrops=o['names'][1:], category=cat[n], sheet=o['sheet'], x=x, y=y, w=w, h=h, file=f'vhb/sprites/{cat[n]}/{n}.svg'))
    for k, ls in layers.items():
        W, H = sheets[k].size; write(f'{OUT}/sheets/{k[:-4]}.svg', svg(W, H, ''.join(ls)))
    # people
    cols = 8; ps = ''
    for i in range(1, 32):
        art = S.person(i); write(f'{OUT}/people/people-{i:02d}.svg', svg(120, 192, art))
        ps += g(art, f'translate({((i - 1) % cols) * 130 + 10} {((i - 1) // cols) * 210 + 10})', f'people-{i:02d}')
    write(f'{OUT}/people/people-sheet.svg', svg(cols * 130 + 10, 4 * 210 + 10, ps))
    # sky
    write(f'{OUT}/sky/sky-rear.svg', svg(500, 240, S.clouds(500, 240, 11, 5, .55)))
    write(f'{OUT}/sky/sky-front.svg', svg(500, 560, S.clouds(500, 560, 23, 7, .9)))
    json.dump(index, open(f'{OUT}/sprite-index.json', 'w'), indent=1)
    print(len(index), 'art objects,', 31, 'people, 2 sky bands')


if __name__ == '__main__':
    main()
