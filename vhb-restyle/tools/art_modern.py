"""Modern redraw: bolder, simpler silhouettes than the first pass (one-box vehicles, lollipop trees, globe lamps,
flat canopies, pictogram people). Written once against the style API in styles.py."""
import re
from svgkit import *
import art_vehicles as V, art_street as S

SK = skin


def mir(s, w, on): return mirror(s, w) if on else s


# ------------------------------------------------------------------ vehicles
def car(st, w, h, rear=False, signal=None, cw=145, bodyc=white, belt=teal, door=None, topper=None):
    W = min(cw, w); side = signal or door; ox = (w - W) if side == 'left' else 0; s = ''; t = .1 * h if topper else 0; H = h - t
    if signal: s += circ(ox + (.12 * W if signal == 'left' else .88 * W), t + .55 * H, .16 * W, papaya, .3)
    if door:                                   # an open door swung out to one side
        dw = w - W + .06 * W; dx = 0 if door == 'left' else w - dw
        s += st.r(dx, t + .34 * H, dw, .44 * H, bodyc, 8) + st.glass(dx + dw * .14, t + .38 * H, dw * .62, .16 * H, 5)
    c = st.r(.08 * W, .78 * H, .18 * W, .22 * H, charcoal, 7, ol=False) + st.r(.74 * W, .78 * H, .18 * W, .22 * H, charcoal, 7, ol=False)
    c += st.r(.17 * W, .02 * H, .66 * W, .6 * H, bodyc, 30) + st.r(.02 * W, .4 * H, .96 * W, .48 * H, belt, 24) + st.r(.02 * W, .4 * H, .96 * W, .26 * H, bodyc, 20, ol=False)
    c += st.glass(.24 * W, .09 * H, .52 * W, .28 * H, 16)
    c += st.r(.09 * W, .5 * H, .82 * W, .075 * H, berry if rear else lamp, 5, ol=False)
    if rear: c += st.r(.4 * W, .7 * H, .2 * W, .1 * H, white, 3, ol=False)
    if signal: c += rr((.09 if signal == 'left' else .73) * W, .5 * H, .18 * W, .075 * H, papaya, 5)
    if topper: c += st.r(.4 * W, -t, .2 * W, t + .04 * H, topper, 5)
    return s + g(c, f'translate({f(ox)} {f(t)})')


def car_side(st, w, h, facing='left'):
    s = st.p(f'M{f(.02*w)} {f(.82*h)}V{f(.52*h)}Q{f(.03*w)} {f(.38*h)} {f(.2*w)} {f(.34*h)}Q{f(.34*w)} {f(.03*h)} {f(.55*w)} {f(.03*h)}H{f(.72*w)}Q{f(.9*w)} {f(.05*h)} {f(.97*w)} {f(.42*h)}V{f(.82*h)}Z', white)
    s += st.r(.04 * w, .62 * h, .92 * w, .12 * h, teal, 5, ol=False)
    s += st.glassp(f'M{f(.27*w)} {f(.36*h)}Q{f(.38*w)} {f(.1*h)} {f(.55*w)} {f(.1*h)}H{f(.7*w)}Q{f(.83*w)} {f(.12*h)} {f(.88*w)} {f(.36*h)}Z')
    s += st.ln(.57 * w, .1 * h, .57 * w, .36 * h, white, 5)
    for x in (.22, .78): s += st.c(x * w, .8 * h, .19 * h, charcoal) + st.c(x * w, .8 * h, .07 * h, white, ol=False)
    s += st.r(.02 * w, .46 * h, .06 * w, .08 * h, lamp, 3, ol=False) + st.r(.93 * w, .46 * h, .04 * w, .08 * h, berry, 2, ol=False)
    return mir(s, w, facing != 'left')


def bus(st, w, h, rear=False):
    s = st.r(.12 * w, .9 * h, .16 * w, .1 * h, charcoal, 5, ol=False) + st.r(.72 * w, .9 * h, .16 * w, .1 * h, charcoal, 5, ol=False)
    s += st.r(0, .2 * h, .06 * w, .13 * h, midnight, 4, ol=False) + st.r(.94 * w, .2 * h, .06 * w, .13 * h, midnight, 4, ol=False)
    s += st.r(.06 * w, .5 * h, .88 * w, .42 * h, teal, 18) + st.r(.06 * w, 0, .88 * w, .7 * h, white, 30)
    s += st.p(f'M{f(.06*w)} {f(.78*h)}C{f(.35*w)} {f(.7*h)} {f(.6*w)} {f(.86*h)} {f(.94*w)} {f(.74*h)}V{f(.8*h)}C{f(.6*w)} {f(.92*h)} {f(.35*w)} {f(.76*h)} {f(.06*w)} {f(.84*h)}Z', citron, ol=False)
    if rear:
        s += st.glass(.2 * w, .12 * h, .6 * w, .22 * h, 14) + st.r(.28 * w, .42 * h, .44 * w, .16 * h, gray, 8, ol=False)
    else:
        s += st.r(.2 * w, .035 * h, .6 * w, .07 * h, midnight, 8, ol=False) + st.r(.24 * w, .052 * h, .3 * w, .036 * h, citron, 4, ol=False)
        s += st.glass(.12 * w, .14 * h, .76 * w, .42 * h, 18) + st.ln(.5 * w, .15 * h, .5 * w, .55 * h, white, 5)
    lc = berry if rear else lamp
    s += st.r(.11 * w, .6 * h, .16 * w, .05 * h, lc, 5, ol=False) + st.r(.73 * w, .6 * h, .16 * w, .05 * h, lc, 5, ol=False)
    return s + st.tone(.62 * w, .08 * h, .3 * w, .5 * h) + st.r(.06 * w, .87 * h, .88 * w, .055 * h, midnight, 6, ol=False)


