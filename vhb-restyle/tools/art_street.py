"""Nature, street furniture, transit shelters, buildings, lots, sky and people in the VHB palette."""
from svgkit import *
from art_vehicles import car, car_side, _glint


def clip_poly(pts, w, h):
    """Clip a polygon to the 0..w / 0..h box so tiles never bleed into their neighbours."""
    def cut(ps, inside, inter):
        out = []
        for i, p in enumerate(ps):
            q = ps[i - 1]
            if inside(p):
                if not inside(q): out.append(inter(q, p))
                out.append(p)
            elif inside(q): out.append(inter(q, p))
        return out
    def ix(x): return lambda a, b: (x, a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0]))
    def iy(y): return lambda a, b: (a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]), y)
    for ins, it in ((lambda p: p[0] >= 0, ix(0)), (lambda p: p[0] <= w, ix(w)), (lambda p: p[1] >= 0, iy(0)), (lambda p: p[1] <= h, iy(h))):
        pts = cut(pts, ins, it)
        if not pts: return []
    return pts


def hatching(w, h):
    s = ''
    for x in (-.55, 0, .55):
        p = clip_poly([(x * w, 0), (x * w + .14 * w, 0), (x * w + .14 * w + h * .9, h), (x * w + h * .9, h)], w - 1, h)
        if p: s += poly(p, white)
    return s


# ---------------------------------------------------------------- nature
def _canopy(cx, cy, rx, ry, seed, n=16):
    """A crown built from overlapping brand leaf shapes: a few big dark ones for mass, smaller bright ones for light."""
    r = rng(seed); s = ''; m = min(rx, ry)
    base = [(-.45, .15, 1.0, leaf3), (.42, .2, 1.0, leaf3), (0, -.42, 1.05, leaf), (-.2, .35, .95, leaf), (.25, -.05, .9, leaf)]
    for i, (dx, dy, k, c) in enumerate(base):
        x, y, sz = cx + dx * rx, cy + dy * ry, k * m
        s += rot(leafshape(x - sz / 2, y - sz * .55, sz, sz * 1.1, c, i % 2 == 0), (-1) ** i * 18, x, y)
    hi = [(leaf2, .95), (leaf, 1), (citron, .7), (leaf2, .9), (teal, .45), (leaf3, 1)]
    for i in range(n):
        a = r.uniform(0, 6.283); d = r.uniform(.15, 1) ** .7
        x = cx + math.cos(a) * rx * d * .8; y = cy + math.sin(a) * ry * d * .8
        sz = r.uniform(.3, .52) * m; c, o = hi[i % len(hi)]
        s += rot(leafshape(x - sz / 2, y - sz * .6, sz, sz * 1.2, c, r.random() < .5, o), r.uniform(-40, 40), x, y)
    return s


def tree_big(w, h, fx):
    s = rr(fx - 6, .5 * h, 12, .5 * h, espresso, 3)
    s += line(fx, .66 * h, fx - .2 * w, .5 * h, espresso, 7) + line(fx, .6 * h, fx + .18 * w, .46 * h, espresso, 7)
    return s + _canopy(w / 2, .29 * h, w * .42, h * .25, 7, 20)


def tree_palm(w, h, fx):
    top = .2 * h
    s = path(f'M{f(fx)} {f(h)}Q{f(fx-10)} {f(.6*h)} {f(fx+2)} {f(top)}', 'none', wood, 14)
    for i in range(1, 9): s += line(fx - 7, top + i * (h - top) / 9, fx + 7, top + i * (h - top) / 9 - 4, espresso, 2, o=.35)
    fr = [(-170, .46, leaf3), (-150, .5, leaf), (-118, .42, leaf2), (-62, .42, leaf), (-30, .5, leaf3), (-8, .45, leaf2), (20, .36, leaf), (158, .36, leaf3), (-90, .3, citron)]
    for a, ln, c in fr:
        L = ln * w
        s += rot(path(f'M0 0Q{f(L*.5)} {f(-L*.28)} {f(L)} {f(L*.08)}Q{f(L*.5)} {f(L*.12)} 0 0Z', c), a, 0, 0).replace('<g transform="', f'<g transform="translate({f(fx+2)} {f(top)}) ', 1)
    return s + circ(fx + 2, top, 9, espresso)


