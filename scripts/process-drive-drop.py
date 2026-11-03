#!/usr/bin/env python3
"""Turn Peter's Drive drop (incoming/Rebik Site) into site assets.
Writes optimised WebP to src/assets/projects/<slug>/, MP4 to public/video/<slug>/,
booklet pages to src/assets/booklets/<id>/, and a manifest to incoming/_renders/manifest.json.
Usage: python3 process_assets.py <repo_root> [only_slug]
"""
import json, os, re, subprocess, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

ROOT = sys.argv[1]
ONLY = sys.argv[2] if len(sys.argv) > 2 else None
DROP = os.path.join(ROOT, 'incoming', 'Rebik Site', 'Project Pages')
OUT_IMG = os.path.join(ROOT, 'src', 'assets', 'projects')
OUT_VID = os.path.join(ROOT, 'public', 'video')
OUT_BK = os.path.join(ROOT, 'src', 'assets', 'booklets')
TMP = os.path.join(ROOT, 'incoming', '_renders', 'tmp')
os.makedirs(TMP, exist_ok=True)
MAXW = 2000
FORCE = os.environ.get('FORCE') == '1'
CROPS = json.load(open(os.path.join(ROOT, 'incoming', '_renders', 'idml_crops.json'))) if os.path.exists(os.path.join(ROOT, 'incoming', '_renders', 'idml_crops.json')) else {}

