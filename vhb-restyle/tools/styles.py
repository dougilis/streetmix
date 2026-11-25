"""Two rendering styles for the modern sprite set. The drawings in art_modern.py are written once against this small
API and come out as either a limited-ink print (bold silhouettes, overprint, halftone) or an inked marker sketch.

Why these two: 2026 illustration writing points the same way from several directions: flat shapes are still the base,
but with one layer of something tactile on top (halftone and print grain, limited palettes, visible linework, a
human hand), while glossy gradients and low-poly faceting read as dated."""
import random, zlib
from svgkit import *


def mix(c, d, t):
    a = [int(c[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(d[i:i + 2], 16) for i in (1, 3, 5)]
    return '#%02X%02X%02X' % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


PAPER = '#F7F4EC'


class Print:
    """Risograph-style: seven inks on warm paper, no outlines, shapes overprint each other, shade is a halftone screen."""
    name = 'print'; sky = (cobalt, aqua, '#8CCBD6'); dirt = midnight
    INK = {white: PAPER, body: PAPER, body2: '#E4E0D4', lgrey: '#E4E0D4', concrete: '#D6D2C6', gray: '#9A9CBB', dgrey: '#4A4E8A',
           charcoal: midnight, espresso: midnight, cobalt: aqua, plum: midnight, wood: papaya, leaf2: leaf, leaf3: teal,
           glass2: aqua, lamp: '#FFF1B8', tealT: '#CFE3DF', cobaltT: '#CFE6EB'}
    SURF = {'surface-bike-lane-green': leaf, 'surface-divider-median': '#D6D2C6', 'surface-asphalt': '#34387A', 'surface-bus-lane-red': berry,
            'surface-light-rail-grey': '#4A4E8A', 'surface-sidewalk-concrete': '#EAE6DA', 'surface-transit-platform-raised': '#EAE6DA'}

    def seed(self, name): self.rnd = random.Random(zlib.crc32(name.encode()))
    def col(self, c): return self.INK.get(c, c)
    def r(self, x, y, w, h, c, rad=0, o=None, ol=True): return rr(x, y, w, h, self.col(c), rad, o)
    def c(self, cx, cy, r, c, o=None, ol=True): return circ(cx, cy, r, self.col(c), o)
    def pg(self, pts, c, o=None, ol=True): return poly(pts, self.col(c), o)
    def p(self, d, c, o=None, ol=True): return path(d, self.col(c), o=o)
    def ln(self, x1, y1, x2, y2, c, sw): return line(x1, y1, x2, y2, self.col(c), sw)
    def stroke(self, d, c, sw): return path(d, 'none', self.col(c), sw)
    def ring(self, cx, cy, r, c, sw): return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{self.col(c)}" stroke-width="{f(sw)}"/>'
    def edge(self, x, y1, y2): return ''
    def glass(self, x, y, w, h, rad=8):
        return rr(x, y, w, h, midnight, rad) + poly([(x + w * .5, y + 2), (x + w * .78, y + 2), (x + w * .42, y + h - 2), (x + w * .14, y + h - 2)], aqua, .45)
    def glassp(self, d): return path(d, midnight)
    def tone(self, x, y, w, h, c=midnight, o=.2, toward='r'):
        """Halftone screen: dots growing toward one side."""
        step = 10
        while (w / step) * (h / step) > 140: step += 2
        s = ''; nx, ny = max(1, int(w / step)), max(1, int(h / step))
        for i in range(nx):
            for j in range(ny):
                t = (i + .5) / nx if toward == 'r' else (j + .5) / ny
                rad = step * .46 * t ** 1.3
                if rad > 1.1: s += circ(x + (i + .5) * w / nx + (step * .25 if j % 2 else 0) * (toward == 'r'), y + (j + .5) * h / ny, rad, c)
        return f'<g opacity="{o}">{s}</g>' if s else ''


class Sketch:
    """An urban designer's marker rendering: a slightly loose ink line that overshoots its corners, with flat marker
    colour dropped in a touch off-register behind it."""
    name = 'sketch'; ink = midnight; sw = 4; sky = ('#DCEEF2', '#EAF4F4', '#F7F4EC'); dirt = '#6E7085'
    SURF = {'surface-bike-lane-green': '#A9C487', 'surface-divider-median': '#E3E1D8', 'surface-asphalt': '#6E7085', 'surface-bus-lane-red': '#A8456A',
            'surface-light-rail-grey': '#8C8EA3', 'surface-sidewalk-concrete': '#F1EFE7', 'surface-transit-platform-raised': '#F1EFE7'}
    KEEP = {white: '#FFFFFF', body: '#FFFFFF', lamp: '#FFF1B8', midnight: '#3D4388', charcoal: '#3D4388', espresso: '#5A4A6A'}

    def seed(self, name): self.rnd = random.Random(zlib.crc32(name.encode()))
    def j(self, a=1.5): return self.rnd.uniform(-a, a)
    def col(self, c):
        if c in self.KEEP: return self.KEEP[c]
        return mix(c, '#FFFFFF', .3) if c.startswith('#') and len(c) == 7 else c
    def _off(self, size, ol): return (3, -3) if ol and size > 16 else (0, 0)
    def _ink(self, d): return path(d, 'none', self.ink, self.sw)
    def r(self, x, y, w, h, c, rad=0, o=None, ol=True):
        dx, dy = self._off(min(w, h), ol); s = rr(x + dx, y + dy, w, h, self.col(c), rad, o)
        if not ol: return s
        j = self.j
        if rad >= 6:
            q = min(rad, w / 2, h / 2)
            d = (f'M{f(x+q)} {f(y+j())}L{f(x+w-q)} {f(y+j())}Q{f(x+w)} {f(y)} {f(x+w+j())} {f(y+q)}L{f(x+w+j())} {f(y+h-q)}Q{f(x+w)} {f(y+h)} {f(x+w-q)} {f(y+h+j())}'
                 f'L{f(x+q)} {f(y+h+j())}Q{f(x)} {f(y+h)} {f(x+j())} {f(y+h-q)}L{f(x+j())} {f(y+q)}Q{f(x)} {f(y)} {f(x+q+2)} {f(y+j())}')
        else:
            v = min(5, min(w, h) * .18)
            d = (f'M{f(x-v)} {f(y+j())}L{f(x+w+v)} {f(y+j())}M{f(x+w+j())} {f(y-v)}L{f(x+w+j())} {f(y+h+v)}'
                 f'M{f(x+w+v)} {f(y+h+j())}L{f(x-v)} {f(y+h+j())}M{f(x+j())} {f(y+h+v)}L{f(x+j())} {f(y-v)}')
        return s + self._ink(d)
    def c(self, cx, cy, r, c, o=None, ol=True):
        dx, dy = self._off(r * 2, ol); s = circ(cx + dx, cy + dy, r, self.col(c), o)
        if not ol: return s
        return s + f'<ellipse cx="{f(cx+self.j())}" cy="{f(cy+self.j())}" rx="{f(r+self.j(1))}" ry="{f(r+self.j(1))}" fill="none" stroke="{self.ink}" stroke-width="{self.sw}"/>'
    def pg(self, pts, c, o=None, ol=True):
        dx, dy = self._off(30, ol); s = poly([(x + dx, y + dy) for x, y in pts], self.col(c), o)
        if not ol: return s
        d = ''
        for i, (x, y) in enumerate(pts):
            x2, y2 = pts[(i + 1) % len(pts)]; L = max(1, math.hypot(x2 - x, y2 - y)); ux, uy = (x2 - x) / L * 4, (y2 - y) / L * 4
            d += f'M{f(x-ux+self.j(1))} {f(y-uy+self.j(1))}L{f(x2+ux+self.j(1))} {f(y2+uy+self.j(1))}'
        return s + self._ink(d)
    def p(self, d, c, o=None, ol=True):
        s = g(path(d, self.col(c), o=o), 'translate(3 -3)') if ol else path(d, self.col(c), o=o)
        return s + (self._ink(d) if ol else '')
    def ln(self, x1, y1, x2, y2, c, sw): return line(x1 + self.j(1), y1, x2 + self.j(1), y2, self.ink if sw <= 8 else self.col(c), min(sw, 6) if sw <= 8 else sw)
    def stroke(self, d, c, sw): return path(d, 'none', self.ink, min(sw, 5))
    def ring(self, cx, cy, r, c, sw): return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{self.ink}" stroke-width="{self.sw}"/>'
    def edge(self, x, y1, y2): return line(x + self.j(1), y1, x + self.j(1), y2, self.ink, self.sw)
    def glass(self, x, y, w, h, rad=8):
        s = self.r(x, y, w, h, aquaT, rad)
        k = min(w, h) * .3
        return s + line(x + w * .3, y + h * .25 + k, x + w * .3 + k, y + h * .25, self.ink, 2.5, o=.6) + line(x + w * .45, y + h * .3 + k, x + w * .45 + k * .7, y + h * .3 + k * .3, self.ink, 2.5, o=.6)
    def glassp(self, d): return self.p(d, aquaT)
    def tone(self, x, y, w, h, c=None, o=.5, toward='r'):
        """Hatching: a few quick diagonal strokes on the shade side."""
        s = ''; n = max(2, min(6, int(w / 16)))
        for i in range(n):
            x0 = x + w * (.45 + .5 * i / n); L = min(h * .8, 60) * (.5 + .5 * i / n)
            s += line(x0, y + h * .15 + L, x0 + L * .35, y + h * .15, self.ink, 2.2)
        return f'<g opacity="{o}">{s}</g>'


STYLES = {'print': Print, 'sketch': Sketch}