def bush(w, h):
    return leafshape(.02 * w, .3 * h, .5 * w, .7 * h, leaf3) + leafshape(.4 * w, .1 * h, .58 * w, .9 * h, leaf, True) + leafshape(.25 * w, .45 * h, .4 * w, .55 * h, citron, o=.8)


def grass_strip(w, h):
    s = rr(0, h * .45, w, h * .55, leaf3)
    for i in range(8): s += leafshape(i * w / 8 + 1, (0 if i % 2 else .2) * h, w / 8 - 2, h * .9, leaf if i % 3 else leaf2, i % 2 == 0)
    return s


def flowers(w, h):
    s = ''
    for x, top, c in ((.18, .1, berry), (.5, .3, papaya), (.82, 0, plum)):
        s += line(x * w, h, x * w, top * h + 8, leaf3, 3) + leafshape(x * w, .55 * h, .16 * w, .22 * h, leaf, True)
        s += leafshape(x * w - .13 * w, top * h, .26 * w, .3 * h, c)
    return s


def planter_box(w, h):
    s = leafshape(.12 * w, .12 * h, .3 * w, .45 * h, leaf3) + leafshape(.36 * w, 0, .3 * w, .55 * h, leaf, True) + leafshape(.6 * w, .15 * h, .28 * w, .4 * h, leaf2)
    s += circ(.3 * w, .14 * h, 7, berry) + circ(.56 * w, .08 * h, 7, papaya) + circ(.76 * w, .2 * h, 6, plum)
    return s + poly([(0, .5 * h), (w, .5 * h), (.86 * w, h), (.14 * w, h)], gray) + rr(0, .5 * h, w, .1 * h, lgrey, 3)


def lot_grass(w, h):
    s = rr(0, h * .55, w, h * .45, leaf3)
    for i in range(6): s += leafshape(i * w / 6 + 1, (.05 if i % 2 else .3) * h, w / 6 - 2, h * .65, leaf if i % 2 else leaf2, i % 2 == 0)
    return s


# ---------------------------------------------------------------- furniture
def wayfinding(w, h):
    s = rr(.1 * w, .78 * h, .8 * w, .22 * h, gray)
    s += rc(0, 0, w, .8 * h, midnight, 10, 10, 0, 0) + rc(0, 0, w, .045 * h, aqua, 10, 10, 0, 0)
    pad = max(4, .1 * w)
    s += rr(pad, .08 * h, (w - 2 * pad) * .7, 4, white, 2) + rr(pad, .12 * h, (w - 2 * pad) * .45, 3, white, 1, .6)
    mx, my, mw, mh = pad, .2 * h, w - 2 * pad, .42 * h
    s += rr(mx, my, mw, mh, tealT, 3)
    if w > 50:
        s += line(mx, my + mh * .35, mx + mw, my + mh * .2, white, 4, 'butt') + line(mx + mw * .4, my, mx + mw * .55, my + mh, white, 4, 'butt')
        s += leafshape(mx + mw * .08, my + mh * .5, mw * .25, mh * .35, leaf) + circ(mx + mw * .72, my + mh * .62, 5, berry)
    s += rr(pad, .67 * h, (w - 2 * pad) * .55, 3, white, 1, .6)
    return s


def bench_front(w, h):
    return rr(0, 0, w, .32 * h, wood, 3) + rr(.08 * w, .3 * h, .08 * w, .7 * h, dgrey) + rr(.84 * w, .3 * h, .08 * w, .7 * h, dgrey)


def bench_side(w, h, side):
    s = rr(.1 * w, .5 * h, .75 * w, .1 * h, wood, 3) + rot(rr(.72 * w, 0, .1 * w, .58 * h, wood, 3), 10, .77 * w, .55 * h)
    s += line(.2 * w, .58 * h, .12 * w, h, dgrey, 5) + line(.7 * w, .58 * h, .8 * w, h, dgrey, 5)
    return s if side == 'right' else mirror(s, w)


