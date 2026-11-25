"""Tiny SVG helpers + VHB palette shared by the sprite generator."""
import math, random

# Sampled from the vector swatches in the VHB brand book (pp. 66-67). Confirm against the Brand Toolkit values.
PAL = dict(teal='#006B6E', deep='#005356', aqua='#00839B', leaf='#789B4A', gray='#97989A', cobalt='#0071B9',
           midnight='#272B67', plum='#662F6C', berry='#8B1D41', papaya='#CE812D', citron='#B4CC43',
           charcoal='#212721', espresso='#3E2B2F', dgrey='#5E5C5A', lgrey='#E5E5E5', white='#FFFFFF')
# Tints / shades derived from the palette for shading only
TINT = dict(body='#F4F6F6', body2='#D9DCDD', glass2='#3A4088', aquaT='#CFE6EB', leafT='#DDE8CC', tealT='#CCE1E2',
            cobaltT='#CCE3F1', concrete='#DADBDC', leaf2='#8FB25C', leaf3='#5F8038', wood='#A8703A',
            lamp='#FFF4C7', yellow='#F2C230', skin=['#F6D3B8', '#E3AE86', '#C48A5E', '#8D5A3B', '#5B3A29'])
globals().update(PAL); globals().update(TINT)

def f(v): return ('%.1f' % v).rstrip('0').rstrip('.')
def op(o): return '' if o is None or o >= 1 else f' opacity="{o}"'
def rr(x, y, w, h, fill, r=0, o=None):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"' + (f' rx="{f(r)}"' if r else '') + f' fill="{fill}"{op(o)}/>'
def rc(x, y, w, h, fill, tl=0, tr=0, br=0, bl=0, o=None):
    m = min(w, h) / 2; tl, tr, br, bl = [min(v, m) for v in (tl, tr, br, bl)]
    d = (f'M{f(x+tl)} {f(y)}H{f(x+w-tr)}' + (f'A{f(tr)} {f(tr)} 0 0 1 {f(x+w)} {f(y+tr)}' if tr else '') + f'V{f(y+h-br)}' +
         (f'A{f(br)} {f(br)} 0 0 1 {f(x+w-br)} {f(y+h)}' if br else '') + f'H{f(x+bl)}' +
         (f'A{f(bl)} {f(bl)} 0 0 1 {f(x)} {f(y+h-bl)}' if bl else '') + f'V{f(y+tl)}' +
         (f'A{f(tl)} {f(tl)} 0 0 1 {f(x+tl)} {f(y)}' if tl else '') + 'Z')
    return f'<path d="{d}" fill="{fill}"{op(o)}/>'
def leafshape(x, y, w, h, fill, flip=False, o=None, big=.5, small=.08):
    """The brand's leaf/droplet swatch: two opposite corners swept round, two kept tight."""
    b, s = min(w, h) * big, min(w, h) * small
    return rc(x, y, w, h, fill, s, b, s, b, o) if flip else rc(x, y, w, h, fill, b, s, b, s, o)
def poly(pts, fill, o=None):
    return '<polygon points="' + ' '.join(f'{f(x)},{f(y)}' for x, y in pts) + f'" fill="{fill}"{op(o)}/>'
def circ(cx, cy, r, fill, o=None): return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}"{op(o)}/>'
def ell(cx, cy, rx, ry, fill, o=None): return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}"{op(o)}/>'
def line(x1, y1, x2, y2, stroke, sw, cap='round', o=None):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{stroke}" stroke-width="{f(sw)}" stroke-linecap="{cap}"{op(o)}/>'
def path(d, fill='none', stroke=None, sw=0, o=None, cap='round'):
    s = f' stroke="{stroke}" stroke-width="{f(sw)}" stroke-linecap="{cap}" stroke-linejoin="round"' if stroke else ''
    return f'<path d="{d}" fill="{fill}"{s}{op(o)}/>'
def g(content, transform=None, id=None):
    return '<g' + (f' id="{id}"' if id else '') + (f' transform="{transform}"' if transform else '') + f'>{content}</g>'
def mirror(content, w): return g(content, f'translate({f(w)} 0) scale(-1 1)')
def flipv(content, h): return g(content, f'translate(0 {f(h)}) scale(1 -1)')
def rot(content, a, cx, cy): return g(content, f'rotate({f(a)} {f(cx)} {f(cy)})')
def svg(w, h, content, bg=None):
    b = rr(0, 0, w, h, bg) if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{f(w)}" height="{f(h)}" viewBox="0 0 {f(w)} {f(h)}">{b}{content}</svg>'
def rng(seed): return random.Random(seed)
