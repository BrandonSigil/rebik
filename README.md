# peterrebik.com

Portfolio site for Peter Rebik, built with [Astro](https://astro.build). It's fully static, with no client framework and ~4 KB of JS total, and it's hosted on Render.

## Run it

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # → dist/
npm run preview
```

Node 22+.

## Where things live

| What | File |
|---|---|
| **Brand guide** (colors, type, spacing, motion rules) | [`BRAND.md`](BRAND.md) · live at `/styleguide` |
| Design tokens (the actual values) | `src/styles/tokens.css` |
| Global styles, type classes, buttons | `src/styles/global.css` |
| Email, nav, footer links, marquee words | `src/data/site.ts` |
| “How I can help” cards | `src/data/skills.yaml` |
| Reviews | `src/data/reviews.yaml` |
| **Projects** | `src/content/work/*.md` |
| Project page template | `src/pages/work/[slug].astro` |
| “My Role” chips | `src/data/roles.yaml` |
| Homepage sections | `src/components/*.astro` (composed in `src/pages/index.astro`) |
| Icons (SVG, `currentColor`) | `src/icons/` |
| Source wireframe | `docs/wireframe-landing.pdf` |
| Theme switch (`original` / `2026`) | `theme` in `src/data/site.ts` · preview with `?theme=original` |
| 2026 theme overrides | `src/styles/themes/2026.css` |
| About split + sponsorship card (2026 theme) | `src/components/AboutSplit.astro` |
| Bold hero + intro (2026 theme) | `src/components/HeroBold.astro`, `src/components/Intro.astro` |
| Work drag carousel (2026 theme) | `src/components/WorkDrag.astro` · image per project = `feature` in its `.md` |
| Skills reel art (placeholder) | `src/assets/skills/` (`<name>-bg.jpg` + `<name>-icon.svg`) · regenerate with `python3 scripts/generate-skill-art.py` |

## Common edits

**Add a project:** copy `src/content/work/_template.md` to `src/content/work/my-project.md`, drop images in `src/assets/work/my-project/`, and fill in the frontmatter. The file name becomes the URL (`/work/my-project`). `order` sets the order everywhere (carousel, work index, See Prev / See Next). Set `featured: false` to keep a project off the homepage carousel, or `draft: true` to hide it everywhere.

**Project page layout:** `employer` is the lime line above the title, `roles` and `skills` become the chip lists (ids from `roles.yaml` / `skills.yaml`), `intro` is the dark "Brief" card under them, and the Markdown body becomes the mint write-up cards, one per `## ` heading (Challenge / Approach / Results). The last word of each heading gets the volt highlight. `gallery` is the image column: each top-level `-` is one row of 1–3 images that share a height. Add `fit: contain` to an image to stop it being cropped. Click any image for the full-screen viewer.

**Project images from the old site:** `npm run images` downloads Peter's originals from Squarespace into `src/assets/work/<project>/` (replacing the grey placeholders) as WebP. The list lives in `scripts/work-images.json`.

**Swap a project out:** delete its `.md` (or set `draft: true`). Nothing else needs to change.

**Edit a review:** edit `src/data/reviews.yaml`. Grid order follows `order`.

**Change homepage copy:** headings and paragraphs are in the matching component (`Hero.astro`, `Skills.astro`, `About.astro`, and so on).

## Deploy (Render)

`render.yaml` is a Blueprint. In Render, go to **New → Blueprint**, pick this repo, and deploy. Every push to `main` redeploys, and PRs get preview URLs. Hashed assets under `/_astro/` are served with immutable caching.

## Open TODOs

- [ ] Replace extracted wireframe images with Peter's full-res originals (`src/assets/`)
- [ ] Swap `logo-mark-2x.png` for the SVG logo
- [ ] Run `npm run images` to swap the grey gallery placeholders for Peter's real images, then commit
- [ ] Review image alt text in `src/content/work/*.md` (auto-generated from file names)
- [ ] Remaining reviews (“Should have soon.”)
- [ ] Point the `peterrebik.com` domain at Render