def bike_side(w, h, frame=teal):
    r = .36 * h; y = h - r - 3; sw = 5
    s = ''.join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="none" stroke="{charcoal}" stroke-width="{sw}"/>' for x in (r + 3, w - r - 3))
    a, b = r + 3, w - r - 3
    s += path(f'M{f(a)} {f(y)}L{f(a+.2*w)} {f(y-.4*h)}H{f(b-.16*w)}L{f(b)} {f(y)}M{f(a+.2*w)} {f(y-.4*h)}L{f(w*.5)} {f(y)}L{f(b-.16*w)} {f(y-.4*h)}M{f(w*.5)} {f(y)}H{f(a)}', 'none', frame, 5)
    s += line(a + .15 * w, y - .48 * h, a + .28 * w, y - .48 * h, charcoal, 5) + line(b - .2 * w, y - .54 * h, b - .08 * w, y - .54 * h, charcoal, 5) + line(b - .16 * w, y - .4 * h, b - .14 * w, y - .54 * h, charcoal, 4)
    return s


def bike_rack_side(w, h, side, road=False):
    s = path(f'M{f(.38*w)} {f(h)}V{f(.36*h)}Q{f(.5*w)} {f(.14*h)} {f(.62*w)} {f(.36*h)}V{f(h)}', 'none', gray, 7, cap='butt')
    s += bike_side(w, h, cobalt if road else teal)
    return s if side == 'right' else mirror(s, w)


def bike_rack_front(w, h, side):
    s = path(f'M{f(.7*w)} {f(h)}V{f(.35*h)}Q{f(.85*w)} {f(.2*h)} {f(.98*w)} {f(.35*h)}V{f(h)}', 'none', gray, 6)
    s += rr(.36 * w, .3 * h, 7, .7 * h, charcoal, 3) + rr(.34 * w, .2 * h, 11, .5 * h, teal, 3)
    s += line(.05 * w, .14 * h, .72 * w, .14 * h, charcoal, 6) + rr(.3 * w, 0, .22 * w, .09 * h, espresso, 3)
    return s if side == 'left' else mirror(s, w)


def parklet(w, h, side):
    s = rr(0, .9 * h, w, .1 * h, dgrey) + rr(.06 * w, .86 * h, .06 * w, .14 * h, charcoal) + rr(.88 * w, .86 * h, .06 * w, .14 * h, charcoal)
    s += leafshape(.2 * w, .02 * h, .2 * w, .4 * h, leaf3) + leafshape(.36 * w, 0, .2 * w, .42 * h, leaf, True) + leafshape(.52 * w, .06 * h, .2 * w, .36 * h, leaf2)
    s += circ(.16 * w, .22 * h, 8, papaya) + circ(.52 * w, .1 * h, 7, citron) + circ(.76 * w, .2 * h, 8, berry)
    s += rc(.02 * w, .36 * h, .8 * w, .5 * h, teal, 8, 8, 4, 4) + rr(.02 * w, .36 * h, .8 * w, .07 * h, deep, 4)
    for i in range(3): s += leafshape((.07 + i * .26) * w, .5 * h, .2 * w, .28 * h, aqua, i % 2 == 1, .55)
    s += rot(rr(.85 * w, .26 * h, .07 * w, .5 * h, wood, 3), 8, .88 * w, .7 * h) + rr(.8 * w, .7 * h, .2 * w, .07 * h, wood, 3)
    return s if side == 'right' else mirror(s, w)


def lamp_modern(w, h, px, arms):
    """px = pole centre; arms = list of (direction, height fraction, reach in px)."""
    s = poly([(px - 9, h), (px - 4, 0), (px + 4, 0), (px + 9, h)], gray) + rr(px - 13, h - 26, 26, 26, dgrey, 3)
    for d, top, reach in arms:
        y = top * h; x2 = px + d * reach
        s += path(f'M{f(px)} {f(y+70)}Q{f(px)} {f(y+12)} {f(px+d*60)} {f(y+10)}L{f(x2)} {f(y+6)}', 'none', gray, 8)
        hx = x2 - (90 if d > 0 else 0)
        s += leafshape(hx, y - 2, 90, 22, lgrey, d < 0) + rr(hx + 8, y + 16, 74, 7, lamp, 3)
    return s


