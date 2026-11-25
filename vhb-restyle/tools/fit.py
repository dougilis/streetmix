#!/usr/bin/env python3
"""Measures each probe render and records the transform that keeps the art inside its footprint (bottom edge = ground stays put).
Run: generate.py -> node render.js --probe -> fit.py -> generate.py"""
import json, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); PAD = 40
objs = json.load(open(HERE + '/../art-objects.json')); fits = {}
TILING = ('waterfront', 'lot-', 'surface', 'striped', 'parking-lot', 'ground-cover')   # must meet their neighbours edge to edge: fixed in the art, never rescaled
for o in objs:
    n = o['names'][0]
    if n.startswith(TILING): continue
    w, h = o['bbox'][2:]; b = Image.open(f'{HERE}/.probe/{n}.png').convert('RGBA').getbbox()
    x0, y0, x1, y1 = b[0] - PAD, b[1] - PAD, b[2] - PAD, b[3] - PAD
    if x0 >= 0 and y0 >= 0 and x1 <= w and y1 <= h: continue
    s = min(1, w / (x1 - x0), h / (y1 - y0))
    # scale about the bottom-centre, then slide back inside
    X0, X1 = w / 2 + (x0 - w / 2) * s, w / 2 + (x1 - w / 2) * s; Y0, Y1 = h + (y0 - h) * s, h + (y1 - h) * s
    dx = -X0 if X0 < 0 else (w - X1 if X1 > w else 0); dy = -Y0 if Y0 < 0 else (h - Y1 if Y1 > h else 0)
    fits[n] = f'translate({w / 2 * (1 - s) + dx:.2f} {h * (1 - s) + dy:.2f}) scale({s:.4f})'
json.dump(fits, open(HERE + '/fit.json', 'w'), indent=1); print(len(fits), 'sprites adjusted')