def _panto(st, w, top, bottom):
    return st.ln(.22 * w, top + 4, .78 * w, top + 4, charcoal, 6) + st.ln(.32 * w, top + 4, .45 * w, bottom, charcoal, 6) + st.ln(.68 * w, top + 4, .55 * w, bottom, charcoal, 6)


def light_rail(st, w, h, rear=False):
    t = .2 * h
    s = _panto(st, w, 0, t + 6) + st.r(.14 * w, .95 * h, .12 * w, .05 * h, charcoal, 3, ol=False) + st.r(.74 * w, .95 * h, .12 * w, .05 * h, charcoal, 3, ol=False)
    s += st.r(.03 * w, .62 * h, .94 * w, .33 * h, teal, 16) + st.r(.03 * w, t, .94 * w, .6 * h, white, 40)
    s += st.r(.2 * w, t + .03 * h, .6 * w, .045 * h, midnight, 8, ol=False) + st.r(.25 * w, t + .04 * h, .16 * w, .024 * h, berry if rear else citron, 3, ol=False)
    s += st.glass(.11 * w, t + .1 * h, .78 * w, .38 * h, 28)
    lc = berry if rear else lamp
    s += st.r(.1 * w, .73 * h, .2 * w, .03 * h, lc, 5, ol=False) + st.r(.7 * w, .73 * h, .2 * w, .03 * h, lc, 5, ol=False)
    s += st.p(f'M{f(.03*w)} {f(.84*h)}C{f(.35*w)} {f(.8*h)} {f(.6*w)} {f(.89*h)} {f(.97*w)} {f(.82*h)}V{f(.86*h)}C{f(.6*w)} {f(.93*h)} {f(.35*w)} {f(.84*h)} {f(.03*w)} {f(.88*h)}Z', citron, ol=False)
    return s + st.tone(.6 * w, t + .05 * h, .32 * w, .5 * h)


def streetcar(st, w, h, rear=False):
    t = .19 * h
    s = _panto(st, w, 0, t + 6) + st.r(.15 * w, .94 * h, .1 * w, .06 * h, charcoal, 3, ol=False) + st.r(.75 * w, .94 * h, .1 * w, .06 * h, charcoal, 3, ol=False)
    s += st.r(.06 * w, t, .88 * w, .74 * h, white if rear else teal, 30) + st.r(.06 * w, t, .88 * w, .16 * h, teal if rear else white, 30, ol=False)
    s += st.glass(.12 * w, t + .1 * h, .36 * w, .2 * h, 12) + st.glass(.52 * w, t + .1 * h, .36 * w, .2 * h, 12)
    s += st.r(.06 * w, t + .34 * h, .88 * w, .03 * h, citron, 0, ol=False) + st.c(.5 * w, .68 * h, .05 * w, charcoal if rear else lamp)
    lc = berry if rear else papaya
    s += st.r(.18 * w, .65 * h, .12 * w, .035 * h, lc, 4, ol=False) + st.r(.7 * w, .65 * h, .12 * w, .035 * h, lc, 4, ol=False)
    return s + st.r(.06 * w, .88 * h, .88 * w, .055 * h, midnight, 6, ol=False)


def truck(st, w, h, rear=False):
    if rear:
        s = st.r(.1 * w, .9 * h, .17 * w, .1 * h, charcoal, 5, ol=False) + st.r(.73 * w, .9 * h, .17 * w, .1 * h, charcoal, 5, ol=False)
        s += st.r(0, 0, w, .86 * h, white, 14) + st.ln(.5 * w, .04 * h, .5 * w, .82 * h, gray, 4)
        s += leafshape(.58 * w, .16 * h, .26 * w, .24 * h, st.col(teal)) + leafshape(.66 * w, .28 * h, .22 * w, .2 * h, st.col(citron), True, .85)
        s += st.tone(.6 * w, .45 * h, .36 * w, .36 * h) + st.r(0, .85 * h, w, .06 * h, midnight, 5, ol=False)
        return s + st.r(.05 * w, .87 * h, .1 * w, .03 * h, berry, 3, ol=False) + st.r(.85 * w, .87 * h, .1 * w, .03 * h, berry, 3, ol=False)
    s = st.r(.12 * w, .9 * h, .16 * w, .1 * h, charcoal, 5, ol=False) + st.r(.72 * w, .9 * h, .16 * w, .1 * h, charcoal, 5, ol=False)
    s += st.r(0, .34 * h, .07 * w, .12 * h, midnight, 4, ol=False) + st.r(.93 * w, .34 * h, .07 * w, .12 * h, midnight, 4, ol=False)
    s += st.r(.05 * w, 0, .9 * w, .5 * h, tealT, 12) + leafshape(.62 * w, .05 * h, .2 * w, .15 * h, st.col(teal)) + leafshape(.7 * w, .12 * h, .15 * w, .12 * h, st.col(citron), True, .85)
    s += st.r(.1 * w, .26 * h, .8 * w, .66 * h, white, 24) + st.glass(.17 * w, .32 * h, .66 * w, .22 * h, 12)
    s += st.r(.1 * w, .72 * h, .8 * w, .2 * h, teal, 14, ol=False) + st.r(.16 * w, .62 * h, .18 * w, .06 * h, lamp, 5, ol=False) + st.r(.66 * w, .62 * h, .18 * w, .06 * h, lamp, 5, ol=False)
    return s + st.r(.08 * w, .86 * h, .84 * w, .055 * h, midnight, 6, ol=False)