def lamp_trad(w, h, px, arms):
    s = poly([(px - 6, h), (px - 3, 30), (px + 3, 30), (px + 6, h)], charcoal) + rr(px - 9, h - 30, 18, 30, charcoal, 3)
    def lantern(cx, y):
        return poly([(cx - 12, y + 8), (cx + 12, y + 8), (cx + 8, y + 36), (cx - 8, y + 36)], lamp) + \
            poly([(cx - 15, y + 10), (cx, y - 4), (cx + 15, y + 10)], charcoal) + rr(cx - 9, y + 34, 18, 5, charcoal, 2)
    if not arms: return s + lantern(px, 0)
    for d in arms:
        cx = px + d * (w - 30); s += line(px, 26, cx, 26, charcoal, 5) + lantern(cx, 14)
    return s + circ(px, 20, 6, charcoal)


def banner(w, h, side, colors):
    bw = w * .68; x = w - bw - 4
    s = rr(0, 4, w, 5, dgrey, 2) + rr(0, h - 10, w, 5, dgrey, 2)
    n = len(colors)
    for i, c in enumerate(colors): s += rr(x + i * bw / n, 8, bw / n + .5, h - 18, c)
    return s if side == 'left' else mirror(s, w)


def bollard(w, h):
    return rc(0, 0, w, h, citron, w / 2, w / 2, 2, 2) + rr(0, .16 * h, w, .08 * h, charcoal) + rr(0, .3 * h, w, .05 * h, white, o=.8)


def dome(w, h): return rc(0, 0, w, h, lgrey, w / 2, w / 2, 0, 0)


def shelter(w, h, side, roof=teal, accent=citron):
    """Drawn for the 'left' sprite: glass shelter on the left, stop flag pole on the right."""
    s = rr(.9 * w, .04 * h, 9, .96 * h, lgrey, 3) + leafshape(.82 * w, .02 * h, .13 * w, .14 * h, midnight) + rr(.845 * w, .05 * h, .08 * w, .025 * h, accent, 2)
    s += rr(.04 * w, .3 * h, 9, .7 * h, dgrey) + rr(.56 * w, .22 * h, 9, .78 * h, dgrey)
    s += rr(.09 * w, .34 * h, .44 * w, .44 * h, cobaltT, 4, .9) + poly([(.3 * w, .34 * h), (.42 * w, .34 * h), (.2 * w, .78 * h), (.09 * w, .78 * h)], white, .45)
    s += poly([(0, .3 * h), (.68 * w, .15 * h), (.68 * w, .2 * h), (0, .36 * h)], roof)
    s += rr(.1 * w, .86 * h, .3 * w, .04 * h, roof, 3) + rr(.14 * w, .9 * h, 6, .1 * h, dgrey) + rr(.34 * w, .9 * h, 6, .1 * h, dgrey)
    return s if side == 'left' else mirror(s, w)


# ---------------------------------------------------------------- buildings
def window(x, y, w, h, frame=white, flip=False):
    return rr(x - 5, y - 5, w + 10, h + 10, frame, 3) + leafshape(x, y, w, h, midnight, flip, big=.22, small=.04) + \
        poly([(x + w * .5, y + 3), (x + w * .7, y + 3), (x + w * .35, y + h - 3), (x + w * .15, y + h - 3)], white, .12)


def building_upper(w, h, wall, trim, n, frame=white):
    s = rr(0, 0, w, h, wall) + rr(0, h - 12, w, 12, trim)
    ww = w * .62 / n; gap = (w - ww * n) / (n + 1)
    for i in range(n): s += window(gap + i * (ww + gap), .2 * h, ww, .5 * h, frame, i % 2 == 1)
    return s


def building_roof(w, h, trim): return rr(0, h * .35, w, h * .65, trim) + rr(-0, 0, w, h * .4, lgrey, 3)


