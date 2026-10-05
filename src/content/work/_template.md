---
# Copy this file, rename it (e.g. my-project.md — the file name becomes the URL /work/my-project),
# and remove the leading underscore. Put images in src/assets/work/.
title: "Project Title"
cardTitle: "Project\nTitle"          # optional: \n forces a line break on the homepage card
summary: "One sentence outcome, ideally with a number."
cover: ../../assets/work/your-cover.jpg   # 3:2 landscape works best
coverAlt: "Describe the image for screen readers"
order: 6                              # carousel order, left → right (middle item starts centered)
featured: true                        # show in homepage carousel
draft: false                          # true = hidden everywhere
client: "Client name"
role: "Art Direction, Design"
year: 2026
services: ["Brand Identity", "Campaign"]
results:
  - { value: "2x", label: "what improved" }
gallery:
  - { src: ../../assets/work/your-image.jpg, alt: "…", layout: full }
  - { src: ../../assets/work/your-image-2.jpg, alt: "…", layout: half, caption: "Optional caption" }
  - { src: ../../assets/work/your-image-3.jpg, alt: "…", layout: half }
---

## The challenge

Write the problem here.

## The approach

Write how you solved it. You can drop images inline too:

![Alt text](../../assets/work/your-image.jpg)

## The outcome

Write the results here.