def train(st, w, h):
    s = st.r(.12 * w, .94 * h, .14 * w, .06 * h, charcoal, 3, ol=False) + st.r(.74 * w, .94 * h, .14 * w, .06 * h, charcoal, 3, ol=False)
    s += st.r(.06 * w, .04 * h, .88 * w, .9 * h, midnight, 46) + st.glass(.14 * w, .14 * h, .72 * w, .22 * h, 18)
    for i in range(3):
        y = (.46 + i * .12) * h
        s += st.pg([(.18 * w, y + .09 * h), (.5 * w, y), (.82 * w, y + .09 * h), (.82 * w, y + .14 * h), (.5 * w, y + .05 * h), (.18 * w, y + .14 * h)], citron if i != 1 else white, ol=False)
    return s + st.c(.4 * w, .08 * h, .035 * w, lamp, ol=False) + st.c(.6 * w, .08 * h, .035 * w, lamp, ol=False) + st.r(.04 * w, .88 * h, .92 * w, .06 * h, gray, 6, ol=False)


def cyclist(st, w, h, rear=False, top=aqua, hat=citron, sk=SK[2], pants=midnight):
    c = w / 2
    s = st.r(c - 4, .58 * h, 8, .42 * h, charcoal, 4, ol=False)
    s += st.r(c - .3 * w, .6 * h, .2 * w, .26 * h, pants, 5, ol=False) + st.r(c + .1 * w, .6 * h, .2 * w, .26 * h, pants, 5, ol=False)
    s += st.r(c - .32 * w, .24 * h, .64 * w, .4 * h, top, .28 * w) + st.ln(.03 * w, .44 * h, .97 * w, .44 * h, charcoal, 6)
    s += st.c(c, .14 * h, .2 * w, sk) + st.p(f'M{f(c-.25*w)} {f(.13*h)}Q{f(c)} {f(-.04*h)} {f(c+.25*w)} {f(.13*h)}Z', hat)
    return s + (st.c(c, .66 * h, 4, berry, ol=False) if rear else st.c(c, .5 * h, 4, lamp, ol=False))


# ------------------------------------------------------------------ nature
def tree_big(st, w, h, fx):
    s = st.r(fx - 7, .46 * h, 14, .54 * h, espresso, 5, ol=False) + st.ln(fx, .62 * h, fx - .2 * w, .48 * h, espresso, 8) + st.ln(fx, .56 * h, fx + .2 * w, .44 * h, espresso, 8)
    s += st.c(.5 * w, .2 * h, .34 * w, leaf3) + st.c(.3 * w, .33 * h, .27 * w, leaf, .92) + st.c(.7 * w, .33 * h, .26 * w, citron, .8)
    for x, y, a in ((.36, .18, -20), (.6, .14, 25), (.5, .32, 0), (.26, .36, -30), (.72, .36, 30)):
        s += rot(leafshape(x * w - 9, y * h - 14, 18, 28, st.col(white), a < 0, .55), a, x * w, y * h)
    return s + st.tone(.5 * w, .1 * h, .4 * w, .34 * h)


def tree_palm(st, w, h, fx):
    top = .22 * h
    s = path(f'M{f(fx)} {f(h)}Q{f(fx-12)} {f(.6*h)} {f(fx+2)} {f(top)}', 'none', st.col(wood), 14)
    for a, ln, c in ((-168, .46, leaf3), (-140, .5, leaf), (-105, .4, citron), (-70, .42, leaf), (-38, .5, leaf3), (-10, .44, leaf)):
        L = ln * w
        s += g(st.p(f'M0 0Q{f(L*.5)} {f(-L*.34)} {f(L)} {f(L*.06)}Q{f(L*.5)} {f(L*.1)} 0 0Z', c), f'translate({f(fx+2)} {f(top)}) rotate({a})')
    return s + st.c(fx + 2, top, 10, espresso, ol=False)


def bush(st, w, h):
    r1, r2, r3 = min(.3 * w, .36 * h), min(.34 * w, .46 * h), min(.2 * w, .22 * h)
    return st.c(.32 * w, h - r1, r1, leaf3, ol=False) + st.c(.64 * w, h - r2, r2, leaf, ol=False) + st.c(.5 * w, h - r3, r3, citron, .8, ol=False)


def tufts(st, w, h, n):
    s = st.r(0, h * .55, w, h * .45, leaf3, 0, ol=False)
    for i in range(n): s += st.r(i * w / n + 1, (0 if i % 2 else .22) * h, w / n - 2, h * .7, leaf if i % 2 else citron, (w / n - 2) / 2, ol=False)
    return s


def flowers(st, w, h, cols=(berry, papaya, citron)):
    s = ''
    for (x, top), c in zip(((.2, .12), (.5, .3), (.8, .02)), cols):
        s += st.ln(x * w, h, x * w, top * h + 8, leaf3, 3) + st.c(x * w, top * h + .14 * h, .13 * w, c, ol=False)
    return s


def planter_box(st, w, h):
    s = st.c(.28 * w, .3 * h, .2 * w, leaf3, ol=False) + st.c(.52 * w, .2 * h, .22 * w, leaf, ol=False) + st.c(.74 * w, .32 * h, .18 * w, citron, .85, ol=False)
    return s + st.c(.4 * w, .12 * h, 6, berry, ol=False) + st.c(.66 * w, .16 * h, 6, papaya, ol=False) + st.r(.04 * w, .46 * h, .92 * w, .54 * h, teal, 12)