# Project folder, layout PDF, page height (pt). Rows: list of rows; a row is
#  ('img', [item, ...])                      1–3 tiles side by side
#  ('cols', [[item, ...], [item, ...]], [w1, w2])   mosaic: columns of stacked tiles, relative widths
#  ('heading', title, text)
#  ('booklet', id, title, spreads)
# item = (source, w, h)              source = file in Links/, w×h = the frame in the layout (pt)
#      | ('crop', x, y, w, h)        cut from the layout PDF (composite tiles built in InDesign)
P = {}
P['annual-report'] = dict(folder='Pierce Transit Annual Report', pdf='Pierce Transit Annual Report.pdf', H=3200, rows=[
    ('img', [('DSC_7190.jpg', 418, 220)]),
    ('img', [('Annual Report 1.png', 418, 220)]),
    ('img', [('Annual Report 3.png', 206, 200), ('Annual Report 2.png', 206, 200)]),
    ('img', [('Annual Report 4.png', 418, 220)]),
    ('cols', [[('2024 Annual Report (social media ad).jpg', 198, 248)],
              [('2024 Annual Report - McClatchy Ads (320x50).jpg', 212, 33),
               ('2024 Annual Report - McClatchy Ads (728x90).jpg', 212, 26),
               ('2024 Annual Report - McClatchy Ads (300x250).jpg', 212, 177)]], [198, 212]),
    ('booklet', 'pt-annual-report-2024', '2024 Annual Report', True),
])
P['brand-refresh'] = dict(folder='Pierce Transit Brand Referesh', pdf='Project Page (Pierce Transit Brand Referesh).pdf', H=5000, rows=[
    ('booklet', 'pt-brand-guide', 'Brand Guide (Sept 2025)', False),
    ('img', [('crop', -54, -1050, 206, 248, 'asset-library'), ('crop', 158, -1049, 206, 248, 'icon-set')]),
    ('img', [('crop', -54, -788, 418, 454, 'presentation-templates')]),
    ('img', [('crop', -54, -321, 206, 160, 'department-lockups'), ('Certificate Template.png', 206, 160)]),
    ('img', [('image_f479d0f8.jpg', 417, 317)]),
    ('heading', 'Design examples', 'See some examples of designs done using the refreshed brand guidelines, assets, and templates.'),
    ('img', [('image_3d788674.jpg', 417, 212)]),
    ('img', [('image_aa905368.jpg', 417, 194)]),
    ('img', [('image_1934822.jpg', 202, 271), ('image_5bff3713.jpg', 202, 271)]),
    ('img', [('crop', -54, 990, 417, 194, 'sponsored-web-content')]),
    ('img', [('Business Summit 2024 Strickland 04.jpg', 417, 248)]),
    ('img', [('image_446ff6cf (1).jpg', 417, 413)]),
    ('img', [('image_72d80dfd.jpg', 417, 413)]),
])
P['gig-harbor-connector'] = dict(folder='Pierce Transit Connector', pdf='Pierce Transit Connector.pdf', H=3200, rows=[
    ('img', [('Gig Harbor Connector Magazine Ad FINAL.jpg', 418, 220)]),
    ('img', [('Background Pattern - RGB (gradient icons)_Horizontal Gradient copy.jpg', 418, 220)]),
    ('img', [('Connector (logo on white alt).jpg', 206, 170), ('Connector (logo on blue).png', 206, 170)]),
    ('img', [('Connector (vehicle drivers).jpg', 418, 220)]),
    ('img', [('Connector (vehicle passenger).jpg', 418, 220)]),
    ('img', [('Gig Harbor Waterfront Connector Stop (1).png', 418, 235)]),
    ('img', [('Gig Harbor Waterfront Connector Ad (1).png', 418, 235)]),
    ('img', [('Gig Harbor Waterfront Connector Brochure.png', 418, 313)]),
])
P['perception-campaign'] = dict(folder='Pierce Transit Perception Campaign', pdf='Project Page (perception).pdf', H=3200, rows=[
    ('img', [('Public Perception - Billboard (mockup).png', 418, 255)]),
    ('img', [('26-City-Billboard-Mockups.png', 206, 160), ('01. Urban Bus Stop Poster Mockup.png', 206, 160)]),
    ('img', [('crop', -54, -1091, 418, 263, 'transit-king')]),
    ('cols', [[('Perception - Digital Ads (160x600).jpg', 96, 359)], [('Perception - Digital Ads (160x600)2.jpg', 96, 359)],
              [('Perception - Digital Ads (300x250).jpg', 210, 175), ('Perception - Digital Ads (300x250)2.jpg', 210, 175)]], [96, 96, 210]),
    ('img', [('Perception - Digital Ads (728x90).jpg', 418, 52)]),
    ('img', [('Perception - Digital Ads (728x90)2.jpg', 418, 52)]),
    ('img', [('crop', -54, -337, 418, 576, 'landing-page')]),
    ('img', [('Perception Wireframe2.jpg', 206, 602), ('Perception Wireframe3.jpg', 206, 602)]),
])
P['recruitment-campaign'] = dict(folder='Pierce Transit Recruitment Campaign', pdf='Pierce Transit Recruitment Campaign.pdf', H=3200, rows=[
    ('img', [('Semi Driving by Recruitment Billboard.jpg', 418, 220)]),
    ('img', [('Photo Sep 15, 12 41 16 PM copy.jpg', 418, 220)]),
    ('img', [('Recruitment (day ad shelter).jpg', 206, 200), ('Recruitment (night ad shelter).jpg', 206, 200)]),
    ('img', [('Recruitment Bus Ad.png', 418, 220)]),
    ('img', [('Brochure (cover).png', 206, 200), ('Recruitment (postcard).png', 206, 200)]),
    ('img', [('image[23].jpg', 418, 220)]),
    ('cols', [[('Recruitment - Digital Ads (160x600).jpg', 96, 359)], [('Recruitment - Digital Ads (160x600)2.jpg', 96, 359)],
              [('Recruitment - Digital Ads (300x250).jpg', 210, 175), ('Recruitment - Digital Ads (300x250)2.jpg', 210, 175)]], [96, 96, 210]),
    ('img', [('Recruitment - Digital Ads (728x90).jpg', 418, 52)]),
    ('img', [('Recruitment - Digital Ads (728x90)2.jpg', 418, 52)]),
])
logos = ['45 Year Anniversary', '2045 Long Range Plan', 'Connector', 'Hardship Assistance Response Team', 'Beautiful Day Cleaning_icon',
         'Beautiful Day Cleaning', 'Bend Retreat_abstract', 'Bend Retreat_landscape', 'Brickhouse Deli', 'Cause Brokers Non-Profit Real Estate',
         'CORE Housing PAC', 'DPC Students', 'Heart House_concept', 'John Moiola Ranches_icon', 'John Moiola Ranches', 'Known Supply Co',
         'Landscape_concept', 'Logistics of the Desert', 'P Roads_concept', 'Paddle Gang Club_dogs', 'Paddle Gang Club', 'Panda Key Real Estate',
         'Rebik Design_icon', 'Reeves Garden Design', 'Smith Kandal Insurance and Real Estate', 'VanMeier Logistics', 'Windsor Christian',
         'C_concept', 'D_concept', 'F_concept']
