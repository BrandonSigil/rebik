"""
Generates the six abstract art cards for the "How I can help" reel (2026 theme).

One family: soft, grainy "liquid" gradients (domain-warped bands) in the site palette,
bright, friendly ribbons of volt, leaf green, soft ember and bone on a pale-volt base. Each card gets its own
seed, flow and colour emphasis, plus a simple pine line illustration across its middle band. The top is
lifted a little so the pine card titles stay readable.

Each card is two files in src/assets/skills/: <name>-bg.jpg (the gradient) and <name>-icon.svg
(the full-card illustration, inlined on top by SkillsReel so its parts can animate on hover).
Placeholder art (license-free, on-palette). Swap a -bg.jpg for a real photo with the same name, and
delete its -icon.svg if the photo shouldn't carry an illustration.

    python3 scripts/generate-skill-art.py
"""
import os
import numpy as np
from PIL import Image, ImageFilter

W, H = 1000, 1250
OUT = os.environ.get('SKILL_ART_OUT') or os.path.join(os.path.dirname(__file__), '..', 'src', 'assets', 'skills')


def hexrgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)


PINE, DEEP, MOSS, GRASS, VOLT, BONE, MIST, EMBER = map(
    hexrgb, ['#0C1F14', '#12301E', '#1F5130', '#2C7A3F', '#C4F04D', '#F4F3EE', '#E6EEDC', '#FF6A3D'])
# Bright, friendly mixes for the backgrounds
VOLT_SOFT, LEAF = hexrgb('#D5F77F'), hexrgb('#8FD14F')
PALE = VOLT + (BONE - VOLT) * 0.55     # pale volt
PEACH = EMBER + (BONE - EMBER) * 0.45  # soft ember

yy, xx = np.mgrid[0:H, 0:W].astype(float)
u, v = xx / W, yy / H


def ramp(t, stops):
    """t in [0,1] -> colour via [(pos, rgb), ...] with smoothstep between stops."""
    t = np.clip(t, 0, 1)
    out = np.zeros(t.shape + (3,))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        m = (t >= p0) & (t <= p1)
        k = ((t - p0) / max(p1 - p0, 1e-6))[..., None]
        k = k * k * (3 - 2 * k)
        out[m] = (c0 + (c1 - c0) * k)[m]
    return out


def mix(a, b, k):
    return a + (b - a) * k


def liquid(name, seed, stops, *, scale=3.0, warp=0.45, iters=4, freq=(1.6, 0.9),
           blur=16, sheen=0.3, grain_amt=7, lift_top=0.3, art=None):
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 6.28, 8)
    x, y = u * scale, v * scale * (H / W)
    for i in range(iters):
        x, y = (x + warp * np.sin(1.7 * y + ph[i]),
                y + warp * np.cos(1.9 * x + ph[i + 4]))
    f = np.sin(x * freq[0] + y * freq[1] + ph[0])
    t = 0.5 + 0.5 * f
    col = ramp(t, stops)

    # Soft lighting from the field's slope gives a silky, folded look (kept gentle)
    gy, gx = np.gradient(f)
    shade = np.clip(0.5 + 14 * (gx * -0.6 + gy * -0.8), 0, 1)[..., None]
    col = col * (0.97 + sheen * (shade - 0.5) * 2 * 0.4)

    # Lift the top slightly toward pale volt so the pine title always has a calm backdrop
    top = np.clip(1 - v / 0.45, 0, 1)[..., None] ** 1.4
    col = mix(col, PALE, top * lift_top)

    img = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(img).astype(float)
    n = rng.normal(0, grain_amt, a.shape[:2])[..., None]
    Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8)).save(os.path.join(OUT, f'{name}-bg.jpg'), quality=88)
    print('wrote', f'{name}-bg.jpg')
    # The illustration is its own inline SVG (same 1000x1250 space) so its parts can animate on hover
    if art:
        write_icon(name, art)


# ---------- Line illustrations (SVG) ----------
# Each illustration is written as an SVG in the card's own 1000x1250 space (<name>-icon.svg) and
# inlined by SkillsReel, so its parts can animate on hover. Strokes sit on layers ("soft", "line",
# "accent", "white"); each layer is one <g> with a single opacity, so crossing strokes never double
# up. Geometry is scaled by K around the card centre (CX, CY); stroke widths are not scaled.
K = 0.7                            # overall illustration scale
CX, CY = W / 2, H * 0.52           # centre of the band between the title and the tags
STROKE = 14
LAYERS = ('soft', 'line', 'accent', 'white')
OPACITY = {'soft': 0.45, 'line': 0.92, 'accent': 1.0, 'white': 1.0}
COLOUR = {'soft': '#0C1F14', 'line': '#0C1F14', 'accent': '#0C1F14', 'white': '#FFFFFF'}