# ------------------------------------------------------------------ furniture
def wayfinding(st, w, h):
    pad = max(4, .12 * w)
    s = st.r(.3 * w, .7 * h, .4 * w, .3 * h, gray, 0, ol=False) + st.r(0, 0, w, .78 * h, midnight, min(14, w * .3)) + st.r(pad, .06 * h, (w - 2 * pad) * .6, 5, citron, 2, ol=False)
    s += st.r(pad, .16 * h, w - 2 * pad, .36 * h, white, 5, ol=False)
    if w > 50: s += leafshape(pad + 6, .3 * h, (w - 2 * pad) * .3, .16 * h, st.col(leaf)) + circ(w - pad - 12, .26 * h, 5, st.col(berry)) + line(pad, .4 * h, w - pad, .24 * h, st.col(aqua), 4, 'butt')
    return s + st.r(pad, .58 * h, (w - 2 * pad) * .7, 4, white, 2, .7, ol=False) + st.r(pad, .64 * h, (w - 2 * pad) * .45, 4, white, 2, .7, ol=False)


def bench_front(st, w, h): return st.r(0, 0, w, .36 * h, wood, 5) + st.r(.1 * w, .34 * h, .08 * w, .66 * h, midnight, 0, ol=False) + st.r(.82 * w, .34 * h, .08 * w, .66 * h, midnight, 0, ol=False)


def bench_side(st, w, h, side):
    s = st.r(.08 * w, .5 * h, .72 * w, .12 * h, wood, 4) + st.r(.72 * w, .02 * h, .11 * w, .58 * h, wood, 4)
    return mir(s + st.ln(.2 * w, .62 * h, .14 * w, h, midnight, 6) + st.ln(.68 * w, .62 * h, .76 * w, h, midnight, 6), w, side != 'right')


def bike_side(st, w, h, frame):
    r = .36 * h; y = h - r - 3; a, b = r + 3, w - r - 3
    s = st.ring(a, y, r, charcoal, 5) + st.ring(b, y, r, charcoal, 5)
    s += path(f'M{f(a)} {f(y)}L{f(a+.2*w)} {f(y-.4*h)}H{f(b-.16*w)}L{f(b)} {f(y)}M{f(a+.2*w)} {f(y-.4*h)}L{f(w*.5)} {f(y)}L{f(b-.16*w)} {f(y-.4*h)}', 'none', st.col(frame) if st.name == 'print' else frame, 5)
    return s + st.ln(a + .14 * w, y - .48 * h, a + .28 * w, y - .48 * h, charcoal, 6) + st.ln(b - .2 * w, y - .54 * h, b - .06 * w, y - .54 * h, charcoal, 6)


def bike_rack_side(st, w, h, side, road):
    s = st.stroke(f'M{f(.38*w)} {f(h)}V{f(.4*h)}Q{f(.5*w)} {f(.16*h)} {f(.62*w)} {f(.4*h)}V{f(h)}', gray, 7)
    return mir(s + bike_side(st, w, h, papaya if road else teal), w, side != 'right')


def bike_rack_front(st, w, h, side):
    s = st.stroke(f'M{f(.7*w)} {f(h)}V{f(.4*h)}Q{f(.84*w)} {f(.24*h)} {f(.96*w)} {f(.4*h)}V{f(h)}', gray, 6)
    s += st.r(.36 * w, .3 * h, 8, .7 * h, charcoal, 4, ol=False) + st.r(.33 * w, .22 * h, 14, .46 * h, teal, 6) + st.ln(.06 * w, .16 * h, .72 * w, .16 * h, charcoal, 6)
    return mir(s, w, side != 'left')


def parklet(st, w, h, side):
    s = st.r(0, .9 * h, w, .1 * h, midnight, 0, ol=False)
    s += st.c(.24 * w, .26 * h, .14 * w, leaf3, ol=False) + st.c(.44 * w, .18 * h, .16 * w, leaf, ol=False) + st.c(.62 * w, .26 * h, .13 * w, citron, .85, ol=False)
    s += st.c(.34 * w, .12 * h, 7, papaya, ol=False) + st.c(.56 * w, .1 * h, 7, berry, ol=False)
    s += st.r(.03 * w, .36 * h, .78 * w, .54 * h, teal, 16) + st.r(.1 * w, .5 * h, .64 * w, .08 * h, citron, 6, ol=False)
    return mir(s + st.r(.84 * w, .3 * h, .08 * w, .46 * h, wood, 4) + st.r(.8 * w, .7 * h, .2 * w, .08 * h, wood, 4), w, side != 'right')


def lamp_modern(st, w, h, px, arms):
    s = st.r(px - 5, 6, 10, h - 6, gray, 5, ol=False) + st.edge(px - 5, 20, h - 26) + st.edge(px + 5, 20, h - 26) + st.r(px - 12, h - 26, 24, 26, midnight, 5, ol=False)
    for d, top, reach in arms:
        y = top * h + 12; x2 = px + d * reach
        s += path(f'M{f(px)} {f(y+60)}Q{f(px)} {f(y)} {f(px+d*60)} {f(y)}H{f(x2-d*40)}', 'none', st.col(gray) if st.name == 'print' else midnight, 8 if st.name == 'print' else 4)
        hx = x2 - (96 if d > 0 else 0)
        s += st.r(hx, y - 10, 96, 20, white, 10) + st.r(hx + 12, y + 6, 72, 8, lamp, 4, ol=False)
    return s


