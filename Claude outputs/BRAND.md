# Peter Rebik: Brand Guide

The source of truth for the visual system. Values live in [`src/styles/tokens.css`](src/styles/tokens.css). Change them there, never hard-code them in components. A live, rendered version is at **`/styleguide`** when you run the site (it's not linked anywhere and is set to `noindex`).

Source wireframe: [`docs/wireframe-landing.pdf`](docs/wireframe-landing.pdf). Page 1 is desktop, page 2 is desktop hover states, page 3 is mobile.

---

## 1. Color

### Primary
| Token | Hex | Use |
|---|---|---|
| `--color-forest` | `#162d16` | Nav, all headings, footer, CTA band, active skill card |
| `--color-lime` | `#98d81e` | Buttons, underlines, scribble, icons, stars, logo, footer headings |

### Secondary
| Token | Hex | Use |
|---|---|---|
| `--color-lime-soft` | `#ade04b` | **Hover** fill for any lime element (buttons, slider arrows) |
| `--color-mint` | `#e2f7d2` | Alternating section background, visa panel, chips |
| `--color-white` | `#ffffff` | Main background, cards, nav link text |

### Tertiary / neutrals
| Token | Hex | Use |
|---|---|---|
| `--color-ink` | `#000000` | Paragraph text |
| `--color-graphite` | `#4d4d4d` | Fine print (hero sponsorship note, review roles) |
| `--color-sage` | `#8b968b` | Footer text, nav link hover, divider on dark |
| `--color-sage-dark` | `#5c6c5c` | Reserve: footer text where more contrast is needed |

**Rules**
- Lime is an accent. Never set body text in lime on white, because it fails contrast. Lime text is only for display type (eyebrow, logo, “View Project”) or on forest.
- Forest on lime and forest on mint both pass AA. Use them for any text on accent fills.
- Section rhythm alternates white → mint → white → mint → white → forest.

---

## 2. Typography

| Role | Family | Notes |
|---|---|---|
| Headings, buttons, labels | **Dela Gothic One** 400 | `--font-display`. Only one weight exists. |
| Paragraphs, nav, captions | **Epilogue** 400 / 600 | `--font-body` |

Both fonts are self-hosted via `@fontsource` (no Google request), Latin subset only, with the two critical files preloaded.

### Hierarchy (fluid, mobile → desktop)

| Class / element | Token | Size | Line height | Used for |
|---|---|---|---|---|
| `h1`, `.t-display` | `--fs-display` | 40 → 52px | 1.1 | Hero title, every section title |
| `.t-h2` | `--fs-h2` | 22 → 30px | 1.05 | Skill card titles |
| `.t-h3` | `--fs-h3` | 20 → 24px | 1.15 | Project page sub-heads |
| `.t-h4` | `--fs-h4` | 17 → 20px | 1.15 | Hero eyebrow, visa title |
| `.t-h5` | `--fs-h5` | 16px | 1.15 | Footer column headings |
| `.btn` | `--fs-button` | 15px | 1 | All buttons (Dela) |
| `.t-body-lg` | `--fs-body-lg` | 17 → 19px | 1.4 | Section intros, hero lede, about |
| `p` | `--fs-body` | 16px | 1.4 | Reviews, card summaries |
| `.t-small` | `--fs-small` | 15px | 1.4 | Visa copy, review org |
| `.t-xs` | `--fs-xs` | 13px | — | Nav, footer, roles |
| — | `--fs-micro` | 12px | 1.5 | Hero note, helper text |

**Rules**
- Every section title is a `t-display` with one highlighted phrase wrapped in `<span class="hl">…</span>`, which gives the lime underline that draws in on scroll. Use one per heading.
- Headings use `text-wrap: balance`. Force a break with `<br/>` only when the wireframe calls for it.
- Long-form paragraphs (About, CTA) are justified on desktop with `hyphens: auto` and left-aligned on mobile.
- UK spelling throughout (*organisations*). The page is `lang="en-GB"`.

---

## 3. Layout & spacing

- **4px base scale:** `--space-1` (4) … `--space-10` (96).
- **Section padding:** `--section-pad` (64 → 104px).
- **Gutter:** `--gutter` (20 → 36px).
- **Containers:** `.container` 1140, `.container-md` 940 (cards, hero), `.container-sm` 640 (reading).
- **Breakpoints:** `760px` (mobile ↔ desktop), `900px` (3 → 2 column grids), `1400px` (larger carousel).

## 4. Shape & elevation

| Token | Value | Use |
|---|---|---|
| `--radius-sm` | 10px | Small images |
| `--radius-md` | 14px | Hero collage, carousel images |
| `--radius-lg` | 20px (18 mobile) | Cards, panels, visa box |
| `--radius-pill` | 999px | Buttons, chips |
| `--shadow-sm` | subtle | Resting carousel image |
| `--shadow-md` | soft | Hovered cards / tiles |
| `--shadow-lift` | tight | Hovered buttons |

---

## 5. Motion

Motion should feel **quick, confident, never bouncy for its own sake.**

| Token | Value | Use |
|---|---|---|
| `--ease-out` | `cubic-bezier(.22,1,.36,1)` | Default for everything |
| `--ease-in-out` | `cubic-bezier(.65,0,.35,1)` | Carousel rotation |
| `--ease-spring` | `cubic-bezier(.34,1.56,.64,1)` | Small playful pops (logo, stars, portrait). Use sparingly. |
| `--dur-fast` | 160ms | Color changes |
| `--dur-base` | 280ms | Hover scale / lift |
| `--dur-slow` | 600ms | Carousel, scroll reveals |
| `--dur-draw` | 1100ms | Underline + scribble draw-in |
| `--hover-scale` | 1.1 | Wireframe spec: interactive elements scale ×1.1 |

### Interaction spec (from the wireframe's hover page)
| Element | Rest | Hover |
|---|---|---|
| Nav link | white | `#8b968b` + underline slides in |
| Nav “Let’s Talk” | lime outline + lime text | lime fill, forest text, ×1.1 |
| Primary button | lime fill, forest text | `#ade04b`, ×1.1, lift shadow |
| Secondary button | lime outline, forest text | `#ade04b` fill, ×1.1, lift shadow |
| Hero collage tile | — | ×1.1 + slight rotation (±2–3°) |
| Skill card | white, icon + title | forest fill, white description, ×1.1 (tap to toggle on touch) |
| Slider arrows | lime | `#ade04b`, ×1.1 |
| Carousel | center ×1, sides ×0.83, edges ×0.7 + faded | Side card click rotates it to center. Autoplays every 6s, pauses on hover/focus/off-screen |
| Footer links | sage | white |

### Ambient motion
- Lime marquee scrolls slowly (60s loop) and pauses on hover.
- Section content fades up on scroll (`data-reveal`, staggered with `--i`).
- Hero scribble around “clear” and the underline draw in on load.

**Accessibility:** `prefers-reduced-motion` zeroes every duration and sets `--hover-scale: 1`. The marquee and carousel autoplay stop, and reveals show immediately.

---

## 6. Iconography & imagery

- Icons are SVGs extracted from the wireframe in `src/icons/`. They use `currentColor`, so set `color` to recolor. Render them with `<Icon name="…" />`.
- Stroke weight is about 2.75 at a 40-unit box. Keep any new icons consistent with that.
- Photos are rounded (`--radius-md`), `object-fit: cover`, and are optimized to WebP by Astro at build time. Use 3:2 landscape for project covers.
- Logo: `src/assets/brand/logo-mark-2x.png` (rebuilt at 2x from the wireframe PDF with an unclipped circle) plus the wordmark set live in Dela Gothic One. **TODO:** swap the PNG mark for Peter's SVG when he sends it.

---

## 7. Voice

Clear, warm, confident. Short sentences. Lead with outcomes, and use numbers when you have them (“Reduced design time by ~30%”).

---

## 8. Project page (`/work/[slug]`)

From Peter's project wireframe.

- **Layout:** 2 : 3 columns in `.container` (text left, images right), stacked below 900px. The text column is sticky: it scrolls until its bottom is in view, then holds while the images continue.
- **Title block:** employer eyebrow (`t-h4`, lime in the original theme, moss in 2026), then the `t-display` title.
- **My Role / Skills Used / Brief:** plain semibold labels with no dash, always open; they're no longer collapsible `<details>`. The chips are mint pills with a lime icon dot. Skill chips use the homepage skill icons and link back to `/#help`, labelled in lowercase with `&` written as `+`.
- **Brief (Oct 2026):** the frontmatter `intro` sits under a "Brief" label in a solid dark pine card. The first paragraph is white at body-lg size and medium weight. The rest is sage, for 7.5:1 contrast on pine.
- **Write-up cards (Oct 2026):** the Markdown body is split into one mint card per `## ` section, 12px apart. The split happens in `[slug].astro` from `entry.rendered.html`, with `<Content />` as the fallback. Each `## ` heading gets the homepage title treatment at a smaller scale (clamp 24 → 32px, tight leading). Its last word is wrapped in `.hl`, so on the 2026 theme it's the italic serif with the volt highlighter that draws in on reveal ("The *Challenge*"). This is shared template code, so it can go to main as well.
- **Write-up bullets (Oct 2026):** on the 2026 theme the bullets are graphite (#4f5b52), a soft near-black that reads on the mint cards. The old moss rule never applied, because Astro scoped the `[data-theme]` part; it's now wrapped in `:global()`.
- **Nav:** "Work" in the header (desktop and mobile) goes to the `/work` index page, on both themes. The footer quick links and the "See My Work" buttons still jump to the homepage section.
- **Write-up card:** mint panel, `--radius-lg`. Headings are `--fs-h4`, body is `--fs-small`, and list bullets are lime dots.
- **Images:** rows of 1, 2 or 3 tiles with a 10px gap and `--radius-md`. Each row's tiles share one aspect ratio, based on the average of their images, so the row lines up. An image whose shape is far off the row's shape is letterboxed (`contain`) instead of cropped. Every tile opens the lightbox (arrow keys, Esc).
- **Prev / next band:** lime band with forest outline pills (“See Prev”, “See Next”) and long arrows. Hover: `#ade04b` fill, ×1.1, lift shadow.

---

# Theme B: "2026" (tinker branch)

This is an alternative theme layered on top of the original. The original tokens in `tokens.css` are untouched, and `src/styles/themes/2026.css` overrides them when `<html data-theme="2026">` is set.

- **Switch the whole site:** set `theme` in `src/data/site.ts` to `'2026'` or `'original'`.
- **Preview in a browser:** add `?theme=original` or `?theme=2026` to the URL. The choice is remembered; `?theme=reset` clears it. The preview swaps colors and type only. The skills section layout (reel vs. grid) follows `site.theme` at build time.

## Color (B)
| Name | Token | Hex | Use | Contrast |
|---|---|---|---|---|
| Pine | `--color-forest` | `#0c1f14` | Text, nav, footer, dark sections | 15.5:1 on bone |
| Volt | `--color-lime` | `#c4f04d` | Fills, CTAs, highlighter marker. **Never as text on light.** | pine on volt 13:1 |
| Volt soft | `--color-lime-soft` | `#d5f77f` | Hover on volt | — |
| Moss | `--color-moss` / `--accent-text` | `#1f5130` | Green *text* on light (eyebrow, View Project) | 8.3:1 on bone |
| Bone | `--color-bone` / `--bg` | `#f4f3ee` | Page background (warm off-white) | — |
| Mist | `--color-mint` | `#e6eedc` | Alternate sections | — |
| Graphite | `--color-graphite` | `#4f5b52` | Muted text | 6.4:1 on bone |
| Sage | `--color-sage` | `#9fb0a3` | Text on pine (footer) | 7.5:1 on pine |
| Ember | `--color-ember` | `#ff6a3d` | Rare warm pop, art only | — |

Every text pairing passes WCAG AA, and most pass AAA.

## Type (B)
| Role | Typeface | Free stand-in for | Notes |
|---|---|---|---|
| Display / headings | **Bricolage Grotesque** (variable, optical size) | expressive agency grotesks (Die Grotesk, Söhne Schmal) | weight 720, tracking −0.035em, leading 0.98 |
| Body | **Geist** | Söhne / ABC Diatype / Neue Montreal | neutral neo-grotesk |
| Labels, buttons, tags | **Geist Mono** | Berkeley Mono / ABC Diatype Mono | UPPERCASE, +0.06em tracking, 13px |
| Accent (`.hl` words) | **Instrument Serif *Italic*** | Editorial New / Reckless | sits on a volt highlighter marker |

All four are SIL Open Font License, self-hosted via `@fontsource`.

**Pattern:** every section title is a heavy grotesk, with *one* phrase set in serif italic on a volt marker. On dark sections the marker is dropped and the phrase turns volt.

## Skills reel (B)
- `SkillsReel.astro` replaces the 3×2 grid. The original `Skills.astro` is kept for the original theme.
- It scrolls slowly (70s loop). It pauses on hover or keyboard focus, has an explicit Pause/Play button (WCAG 2.2.2), and also pauses when off-screen.
- Hover, focus or tap opens a card: the image blurs and darkens, the description slides up, the tags turn volt, and the other cards dim.
- With reduced motion it becomes a swipeable row instead.
- Card art lives in `src/assets/skills/` at a 4:5 ratio, as pairs: `<name>-bg.jpg` (gradient) + `<name>-icon.svg` (full-card 1000×1250 illustration that `SkillsReel` inlines on top, matched by name). It's placeholder generative art from `scripts/generate-skill-art.py`. All six cards are one family: soft “liquid” gradients with bright, friendly ribbons of volt, leaf green (#8FD14F), soft ember and bone on a pale-volt base. The waves and grain are kept subtle with a 16px blur and light noise. Each card also carries a simple line illustration, centred in its middle band at 70% scale. It's drawn in pine (the brand dark green), with lighter pine for secondary strokes and one solid pine accent. Each colour sits on its own layer, so crossing strokes never double up, and outlines are single closed paths so the joins are clean. The illustrations are: target rings (Brand), an eye (Creative), two speech bubbles (Messaging), a connected 3×3 module grid (Systems), a browser window with a pointer (Digital), and five thick lines that start scattered and come together into parallel lines, edge to edge (Alignment). Alignment keeps the full width; only its height is scaled. Each card has its own flow and accent: volt for Brand, ember/volt/bone for Creative, ember for Messaging, grass/mist for Systems, volt for Digital, and a mix for Alignment. The top of each card is lifted toward pale volt so the pine titles stay readable. Swap in a photo with the same file name, or change `image:` in `skills.yaml`.

## Work carousel (B)
- `WorkDrag.astro` replaces the centred `WorkCarousel.astro` when `site.theme` is `'2026'`. The original carousel is kept for the original theme. Modelled on Salient's “Architect” demo.
- **Layout:** 4:5 feature images, `clamp(260px, 27vw, 400px)` wide. The first card lines up with the container and the row bleeds off the right edge. Each card shows a number and employer (mono label), the title and the summary. It includes every published project, in `order`.
- **Image:** `feature` in the project's frontmatter, cropped with `featurePosition`. Without one it falls back to the first gallery image, then the cover.
- **Drag (mouse):** momentum throw, then a glide that snaps to the nearest card. Cards ease to ×0.95 while dragging, and a drag never counts as a click. **Touch, trackpad and keyboard** use native horizontal scrolling with snap.
- **Cursor:** a volt circle with ‹ › trails the mouse over the row and shrinks while pressed, with the arrows spreading apart. Fine pointers only.
- **Hover:** the image zooms ×1.06 (0.75s) and an underline draws under the title (0.55s), both `cubic-bezier(.2,.75,.5,1)`.
- **Entrance:** cards slide in from the right, staggered 90ms.
- **Controls:** a progress bar and prev/next arrows. The arrows are the non-drag alternative for WCAG 2.5.7. There is no count anywhere in the section.
- Reduced motion turns off the entrance, the scale and the momentum.


## Reviews (B)
- `ReviewsSlider.astro` replaces the card grid when `site.theme` is `'2026'`. The original `Reviews.astro` is kept for the original theme.
- **Layout:** one large quote at a time, in the body font at 24–42px. Below it is the role, with the organisation in serif italic underneath. Then a “1 / 6” counter and chevron arrows. There are no stars or avatars.
- **Motion:** slides cross-fade and drift 40px in the direction of travel. Arrows, the ← → keys and swipe all move it. There is no autoplay.
- Quotes that still read “Should have soon.” are hidden. `order` in `reviews.yaml` alternates clients so the same organisation doesn't appear twice in a row.

## Hero + Intro (B)
- `HeroBold.astro` and `Intro.astro` replace `Hero.astro` when `site.theme` is `'2026'`. The marquee is dropped in this theme. Modelled on Salient's “Signal” demo.
- **Hero:** a full-viewport volt panel (`100svh` minus the nav) with the statement in three lines at `clamp(48px, 8.4vw + 16px, 168px)`, leading 0.9 and tracking −0.045em. The middle line is indented. “clear” is set in Instrument Serif italic. The lines rise in from a mask on load. A meta row sits underneath, with a pine rule above it: role on the left, a one-line summary in the middle and “Scroll ↓” on the right.
- **Scroll:** the circle around “clear” draws as you scroll, finishing at 40% of the hero's height. Scroll only sets a target, and the stroke glides toward it every frame (exponential smoothing, about 0.14s). That way mouse-wheel notches draw smoothly instead of in steps. When the Intro section passes 60% of the viewport, `html.hero-mode` is removed. The page background then fades from volt to bone over 0.8s, and the header fades from volt/pine back to pine/volt.
- **Header in hero mode:** volt background, pine logo and links, and a pine outline “Let's Talk” button. The logo mark is now a CSS mask, so it takes on the current text colour.
- **Intro:** a large statement (Geist 400, 28–68px, max 22 characters per line) with “Peter Rebik.” on the volt marker. Its words light up from 16% to 100% opacity as it scrolls through the viewport. Below that is a 12-column row: copy and links in columns 6–9 and a 4:5 portrait card in 10–12.
- **Image trail:** moving the mouse over the hero leaves a trail of the six original-hero collage images. A new one appears every 110px of mouse travel (checked once per frame), cycling through them in order. Each is 150–220px wide with a random ±20° tilt. Timing matches Salient's “scale” trail. It grows 0→1 over 0.9s with `cubic-bezier(0,.2,.2,1)`, a quick start with a long settle, so it reads as “grow and hold”, while fading in over 0.3s. It then shrinks 1→0 over 0.7s (ease-out-quart), fading over the last 0.3s. Each image lives about 1.6s, so several overlap. It sits above the text but below the header. Mouse and pen only, not touch.
- **Circle:** white, sitting behind the “clear” lettering.
- Reduced motion: the circle is shown fully drawn, the words are fully lit, there is no rise-in, and the image trail is off.

## Skills reel (B), later changes
- **Bright cards (Oct 2026):** the dark, moody art felt off next to the rest of the site, and a volt wash over it looked muddy. The backgrounds were regenerated in a bright palette instead: pale volt, volt soft, volt, leaf and bone, with soft ember on Creative, Messaging and Alignment.  Illustrations and all card text are pine: title, number, description and chips. Chips are translucent bone with a faint pine border. The scrims are pale volt. On hover, the art blurs under a 70% pale-volt scrim, and the chips flip to pine with volt text.
- **Illustration tweaks:** on Alignment, the middle line uses the soft grey-green (pine at 45%, like the secondary strokes on the other icons). On Messaging, the front bubble is see-through: no fill, and the back bubble's outline stops at its edge. Its two text lines are solid pine.
- **Icon hover (Oct 2026):** each illustration is an inline SVG on its own layer, not baked into the background. Each stroke layer is one `<g>` with a single opacity, and SVG masks stand in for the old erasers. One timing, `--reveal: 0.65s` on `.rcard`, drives everything on hover. Each icon's move fits inside it. The icon floats up just a touch (−3%, ease-out) and fades smoothly from the start (`--fade: cubic-bezier(0.37, 0, 0.63, 1)` over 85% of `--reveal`). When open, the description gets an extra `--space-3` bottom margin (double the grid gap) so it sits further from the chips. The description waits until halfway (0.33s), when the icon is mostly faded, then fades and slides in over 0.38s, so the text lands as the move ends and the two never stack. There's no white flash. Messaging's bubbles shrink only to 0.8×, and the pops are 1.08×. On leave the icon settles back in (0.6s), and the text hides quickly (0.2s). The moves are:
  - **Brand:** each ring unwinds from a full circle to a 1% dot (0.4s each, 0.06s apart, alternating directions), and the centre dot pulses.
  - **Creative:** the eye blinks shut like a real eye. The upper lid sweeps down to meet the lower one in a soft downward curve (a 0.4s SMIL morph of the outline). The iris and pupil are clipped by that same moving lid shape, so they're covered rather than squashed.
  - **Messaging:** the back bubble types two lines, then both bubbles shrink away, front first.
  - **Systems:** the eight empty modules fill one by one in a snake (0.05s apart) that ends beside the solid module, which pops.
  - **Digital:** the pointer glides to the button and clicks (0.4s), then the button grows to fill the window (0.27s from 0.38s).
  - **Alignment:** all five lines ease straight (0.65s), and ease back on leave.
  - **How it runs:** the line and button changes use SMIL (`<animate data-morph="in|out">`), because CSS `d` and rect-geometry transitions don't work in Safari. The component script starts the "in" animations on pointer or focus, after their `data-delay`, using timers so a quick leave cancels them. On leave it runs "out" only for animations that actually started. Everything else is CSS keyed off `[data-icon]`.
  - **Reduced motion:** no moves, no lift, just a fade.
- **Restored (Oct 2026):** the mobile reel width (72vw under 860px), the reduced-motion swipe row, tap-to-open on touch (which pauses the reel while a card is open), and the off-screen pause. These had been dropped by accident when the Pause button was removed.
- **Reel controls (Oct 2026):** the reel is now driven by JS instead of a CSS animation: one looping offset, rendered with `translate3d`. That lets people move it:
  - **Arrows:** two subtle 40px chevron buttons at bottom right (faint outline, 70% opacity, volt on hover) nudge it one card per click (0.65s ease-in-out). They land on a card edge, and rapid clicks stack.
  - **Trackpad:** horizontal swipes move the reel directly.
  - **Touch:** dragging works on phones. A real drag doesn't count as a tap-to-open.
  - **Auto-scroll:** still one loop per `--speed`. It pauses on hover or focus, while a card is open, during a drag and off-screen.
  - **Reduced motion:** the reel stays a native swipe row, and the arrows scroll it by a card.
- The head is just the “Skills” eyebrow and the title. The intro paragraph, the Let's Talk link, the “Hover or tap” hint and the Pause button were all removed.
- The scroll is slower: 100s per loop on desktop, 80s on mobile. It still pauses on hover, on keyboard focus, while a card is tapped open, and when off-screen.
- The section now sits *after* the work carousel, on the plain page background (no mint), with no top padding so the gap to the work section stays one section-pad. Nav and footer links follow this order in the 2026 theme.
- Section eyebrows no longer show totals (“Skills”, “Selected work”, “Client feedback”).


## About (B)
- `AboutSplit.astro` replaces the centred `About.astro` when `site.theme` is `'2026'`.
- **Layout:** two columns at 7 : 5, stacked below 900px. On the left: an “About” eyebrow, the title “More *about* me.” and two bio paragraphs at `--fs-body-lg`, left-aligned and not justified. On the right: the UK Skilled Worker Sponsorship card. It's mint, `--radius-lg`, with the flags, title and copy left-aligned, and holds the section's Let's Talk button.
- There's no portrait and no “Hi, I'm Peter”, because the Intro section already covers both. The bio copy is trimmed so it doesn't repeat the Intro.
- **High-res source images (Oct 2026):** the hero trail images (annual report, Beautiful Day, farmers market, phone), the Recruitment, Smith-Kandal and Windsor Christian covers, and Peter's portrait were re-cut from Peter's originals in his Drive "Links" folder. Each uses the same crop as before, at up to 1600px for the hero and 2000px for covers, saved as JPG. Peter's 1080px bio pic is now `brand/peter-about.jpg`, and the old 155px avatar was removed. The original hero uses the same file for its avatar. The hero trail now requests 880px images, and the Intro portrait offers 280/560/840w. Still low-res, waiting on the files: `hero/brand-guidelines.png`, `hero/billboard.png` (also the OG image), and the `brand-refresh.png` and `perception-campaign.png` covers.

## Hiring-readiness pass (B, Oct 12 2026)
From the site audit. This pass covers everything that didn't need input from Peter.

- **Results stat row:** the `results` frontmatter now renders under the project title as 2–3 big heading-font numbers with small labels between two hairlines (mono uppercase labels in 2026). This is shared template code, so it can go to main too.
- **Headline stat pill:** the first `results` entry sits on the bottom-left of the image as a volt pill (number in the heading font, label in mono), on the `/work` grid only. It was removed from the homepage WorkDrag cards, where the summary already carries the number. The `/work` grid also shows the employer label above the title.
- **Work order:** the strongest numbers lead. Perception, Recruitment, Gig Harbor, Brand Refresh, Smith-Kandal, Windsor, Annual Report, Select Logos, Kitchen Sink. The Smith-Kandal summary now carries its ~40%.
- **Copy:** "designer and art director *who* bridges". The case studies use UK spelling (colour, organisation, centralised…), with "ADA" now reading "accessibility (ADA / WCAG)" and "theaters" now "cinemas". The Kitchen Sink and Select Logos intros are rewritten, and their employer is "Various clients".
- **Candidate framing (2026 only):** the skills title is "What I *bring*." (footer link "What I Bring"), the reviews eyebrow is "Feedback", and the CTA copy is "Hiring a senior designer or art director in the UK?…" The footer sign-off is `site.footerLine`, so it no longer repeats the Intro.
- **Copy email:** `CopyEmail.astro` adds an outline "Copy email" button next to Let's Talk in the CTA (dark tone) and the visa card, plus a text link in the footer. It shows "Copied ✓" and announces the copy through an `aria-live` region. The CTA also shows the address underneath. All 2026 only.
- **Alt text:** every gallery image has real, descriptive alt text, drafted from the images. Peter should check them.
- **Accessibility:** the footer legal line is sage instead of 60% opacity (it was 3.55:1). Footer links have 4px block padding, so they're 24px tap targets. Reel cards get `aria-labelledby` and `aria-describedby`, and Enter / Space pin a card open. Unlit Intro words start at 38% opacity (was 16%). The CTA copy is centred, not justified. The result is zero axe violations on `/`, `/work`, project pages and 404, at both 1440 and 390.
- **Mobile hero:** capped at `min(100svh − nav, 620px)` below 760px, so the work arrives about a screen sooner.
- **Performance:** SkillsReel strips the C2PA `<metadata>` from the inline icons at render time (the source SVGs keep it). That takes the homepage HTML from 365 KB to 278 KB. `/work` covers 1–3 are eager, with `fetchpriority=high` on the first. Project pages give the priority hint to gallery images 1–2. WorkDrag images are all lazy. The logo mask is served as WebP.
- **SEO and sharing:** `brand/og-card.jpg` (1200×630: the statement on volt, with two campaign tiles and Peter's portrait on top) is the default share image on the 2026 theme; the original theme still uses the billboard. Pages now have og:site_name, og:locale, og:image width/height/alt and the twitter:* tags. The homepage has Person JSON-LD. There's a hand-rolled `sitemap.xml` (the homepage, /work and every project) with a matching `Sitemap:` line in robots.txt. Also added: `apple-touch-icon.png`, `icon-192/512.png` and `site.webmanifest`. `/404` is `noindex` with no canonical, and `noindex` pages no longer output a canonical. The `/work` description is longer.
- **Waiting on Peter:** CV PDF, LinkedIn, own-domain email, the visa route and the sponsorship-card wording, start date, project year/team lines, process and before/after images, named reviews, and the 3 missing quotes. Also: the Easter banner (`kitchen-sink/23-easter`) misspells "thief" as "THEIF".