P['select-logos'] = dict(folder='Select Logos', pdf='Logos (all).pdf', H=5000, rows=[
    ('img', [(f'Peter Rebik - Select Logos (color)_{a}.jpg', 205, 162), (f'Peter Rebik - Select Logos (color)_{b}.jpg', 205, 162)])
    for a, b in zip(logos[0::2], logos[1::2])
])
P['smith-kandal-rebrand'] = dict(folder='Smith Kandal Rebrand', pdf='Smith Kandal Rebrand.pdf', H=4000, rows=[
    ('img', [('Smith-Kandal (hero image).png', 418, 220)]),
    ('img', [('Smith-Kandal logo (before-after).jpg', 418, 302)]),
    ('img', [('Smith Kandal Logo (rough drafts - all).jpg', 418, 250)]),
    ('img', [('Smith-Kandal - Final Options.jpg', 418, 295)]),
    ('img', [('Smith-Kandal (logo symbols).png', 418, 302)]),
    ('img', [('Smith-Kandal badge (color).jpg', 206, 160), ('Smith-Kandal logo (vertical).jpg', 206, 160)]),
    ('img', [('Smith-Kandal-Logo-animated.gif', 418, 182)]),
    ('img', [('Smith Kandal 3.png', 418, 340)]),
    ('img', [('Smith Kandal Trucker Hat (embroidered badge).jpg', 418, 283)]),
    ('img', [('Smith-Kandal logo (85 lockup).jpg', 206, 160), ('Smith-Kandal logo (85 billboard).jpg', 206, 160)]),
    ('img', [('2. Business Cards Mock-Up.png', 206, 160), ('Smith-Kandal (app icons).png', 206, 160)]),
    ('img', [('Smith Kandal Website.png', 418, 253)]),
    ('img', [('01. Sign Board Mockup.png', 206, 160), ('Smith Kandal Door Logo.png', 206, 160)]),
    ('img', [('Full Length.mp4', 418, 235)]),
])
P['windsor-christian-rebrand'] = dict(folder='Windsor Christian Rebrand', pdf='Windsor Christian Rebrand.pdf', H=6000, rows=[
    ('img', [('Windsor Christian 1.png', 418, 238)]),
    ('img', [('Windsor Logo (before and after).jpg', 418, 352)]),
    ('img', [('Windsor Logo - Roughs (all).png', 418, 238)]),
    ('img', [('Windsor Christian 4.png', 418, 323)]),
    ('img', [('Windsor Christian (church logo white).jpg', 206, 200), ('Windsor Christian (church logo blue).jpg', 206, 200)]),
    ('img', [('Windsor Christian (church badge blue).jpg', 206, 200), ('Windsor Christian (academy logo white).jpg', 206, 200)]),
    ('img', [('Windsor Christian Church Logos DIGITAL-30.jpg', 418, 152)]),
    ('img', [('Windsor Christian Church Logos DIGITAL-31.jpg', 418, 220)]),
    ('img', [('Windsor Academy Uniform (concept).jpg', 206, 200), ('Windsor Church Hat (concept).jpg', 206, 200)]),
    ('cols', [[('Portfolio Presentation (WCC Home Original)-03.png', 206, 601), ('Onboarding Task Flow.png', 206, 279)],
              [('crop', 158, -741, 206, 885, 'wireframe-and-nav')]], [206, 206]),
    ('img', [('Event Search User Flow.png', 418, 223)]),
    ('img', [('Windsor-website-scroll.gif', 418, 279)]),
    ('img', [('Man Holding iPhone Mockup alt.png', 418, 241)]),
    ('img', [('Windsor Christian 8.png', 418, 241)]),
    ('img', [('Windsor Christian 9.png', 418, 241)]),
])

