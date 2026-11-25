"""Vehicles, cyclists and road markings, redrawn in the VHB palette.
Every function draws into a (w, h) box whose bottom edge is the ground line."""
from svgkit import *


def _glint(x, y, w, h):
    return poly([(x + .22 * w, y), (x + .42 * w, y), (x + .2 * w, y + h), (x, y + h)], white, .13)


def _curves(x, y, w, h, c1=teal, c2=aqua, c3=citron):
    """Three flowing bands lifted from the logo's 'improving mobility' curves."""
    def band(t, b, c):
        return path(f'M{f(x)} {f(y+t*h)}C{f(x+.3*w)} {f(y+(t-.25)*h)} {f(x+.65*w)} {f(y+(t+.3)*h)} {f(x+w)} {f(y+(t-.1)*h)}'
                    f'V{f(y+(b-.1)*h)}C{f(x+.65*w)} {f(y+(b+.3)*h)} {f(x+.3*w)} {f(y+(b-.25)*h)} {f(x)} {f(y+b*h)}Z', c)
    return band(.2, .55, c1) + band(.62, .8, c2) + band(.87, .97, c3)


def car(w, h, rear=False, signal=None, cw=145):
    W = min(cw, w); ox = (w - W) if signal == 'left' else 0
    s = ''
    if signal:
        s += circ(ox + (.14 * W if signal == 'left' else .86 * W), .53 * h, .17 * W, papaya, .3)
    def half():
        return rr(.07 * W, .78 * h, .16 * W, .22 * h, charcoal, 5) + rr(0, .33 * h, .085 * W, .075 * h, body2, 3)
    c = half() + mirror(half(), W)
    c += rc(.03 * W, .42 * h, .94 * W, .46 * h, body, 18, 18, 8, 8)
    c += poly([(.16 * W, .44 * h), (.27 * W, .03 * h), (.73 * W, .03 * h), (.84 * W, .44 * h)], body2)
    c += poly([(.205 * W, .42 * h), (.3 * W, .085 * h), (.7 * W, .085 * h), (.795 * W, .42 * h)], midnight)
    c += poly([(.34 * W, .085 * h), (.44 * W, .085 * h), (.33 * W, .42 * h), (.245 * W, .42 * h)], white, .13)
    c += rr(.03 * W, .64 * h, .94 * W, .085 * h, teal) + rr(.03 * W, .725 * h, .94 * W, .025 * h, citron)
    c += rr(.05 * W, .79 * h, .9 * W, .09 * h, gray, 4)
    lc = berry if rear else lamp
    c += leafshape(.07 * W, .47 * h, .17 * W, .12 * h, lc) + mirror(leafshape(.07 * W, .47 * h, .17 * W, .12 * h, lc), W)
    c += rr(.41 * W, .49 * h, .18 * W, .1 * h, lgrey, 2) if rear else rr(.34 * W, .49 * h, .32 * W, .1 * h, dgrey, 5)
    if signal:
        sl = leafshape(.07 * W, .47 * h, .17 * W, .12 * h, papaya)
        c += sl if signal == 'left' else mirror(sl, W)
    return s + g(c, f'translate({f(ox)} 0)')


def car_side(w, h, facing='left'):
    s = circ(.2 * w, .8 * h, .2 * h, charcoal) + circ(.8 * w, .8 * h, .2 * h, charcoal)
    s = path(f'M{f(.02*w)} {f(.78*h)}V{f(.5*h)}Q{f(.03*w)} {f(.4*h)} {f(.12*w)} {f(.37*h)}L{f(.3*w)} {f(.3*h)}L{f(.42*w)} {f(.04*h)}'
             f'H{f(.8*w)}Q{f(.9*w)} {f(.05*h)} {f(.95*w)} {f(.3*h)}L{f(.98*w)} {f(.5*h)}V{f(.78*h)}Z', body) + \
        rr(.02 * w, .58 * h, .96 * w, .1 * h, teal) + rr(.02 * w, .68 * h, .96 * w, .03 * h, citron) + s
    s += circ(.2 * w, .8 * h, .09 * h, lgrey) + circ(.8 * w, .8 * h, .09 * h, lgrey)
    s += poly([(.34 * w, .32 * h), (.44 * w, .1 * h), (.58 * w, .1 * h), (.58 * w, .32 * h)], midnight)
    s += poly([(.61 * w, .1 * h), (.79 * w, .1 * h), (.88 * w, .32 * h), (.61 * w, .32 * h)], midnight)
    s += leafshape(.02 * w, .42 * h, .07 * w, .1 * h, lamp) + rr(.93 * w, .4 * h, .05 * w, .1 * h, berry, 2)
    return s if facing == 'left' else mirror(s, w)