def building_ground(w, h, wall_w, wall, trim, awning, side, frame=white):
    """Drawn with the wall flush left and the awning overhanging to the right (street side of a left-hand building)."""
    s = rr(0, 0, wall_w, h - 14, wall) + rr(0, h - 14, wall_w, 14, charcoal)
    s += rr(.06 * wall_w, .5 * h, .16 * wall_w, .24 * h, frame, 3) + leafshape(.075 * wall_w, .52 * h, .13 * wall_w, .2 * h, midnight, big=.2, small=.04)
    dx = .34 * wall_w
    s += rr(dx, .44 * h, .58 * wall_w, h * .56 - 14, frame, 3)
    s += rr(dx + 8, .46 * h, .27 * wall_w - 8, h * .54 - 26, midnight, 3) + rr(dx + .29 * wall_w + 4, .46 * h, .27 * wall_w - 8, h * .54 - 26, midnight, 3)
    s += _glint(dx + 20, .46 * h, .14 * wall_w, h * .54 - 26)
    s += poly([(.3 * wall_w, .26 * h), (wall_w + 2, .26 * h), (w, .44 * h), (.27 * wall_w, .44 * h)], awning)
    s += poly([(wall_w, .26 * h), (wall_w + 2, .26 * h), (w, .44 * h), (wall_w, .44 * h)], espresso, .25)
    for i in range(1, 5): s += rr(.3 * wall_w + i * .14 * wall_w, .26 * h, .07 * wall_w, .18 * h, white, o=.22)
    s += leafshape(.06 * wall_w, .1 * h, .14 * wall_w, .1 * h, trim, o=.6)
    return s if side == 'left' else mirror(s, w)


def home(w, h, wall, trim, roofc, side, frame=white):
    """Ground sprite of the house, drawn for the left-hand lot: body flush left, porch and stairs to the right."""
    bw = 327.0; base = h - 12
    s = rr(0, 0, bw, base, wall) + rr(0, 232, bw, 12, trim) + rr(0, 468, bw, 10, trim)
    s += window(.14 * bw, 60, .2 * bw, 110, frame) + window(.6 * bw, 60, .26 * bw, 110, frame, True)
    for x in (.09, .37, .55, .89): s += rr(x * bw - 6, 55, 14, 120, trim, 2)
    s += window(.14 * bw, 300, .26 * bw, 110, frame) + window(.62 * bw, 300, .2 * bw, 110, frame, True)
    s += rr(.12 * bw, 500, .16 * bw, 34, midnight, 3) + rr(.68 * bw, 500, .16 * bw, 34, midnight, 3)
    px = bw + 205
    s += rr(px - 14, 296, 12, 140, trim) + poly([(bw - 4, 244), (bw + 150, 244), (px + 40, 296), (bw - 4, 296)], roofc) + rr(bw, 296, px - bw + 20, 8, espresso, o=.4)
    s += rr(bw, 430, px - bw, base - 430, lgrey) + rr(bw, 424, px - bw + 6, 10, trim)
    for i in range(6): s += rr(bw + 16 + i * 30, 380, 5, 46, dgrey)
    s += rr(bw, 374, px - bw, 7, dgrey)
    n = 6; sw_ = (w - px - 30) / n
    for i in range(n): s += rr(px + i * sw_, 430 + i * (base - 430) / n, sw_ + 1, base - 430 - i * (base - 430) / n, concrete if i % 2 else lgrey)
    s += line(px + 4, 380, w - 34, base - 60, dgrey, 6) + rr(w - 38, base - 70, 22, 70, lgrey, 3)
    for i in range(1, 6): s += rr(px + i * sw_ - 2, 384 + i * (base - 444) / n, 5, 48, dgrey)
    s += leafshape(bw + 12, base - 46, 40, 46, leaf3) + leafshape(bw + 44, base - 60, 44, 60, leaf, True) + circ(bw + 100, base - 30, 8, berry) + circ(bw + 126, base - 22, 7, papaya) + line(bw + 100, base - 22, bw + 100, base, leaf3, 3) + line(bw + 126, base - 15, bw + 126, base, leaf3, 3)
    s += rr(0, base, w, 12, charcoal)
    return s if side == 'left' else mirror(s, w)