K = 'Kitchen Sink (images)'
def ks(sub, f, w, h): return (f'{sub}/{f}', w, h)
P['kitchen-sink'] = dict(folder=K, links='', pdf=None, H=0, rows=[
    ('heading', 'Cause Brokers', 'Brand identity and website for a non-profit real estate brokerage.'),
    ('img', [ks('Cause Brokers', 'Cause-Brokers-website-scroll.gif', 2560, 1706)]),
    ('img', [ks('Cause Brokers', 'Peter Rebik Portfolio (Cause Brokers)_Brand Pattern.jpg', 2728, 957)]),
    ('img', [ks('Cause Brokers', 'Peter Rebik Portfolio (Cause Brokers)_Business Cards (front and back).jpg', 2728, 1333)]),
    ('img', [ks('Cause Brokers', 'Peter Rebik Portfolio (Cause Brokers)_Website (mobile).jpg', 5455, 2664)]),
    ('heading', 'Taylor & Taylor Farms', 'Identity, print and website.'),
    ('img', [ks('Taylor & Taylor Farms', 'Taylor-and-Taylor-website-scroll.gif', 2560, 1706)]),
    ('img', [ks('Taylor & Taylor Farms', 'Peter Rebik Portfolio (Taylor & Taylor)_Business Cards (front and back).jpg', 2728, 1333)]),
    ('img', [ks('Taylor & Taylor Farms', 'Peter Rebik Portfolio (Taylor & Taylor)_Website (mobile).jpg', 5455, 2664)]),
    ('heading', 'Coastline Family Farms', 'Packaging refresh and trade advertising.'),
    ('img', [ks('Coastline Family Farms', '1. Coastline Label (before and after)-15.png', 2106, 2105),
             ks('Coastline Family Farms', '2. Coastline Label-Variety-03.jpg', 1801, 1800),
             ks('Coastline Family Farms', 'Coastline Family Farms Red Onions.png', 1244, 1264)]),
    ('img', [ks('Coastline Family Farms', 'Western Grower Magazine Onion Feature and Family Farm Ad.png', 1672, 941)]),
    ('heading', 'Beautiful Day Cleaning', 'Brand, vehicle, print and social.'),
    ('img', [ks('Beautiful Day', 'Beautiful Day - Van (back).png', 4500, 3000)]),
    ('img', [ks('Beautiful Day', 'Brading Social Posts-30.png', 1501, 1500), ks('Misc', 'BD New Website_Instagram.png', 4501, 4501),
             ks('Beautiful Day', 'Business Cards (FALLING) copy.png', 2200, 2600)]),
    ('heading', 'Moundsville Baptist Church', 'Sermon series graphics, social and a website wireframe.'),
    ('cols', [[ks('Moundsville Baptist Church', 'MBC A Gospel People-01.png', 8000, 4500),
               ks('Moundsville Baptist Church', 'MBC Advent 2022-01.png', 8001, 4501),
               ks('Moundsville Baptist Church', 'Hebrews 12.3_Instagram.png', 4501, 4501)],
              [ks('Moundsville Baptist Church', 'MBC Wireframe (2nd Draft)-01.png', 874, 3810)]], [2, 1]),
    ('img', [ks('Moundsville Baptist Church', '279434224_5457232887644258_866262555927464512_n.jpg', 2048, 1152),
             ks('Moundsville Baptist Church', '5c8965eadbbda.png', 1080, 608)]),
    ('heading', 'UP Vikings Baseball', 'Jersey and apparel design.'),
    ('img', [ks('UP Vikings Baseball Jerseys', 'Chambers Baseball Jersey Mockup.png', 1448, 1086)]),
    ('img', [ks('UP Vikings Baseball Jerseys', 'UP Viings Baseball_Baseball Shirt Front And Back copy.jpg', 9167, 6108),
             ks('UP Vikings Baseball Jerseys', 'UP Viings Baseball_Baseball Shirt Front And Back copy 2.jpg', 9167, 6108)]),
    ('heading', 'DPC Students', 'Apparel and a social template for a student ministry.'),
    ('img', [ks('DPC Students', 'DPC Students (shirts).png', 938, 938), ks('DPC Students', 'DPC Students (social template).png', 938, 938)]),
    ('heading', 'Pierce Transit', 'Everyday design beyond the big campaigns: vehicles, banners, posters, presentations and wayfinding.'),
    ('img', [ks('Pierce Transit (misc)', '2025 Chevy Traverse Rideshare (mock up)_Side (driver).png', 8000, 4500)]),
    ('img', [ks('Pierce Transit (misc)', 'Farmers Market (30x60 Banners)_Page_1.jpg', 6184, 12184),
             ks('Pierce Transit (misc)', 'Farmers Market (30x60 Banners)_Page_2.jpg', 3432, 6762),
             ks('Pierce Transit (misc)', 'Farmers Market (30x60 Banners)_Page_3.jpg', 2474, 4874),
             ks('Pierce Transit (misc)', 'Farmers Market (30x60 Banners)_Page_4.jpg', 6524, 12854)]),
    ('img', [ks('Pierce Transit (misc)', 'Operator of the Month (ad shelter).jpg', 14100, 20400),
             ks('Pierce Transit (misc)', 'Project Spotlight Poster (TDS Wayfinding) v2.jpg', 4800, 7200)]),
    ('img', [ks('Pierce Transit (misc)', 'COMMUNITYLINE-blueshelter-sketch-8.7.24.jpg', 2270, 1659),
             ks('Pierce Transit (misc)', 'IMG_1829.jpeg', 1288, 1604)]),
    ('img', [ks('Pierce Transit (misc)', 'LRP Appendix Graphic (grouped)_Page_2.jpg', 5100, 3300)]),
    ('img', [ks('Pierce Transit (misc)', 'Rebrand Presentation v4.jpg', 3780, 804)]),
    ('img', [ks('Pierce Transit (misc)', 'Rebrand Presentation v4 1.jpg', 1874, 1890),
             ks('Pierce Transit (misc)', 'Rebrand Presentation v4 2.jpg', 1874, 1890),
             ks('Pierce Transit (misc)', 'Rebrand Presentation v4 3.jpg', 1874, 1890)]),
    ('img', [ks('Pierce Transit (misc)', 'Routes Wrap (gilling cng) v1.pdf', 0, 0)]),
    ('heading', 'Odds and ends', 'Merch, signage, email and a few favourites.'),
    ('img', [ks('Misc', 'Bend 2025_Hats (white-gold).png', 10151, 4688)]),
    ('img', [ks('Misc', 'Known Burst Hoodie (navy).png', 4000, 4000), ks('Misc', 'Known Cursive Hoodie (navy).png', 4000, 4000)]),
    ('img', [ks('Misc', 'Brickhouse window logo.jpg', 4000, 2700), ks('Misc', 'Easter.png', 2500, 1800)]),
    ('cols', [[ks('Misc', 'March 2021 Board Presentation (full version)Brading Social Posts (Paddle Gang)-12.png', 3001, 3001),
               ks('Misc', 'March 2021 Board Presentation (full version)Brading Social Posts (Paddle Gang)-13.png', 3001, 3001)],
              [ks('Misc', 'RentWatch Email Screenshots-02.PNG', 4139, 10712)]], [1, 0.78]),
    ('img', [ks('Misc', 'Gateway-Signs-02.png', 1800, 1800), ks('Misc', 'Speak. Listen.png', 2501, 2500)]),
])


