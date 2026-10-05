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
| Homepage sections | `src/components/*.astro` (composed in `src/pages/index.astro`) |
| Icons (SVG, `currentColor`) | `src/icons/` |
| Source wireframe | `docs/wireframe-landing.pdf` |
| Theme switch (`original` / `2026`) | `theme` in `src/data/site.ts` · preview with `?theme=original` |
| 2026 theme overrides | `src/styles/themes/2026.css` |
| Skills reel art (placeholder) | `src/assets/skills/` · regenerate with `python3 scripts/generate-skill-art.py` |

## Common edits

**Add a project:** copy `src/content/work/_template.md` to `src/content/work/my-project.md`, drop images in `src/assets/work/`, and fill in the frontmatter. The file name becomes the URL (`/work/my-project`). `order` sets the carousel position left to right, and the middle project starts centered. Set `featured: false` to keep a project off the homepage carousel, or `draft: true` to hide it everywhere.

**Swap a project out:** delete its `.md` (or set `draft: true`). Nothing else needs to change.

**Edit a review:** edit `src/data/reviews.yaml`. Grid order follows `order`.

**Change homepage copy:** headings and paragraphs are in the matching component (`Hero.astro`, `Skills.astro`, `About.astro`, and so on).

## Deploy (Render)

`render.yaml` is a Blueprint. In Render, go to **New → Blueprint**, pick this repo, and deploy. Every push to `main` redeploys, and PRs get preview URLs. Hashed assets under `/_astro/` are served with immutable caching.

## Open TODOs

- [ ] Replace extracted wireframe images with Peter's full-res originals (`src/assets/`)
- [ ] Swap `logo-mark.png` for the SVG logo
- [ ] Real project write-ups, client names, and galleries (currently placeholders)
- [ ] Remaining reviews (“Should have soon.”)
- [ ] Point the `peterrebik.com` domain at Render