def bus(w, h, rear=False):
    def half():
        return rr(.1 * w, .9 * h, .15 * w, .1 * h, charcoal, 4) + rr(0, .19 * h, .055 * w, .15 * h, dgrey, 3) + \
            rr(.04 * w, .22 * h, .05 * w, .02 * h, dgrey)
    s = half() + mirror(half(), w)
    s += rc(.07 * w, 0, .86 * w, .93 * h, body, 24, 24, 8, 8) + rc(.07 * w, 0, .86 * w, .12 * h, teal, 24, 24, 0, 0)
    if rear:
        s += rr(.2 * w, .16 * h, .6 * w, .2 * h, midnight, 8) + _glint(.24 * w, .16 * h, .25 * w, .2 * h)
        s += rr(.24 * w, .42 * h, .52 * w, .15 * h, dgrey, 5)
        for i in range(3): s += rr(.28 * w, (.45 + i * .04) * h, .44 * w, .012 * h, gray)
    else:
        s += rr(.14 * w, .028 * h, .72 * w, .075 * h, charcoal, 5)
        s += rr(.18 * w, .047 * h, .07 * w, .037 * h, citron, 2) + rr(.29 * w, .047 * h, .34 * w, .037 * h, citron, 2, .85)
        s += rc(.12 * w, .16 * h, .37 * w, .42 * h, midnight, 14, 3, 3, 3) + rc(.51 * w, .16 * h, .37 * w, .42 * h, midnight, 3, 14, 3, 3)
        s += _glint(.16 * w, .16 * h, .22 * w, .42 * h) + _glint(.55 * w, .16 * h, .22 * w, .42 * h)
    s += _curves(.07 * w, .62 * h, .86 * w, .2 * h)
    lc = berry if rear else lamp
    s += leafshape(.11 * w, .8 * h, .13 * w, .055 * h, lc) + mirror(leafshape(.11 * w, .8 * h, .13 * w, .055 * h, lc), w)
    if rear: s += rr(.42 * w, .78 * h, .16 * w, .07 * h, lgrey, 2) + circ(.14 * w, .7 * h, .022 * w, papaya) + circ(.86 * w, .7 * h, .022 * w, papaya)
    s += rr(.07 * w, .87 * h, .86 * w, .06 * h, dgrey, 4)
    return s


def _pantograph(w, top, bottom):
    c = w / 2
    return line(.22 * w, top + 3, .78 * w, top + 3, charcoal, 5) + line(.3 * w, top + 3, .44 * w, bottom, charcoal, 5) + \
        line(.7 * w, top + 3, .56 * w, bottom, charcoal, 5) + rr(c - .12 * w, bottom - 6, .24 * w, 10, dgrey, 3)


def light_rail(w, h, rear=False):
    t = .21 * h
    s = _pantograph(w, 0, t + 4)
    s += rr(.12 * w, .95 * h, .1 * w, .05 * h, charcoal, 2) + rr(.78 * w, .95 * h, .1 * w, .05 * h, charcoal, 2)
    s += rc(.02 * w, t, .96 * w, .76 * h, body, 30, 30, 6, 6)
    s += rc(.1 * w, t + .035 * h, .8 * w, .06 * h, charcoal, 8, 8, 2, 2)
    s += rr(.15 * w, t + .05 * h, .1 * w, .03 * h, citron if not rear else berry, 2)
    s += rc(.1 * w, t + .11 * h, .8 * w, .4 * h, midnight, 4, 4, 26, 26) + _glint(.2 * w, t + .11 * h, .4 * w, .4 * h)
    s += _curves(.02 * w, .8 * h, .96 * w, .13 * h, teal, aqua, leaf)
    lc = berry if rear else lamp
    s += leafshape(.1 * w, .745 * h, .16 * w, .035 * h, lc) + mirror(leafshape(.1 * w, .745 * h, .16 * w, .035 * h, lc), w)
    s += rr(.02 * w, .93 * h, .96 * w, .035 * h, dgrey, 3)
    return s


