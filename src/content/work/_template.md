---
# Copy this file, rename it (e.g. my-project.md — the file name becomes the URL /work/my-project),
# and remove the leading underscore. Put images in src/assets/work/my-project/.
title: "Project Title"
cardTitle: "Project\nTitle"          # optional: \n forces a line break on the homepage card
employer: "Employer or client"       # small lime line above the title
summary: "One sentence outcome, ideally with a number."   # homepage card + page description
intro: |
  First intro paragraph: the problem, in a sentence or two.

  Second paragraph: your role and what you did.
cover: ../../assets/work/my-project/cover.webp   # homepage card / work index image (3:2 works best)
coverAlt: "Describe the image for screen readers"
order: 10                             # order everywhere (carousel, work index, prev/next)
featured: false                       # show in homepage carousel
draft: false                          # true = hidden everywhere
roles: [graphic-designer, art-director]   # ids from src/data/roles.yaml
skills: [brand-strategy, creative-direction, messaging-story, systems-processes, digital-experiences, alignment-collaboration]  # ids from src/data/skills.yaml
results:
  - { value: "2x", label: "what improved" }
# Images: each top-level "-" is ONE ROW of 1, 2 or 3 images. Images in a row share a height.
# Optional per image: fit: contain (show whole image, no crop) · position: top (where to crop)
gallery:
  - - { src: ../../assets/work/my-project/01.webp, alt: "…" }
  - - { src: ../../assets/work/my-project/02.webp, alt: "…" }
    - { src: ../../assets/work/my-project/03.webp, alt: "…" }
  - - { src: ../../assets/work/my-project/04.webp, alt: "…" }
    - { src: ../../assets/work/my-project/05.webp, alt: "…" }
    - { src: ../../assets/work/my-project/06.webp, alt: "…", fit: contain }
---

## The Challenge

What problem was the organisation facing?

## The Approach

How you solved it. Bullet lists and > quotes work here.

## The Results

- What changed, with numbers where you have them