def home_roof(w, h, roofc, side):
    s = rr(.42 * w, 0, .11 * w, .35 * h, lgrey, 3) + rr(.4 * w, 0, .15 * w, .08 * h, gray, 2)
    s += poly([(0, h), (0, .92 * h), (.12 * w, .27 * h), (.86 * w, .27 * h), (w, .9 * h), (w, h)], roofc)
    s += poly([(.12 * w, .27 * h), (.86 * w, .27 * h), (.9 * w, .45 * h), (.085 * w, .45 * h)], white, .1) + rr(0, .92 * h, w, .08 * h, espresso, o=.5)
    return s if side == 'left' else mirror(s, w)


# ---------------------------------------------------------------- lots
def fence(w, h):
    s = rr(0, h - 20, w, 20, espresso)
    for i in range(-6, 8):
        for d in (1, -1):
            p = clip_poly([(i * 16, 0), (i * 16 + 2.5, 0), (i * 16 + 2.5 + d * (h - 34), h - 34), (i * 16 + d * (h - 34), h - 34)], w - 1, h - 34)
            if len(p) > 2: s += poly(p, gray, .8)
    s += rr(0, 0, w, 7, dgrey) + rr(0, 0, 7, h - 20, dgrey) + rr(w - 7, 0, 7, h - 20, dgrey) + rr(0, h - 38, w, 6, dgrey)
    for i, c in enumerate((leaf3, leaf, leaf2, leaf)): s += leafshape(12 + i * 20, h - 46 - (i % 2) * 8, 14, 30 + (i % 2) * 8, c, i % 2 == 0)
    return s


def water(w, h, seed=3):
    s = rr(0, 6, w, h - 6, cobalt)
    r = rng(seed)
    for i in range(7):
        x = min(max((i + .5) * w / 7 - 22 + r.uniform(-6, 6), 2), w - 46); y = 14 + (i * 37 % (h - 34))
        s += leafshape(x, y, 44, 12, aqua if i % 2 else cobaltT, i % 2 == 0, .75 if i % 2 else .4)
    top = ''.join(leafshape(i * w / 6, 0, w / 6, 14, cobalt, i % 2 == 0) for i in range(6))
    return top + s


def waterfront_edge(w, h, side):
    """Quay for the left-hand waterfront: water on the left, pier at the street (right) edge."""
    wh = 105.0
    s = g(water(w - 40, wh, 5), f'translate(0 {f(h - wh)})')
    for x, y, sz, c in ((.38, .66, 70, dgrey), (.5, .56, 82, gray), (.62, .7, 64, dgrey), (.44, .8, 60, gray), (.66, .5, 60, concrete), (.56, .78, 70, concrete)):
        s += rot(leafshape(x * w - sz / 2, y * h - sz * .35, sz, sz * .7, c, x > .5), -8, x * w, y * h)
    s += poly([(w - 44, h), (w - 36, 8), (w, 8), (w, h)], concrete) + rr(w - 42, 0, 42, 10, lgrey, 3) + rr(w - 12, 10, 12, h - 10, gray, o=.35)
    return s if side == 'left' else mirror(s, w)


def parking_lot(w, h, side, edge):
    """Left-hand lot. Edge piece carries the P sign at the street side; the repeat piece is the lower strip only."""
    s = rr(0, h - 9, w, 9, dgrey); sign = ''
    if edge:
        px = w - 42
        s += poly([(px - 7, h - 9), (px - 3, 90), (px + 3, 90), (px + 7, h - 9)], dgrey)
        s += g(car_side(240, 100, 'left'), f'translate({f(w - 300)} {f(h - 9 - 100)})')
        s += g(car(118, 92), f'translate(8 {f(h - 9 - 92)})').replace(f'fill="{teal}"', f'fill="{aqua}"')
        sx = px if side == 'left' else w - px            # the P itself must never be mirrored
        sign = leafshape(sx - 40, 0, 80, 88, cobalt, big=.3, small=.08) + \
            path(f'M{f(sx-14)} 70V20H{f(sx+6)}Q{f(sx+22)} 20 {f(sx+22)} 36Q{f(sx+22)} 52 {f(sx+6)} 52H{f(sx-14)}', 'none', white, 11, cap='butt')
    else:
        s += g(car(118, 92, rear=True), f'translate(40 {f(h - 9 - 92)})') + rc(250, h - 22, 110, 13, lgrey, 4, 4, 0, 0)
    return (s if side == 'left' else mirror(s, w)) + sign


