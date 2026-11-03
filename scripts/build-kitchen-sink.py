#!/usr/bin/env python3
"""Rebuild the Kitchen Sink gallery from Peter's Drive folder (Nov 2026 layout, `Kitchen Sink.pdf`).

    python3 scripts/build-kitchen-sink.py "<path to Kitchen Sink folder>"

Writes WebP (≤2000px) to src/assets/projects/kitchen-sink/ and replaces the `gallery:` block of
src/content/work/kitchen-sink.md. Needs ImageMagick (`magick`). Group text is Peter's, verbatim.
"""
import os, re, shutil, subprocess, sys

SRC = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'src', 'assets', 'projects', 'kitchen-sink')
MD = os.path.join(ROOT, 'src', 'content', 'work', 'kitchen-sink.md')

# (file, alt) or (file, alt, video) ; a row is a list of 1–3 items ; ('cols', [col, col]) is a mosaic ; ('h', title, text)
PTS, PTR, PTF, PTW = 'Pierce Transit (swag)', 'Pierce Transit (proposed rebrand)', 'Pierce Transit (farmers market collab)', 'Pierce Transit World Cup'
BD, CF, CB, TT, CH, MBC, MI = 'Beautiful Day', 'Coastline Family Farms', 'Cause Brokers', 'Taylor & Taylor Farms', 'Chambers Bay Vikings Baseball Jerseys', 'Moundsville Baptist Church', 'Misc'
LAYOUT = [
  ('h', 'Pierce Transit Swag', 'I designed PNW-inspired merchandise for Pierce Transit, combining minimal visuals and meaningful messaging to build brand awareness, celebrate public transit, and turn supporters into brand evangelists.'),
  [(f'{PTS}/Lightening Bolt - Mock Up (canyon) v1.png', 'Mustard snapback cap with a black arched Pierce Transit patch, a lightning bolt and "Ditch Your Car. Keep Your Cash."'),
   (f'{PTS}/Tan Snapback Hat on Stone Surface.png', 'Back of the mustard snapback cap with a small black Pierce Transit woven label')],
  [(f'{PTS}/Hat Patch - artwork (lightening bolt) v1_Woven Patch.png', 'Patch artwork: arched "Pierce Transit" lettering over a lightning bolt and the script line "Ditch Your Car. Keep Your Cash."'),
   (f'{PTS}/Amber Mug - artwork (lightning bolt).jpg', 'Two amber glass mugs printed with the Pierce Transit lightning-bolt logo and "Ditch Your Car. Keep Your Cash."')],
  ('cols', [[(f'{PTS}/Community Poster (24x36).jpg', 'Blue line-art "Connecting Our Community" poster: a winding transit route linking farms, Mount Rainier, downtown Tacoma and the waterfront')],
            [(f'{PTS}/Monoline Community - Mock Up (poster).png', 'The "Connecting Our Community" poster framed on a blue wall'),
             (f'{PTS}/Your World In Motion - Mock Up (black).png', 'Black "Your World In Motion" T-shirts: a globe-and-bus badge on the front, transit facts listed on the back')]]),
  [(f'{PTS}/Your World In Motion - Mock Up (white).png', 'White "Your World In Motion" T-shirts with a blue and green globe badge on the front and blue transit facts on the back'),
   (f'{PTS}/Your World In Motion v4.jpg', '"Your World In Motion" artwork: a white globe-and-bus badge beside a list of facts on the benefits of public transit')],

  ('h', 'Pierce Transit Rebrand Concept', 'I explored a Pierce Transit rebrand, simplifying the logo, clarifying service names, and introducing distinct, accessible color palettes to strengthen brand recognition and unify the service experience.'),
  [(f'{PTR}/Rebrand Presentation (current vs proposed).jpg', 'Current Pierce Transit logos beside the proposed set: a swooping P-road icon with horizontal, stacked, badge and split lockups')],
  [(f'{PTR}/Rebrand Presentation v6_Page_2.jpg', 'Three icons explaining the concept: Letter P made of simplified roads, We Listen, and We Help')],
  [(f'{PTR}/Rebrand Presentation (logo on white).jpg', 'Proposed Pierce Transit logo in green on white'),
   (f'{PTR}/Rebrand Presentation (logo on green).jpg', 'Proposed Pierce Transit logo in green and white on dark green')],
  [(f'{PTR}/Rebrand Presentation (service logos).jpg', 'Service sub-brands Routes, Zones, Groups, Access+, Rapid, Trolley and Events, each with its own colour, on dark and light backgrounds')],
  [(f'{PTR}/Rebrand Presentation v5.jpg', 'Groups concept: two colleagues walking in front of a large green P icon on dark green'),
   (f'{PTR}/Rebrand Presentation v4 1.jpg', 'Access+ concept: a smiling man in a wheelchair framed by a large green P icon')],
  [(f'{PTR}/Rebrand Presentation v4 2.jpg', 'Events concept: a man leaping with a bass guitar against a pink P icon on plum'),
   (f'{PTR}/Rebrand Presentation v4 3.jpg', 'Trolley concept: a couple with a baby walking in front of a red P icon on maroon')],
  [(f'{PTR}/Routes Wrap (gilling cng).png', 'Side, front and rear views of a bus wrap in green gradients with the large P icon and "Pierce Transit, improving lives with local rides"')],
  [(f'{PTR}/Gemini_Generated_Image_llrpuyllrpuyllrp.jpeg', 'Concept render of a green Pierce Transit bus in the proposed livery on a downtown Tacoma street')],
  [(f'{PTR}/Gemini_Generated_Image_ygdg51ygdg51ygdg.jpeg', 'Concept render of a magenta Events bus at a stop outside the Tacoma Dome')],
  [(f'{PTR}/Pierce Transit Headquarters at Night.png', 'Pierce Transit headquarters at dusk with the proposed logo lit in green on the building')],

  ('h', 'Pierce Transit x Broadway Farmers Market Street Banners', 'I designed colorful, evergreen street banners to promote the Broadway Farmers Market, using bold typography and photography to highlight its diverse offerings, attract visitors, and encourage community engagement.'),
  [(f'{PTF}/IMG_1828.jpeg', 'Worker in a hard hat in a bucket lift hanging a blue Broadway Farmers Market banner beside a Visitor Info sign')],
  [(f'{PTF}/Farmers Market (30x60 Banners)_Page_3.jpg', 'Red Broadway Farmers Market street banner with a heap of fresh cherries and "Fresh food access", at 9th & Broadway'),
   (f'{PTF}/Farmers Market (30x60 Banners)_Page_2.jpg', 'Green Broadway Farmers Market street banner showing four smiling women, "Make community connections", at 9th & Broadway'),
   (f'{PTF}/Farmers Market (30x60 Banners)_Page_1.jpg', 'Pink Broadway Farmers Market street banner with tulips, "Fresh every Thursday" and "Support small business"')],

  ('h', 'Pierce Transit World Cup Fan Zone Express', 'I designed billboards and helped design a custom soccer jersey to build awareness of Pierce Transit’s Fan Zone Express, drive ridership, reduce game-day parking demand, and connect fans to world soccer.'),
  [(f'{PTW}/Crisp Soccer Billboard Above Rainy Highway.png', 'Highway billboard with Mount Rainier behind: "World Soccer is Coming. Are you? Join us." PierceTransit.org/SEA26')],
  [(f'{PTW}/Game On Billboard Over Cityscape.png', 'Billboard over Tacoma reading "Game On. Car Off. Plan your ride at PierceTransit.org/SEA26"')],
  [(f'{PTW}/Less Parking, More Cheering Billboard.png', 'Billboard of a cheering fan in a Pierce Transit jersey: "Less Parking. More Cheering."')],
  [(f'{PTW}/Pierce Transit Football Club Jersey Mockup.png', 'Front and back of a green-to-blue Pierce Transit soccer jersey, number 26')],

  ('h', 'Beautiful Day Rebrand', 'I rebranded Beautiful Day Cleaning Company with a bold, Tacoma-inspired identity across its website, vehicles, apparel, and print materials to strengthen brand recognition and attract new customers.'),
  [(f'{BD}/Beautiful Day Logo (before and after).jpg', 'Beautiful Day logo before (a grey silhouette of a child blowing a dandelion) and after (a gold sun-and-house badge with a bold navy wordmark)')],
  [(f'{BD}/BD Social Media-02.png', 'Beautiful Day badge in gold on navy: a sun over a house, hillside and waves'),
   (f'{BD}/Brading Social Posts-15.png', 'Beautiful Day Cleaning Company wordmark over a navy-tinted Tacoma skyline, "Since 2009, Tacoma WA"')],
  [(f'{BD}/Business Cards (FALLING) copy.png', 'Falling Beautiful Day Cleaning Company business cards, navy logo fronts and white backs for Kyle Klevjer'),
   (f'{BD}/Beautiful Day - Van (back).png', 'Navy van wrapped for Beautiful Day Cleaning Company, listing windows, gutters and roofs')],
  [(f'{BD}/Beautiful Day Shirts.png', 'Navy Beautiful Day Cleaning Company T-shirts showing the large back print and small circular chest logo'),
   (f'{BD}/BD New Website_Instagram.png', 'Beautiful Day social post, "Explore Our New Website!", showing the homepage on laptop, tablet and phone')],

  ('h', 'Coastline Family Farms Label Redesign', 'I redesigned Coastline Family Farms’ produce labels with a vibrant, cohesive system and crop-specific colors to improve shelf recognition, distinguish products, and celebrate its family-farming heritage.'),
  [(f'{CF}/1. Coastline Label (before and after)-15.png', 'Before and after of the Coastline Family Farms onion label: dark green-trimmed design replaced by a navy and purple oval "Red Onions" label'),
   (f'{CF}/2. Coastline Label-Variety-03.jpg', 'Coastline Family Farms label variants for red onions, lettuce and tomatoes, each with a different coloured ribbon')],
  [(f'{CF}/Coastline Family Farms Red Onions.png', 'Purple mesh sack of red onions wearing the redesigned Coastline Family Farms "Red Onions" label'),
   (f'{CF}/Western Grower Magazine Onion Feature and Family Farm Ad.png', 'Western Grower magazine spread with a Coastline Family Farms ad, "Our Families Were Farming, Before Family Farms Were Cool!"')],

  ('h', 'Moundsville Baptist Website Redesign and Graphics', 'I redesigned Moundsville Baptist Church’s website to improve navigation, welcome visitors, and encourage engagement, while creating bold, distinctive sermon graphics to bring each teaching series to life.'),
  ('cols', [[(f'{MBC}/MBC Wireframe (2nd Draft)-01.png', 'Full-length homepage design for Moundsville Baptist Church, headed "A Church for Moundsville", in blue, orange and white')],
            [(f'{MBC}/5c8965eadbbda.png', 'Sermon series graphic: "Relentless Love, a series through Hosea", a waterfall pouring from a city into desert'),
             (f'{MBC}/279434224_5457232887644258_866262555927464512_n.jpg', 'Sermon series graphic: "The Glorious Church, a series through Ephesians" on teal with papercut foliage'),
             (f'{MBC}/MBC Advent 2022-01.png', 'Advent graphic: dark green "Advent, the coming of the Lord" on a red icon pattern'),
             (f'{MBC}/MBC A Gospel People-01.png', 'Sermon series graphic: "The Church: A Gospel People, a new 5-part mini series" on teal'),
             (f'{MBC}/Hebrews 12.3_Instagram.png', 'Instagram scripture post: "Consider Him, Hebrews 12:3" in olive and coral script')]]),

  ('h', 'Cause Brokers Branding and Website Design', 'I branded Cause Brokers and redesigned its website to simplify charitable giving through real estate, helping buyers, sellers, and agents turn property transactions into meaningful community impact.'),
  [(f'{CB}/Cause Brokers Logo (before and after).jpg', 'Cause Brokers logo before (a black CB house mark) and after (a blue house outline holding a family, "Find a realtor. Fund a cause.")'),
   (f'{CB}/Peter Rebik Portfolio (Cause Brokers)_Logo (badge).jpg', 'Cause Brokers badge logo: the family-house icon in an arch ringed by "Fundraising through real estate"')],
  [(f'{CB}/Cause-Brokers-website-scroll.gif', 'Scrolling recording of the Cause Brokers website on a laptop, from "Fundraising Through Real Estate" through How It Works to contact', '/video/kitchen-sink/01-cause-brokers-cause-brokers-website-scroll.mp4'),
   (f'{CB}/Peter Rebik Portfolio (Cause Brokers)_Business Cards (front and back).jpg', 'Stacks of Cause Brokers business cards, navy logo fronts beside white backs printed for Troy Weiman')],
  [(f'{CB}/Peter Rebik Portfolio (Cause Brokers)_Website (mobile).jpg', 'Cause Brokers mobile website screens: "Fundraising Through Real Estate", What We Do, Who We Help, How It Works and partners')],
  [(f'{CB}/Peter Rebik Portfolio (Cause Brokers)_Brand Pattern.jpg', 'Cause Brokers brand pattern: repeating blue gradient house-and-family icons tiled in offset rows')],

  ('h', 'Taylor & Taylor Management Website Design', 'I created a website and downloadable guide to help landowners make informed decisions, build trust in Taylor & Taylor Management, and turn interest into qualified leads.'),
  [(f'{TT}/Taylor-and-Taylor-website-scroll.gif', 'Scrolling recording of the Taylor & Taylor Management website on a laptop, gold and cream pages on land leasing', '/video/kitchen-sink/05-taylor-taylor-farms-taylor-and-taylor-website-scroll.mp4'),
   (f'{TT}/Peter Rebik Portfolio (Taylor & Taylor)_Business Cards (front and back).jpg', 'Taylor & Taylor guide "Maximize Your Profit. Minimize Your Loss.", cover and spreads')],
  [(f'{TT}/Peter Rebik Portfolio (Taylor & Taylor)_Website (mobile).jpg', 'Taylor & Taylor mobile website screens in gold and cream, offering fair, competitive land leasing and purchasing')],

  ('h', 'Chambers Bay Baseball Uniform', 'I designed custom uniforms for the Chambers Bay Vikings travel baseball team, combining bold typography, vibrant colors, and a Chambers Bay-inspired crest to build team identity and pride.'),
  [(f'{CH}/Chambers Baseball Jersey Mockup.png', 'Front and back mock-up of a blue Chambers baseball jersey with light blue sleeves and a Chambers Bay Baseball sleeve patch')],
  [(f'{CH}/UP Viings Baseball_Baseball Shirt Front And Back copy.jpg', 'Chambers Bay Baseball circular crest with a pine tree, ringed by "University Place, Washington"'),
   (f'{CH}/UP Viings Baseball_Baseball Shirt Front And Back copy 2.jpg', 'Arched "Chambers" jersey lettering in white and light blue on royal blue')],

  ('h', 'Miscellaneous', 'A collection of branding, signage, merchandise, and digital design projects, I turn everyday touchpoints into memorable brand experiences through thoughtful design and purposeful storytelling.'),
  ('cols', [[(f'{MI}/2025 Chevy Traverse Rideshare (mock up)_Side (driver).png', 'Side view mock-up of a white Chevy Traverse with Pierce Transit Rideshare livery'),
             (f'{MI}/LRP Appendix Graphic (grouped)_Page_2.jpg', 'Pierce Transit Saturdays service chart comparing route hours for Baseline, Scenario A and Scenario B'),
             (f'{MI}/Project Spotlight Poster (TDS Wayfinding) v2.jpg', 'Pierce Transit "Project Spotlight" poster on Tacoma Dome Station wayfinding, with goals, timeline and signage mock-ups'),
             (f'{MI}/Speak. Listen.png', '"Slow to speak, quick to listen" illustration with overlapping textured tortoise and rabbit silhouettes')],
            [(f'{MI}/COMMUNITYLINE-blueshelter-sketch-8.7.24.jpg', 'Concept sketch of a blue Stream Community Line bus shelter and totem sign'),
             (f'{MI}/Bend 2025_Hats (white-gold).png', 'Two mustard rope caps with black Bend 2025 retreat patches'),
             (f'{MI}/RentWatch Email Screenshots-02.PNG', 'Landlord Solutions email promoting RentWatch, "You Already Have Enough on Your Plate", with feature cards, a promo code and countdown')]]),
  [(f'{MI}/March 2021 Board Presentation (full version)Brading Social Posts (Paddle Gang)-12.png', 'Blue and white Paddle Gang T-shirts printed with the arched sun, mountains and waves logo'),
   (f'{MI}/March 2021 Board Presentation (full version)Brading Social Posts (Paddle Gang)-13.png', 'White Paddle Gang decal on a car\'s rear window')],
  [(f'{MI}/Easter.png', 'Gateway Easter banner split black and white: "On Friday a thief" and "On Sunday a King", around a crown of thorns'),
   (f'{MI}/Gateway-Signs-02.png', 'Gateway church signage set: Guest Parking, Youth Office, Worship Center, a "Chasing the Wind" banner and "Welcome"'),
   (f'{MI}/Brickhouse window logo.jpg', 'Brickhouse Deli logo applied as a white decal on a shop window, "Estd 2017"')],
]