def lamp_trad(st, w, h, px, arms):
    s = st.r(px - 4, 40, 8, h - 40, midnight, 3, ol=False) + st.r(px - 9, h - 28, 18, 28, midnight, 4, ol=False)
    def globe(cx, y): return st.c(cx, y + 18, 15, lamp) + st.r(cx - 8, y + 30, 16, 6, midnight, 2, ol=False)
    if not arms: return s + globe(px, 0)
    reach = (w - 34) if len(arms) == 1 else (w / 2 - 18)
    for d in arms:
        cx = px + d * reach; s += st.ln(px, 44, cx, 44, midnight, 5) + globe(cx, 6)
    return s


def banner(st, w, h, side, colors):
    bw = w * .66; x = w - bw - 5; n = len(colors)
    s = st.r(0, 4, w, 6, midnight, 3, ol=False) + ''.join(st.r(x + i * bw / n, 10, bw / n + .5, h - 22, c, 0, ol=False) for i, c in enumerate(colors))
    return mir(s + st.r(0, h - 12, w, 6, midnight, 3, ol=False), w, side != 'left')


def bollard(st, w, h): return st.r(0, 0, w, h, citron, w / 2, ol=False) + st.r(0, .18 * h, w, .08 * h, midnight, 0, ol=False)
def dome(st, w, h): return st.p(f'M0 {f(h)}Q0 0 {f(w/2)} 0Q{f(w)} 0 {f(w)} {f(h)}Z', lgrey, ol=False)


def shelter(st, w, h, side, roofc):
    s = st.r(.9 * w, .1 * h, 8, .9 * h, gray, 3, ol=False) + st.c(.92 * w, .09 * h, .075 * w, midnight) + st.c(.92 * w, .09 * h, .028 * w, citron, ol=False)
    s += st.r(.05 * w, .24 * h, 9, .76 * h, midnight, 0, ol=False) + st.r(.58 * w, .24 * h, 9, .76 * h, midnight, 0, ol=False)
    s += st.glass(.11 * w, .32 * h, .44 * w, .46 * h, 8) + st.r(0, .17 * h, .72 * w, .075 * h, roofc, 9)
    return mir(s + st.r(.1 * w, .86 * h, .34 * w, .045 * h, wood, 4, ol=False), w, side != 'left')


# ------------------------------------------------------------------ buildings
def building_upper(st, w, h, wall, trim, n):
    s = st.r(0, 0, w, h, wall, 0, ol=False) + st.r(0, h - 10, w, 10, trim, 0, ol=False) + st.edge(1, 0, h) + st.edge(w - 1, 0, h)
    ww = w * .64 / n; gap = (w - ww * n) / (n + 1)
    for i in range(n): s += st.glass(gap + i * (ww + gap), .16 * h, ww, .6 * h, 6)
    return s + st.tone(w * .7, h * .1, w * .28, h * .7, o=.12)


def building_roof(st, w, h, trim): return st.r(0, h * .3, w, h * .7, trim, 0, ol=False) + st.r(0, 0, w, h * .4, white, 4, ol=False)


def building_ground(st, w, h, ww, wall, trim, awning, side):
    s = st.r(0, 0, ww, h - 14, wall, 0, ol=False) + st.r(0, h - 14, ww, 14, midnight, 0, ol=False) + st.edge(1, 0, h - 14) + st.edge(ww - 1, 0, h - 14)
    s += st.r(.3 * ww, .1 * h, .42 * ww, .1 * h, white, 14) + leafshape(.33 * ww, .115 * h, .06 * ww, .07 * h, st.col(trim)) + st.r(.42 * ww, .14 * h, .24 * ww, .025 * h, trim, 3, ol=False)
    s += st.glass(.07 * ww, .5 * h, .15 * ww, .26 * h, 6) + st.glass(.3 * ww, .44 * h, .3 * ww, h * .56 - 16, 6) + st.glass(.62 * ww, .44 * h, .3 * ww, h * .56 - 16, 6)
    return mir(s + st.r(.26 * ww, .32 * h, w - .26 * ww - 3, .07 * h, awning, 8), w, side != 'left')


def home(st, w, h, wall, trim, roofc, side):
    bw = 327.0; base = h - 12; px = bw + 205
    s = st.r(0, 0, bw, base, wall, 0, ol=False) + st.r(0, 232, bw, 8, trim, 0, ol=False) + st.r(0, 468, bw, 8, trim, 0, ol=False) + st.edge(1, 0, base) + st.edge(bw - 1, 248, base)
    s += st.glass(.14 * bw, 56, .24 * bw, 120, 6) + st.glass(.6 * bw, 56, .24 * bw, 120, 6) + st.glass(.14 * bw, 296, .24 * bw, 120, 6) + st.glass(.6 * bw, 296, .24 * bw, 120, 6)
    s += st.r(.14 * bw, 498, .18 * bw, 34, midnight, 4, ol=False) + st.r(.64 * bw, 498, .18 * bw, 34, midnight, 4, ol=False)
    s += st.r(px - 14, 262, 10, 170, trim, 0, ol=False) + st.r(bw - 2, 248, px - bw + 30, 16, roofc, 6)
    s += st.r(bw, 430, px - bw, base - 430, lgrey, 0, ol=False) + st.r(bw, 372, px - bw, 7, midnight, 3, ol=False)
    for i in range(6): s += st.r(bw + 18 + i * 30, 378, 5, 52, midnight, 0, ol=False)
    n = 6; sw_ = (w - px - 30) / n
    for i in range(n): s += st.r(px + i * sw_, 430 + i * (base - 430) / n, sw_ + 1, base - 430 - i * (base - 430) / n, concrete if i % 2 else lgrey, 0, ol=False)
    s += st.ln(px + 4, 378, w - 34, base - 62, midnight, 6) + st.r(w - 38, base - 70, 20, 70, lgrey, 4, ol=False)
    s += st.c(bw + 36, base - 30, 30, leaf3, ol=False) + st.c(bw + 76, base - 24, 24, leaf, ol=False) + st.c(bw + 116, base - 34, 9, berry, ol=False) + st.ln(bw + 116, base - 25, bw + 116, base, leaf3, 3)
    return mir(s + st.r(0, base, w, 12, midnight, 0, ol=False), w, side != 'left')