def streetcar(w, h, rear=False):
    t = .2 * h
    s = _pantograph(w, 0, t + 4)
    def half(): return rr(0, .37 * h, .05 * w, .07 * h, body2, 3) + rr(.14 * w, .94 * h, .08 * w, .06 * h, charcoal, 2)
    s += half() + mirror(half(), w)
    base, cap = (body, teal) if rear else (teal, body)
    s += rc(.07 * w, t, .86 * w, .73 * h, base, 26, 26, 6, 6)
    s += rc(.07 * w, t, .86 * w, .09 * h, cap if rear else body, 26, 26, 0, 0)
    if not rear:
        s += rr(.16 * w, t + .03 * h, .68 * w, .055 * h, charcoal, 4) + rr(.2 * w, t + .043 * h, .08 * w, .03 * h, citron, 2)
    s += rc(.12 * w, t + .115 * h, .37 * w, .17 * h, midnight, 12, 3, 3, 3) + rc(.51 * w, t + .115 * h, .37 * w, .17 * h, midnight, 3, 12, 3, 3)
    s += _glint(.16 * w, t + .115 * h, .2 * w, .17 * h) + _glint(.55 * w, t + .115 * h, .2 * w, .17 * h)
    s += rr(.07 * w, t + .31 * h, .86 * w, .025 * h, citron if not rear else aqua)
    s += circ(.5 * w, .68 * h, .045 * w, lamp if not rear else charcoal)
    lc = papaya if not rear else berry
    s += leafshape(.2 * w, .64 * h, .09 * w, .035 * h, lc) + mirror(leafshape(.2 * w, .64 * h, .09 * w, .035 * h, lc), w)
    s += poly([(.07 * w, .9 * h), (.5 * w, .86 * h), (.93 * w, .9 * h), (.93 * w, .94 * h), (.07 * w, .94 * h)], charcoal)
    return s


def truck(w, h, rear=False):
    if rear:
        s = rr(.1 * w, .9 * h, .16 * w, .1 * h, charcoal, 4) + rr(.74 * w, .9 * h, .16 * w, .1 * h, charcoal, 4)
        s += rc(0, 0, w, .86 * h, body2, 8, 8, 0, 0) + rr(.05 * w, .07 * h, .9 * w, .72 * h, body, 4)
        s += rr(.495 * w, .07 * h, .012 * w, .72 * h, gray)
        for i in range(1, 6): s += rr(.05 * w, (.07 + i * .12) * h, .9 * w, .008 * h, body2)
        s += leafshape(.6 * w, .2 * h, .22 * w, .2 * h, teal, o=.9) + leafshape(.66 * w, .3 * h, .2 * w, .18 * h, leaf, True, .85)
        s += rr(0, .86 * h, w, .06 * h, dgrey, 3) + rr(.4 * w, .8 * h, .2 * w, .05 * h, lgrey, 2)
        s += circ(.08 * w, .89 * h, .03 * w, berry) + circ(.92 * w, .89 * h, .03 * w, berry) + circ(.16 * w, .89 * h, .025 * w, papaya) + circ(.84 * w, .89 * h, .025 * w, papaya)
        return s
    def half(): return rr(.1 * w, .9 * h, .15 * w, .1 * h, charcoal, 4) + rr(0, .32 * h, .06 * w, .13 * h, dgrey, 3)
    s = half() + mirror(half(), w)
    s += rc(.06 * w, 0, .88 * w, .45 * h, body2, 8, 8, 0, 0) + poly([(.06 * w, .0), (.62 * w, 0), (.06 * w, .3 * h)], white, .25)
    s += leafshape(.62 * w, .06 * h, .18 * w, .14 * h, teal) + leafshape(.7 * w, .12 * h, .14 * w, .12 * h, leaf, True, .9)
    s += rc(.1 * w, .26 * h, .8 * w, .66 * h, body, 14, 14, 6, 6)
    s += poly([(.16 * w, .52 * h), (.2 * w, .31 * h), (.8 * w, .31 * h), (.84 * w, .52 * h)], midnight) + _glint(.3 * w, .31 * h, .3 * w, .21 * h)
    s += rr(.36 * w, .6 * h, .28 * w, .16 * h, dgrey, 5)
    for i in range(3): s += rr(.39 * w, (.63 + i * .04) * h, .22 * w, .012 * h, charcoal)
    s += rr(.1 * w, .56 * h, .8 * w, .028 * h, teal)
    s += leafshape(.14 * w, .64 * h, .14 * w, .08 * h, lamp) + mirror(leafshape(.14 * w, .64 * h, .14 * w, .08 * h, lamp), w)
    s += rr(.08 * w, .84 * h, .84 * w, .07 * h, gray, 4)
    return s