def slug(s):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s.lower())).strip('-')[:60].rstrip('-')

n = 0
def convert(item):
    global n
    n += 1
    path = os.path.join(SRC, item[0])
    group = slug(os.path.dirname(item[0]).replace('Pierce Transit', 'pt'))
    name = f'{n:02d}-{group}-{slug(os.path.splitext(os.path.basename(item[0]))[0])}'[:70].rstrip('-') + '.webp'
    out = os.path.join(OUT, name)
    subprocess.run(['magick', path + '[0]', '-auto-orient', '-colorspace', 'sRGB', '-resize', '2000x2000>',
                    '-strip', '-quality', '82', '-define', 'webp:method=6', out], check=True)
    w, h = map(int, subprocess.check_output(['magick', 'identify', '-format', '%w %h', out]).split())
    alt = item[1].replace('"', '\\"')
    vid = f', video: {item[2]}' if len(item) > 2 else ''
    return f'{{ src: ../../assets/projects/kitchen-sink/{name}, alt: "{alt}", ratio: {w / h:.4f}{vid} }}', w / h

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
lines = ['gallery:']
for row in LAYOUT:
    if isinstance(row, tuple) and row[0] == 'h':
        lines += [f'  - heading: "{row[1]}"', f'    text: "{row[2]}"']
    elif isinstance(row, tuple) and row[0] == 'cols':
        cols = [[convert(i) for i in col] for col in row[1]]
        # Column widths so both columns end level: height ∝ width × Σ(1/ratio)
        inv = [sum(1 / r for _, r in col) for col in cols]
        widths = [round(inv[0] / x, 3) for x in inv]
        lines.append(f'  - widths: [{", ".join(str(w) for w in widths)}]')
        lines.append('    cols:')
        for col in cols:
            for j, (s, _) in enumerate(col):
                lines.append(('      - - ' if j == 0 else '        - ') + s)
    else:
        for j, it in enumerate(row):
            s, _ = convert(it)
            lines.append(('  - - ' if j == 0 else '    - ') + s)

md = open(MD).read()
head, rest = md.split('\ngallery:\n', 1)
tail = rest[rest.index('\n---'):]
open(MD, 'w').write(head + '\n' + '\n'.join(lines) + tail)
print(f'{n} images')