# ---------------------------------------------------------------- sky
def clouds(w, h, seed, n, o):
    """A band of soft overlapping leaf and square shapes (the brand-book cover pattern). Wraps horizontally so it tiles."""
    r = rng(seed); s = ''
    for i in range(n):
        cw = r.uniform(110, 220); ch = cw * r.uniform(.28, .4); x = r.uniform(0, w); y = r.uniform(.05, .8) * (h - ch)
        one = leafshape(0, 0, cw, ch, white, r.random() < .5, o) + leafshape(cw * .2, -ch * .45, cw * .5, ch * .9, white, r.random() < .5, o * .8) + \
            rr(cw * .55, -ch * .2, cw * .3, ch * .7, white, 8, o * .7)
        for dx in (0, -w, w):
            if -cw < x + dx < w: s += g(one, f'translate({f(x + dx)} {f(y + ch * .5)})')
    return s


# ---------------------------------------------------------------- people (31 figures, each in a 120 x 192 box, feet on the bottom edge)
TOPS = [aqua, teal, leaf, cobalt, plum, berry, papaya, citron, midnight, white, gray, deep]
BOTS = [midnight, charcoal, dgrey, espresso, deep, gray, plum]
HAIR = [espresso, charcoal, '#7A4A2A', gray, lgrey, '#C9963F']


def figure(cx, base, ht, skin_c, hair_c, top, bot, dress=False, r=None, flip=False):
    hd = ht * .075; s = ''
    lw = ht * .05; hip = base - ht * .47
    if dress:
        s += poly([(cx - ht * .09, hip - ht * .1), (cx + ht * .09, hip - ht * .1), (cx + ht * .14, hip + ht * .22), (cx - ht * .14, hip + ht * .22)], top)
        s += rr(cx - lw - 1, hip + ht * .22, lw, ht * .25, skin_c, 2) + rr(cx + 1, hip + ht * .22, lw, ht * .25, skin_c, 2)
    else:
        s += rc(cx - lw - 2, hip, lw + 1, ht * .47 - 4, bot, 2, 2, 2, 2) + rc(cx + 1, hip, lw + 1, ht * .47 - 4, bot, 2, 2, 2, 2)
    s += rr(cx - lw - 4, base - 5, lw + 4, 5, charcoal, 2) + rr(cx + 1, base - 5, lw + 4, 5, charcoal, 2)
    tw = ht * .2; ty = base - ht * .82
    s += rr(cx - tw / 2 - 5, ty + 4, 6, ht * .3, top if not dress else skin_c, 3) + rr(cx + tw / 2 - 1, ty + 4, 6, ht * .3, top if not dress else skin_c, 3)
    s += leafshape(cx - tw / 2, ty, tw, ht * .38, top, flip, big=.42, small=.12)
    s += rr(cx - 3, ty - 6, 6, 8, skin_c) + circ(cx, ty - hd - 3, hd, skin_c)
    s += rc(cx - hd - 1, ty - 2 * hd - 5, 2 * hd + 2, hd * 1.1, hair_c, hd, hd, 2, 2)
    return s


def dog(x, base, c, sz=1.0):
    s = rr(x, base - 30 * sz, 34 * sz, 15 * sz, c, 6) + rr(x + 3 * sz, base - 18 * sz, 5 * sz, 18 * sz, c, 2) + rr(x + 25 * sz, base - 18 * sz, 5 * sz, 18 * sz, c, 2)
    return s + leafshape(x + 26 * sz, base - 44 * sz, 18 * sz, 18 * sz, c) + line(x + 2 * sz, base - 26 * sz, x - 6 * sz, base - 38 * sz, c, 4 * sz)