def train(w, h):
    s = rr(.1 * w, .93 * h, .14 * w, .07 * h, charcoal, 3) + rr(.76 * w, .93 * h, .14 * w, .07 * h, charcoal, 3)
    s += rr(.42 * w, 0, .16 * w, .06 * h, dgrey, 4) + circ(.44 * w, .03 * h, .035 * w, lamp) + circ(.56 * w, .03 * h, .035 * w, lamp)
    s += rc(.08 * w, .05 * h, .84 * w, .9 * h, midnight, 40, 40, 6, 6)
    s += rc(.14 * w, .09 * h, .72 * w, .08 * h, charcoal, 16, 16, 2, 2) + rr(.2 * w, .11 * h, .2 * w, .04 * h, citron, 2) + rr(.6 * w, .11 * h, .2 * w, .04 * h, citron, 2)
    s += rc(.14 * w, .2 * h, .34 * w, .22 * h, glass2, 10, 2, 2, 2) + rc(.52 * w, .2 * h, .34 * w, .22 * h, glass2, 2, 10, 2, 2)
    for i in range(3):
        y = (.5 + i * .11) * h
        s += poly([(.2 * w, y + .09 * h), (.5 * w, y), (.8 * w, y + .09 * h), (.8 * w, y + .14 * h), (.5 * w, y + .05 * h), (.2 * w, y + .14 * h)], citron if i != 1 else white)
    s += rr(0, .52 * h, .05 * w, .4 * h, gray, 3) + rr(.95 * w, .52 * h, .05 * w, .4 * h, gray, 3)
    s += rr(.04 * w, .88 * h, .92 * w, .07 * h, dgrey, 4)
    return s


def cyclist(w, h, rear=False, top=aqua, hat=citron, skin=skin[2], pants=midnight):
    c = w / 2
    s = rr(c - 3, .58 * h, 6, .42 * h, charcoal, 3)                       # wheel, edge on
    s += rr(c - 2, .5 * h, 4, .2 * h, gray)                                # fork / frame
    s += rr(c - .32 * w, .66 * h, .2 * w, .2 * h, pants, 4) + rr(c + .12 * w, .66 * h, .2 * w, .2 * h, pants, 4)  # legs
    s += rr(c - .36 * w, .84 * h, .24 * w, .05 * h, charcoal, 2) + rr(c + .12 * w, .84 * h, .24 * w, .05 * h, charcoal, 2)
    s += leafshape(c - .34 * w, .24 * h, .68 * w, .38 * h, top, rear)      # torso: brand leaf
    s += rr(.02 * w, .44 * h, .96 * w, .035 * h, charcoal, 3)              # handlebar
    s += rr(.04 * w, .3 * h, .14 * w, .17 * h, top, 4) + rr(.82 * w, .3 * h, .14 * w, .17 * h, top, 4)  # arms
    s += circ(c, .15 * h, .2 * w, skin)
    s += rc(c - .24 * w, .02 * h, .48 * w, .12 * h, hat, 12, 12, 2, 2)
    if rear: s += rr(c - .2 * w, .1 * h, .4 * w, .07 * h, espresso, 3) + circ(c, .64 * h, 3, berry)
    else: s += circ(c, .5 * h, 3.5, lamp)
    return s


# ---------------------------------------------------------------- road markings
def _head(x, y, size, ang):
    return rot(poly([(x, y - size * .9), (x + size * .75, y + size * .25), (x - size * .75, y + size * .25)], '#MK'), ang, x, y)