def home_roof(st, w, h, roofc, side):
    s = st.r(.44 * w, 0, .1 * w, .4 * h, lgrey, 3, ol=False)
    return mir(s + st.pg([(0, h), (.14 * w, .26 * h), (.84 * w, .26 * h), (w, h)], roofc), w, side != 'left')


# ------------------------------------------------------------------ lots
def fence(st, w, h):
    s = st.r(0, h - 18, w, 18, espresso, 0, ol=False)
    for i in range(1, 6): s += rr(i * w / 6 - 1.5, 10, 3, h - 30, st.col(gray), 0, .8)
    for y in (.3, .6): s += rr(0, y * h, w, 3, st.col(gray), 0, .8)
    s += st.r(0, 0, w, 8, midnight, 0, ol=False) + st.r(0, 0, 8, h - 18, midnight, 0, ol=False) + st.r(w - 8, 0, 8, h - 18, midnight, 0, ol=False)
    for i, c in enumerate((leaf3, leaf, citron, leaf)): s += st.r(14 + i * 19, h - 44 - (i % 2) * 8, 12, 28 + (i % 2) * 8, c, 6, ol=False)
    return s


def water(st, w, h, seed=3):
    k = w / 12; s = st.r(0, k, w, h - k, aqua, 0, ol=False) + ''.join(st.c((i + .5) * w / 6, k, k, aqua, ol=False) for i in range(6)); r = rng(seed)
    for i in range(6): s += rr(min(max((i + .5) * w / 6 - 26 + r.uniform(-6, 6), 2), w - 54), 26 + (i * 31 % max(1, int(h - 50))), 52, 7, st.col(white), 3.5, .5 if i % 2 else .3)
    return s


def waterfront_edge(st, w, h, side):
    s = g(water(st, w - 40, 105.0, 5), f'translate(0 {f(h - 105)})')
    for x, y, r_, c in ((.4, .7, 32, gray), (.52, .6, 38, lgrey), (.64, .72, 30, gray), (.5, .82, 26, concrete)): s += st.c(x * w, y * h, r_, c)
    return mir(s + st.r(w - 42, 10, 42, h - 10, concrete, 0, ol=False) + st.edge(w - 42, 10, h - 4) + st.r(w - 48, 0, 48, 12, white, 5, ol=False), w, side != 'left')


def parking_lot(st, w, h, side, edge):
    s = st.r(0, h - 9, w, 9, midnight, 0, ol=False); sign = ''
    if edge:
        px = w - 42; s += st.r(px - 4, 86, 8, h - 95, gray, 0, ol=False)
        s += g(car_side(st, 236, 96, 'left'), f'translate({f(w - 300)} {f(h - 108)})') + g(car(st, 112, 88), f'translate(12 {f(h - 100)})')
        sx = px if side == 'left' else w - px
        sign = st.r(sx - 36, 8, 74, 78, aqua if st.name == 'print' else cobalt, 20) + path(f'M{f(sx-14)} 68V22H{f(sx+6)}Q{f(sx+22)} 22 {f(sx+22)} 37Q{f(sx+22)} 52 {f(sx+6)} 52H{f(sx-14)}', 'none', '#FFFFFF', 11, cap='butt')
    else:
        s += g(car(st, 112, 88, rear=True), f'translate(40 {f(h - 100)})') + st.r(250, h - 22, 110, 13, lgrey, 6, ol=False)
    return mir(s, w, side != 'left') + sign


# ------------------------------------------------------------------ sky + people
def clouds(st, w, h, seed, n, o):
    r = rng(seed); s = ''
    for i in range(n):
        cw = r.uniform(120, 210); ch = cw * .36; x = r.uniform(0, w); y = r.uniform(.05, .8) * (h - ch * 1.6) + ch * .6
        if st.name == 'sketch':
            one = path(f'M{f(ch*.3)} {f(ch)}H{f(cw-ch*.3)}Q{f(cw)} {f(ch)} {f(cw)} {f(ch*.7)}Q{f(cw)} {f(ch*.4)} {f(cw*.78)} {f(ch*.4)}Q{f(cw*.72)} {f(-ch*.1)} {f(cw*.5)} {f(ch*.05)}Q{f(cw*.3)} {f(-ch*.15)} {f(cw*.24)} {f(ch*.42)}Q0 {f(ch*.4)} 0 {f(ch*.7)}Q0 {f(ch)} {f(ch*.3)} {f(ch)}Z', '#FFFFFF', midnight, 3, o)
        else:
            one = rr(0, ch * .4, cw, ch * .6, '#FFFFFF', ch * .3, o) + circ(cw * .36, ch * .42, ch * .42, '#FFFFFF', o) + circ(cw * .62, ch * .5, ch * .32, '#FFFFFF', o)
        for dx in (0, -w, w):
            if -cw < x + dx < w: s += g(one, f'translate({f(x + dx)} {f(y)})')
    return s