def slugify(s):
    s = re.sub(r'\.[a-z0-9]+$', '', s, flags=re.I)
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    return s[:60]


def save_webp(im, path, maxw=MAXW, maxh=5000):
    if im.mode not in ('RGB', 'RGBA'):
        im = im.convert('RGBA' if 'A' in im.getbands() or im.mode == 'P' else 'RGB')
    if im.mode == 'RGBA' and im.getextrema()[3][0] == 255:
        im = im.convert('RGB')
    s = min(1, maxw / im.width, maxh / im.height)
    if s < 1:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im.save(path, 'WEBP', quality=86, method=5)
    return im.width, im.height


def pdf_page(pdf, page, dpi, out_png):
    subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(page), '-l', str(page), '-png', '-singlefile', pdf, out_png[:-4]], check=True)
    return out_png


def crop_layout(proj, x, y, w, h, name, out):
    k = 4  # 288 dpi
    pdf = os.path.join(DROP, proj['folder'], proj['pdf'])
    px, py = round((x + 400) * k), round((y + proj['H'] / 2) * k)
    tmp = os.path.join(TMP, name + '.png')
    subprocess.run(['pdftoppm', '-r', str(72 * k), '-x', str(px), '-y', str(py), '-W', str(round(w * k)), '-H', str(round(h * k)),
                    '-png', '-singlefile', pdf, tmp[:-4]], check=True)
    return save_webp(Image.open(tmp), out)


