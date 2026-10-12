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
- Logo: `src/assets/brand/logo-mark.png` plus the wordmark set live in Dela Gothic One. **TODO:** swap the PNG mark for Peter's SVG when he sends it.

---

## 7. Voice

Clear, warm, confident. Short sentences. Lead with outcomes, and use numbers when you have them (“Reduced design time by ~30%”).

---

## 8. Project page (`/work/[slug]`)

From Peter's project wireframe.

- **Layout:** 2 : 3 columns in `.container` (text left, images right), stacked below 900px. The text column is sticky: it scrolls until its bottom is in view, then holds while the images continue.
- **Title block:** employer eyebrow (`t-h4`, lime), then the `t-display` title.
- **My Role / Skills Used:** native `<details open>` toggles. The lime dash turns into a plus when collapsed. Chips are mint pills with a lime icon dot. Skill chips use the homepage skill icons and link back to `/#help`, labelled in lowercase with `&` written as `+`.
- **Write-up card:** mint panel, `--radius-lg`. Headings are `--fs-h4`, body is `--fs-small`, and list bullets are lime dots.
- **Images:** rows of 1, 2 or 3 tiles with a 10px gap and `--radius-md`. Each row's tiles share one aspect ratio, based on the average of their images, so the row lines up. An image whose shape is far off the row's shape is letterboxed (`contain`) instead of cropped. Every tile opens the lightbox (arrow keys, Esc).
- **Prev / next band:** lime band with forest outline pills (“See Prev”, “See Next”) and long arrows. Hover: `#ade04b` fill, ×1.1, lift shadow.
