#!/usr/bin/env python3
"""Turn a PDF (brand guide, report, menu…) into page images for <Booklet>.

    python3 scripts/pdf-to-booklet.py <file.pdf> <id> [--split] [--dpi 130] [--maxw 1800]

Writes src/assets/booklets/<id>/01.webp, 02.webp, … (any old pages there are replaced).
--split  the PDF is exported as spreads: cut each page in half into two pages.
         (If spread 1 is [back cover | front cover], reorder by hand afterwards.)
Then add a row to the project's `gallery`:   - { booklet: <id>, title: "…", spreads: true }
Needs poppler (`pdftoppm`) and Pillow.
"""
import argparse, glob, os, subprocess, tempfile
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument('pdf'); ap.add_argument('id')
ap.add_argument('--split', action='store_true')
ap.add_argument('--dpi', type=int, default=130)
ap.add_argument('--maxw', type=int, default=1800)
a = ap.parse_args()

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(root, 'src', 'assets', 'booklets', a.id)
os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, '*.webp')):
    os.replace(f, f + '.old')  # keep the previous set aside rather than deleting it

with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(['pdftoppm', '-r', str(a.dpi), '-png', a.pdf, os.path.join(tmp, 'p')], check=True)
    pages = []
    for f in sorted(glob.glob(os.path.join(tmp, 'p-*.png')), key=lambda s: int(s.rsplit('-', 1)[1][:-4])):
        im = Image.open(f).convert('RGB')
        if a.split:
            w, h = im.size
            pages += [im.crop((0, 0, w // 2, h)), im.crop((w // 2, 0, w, h))]
        else:
            pages.append(im)
    for i, im in enumerate(pages, 1):
        if im.width > a.maxw:
            im = im.resize((a.maxw, round(im.height * a.maxw / im.width)), Image.LANCZOS)
        im.save(os.path.join(out, f'{i:02d}.webp'), 'WEBP', quality=82, method=6)
print(f'{len(pages)} pages → {out}')