def gif_to_video(src, slug, name):
    os.makedirs(os.path.join(OUT_VID, slug), exist_ok=True)
    mp4 = os.path.join(OUT_VID, slug, name + '.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-movflags', '+faststart', '-pix_fmt', 'yuv420p',
                    '-vf', "scale='min(1600,iw)':-2", '-c:v', 'libx264', '-crf', '23', '-preset', 'veryfast', '-an', mp4], check=True)
    return f'/video/{slug}/{name}.mp4'


def frame_crop(im, proj, src):
    # Crop to what's visible in the InDesign frame (from the IDML image transforms), so tiles match the layout
    c = CROPS.get(proj['folder'], {}).get(os.path.basename(src))
    if not c or c == [0, 0, 1, 1]:
        return im
    w, h = im.size
    return im.crop((round(c[0] * w), round(c[1] * h), round(c[2] * w), round(c[3] * h)))


def process(slug, proj, report):
    out_dir = os.path.join(OUT_IMG, slug)
    os.makedirs(out_dir, exist_ok=True)
    links = os.path.join(DROP, proj['folder'], proj.get('links', 'Links'))
    n = 0

    def item(it):
        nonlocal n
        n += 1
        if it[0] == 'crop':
            _, x, y, w, h, name = it
            fn = f'{n:02d}-{name}.webp'
            path = os.path.join(out_dir, fn)
            if not os.path.exists(path):
                crop_layout(proj, x, y, w, h, f'{slug}-{name}', path)
            return dict(file=f'projects/{slug}/{fn}', ratio=round(w / h, 4), source=f'(cropped from layout) {name}')
        src, w, h = it
        name = slugify(src)
        fn = f'{n:02d}-{name}.webp'
        path = os.path.join(out_dir, fn)
        full = os.path.join(links, src)
        rec = dict(file=f'projects/{slug}/{fn}', ratio=round(w / h, 4) if h else None, source=src)
        if src.lower().endswith('.mp4'):
            os.makedirs(os.path.join(OUT_VID, slug), exist_ok=True)
            mp4 = os.path.join(OUT_VID, slug, f'{n:02d}-{name}.mp4')
            if not os.path.exists(mp4):
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', full, '-movflags', '+faststart', '-pix_fmt', 'yuv420p',
                                '-vf', "scale='min(1280,iw)':-2", '-c:v', 'libx264', '-crf', '27', '-preset', 'veryfast',
                                '-c:a', 'aac', '-b:a', '96k', mp4], check=True)
            if not os.path.exists(path):
                tmp = os.path.join(TMP, f'{slug}-{name}-poster.png')
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '2', '-i', full, '-frames:v', '1', tmp], check=True)
                save_webp(Image.open(tmp), path)
            rec['video'] = f'/video/{slug}/{n:02d}-{name}.mp4'
            rec['controls'] = True
            return rec
        if src.lower().endswith('.gif'):
            rec['video'] = gif_to_video(full, slug, f'{n:02d}-{name}')
            if FORCE or not os.path.exists(path):
                g = Image.open(full); g.seek(g.n_frames // 2)  # mid-animation frame: the first is often blank
                save_webp(frame_crop(g.convert('RGBA'), proj, src), path)
            return rec
        if FORCE or not os.path.exists(path):
            if src.lower().endswith(('.pdf', '.ai')):
                tmp = pdf_page(full, 1, 100 if os.path.getsize(full) > 10e6 else 200, os.path.join(TMP, f'{slug}-{name}.png'))
                save_webp(Image.open(tmp), path)
            else:
                save_webp(frame_crop(Image.open(full), proj, src), path)
        if rec['ratio'] is None:
            im = Image.open(path); rec['ratio'] = round(im.width / im.height, 4)
        return rec

    rows = []
    for row in proj['rows']:
        kind = row[0]
        if kind == 'img':
            rows.append(dict(type='img', items=[item(i) for i in row[1]]))
        elif kind == 'cols':
            rows.append(dict(type='cols', widths=row[2], cols=[[item(i) for i in col] for col in row[1]]))
        elif kind == 'heading':
            rows.append(dict(type='heading', title=row[1], text=row[2]))
        elif kind == 'booklet':
            rows.append(dict(type='booklet', id=row[1], title=row[2], spreads=row[3]))
    report[slug] = rows


def booklets():
    # Pierce Transit brand guide: 28 landscape pages
    bid = os.path.join(OUT_BK, 'pt-brand-guide'); os.makedirs(bid, exist_ok=True)
    pdf = os.path.join(DROP, 'Pierce Transit Brand Referesh', 'Links', 'Pierce Transit Brand Guide 09.11.25.pdf')
    if len(os.listdir(bid)) < 28:
        subprocess.run(['pdftoppm', '-r', '130', '-png', pdf, os.path.join(TMP, 'ptbg')], check=True)
        for f in sorted(x for x in os.listdir(TMP) if x.startswith('ptbg')):
            i = int(re.search(r'(\d+)\.png$', f).group(1))
            save_webp(Image.open(os.path.join(TMP, f)), os.path.join(bid, f'{i:02d}.webp'), maxw=1800)
    # Annual report: 10 spread images → 20 pages. Spread 1 is [back cover | front cover].
    aid = os.path.join(OUT_BK, 'pt-annual-report-2024'); os.makedirs(aid, exist_ok=True)
    for f in os.listdir(aid):
        os.rename(os.path.join(aid, f), os.path.join(TMP, 'old-ar-' + f))  # replace the earlier page set
    links = os.path.join(DROP, 'Pierce Transit Annual Report', 'Links')
    halves = []
    for s in range(1, 11):
        im = Image.open(os.path.join(links, f'Annual Report Spread {s}.png'))
        w, h = im.size
        halves.append((im.crop((0, 0, w // 2, h)), im.crop((w // 2, 0, w, h))))
    pages = [halves[0][1]] + [p for s in halves[1:] for p in s] + [halves[0][0]]
    for i, p in enumerate(pages, 1):
        save_webp(p, os.path.join(aid, f'{i:02d}.webp'), maxw=1400)


if __name__ == '__main__':
    report = {}
    mpath = os.path.join(ROOT, 'incoming', '_renders', 'manifest.json')
    if os.path.exists(mpath):
        report = json.load(open(mpath))
    if ONLY in (None, 'booklets'):
        booklets()
    for slug, proj in P.items():
        if ONLY and ONLY not in (slug,) and ONLY != 'all':
            continue
        process(slug, proj, report)
        json.dump(report, open(mpath, 'w'), indent=1)
        print('done', slug, flush=True)
    print('ok')
