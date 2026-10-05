"""
Generates the six abstract art cards for the "How I can help" reel.
Placeholder art (license-free, on-palette). Swap any file in src/assets/skills/
for a real photo with the same name to replace it.

    python3 scripts/generate-skill-art.py
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os, math

W, H = 1000, 1250
OUT = os.path.join(os.path.dirname(__file__), '..', 'src', 'assets', 'skills')
rng = np.random.default_rng(7)

def hexrgb(h): h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], float)
PINE, MOSS, GRASS, VOLT, BONE, MIST = map(hexrgb, ['#0C1F14', '#1F5130', '#2C7A3F', '#C4F04D', '#F4F3EE', '#E6EEDC'])
EMBER, LILAC, TEAL, CHROME = map(hexrgb, ['#FF6A3D', '#B9A7FF', '#3FB8A4', '#D9DED6'])

yy, xx = np.mgrid[0:H, 0:W].astype(float)
u, v = xx / W, yy / H

def ramp(t, stops):
    """t in [0,1] → color via list of (pos, rgb)."""
    t = np.clip(t, 0, 1)[..., None]
    out = np.zeros(t.shape[:-1] + (3,))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        m = (t[..., 0] >= p0) & (t[..., 0] <= p1)
        k = ((t - p0) / max(p1 - p0, 1e-6))
        k = k * k * (3 - 2 * k)
        out[m] = (c0 + (c1 - c0) * k)[m]
    return out

def grain(img, amt=14):
    a = np.asarray(img).astype(float)
    n = rng.normal(0, amt, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))

def save(arr_or_img, name, amt=14):
    img = arr_or_img if isinstance(arr_or_img, Image.Image) else Image.fromarray(np.clip(arr_or_img, 0, 255).astype(np.uint8))
    grain(img.convert('RGB'), amt).save(os.path.join(OUT, name), quality=88)
    print('wrote', name)

# 1 · Brand Strategy — offset concentric rings, Bauhaus-cut
def brand_strategy():
    img = Image.new('RGB', (W, H), tuple(PINE.astype(int)))
    d = ImageDraw.Draw(img)
    cx, cy = W * 0.62, H * 0.58
    cols = [VOLT, MOSS, BONE, VOLT, PINE, VOLT]
    for i, r in enumerate([900, 720, 560, 420, 280, 150]):
        c = tuple(cols[i].astype(int))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    # quarter cut-outs
    d.pieslice([cx - 560, cy - 560, cx + 560, cy + 560], 180, 270, fill=tuple(PINE.astype(int)))
    d.pieslice([cx - 280, cy - 280, cx + 280, cy + 280], 0, 90, fill=tuple(BONE.astype(int)))
    d.ellipse([cx - 60, cy - 60, cx + 60, cy + 60], fill=tuple(EMBER.astype(int)))
    save(img, 'brand-strategy.jpg')

# 2 · Creative Direction — silky domain-warped liquid
def creative_direction():
    x, y = u * 3.2, v * 3.2
    for i in range(4):
        x, y = x + 0.45 * np.sin(1.7 * y + i * 1.3), y + 0.45 * np.cos(1.9 * x + i * 0.7)
    f = np.sin(x * 1.6 + y * 0.9)
    gy, gx = np.gradient(f)
    shade = np.clip(0.5 + 18 * (gx * -0.6 + gy * -0.8), 0, 1)
    t = 0.5 + 0.5 * f
    base = ramp(t, [(0, PINE), (0.35, MOSS), (0.62, EMBER), (0.8, VOLT), (1, BONE)])
    spec = np.clip((shade - 0.72) * 3.2, 0, 1)[..., None]
    col = base * (0.55 + 0.6 * shade[..., None]) + spec * 120
    save(col, 'creative-direction.jpg')

# 3 · Messaging & Story — giant cropped quotation mark
def messaging():
    img = Image.new('RGB', (W, H), tuple(EMBER.astype(int)))
    d = ImageDraw.Draw(img)
    fpath = os.path.join(os.path.dirname(__file__), '..', 'node_modules', '@fontsource', 'instrument-serif', 'files', 'instrument-serif-latin-400-italic.woff')
    f = ImageFont.truetype(fpath, 1500)
    d.text((-120, -220), '“', font=f, fill=tuple(PINE.astype(int)))
    small = ImageFont.truetype(fpath, 210)
    d.text((300, 560), 'say it', font=small, fill=tuple(BONE.astype(int)))
    d.text((380, 730), 'clearly.', font=small, fill=tuple(PINE.astype(int)))
    save(img, 'messaging-story.jpg', 12)

# 4 · Systems & Processes — modular Bauhaus tile grid
def systems():
    cols, rows = 4, 5
    cw, ch = W // cols, H // rows
    img = Image.new('RGB', (W, H), tuple(BONE.astype(int)))
    d = ImageDraw.Draw(img)
    pal = [PINE, MOSS, VOLT, BONE, EMBER, GRASS]
    r2 = np.random.default_rng(3)
    for j in range(rows):
        for i in range(cols):
            x0, y0 = i * cw, j * ch
            bg, fg = r2.choice(len(pal), 2, replace=False)
            if (i, j) == (2, 1): bg, fg = 4, 0
            d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=tuple(pal[bg].astype(int)))
            kind = r2.integers(0, 4); rot = r2.integers(0, 4) * 90
            box = [x0 - cw if rot in (90, 180) else x0, y0 - ch if rot in (180, 270) else y0,
                   x0 + cw if rot in (90, 180) else x0 + 2 * cw, y0 + ch if rot in (180, 270) else y0 + 2 * ch]
            c = tuple(pal[fg].astype(int))
            if kind == 0: d.pieslice(box, rot, rot + 90, fill=c)
            elif kind == 1: d.ellipse([x0 + cw * .15, y0 + ch * .15, x0 + cw * .85, y0 + ch * .85], fill=c)
            elif kind == 2: d.rectangle([x0, y0 + ch / 2, x0 + cw, y0 + ch], fill=c)
            else: d.chord([x0, y0, x0 + cw, y0 + ch], rot, rot + 180, fill=c)
    save(img, 'systems-processes.jpg', 10)

# 5 · Digital Experiences — aura gradient orbs
def digital():
    col = np.zeros((H, W, 3)) + PINE
    for (cx, cy, r, c, a) in [(0.25, 0.25, 0.55, LILAC, 1), (0.8, 0.45, 0.5, VOLT, 0.95), (0.35, 0.85, 0.6, TEAL, 0.9), (0.7, 0.95, 0.35, EMBER, 0.7)]:
        dist = np.sqrt(((u - cx) * 1.0) ** 2 + ((v - cy) * 0.8) ** 2) / r
        w = np.exp(-dist ** 2 * 2.2)[..., None] * a
        col = col * (1 - w) + c * w
    img = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(30))
    # glass panel
    d = ImageDraw.Draw(img, 'RGBA')
    d.rounded_rectangle([210, 330, 790, 980], 46, fill=(244, 243, 238, 46), outline=(244, 243, 238, 140), width=3)
    d.rounded_rectangle([270, 400, 560, 430], 15, fill=(244, 243, 238, 150))
    d.rounded_rectangle([270, 460, 700, 480], 10, fill=(244, 243, 238, 90))
    d.rounded_rectangle([270, 500, 640, 520], 10, fill=(244, 243, 238, 90))
    d.ellipse([560, 780, 720, 940], fill=(196, 240, 77, 230))
    save(img, 'digital-experiences.jpg', 16)

# 6 · Alignment & Collaboration — chaotic lines resolving to parallel
def alignment():
    s = 2
    img = Image.new('RGB', (W * s, H * s), tuple(MOSS.astype(int)))
    d = ImageDraw.Draw(img)
    r3 = np.random.default_rng(11)
    n = 46
    for k in range(n):
        y_end = (k + 0.5) / n * H * s
        y0 = r3.uniform(0, H * s); ph = r3.uniform(0, 6.28); amp = r3.uniform(120, 420) * s / 2
        pts = []
        for t in np.linspace(0, 1, 160):
            q = min(t / 0.62, 1.0); e = q * q * (3 - 2 * q)
            y = y0 * (1 - e) + y_end * e + amp * (1 - e) * math.sin(ph + t * 9)
            pts.append((t * W * s, y))
        c = VOLT if k % 5 else BONE
        d.line(pts, fill=tuple(c.astype(int)), width=int(3.2 * s))
    img = img.resize((W, H), Image.LANCZOS)
    save(img, 'alignment-collaboration.jpg', 12)

for fn in [brand_strategy, creative_direction, messaging, systems, digital, alignment]: fn()