def wheelchair(cx, base):
    return f'<circle cx="{f(cx)}" cy="{f(base-24)}" r="22" fill="none" stroke="{charcoal}" stroke-width="5"/>' + circ(cx + 26, base - 7, 7, charcoal) + \
        rr(cx - 18, base - 62, 6, 44, dgrey, 2) + rr(cx - 18, base - 40, 44, 6, dgrey, 2)


def person(i):
    """Figure i (1-31). Widths and kinds follow PERSON_WIDTH in segments/people.js so the crowd spacing still works."""
    r = rng(100 + i); base = 190; cx = 60
    sk = skin[r.randrange(5)]; hr = HAIR[r.randrange(6)]; tp = TOPS[(i * 5) % 12]; bt = BOTS[(i * 3) % 7]
    ht = r.uniform(128, 150); dress = i in (1, 3, 5, 8, 10, 13, 17, 18)
    if i in (21, 22):                       # children
        return figure(cx, base, r.uniform(78, 92), sk, hr, tp, bt, i == 21, flip=True)
    if i in (19, 20):                       # wheelchair users
        s = wheelchair(cx, base)
        seat = base - 34
        s += rr(cx - 8, seat - 2, 36, 10, bt, 4) + rr(cx + 20, seat, 9, 30, bt, 3) + rr(cx + 18, base - 8, 16, 6, charcoal, 2)
        s += leafshape(cx - 14, seat - 50, 26, 52, tp) + rr(cx + 2, seat - 36, 22, 7, tp, 3) + circ(cx - 1, seat - 62, 10, sk) + rc(cx - 12, seat - 74, 22, 12, hr, 10, 10, 2, 2)
        return s
    if i == 16:                              # cane
        return figure(cx, base, 132, sk, lgrey, tp, bt) + line(cx + 26, base - 62, cx + 30, base, wood, 4)
    if i in (17, 18):                        # walker / rollator
        s = figure(cx - 6, base, 128, sk, lgrey if i == 17 else gray, tp, bt, True)
        return s + path(f'M{f(cx+8)} {f(base)}V{f(base-58)}H{f(cx+30)}V{f(base)}', 'none', gray, 4) + rr(cx + 6, base - 34, 26, 4, gray)
    if i == 23: return figure(cx - 12, base, ht, sk, hr, tp, bt, True) + dog(cx + 14, base, charcoal, .8) + line(cx - 2, base - 66, cx + 36, base - 30, dgrey, 2)
    if i == 24: return figure(cx + 14, base, ht, sk, hr, tp, bt) + mirror(dog(60 + 8, base, wood, 1.15), 120) + line(cx + 4, base - 66, cx - 30, base - 42, dgrey, 2)
    if i == 25:                              # kid on a scooter
        return figure(cx, base - 8, 88, sk, hr, tp, bt, flip=True) + rr(cx - 22, base - 8, 44, 4, gray, 2) + circ(cx - 20, base - 4, 4, charcoal) + circ(cx + 20, base - 4, 4, charcoal) + rr(cx + 16, base - 56, 4, 50, gray)
    if i in (26, 28): return figure(cx - 14, base, ht, sk, hr, tp, bt, i == 26) + figure(cx + 22, base, 86, sk, hr, TOPS[(i + 4) % 12], bt, True, flip=True)
    if i == 27: return figure(cx, base, ht, sk, hr, tp, bt, True) + line(cx + 16, base - 64, cx + 34, base, white, 3) + rr(cx + 30, base - 12, 6, 12, berry, 2)
    if i == 29: return figure(cx - 20, base, 140, sk, hr, tp, bt, True) + figure(cx + 22, base, 148, skin[(i + 2) % 5], gray, TOPS[(i + 7) % 12], BOTS[(i + 2) % 7])
    if i == 30: return figure(cx, base, ht, sk, hr, tp, bt) + leafshape(cx + 4, base - 108, 22, 30, citron) + circ(cx + 16, base - 114, 7, skin[(i + 1) % 5])
    return figure(cx, base, ht, sk, hr, tp, bt, dress, flip=i % 2 == 0)