def f(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


def d_of(pts, closed=False):
    return 'M' + ' L'.join(f'{f(x)},{f(y)}' for x, y in pts) + (' Z' if closed else '')


class Canvas:
    """Collects SVG elements per layer.
    cls / style / extra  tag an element for the CSS hover animations in SkillsReel.
    group(cls, origin)   wraps everything drawn inside it (on every layer) in <g class=...>, scaled about `origin`.
    morph / grow_to      add SMIL <animate> pairs (data-morph="in" | "out") that SkillsReel's script starts on hover / leave."""

    SPLINE = 'calcMode="spline" keyTimes="0;1" keySplines="0.45 0 0.2 1" fill="freeze" begin="indefinite"'

    def __init__(self):
        self.items = {k: [] for k in LAYERS}   # (group, markup)
        self.erasers = {k: [] for k in LAYERS}
        self.groups = {}
        self.cur = None
        self.defs = []                         # extra <defs> content (clip paths); ids carry {uid}
        self.name = ''

    @staticmethod
    def P(x, y, k=K):  # design coords -> card coords, scaled about the centre
        return CX + (x - CX) * k, CY + (y - CY) * k

    def pts(self, points, k=K):
        return [self.P(x, y, k) for x, y in points]

    @staticmethod
    def _a(cls=None, style=None, extra=None):
        return (f' class="{cls}"' if cls else '') + (f' style="{style}"' if style else '') + (f' {extra}' if extra else '')

    def _add(self, layer, markup):
        self.items[layer].append((self.cur, markup))

    class _Group:
        def __init__(self, c, key):
            self.c, self.key = c, key

        def __enter__(self):
            self.c.cur = self.key

        def __exit__(self, *exc):
            self.c.cur = None

    def group(self, cls, origin):
        x, y = self.P(*origin)
        self.groups[cls] = f'<g class="{cls}" style="transform-box: view-box; transform-origin: {f(x)}px {f(y)}px">'
        return Canvas._Group(self, cls)

    def _anims(self, attr, a, b, dur_in, dur_out=None, delay=0):
        dur_out = dur_out or dur_in
        return (f'<animate data-morph="in" data-delay="{delay}" attributeName="{attr}" values="{a};{b}" dur="{dur_in}s" {self.SPLINE}/>'
                f'<animate data-morph="out" attributeName="{attr}" values="{b};{a}" dur="{dur_out}s" {self.SPLINE}/>')

    def stroke(self, layer, points, closed=False, width=STROKE, k=K, cls=None, style=None, extra=None, morph=None, dur=0.65):
        d = d_of(self.pts(points, k), closed)
        attrs = f'd="{d}" fill="none" stroke-width="{f(width)}" stroke-linecap="round" stroke-linejoin="round"' + self._a(cls, style, extra)
        if morph is not None:
            d2 = d_of(self.pts(morph, k), closed)
            self._add(layer, f'<path {attrs}>{self._anims("d", d, d2, dur, 0.5)}</path>')
        else:
            self._add(layer, f'<path {attrs}/>')

    def fill(self, layer, points, k=K, cls=None, style=None):
        self._add(layer, f'<path d="{d_of(self.pts(points, k), True)}" stroke="none"' + self._a(cls, style) + '/>')

    def clip(self, key, points, morph=None, dur=0.65, k=K):
        """A clip path (closed shape, optionally morphing with the same SMIL timing). Returns its url()."""
        cid = f'ic-clip-{key}-{{uid}}'
        d = d_of(self.pts(points, k), True)
        anim = self._anims('d', d, d_of(self.pts(morph, k), True), dur, 0.5) if morph is not None else ''
        self.defs.append(f'<clipPath id="{cid}"><path d="{d}">{anim}</path></clipPath>')
        return f'url(#{cid})'

    def erase(self, layers, points, grow=0, k=K):
        """Hide anything on `layers` under this shape (an SVG mask), optionally grown by `grow`."""
        for layer in layers:
            self.erasers[layer].append((d_of(self.pts(points, k), True), grow))

    def circle(self, layer, cx, cy, r, fill=False, width=STROKE, cls=None, style=None, extra=None):
        x, y = self.P(cx, cy)
        paint = 'stroke="none"' if fill else f'fill="none" stroke-width="{f(width)}"'
        self._add(layer, f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r * K)}" {paint}' + self._a(cls, style, extra) + '/>')

    def bar(self, layer, x0, y0, x1, y1, cls=None, style=None, grow_to=None, delay=0):
        """Rounded bar. grow_to=(x0, y0, x1, y1, r) adds a SMIL grow into that rectangle on hover."""
        (a, b), (c, d) = self.P(x0, y0), self.P(x1, y1)
        geo = dict(x=a, y=b, width=c - a, height=d - b, rx=(d - b) / 2)
        attrs = ' '.join(f'{k}="{f(v)}"' for k, v in geo.items()) + ' stroke="none"' + self._a(cls, style)
        if grow_to:
            (A, B), (C, D) = self.P(*grow_to[:2]), self.P(*grow_to[2:4])
            to = dict(x=A, y=B, width=C - A, height=D - B, rx=grow_to[4] * K)
            anims = ''.join(self._anims(k, f(geo[k]), f(to[k]), 0.27, 0.35, delay) for k in geo)
            self._add(layer, f'<rect {attrs}>{anims}</rect>')
        else:
            self._add(layer, f'<rect {attrs}/>')

    def svg(self, name):
        out = [f'<svg class="ic ic--{name}" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" '
               f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">']
        defs, body = list(self.defs), []
        for layer in LAYERS:
            if not self.items[layer]:
                continue
            mask = ''
            if self.erasers[layer]:
                mid = f'ic-{name}-{layer}-{{uid}}'
                cut = ''.join(f'<path d="{d}" fill="#000" stroke="#000" stroke-width="{f(g)}" stroke-linejoin="round"/>'
                              for d, g in self.erasers[layer])
                defs.append(f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
                            f'<rect width="{W}" height="{H}" fill="#fff"/>{cut}</mask>')
                mask = f' mask="url(#{mid})"'
            # wrap consecutive items of the same group
            parts, open_g = [], None
            for g, m in self.items[layer]:
                if g != open_g:
                    if open_g:
                        parts.append('</g>')
                    if g:
                        parts.append(self.groups[g])
                    open_g = g
                parts.append(m)
            if open_g:
                parts.append('</g>')
            col = COLOUR[layer]
            body.append(f'<g class="ic-layer ic-layer--{layer}" opacity="{OPACITY[layer]}" fill="{col}" stroke="{col}"{mask}>'
                        + ''.join(parts) + '</g>')
        if defs:
            out.append('<defs>' + ''.join(defs) + '</defs>')
        out.append('<g class="ic-body">' + ''.join(body) + '</g></svg>')
        return '\n'.join(out) + '\n'


def write_icon(name, painter):
    c = Canvas()
    painter(c)
    path = os.path.join(OUT, f'{name}-icon.svg')
    with open(path, 'w') as fh:
        fh.write(c.svg(name))
    print('wrote', f'{name}-icon.svg')


def arc_pts(cx, cy, r, a0, a1, n=24):
    return [(cx + r * np.cos(np.radians(a)), cy + r * np.sin(np.radians(a))) for a in np.linspace(a0, a1, n)]


def rrect(x0, y0, x1, y1, r, tail=None):
    """Closed rounded-rect outline as one path. tail=(xa, xb, tip_x, tip_y) cuts a speech tail into the bottom edge."""
    p = []
    p += arc_pts(x0 + r, y0 + r, r, 180, 270)
    p += arc_pts(x1 - r, y0 + r, r, 270, 360)
    p += arc_pts(x1 - r, y1 - r, r, 0, 90)
    if tail:
        xa, xb, tx, ty = tail          # bottom edge runs right -> left
        p += [(max(xa, xb), y1), (tx, ty), (min(xa, xb), y1)]
    p += arc_pts(x0 + r, y1 - r, r, 90, 180)
    return p


def art_alignment(c):
    """A few thick lines start scattered on the left and come together into parallel lines, edge to edge."""
    r = np.random.default_rng(11)
    n, gap = 5, 46 * K
    starts = CY + (np.linspace(H * 0.38, H * 0.7, n) - H * 0.54) * K
    r.shuffle(starts)
    for k in range(n):
        y_end = CY + (k - (n - 1) / 2) * gap
        y0, ph, amp = starts[k], r.uniform(0, 6.28), r.uniform(30, 75) * K
        pts, straight = [], []
        for t in np.linspace(0, 1, 90):
            q = min(t / 0.62, 1.0)
            e = q * q * (3 - 2 * q)
            x = -30 + t * (W + 60)
            pts.append((x, y0 * (1 - e) + y_end * e + amp * (1 - e) * np.sin(ph + t * 7)))
            straight.append((x, y_end))
        # full width (not scaled); on hover every line eases straight (SMIL morph) before the icon fades
        c.stroke('soft' if k == 2 else 'line', pts, k=1, width=18, morph=straight)


def art_brand(c):
    """Target rings. On hover each ring unwinds from a full circle to a dot, staggered (CSS dash offset)."""
    c.circle('line', CX, CY, 330, cls='ic-ring', style='--n:0', extra='pathLength="1"')
    c.stroke('accent', arc_pts(CX, CY, 245, 180, 270, 30), cls='ic-ring ic-ring--rev', style='--n:1', extra='pathLength="1"')
    c.stroke('soft', arc_pts(CX, CY, 245, 270, 540, 60), cls='ic-ring', style='--n:2', extra='pathLength="1"')
    c.circle('line', CX, CY, 160, cls='ic-ring ic-ring--rev', style='--n:3', extra='pathLength="1"')
    c.circle('soft', CX, CY, 80, cls='ic-ring', style='--n:4', extra='pathLength="1"')
    c.circle('accent', CX, CY, 28, fill=True, cls='ic-dot')


def art_creative(c):
    """An eye: one closed almond outline, iris ring and pupil.
    On hover it blinks shut like a real eye: the upper lid sweeps down to meet the lower one (SMIL morph of the
    outline), and the iris and pupil are clipped by the same moving lid shape instead of squashing."""
    w, h = 330, 175
    ts = np.linspace(0, 1, 90)
    lid = lambda hh: [(CX - w + 2 * w * t, CY + hh * np.sin(np.pi * t)) for t in ts]
    low = lambda hh: [(CX + w - 2 * w * t, CY + hh * np.sin(np.pi * t)) for t in ts][1:-1]
    open_eye = lid(-h) + low(h)
    shut_eye = lid(h * 0.32) + low(h * 0.36)      # lids meet in a soft downward curve
    c.stroke('line', open_eye, closed=True, morph=shut_eye, dur=0.4)
    clip = c.clip('eye', open_eye, morph=shut_eye, dur=0.4)
    c.circle('soft', CX, CY, 92, extra=f'clip-path="{clip}"')
    c.circle('accent', CX, CY, 48, fill=True, extra=f'clip-path="{clip}"')


def art_messaging(c):
    """Two speech bubbles; the front one is see-through but hides the back one where they overlap.
    On hover the back bubble types two lines, then both bubbles shrink away, front first."""
    bx0, by0 = CX - 300, CY - 215
    back = rrect(bx0, by0, bx0 + 380, by0 + 250, 60, tail=(bx0 + 150, bx0 + 80, bx0 + 55, by0 + 330))
    fx0, fy0 = CX - 60, CY - 25
    front = rrect(fx0, fy0, fx0 + 360, fy0 + 235, 60, tail=(fx0 + 300, fx0 + 230, fx0 + 305, fy0 + 310))
    with c.group('ic-b1', (bx0 + 190, by0 + 125)):
        c.stroke('line', back, closed=True)
        c.bar('accent', bx0 + 60, by0 + 62, bx0 + 300, by0 + 86, cls='ic-type', style='--n:0')
        c.bar('accent', bx0 + 60, by0 + 122, bx0 + 210, by0 + 146, cls='ic-type', style='--n:1')
    c.erase(['line'], front, grow=STROKE * 3)   # clear background: the back bubble stops at the front one
    with c.group('ic-b2', (fx0 + 180, fy0 + 118)):
        c.stroke('accent', front, closed=True)
        c.bar('accent', fx0 + 60, fy0 + 72, fx0 + 290, fy0 + 96)
        c.bar('accent', fx0 + 60, fy0 + 132, fx0 + 230, fy0 + 156)


def art_systems(c):
    """A 3x3 modular grid, connected, with one module highlighted.
    On hover the empty modules fill one by one (a snake ending next to the solid one), which then pops."""
    size, gap = 150, 60
    step = size + gap
    ox, oy = CX - step - size / 2, CY - step - size / 2
    for j in range(3):
        for i in range(3):
            x, y = ox + i * step, oy + j * step
            if i < 2:
                c.stroke('soft', [(x + size, y + size / 2), (x + step, y + size / 2)], width=10)
            if j < 2:
                c.stroke('soft', [(x + size / 2, y + size), (x + size / 2, y + step)], width=10)
    order = [(0, 2), (1, 2), (2, 2), (2, 1), (1, 1), (0, 1), (0, 0), (1, 0)]
    for j in range(3):
        for i in range(3):
            x, y = ox + i * step, oy + j * step
            box = rrect(x, y, x + size, y + size, 30)
            c.erase(['soft'], box)
            if (i, j) == (2, 0):
                c.fill('accent', box, cls='ic-target')
            else:
                c.stroke('line', box, closed=True)
                c.fill('accent', box, cls='ic-fill', style=f'--n:{order.index((i, j))}')


def art_digital(c):
    """A browser window with content bars, a button and a pointer.
    On hover the pointer glides to the button and clicks; the button then grows to fill the window (SMIL)."""
    x0, y0, x1, y1 = CX - 320, CY - 240, CX + 320, CY + 230
    c.stroke('line', rrect(x0, y0, x1, y1, 40), closed=True)
    c.stroke('line', [(x0, y0 + 80), (x1, y0 + 80)])
    for i in range(3):
        c.circle('line', x0 + 50 + i * 40, y0 + 40, 11, fill=True)
    for i, (ww, layer) in enumerate([(330, 'line'), (450, 'soft'), (390, 'soft')]):
        c.bar(layer, x0 + 60, y0 + 140 + i * 62, x0 + 60 + ww, y0 + 168 + i * 62)
    px, py = x1 - 170, y1 - 150
    tx, ty = c.P(px, py)
    dx, dy = (x0 + 205 - px) * K, (y1 - 98 - py) * K       # pointer tip -> onto the button
    c.fill('line', [(px, py), (px, py + 120), (px + 32, py + 88), (px + 58, py + 140),
                    (px + 78, py + 130), (px + 52, py + 80), (px + 95, py + 78)],
           cls='ic-cursor', style=f'--dx:{f(dx)}px; --dy:{f(dy)}px; transform-box: view-box; transform-origin: {f(tx)}px {f(ty)}px')
    c.bar('accent', x0 + 60, y1 - 120, x0 + 280, y1 - 60, grow_to=(x0, y0, x1, y1, 40), delay=0.38)



# Bright, friendly ribbons on a pale mist/volt base; blur + low grain keep the waves soft.
liquid('brand-strategy', 21, [(0, PALE), (0.35, PALE), (0.55, VOLT), (0.72, LEAF), (0.86, VOLT_SOFT), (1, VOLT_SOFT)],
       scale=2.4, warp=0.5, freq=(1.2, 1.4), art=art_brand)
liquid('creative-direction', 7, [(0, PALE), (0.35, VOLT_SOFT), (0.55, VOLT), (0.68, PEACH), (0.8, BONE), (0.9, LEAF), (1, VOLT_SOFT)],
       scale=3.2, warp=0.45, freq=(1.6, 0.9), art=art_creative)
liquid('messaging-story', 33, [(0, PALE), (0.38, VOLT_SOFT), (0.58, PEACH), (0.74, mix(EMBER, PEACH, .5)), (0.88, VOLT), (1, VOLT_SOFT)],
       scale=2.8, warp=0.55, freq=(0.8, 1.7), art=art_messaging)
liquid('systems-processes', 4, [(0, PALE), (0.38, VOLT_SOFT), (0.58, LEAF), (0.76, VOLT), (0.88, BONE), (1, PALE)],
       scale=3.6, warp=0.35, iters=3, freq=(1.9, 0.5), art=art_systems)
liquid('digital-experiences', 58, [(0, VOLT_SOFT), (0.36, PALE), (0.58, VOLT), (0.78, LEAF), (0.9, BONE), (1, VOLT_SOFT)],
       scale=2.6, warp=0.6, freq=(1.3, 1.1), art=art_digital)
liquid('alignment-collaboration', 90, [(0, PALE), (0.4, VOLT_SOFT), (0.6, LEAF), (0.72, PEACH), (0.84, VOLT), (0.94, BONE), (1, VOLT_SOFT)],
       scale=3.0, warp=0.4, freq=(2.1, 0.6), art=art_alignment)