def arrow(w, h, kind, inbound=False, color=white, o=None):
    """Outbound arrows point up; the app's inbound art is the same glyph flipped vertically."""
    sw = min(w * .22, 11); hs = sw * 1.9
    def shaft(d): return path(d, 'none', '#MK', sw, cap='butt')
    def left(x0=.72, top=.42):
        return shaft(f'M{f(x0*w)} {f(h)}V{f((top+.25)*h)}Q{f(x0*w)} {f(top*h)} {f((x0-.3)*w)} {f(top*h)}H{f(hs*.8)}') + _head(hs * .9, top * h, hs, -90)
    if kind == 'straight':
        s = shaft(f'M{f(w/2)} {f(h)}V{f(hs)}') + _head(w / 2, hs, hs, 0)
    elif kind == 'left': s = left(.72, .38)
    elif kind == 'right': s = mirror(left(.72, .38), w)
    elif kind == 'left-straight':
        s = shaft(f'M{f(.7*w)} {f(h)}V{f(hs)}') + _head(.7 * w, hs, hs, 0) + \
            shaft(f'M{f(.7*w)} {f(.8*h)}Q{f(.7*w)} {f(.58*h)} {f(.45*w)} {f(.58*h)}H{f(hs*.8)}') + _head(hs * .9, .58 * h, hs, -90)
    elif kind == 'right-straight': s = mirror(arrow(w, h, 'left-straight', False, '#MK'), w)
    elif kind == 'both':
        hw = w / 2
        one = shaft(f'M{f(hw)} {f(h)}V{f(.75*h)}Q{f(hw)} {f(.4*h)} {f(.3*w)} {f(.4*h)}H{f(hs*.8)}') + _head(hs * .9, .4 * h, hs, -90)
        s = one + mirror(one, w)
    elif kind == 'shared':
        a = g(left(.72, .38), f'translate(0 {f(.42*h)}) scale(.55 .58)')
        b = g(flipv(mirror(left(.72, .38), w), h), f'translate({f(.45*w)} 0) scale(.55 .58)')
        s = a + b
    if inbound: s = flipv(s, h)
    return g(s.replace('#MK', color)) if o is None else f'<g opacity="{o}">' + s.replace('#MK', color) + '</g>'


def sharrow(w, h, inbound=False):
    sw = 4.5
    def chev(y): return path(f'M{f(.12*w)} {f(y+.16*h)}L{f(.5*w)} {f(y)}L{f(.88*w)} {f(y+.16*h)}', 'none', white, 6, cap='butt')
    r = .17 * w; y = .76 * h
    bike = f'<circle cx="{f(.24*w)}" cy="{f(y)}" r="{f(r)}" fill="none" stroke="{white}" stroke-width="{sw}"/>' \
           f'<circle cx="{f(.76*w)}" cy="{f(y)}" r="{f(r)}" fill="none" stroke="{white}" stroke-width="{sw}"/>'
    bike += path(f'M{f(.24*w)} {f(y)}L{f(.42*w)} {f(y-.24*h)}H{f(.68*w)}L{f(.76*w)} {f(y)}M{f(.42*w)} {f(y-.24*h)}L{f(.52*w)} {f(y)}L{f(.68*w)} {f(y-.24*h)}'
                 f'M{f(.36*w)} {f(y-.3*h)}H{f(.48*w)}M{f(.62*w)} {f(y-.32*h)}H{f(.74*w)}', 'none', white, sw)
    s = chev(.03 * h) + chev(.2 * h) + bike
    return g(s, f'rotate(180 {f(w/2)} {f(h/2)})') if inbound else s


def bar(w, h, color=white): return rr(0, 0, w, h, color)


def center_line(w, h, side):
    solid = rr(0, 0, 8, h, yellow); d = ''.join(rr(w - 8, y, 8, h * .28, yellow) for y in (0, h * .72))
    s = solid + d
    return s if side == 'right' else mirror(s, w)


def stall_line(w, h, side):
    s = rr(w - 8, 0, 8, h, white) + rr(0, h / 2 - 4, w, 8, white)
    return s if side == 'right' else mirror(s, w)


def rails(w, h, color): return rr(0, 0, 8, h, color) + rr(w - 8, 0, 8, h, color)