def figure(st, cx, base, ht, sk, hair, top, bot, dress=False):
    hd = ht * .075; lw = ht * .055; hip = base - ht * .46; tw = ht * .2; ty = base - ht * .82; s = ''
    if dress:
        s += st.r(cx - lw - 1, hip + ht * .2, lw, ht * .26 - 4, sk, lw / 2, ol=False) + st.r(cx + 1, hip + ht * .2, lw, ht * .26 - 4, sk, lw / 2, ol=False)
        s += st.pg([(cx - tw * .45, hip - ht * .1), (cx + tw * .45, hip - ht * .1), (cx + tw * .75, hip + ht * .22), (cx - tw * .75, hip + ht * .22)], top)
    else:
        s += st.r(cx - lw - 2, hip - 6, lw + 1, ht * .46 + 2, bot, lw / 2) + st.r(cx + 1, hip - 6, lw + 1, ht * .46 + 2, bot, lw / 2)
    s += st.r(cx - lw - 4, base - 5, lw + 5, 5, charcoal, 2, ol=False) + st.r(cx + 1, base - 5, lw + 5, 5, charcoal, 2, ol=False)
    s += st.r(cx - tw / 2 - 5, ty + 5, 7, ht * .3, top if not dress else sk, 3.5, ol=False) + st.r(cx + tw / 2 - 2, ty + 5, 7, ht * .3, top if not dress else sk, 3.5, ol=False)
    s += st.r(cx - tw / 2, ty, tw, ht * .4, top, tw * .42) + st.c(cx, ty - hd - 2, hd, sk)
    return s + st.p(f'M{f(cx-hd-1)} {f(ty-hd-2)}Q{f(cx-hd)} {f(ty-2*hd-6)} {f(cx)} {f(ty-2*hd-5)}Q{f(cx+hd)} {f(ty-2*hd-6)} {f(cx+hd+1)} {f(ty-hd-2)}Z', hair, ol=False)


def dog(st, x, base, c, k=1.0):
    return st.r(x, base - 30 * k, 36 * k, 16 * k, c, 8 * k) + st.r(x + 3 * k, base - 18 * k, 6 * k, 18 * k, c, 3, ol=False) + st.r(x + 26 * k, base - 18 * k, 6 * k, 18 * k, c, 3, ol=False) + st.c(x + 36 * k, base - 34 * k, 10 * k, c)


def person(st, i):
    r = rng(100 + i); base = 190; cx = 60
    sk = SK[r.randrange(5)]; hr = S.HAIR[r.randrange(6)]; tp = S.TOPS[(i * 5) % 12]; bt = S.BOTS[(i * 3) % 7]
    ht = r.uniform(128, 150); dress = i in (1, 3, 5, 8, 10, 13, 17, 18)
    if i in (21, 22): return figure(st, cx, base, r.uniform(78, 92), sk, hr, tp, bt, i == 21)
    if i in (19, 20):
        seat = base - 34
        s = st.ring(cx, base - 24, 22, charcoal, 5) + st.c(cx + 26, base - 7, 7, charcoal, ol=False) + st.r(cx - 18, base - 62, 6, 44, midnight, 3, ol=False)
        s += st.r(cx - 8, seat - 2, 36, 11, bt, 5, ol=False) + st.r(cx + 20, seat, 10, 30, bt, 5, ol=False) + st.r(cx + 18, base - 8, 16, 6, charcoal, 2, ol=False)
        return s + st.r(cx - 14, seat - 52, 26, 54, tp, 11) + st.c(cx - 1, seat - 64, 10, sk)
    if i == 16: return figure(st, cx, base, 132, sk, lgrey, tp, bt) + st.ln(cx + 26, base - 62, cx + 30, base, wood, 4)
    if i in (17, 18): return figure(st, cx - 6, base, 128, sk, lgrey if i == 17 else gray, tp, bt, True) + st.stroke(f'M{f(cx+8)} {f(base)}V{f(base-58)}H{f(cx+30)}V{f(base)}', gray, 4)
    if i == 23: return figure(st, cx - 12, base, ht, sk, hr, tp, bt, True) + dog(st, cx + 14, base, charcoal, .8)
    if i == 24: return figure(st, cx + 14, base, ht, sk, hr, tp, bt) + mirror(dog(st, 68, base, wood, 1.1), 120)
    if i == 25: return figure(st, cx, base - 8, 88, sk, hr, tp, bt) + st.r(cx - 22, base - 8, 44, 4, gray, 2, ol=False) + st.c(cx - 20, base - 4, 4, charcoal, ol=False) + st.c(cx + 20, base - 4, 4, charcoal, ol=False) + st.r(cx + 16, base - 56, 4, 50, gray, 0, ol=False)
    if i in (26, 28): return figure(st, cx - 14, base, ht, sk, hr, tp, bt, i == 26) + figure(st, cx + 22, base, 86, sk, hr, S.TOPS[(i + 4) % 12], bt, True)
    if i == 27: return figure(st, cx, base, ht, sk, hr, tp, bt, True) + line(cx + 16, base - 64, cx + 34, base, '#FFFFFF', 3) + rr(cx + 30, base - 12, 6, 12, st.col(berry), 2)
    if i == 29: return figure(st, cx - 20, base, 140, sk, hr, tp, bt, True) + figure(st, cx + 22, base, 148, SK[(i + 2) % 5], gray, S.TOPS[(i + 7) % 12], S.BOTS[(i + 2) % 7])
    if i == 30: return figure(st, cx, base, ht, sk, hr, tp, bt) + st.r(cx + 4, base - 108, 22, 30, citron, 10) + st.c(cx + 16, base - 114, 7, SK[(i + 1) % 5], ol=False)
    return figure(st, cx, base, ht, sk, hr, tp, bt, dress)


# ------------------------------------------------------------------ dispatch
BLD = {'narrow-left': (teal, deep, citron, 2), 'narrow-right': (body, gray, papaya, 2), 'wide-left': (aquaT, aqua, leaf, 4), 'wide-right': (aqua, midnight, citron, 4)}
HOME = {'left': (aqua, deep, midnight), 'right': (leafT, leaf, espresso)}
PRIDE = ['#E24C4B', papaya, yellow, leaf, cobalt, plum]


def draw(o, st, ctx):
    n = o['names'][0]; x, y, w, h = o['bbox']; side = 'left' if n.endswith('left') or '-left-' in n else 'right'; st.seed(n)
    if n in st.SURF: return rr(0, 0, w, h, st.SURF[n])
    if n.startswith('lot-fence'): return fence(st, w, h)
    if n == 'lot-grass': return tufts(st, w, h, 6)
    if n.startswith('wayfinding'): return wayfinding(st, w, h)
    if n.startswith('bike-rack-parallel'): return bike_rack_front(st, w, h, side)
    if n.startswith('bike-rack'): return bike_rack_side(st, w, h, side, 'road' in n)
    if n == 'bench-center': return bench_front(st, w, h)
    if n.startswith('bench'): return bench_side(st, w, h, side)
    m = re.match(r'arrow-(inbound|outbound)-(.+)', n)
    if m:
        grey = m.group(2).startswith('grey'); return V.arrow(w, h, 'straight' if grey else m.group(2), m.group(1) == 'inbound', white, .45 if grey else None)
    if n.startswith('waterfront'): return waterfront_edge(st, w, h, side) if n.endswith('edge') else water(st, w, h)
    if n.startswith('parking-stall'): return V.stall_line(w, h, side)
    if n.startswith('lamp-modern'):
        px = ctx.foot(o); return lamp_modern(st, w, h, px, {'both': [(-1, 0, px), (1, .2, min(w - px, 210))], 'right': [(1, 0, w - px)], 'left': [(-1, 0, px)]}[n.split('-')[-1]])
    if n.startswith('lamp-traditional'): return lamp_trad(st, w, h, ctx.foot(o), {'both': [], 'left': [-1], 'right': [1]}[n.split('-')[-1]])
    if n.startswith('bus-'): return bus(st, w, h, 'rear' in n)
    if n.startswith('car-side'): return car_side(st, w, h, side)
    if n.startswith('car-'): return car(st, w, h, 'rear' in n, 'left' if 'signal-left' in n else 'right' if 'signal-right' in n else None)
    if n == 'tree-palm': return tree_palm(st, w, h, ctx.foot(o))
    if n == 'tree-big': return tree_big(st, w, h, ctx.foot(o))
    if n.startswith('light-rail'): return light_rail(st, w, h, 'rear' in n)
    if n.startswith('streetcar'): return streetcar(st, w, h, 'rear' in n)
    if n.startswith('cyclist-a'): return cyclist(st, w, h, 'rear' in n, aqua, citron, SK[3], midnight)
    if n.startswith('cyclist-b'): return cyclist(st, w, h, 'rear' in n, berry, papaya, SK[0], dgrey)
    if n.startswith('rail-tracks'): return V.rails(w, h, st.col(charcoal) if 'dark' in n else st.col(gray))
    if n.startswith('truck'): return truck(st, w, h, 'rear' in n)
    if n.startswith('train'): return train(st, w, h)
    if n.startswith('center-line'): return V.center_line(w, h, side)
    if n.startswith('lane-edge'): return V.bar(w, h)
    if n.startswith('sharrow'): return V.sharrow(w, h, 'inbound' in n)
    if n == 'striped-buffer-hatching': return S.hatching(w, h)
    if n.startswith('parklet'): return parklet(st, w, h, side)
    if n == 'flowers': return flowers(st, w, h)
    if n == 'bollard': return bollard(st, w, h)
    if n == 'planter-box': return planter_box(st, w, h)
    if n == 'divider-dome': return dome(st, w, h)
    if n.startswith('transit-shelter'): return shelter(st, w, h, side, leaf if 'light-rail' in n else teal)
    if n.startswith('banner'): return banner(st, w, h, side, PRIDE)
    if n.startswith('parking-lot'): return parking_lot(st, w, h, side, n.endswith('edge'))
    if n == 'ground-cover-grass':
        s = ''
        for part, fn in (('ground-cover-grass', lambda a, b: tufts(st, a, b, 8)), ('bush', lambda a, b: bush(st, a, b))):
            mm = ctx.bymanifest[part]; bx, by, bw, bh = ctx.content_bbox(mm['sheet'], mm['px'], mm['py'], mm['pw'], 40 if part == 'ground-cover-grass' else mm['ph'])
            s += g(fn(bw, bh), f'translate({bx - x} {by - y})')
        return s
    m = re.match(r'building-(narrow|wide)-(left|right)-(roof|upper-floor|ground-floor)', n)
    if m:
        wall, trim, awn, nwin = BLD[m.group(1) + '-' + m.group(2)]
        if m.group(3) == 'roof': return building_roof(st, w, h, trim)
        if m.group(3) == 'upper-floor': return building_upper(st, w, h, wall, trim, nwin)
        return building_ground(st, w, h, ctx.byname[n.replace('ground-floor', 'upper-floor')]['bbox'][2], wall, trim, awn, m.group(2))
    m = re.match(r'building-home-(left|right)-(roof|ground-floor)', n)
    if m:
        wall, trim, roofc = HOME[m.group(1)]
        return home_roof(st, w, h, roofc, m.group(1)) if m.group(2) == 'roof' else home(st, w, h, wall, trim, roofc, m.group(1))
    raise KeyError(n)
