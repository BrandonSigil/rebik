import { defineCollection, reference } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';

/**
 * WORK — one Markdown file per project in src/content/work/.
 * Add a project: copy src/content/work/_template.md, rename, fill in.
 * Files starting with "_" are ignored.
 */
const galleryImage = (image: () => any) =>
  z.object({
    src: image(),
    alt: z.string(),
    /** Optional: 'contain' shows the whole image (letterboxed) instead of cropping to fill the tile. */
    fit: z.enum(['cover', 'contain']).optional(),
    /** Optional CSS object-position for cropping, e.g. "top" or "30% 50%". */
    position: z.string().optional(),
  });

const work = defineCollection({
  loader: glob({ pattern: ['**/*.md', '!**/_*.md'], base: './src/content/work' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      /** Optional title for the homepage card. Use \n to force a line break. */
      cardTitle: z.string().optional(),
      /** Small lime line above the project title (employer / client, e.g. "Pierce Transit", "Freelance"). */
      employer: z.string().optional(),
      /** One-line outcome shown on the homepage card + used as the page description. */
      summary: z.string(),
      /** Intro paragraphs under the title. Separate paragraphs with a blank line. */
      intro: z.string().default(''),
      /** Homepage carousel / work index image. */
      cover: image(),
      coverAlt: z.string(),
      /** Lower numbers appear first (carousel, work index, prev/next order). */
      order: z.number().default(100),
      /** Show in the homepage carousel. */
      featured: z.boolean().default(true),
      draft: z.boolean().default(false),
      /** "My Role" chips. IDs from src/data/roles.yaml. */
      roles: z.array(reference('roles')).default([]),
      /** "Skills Used" chips. IDs from src/data/skills.yaml (the homepage "How I can help" cards). */
      skills: z.array(reference('skills')).default([]),
      /** Headline results, e.g. { value: "50%+", label: "more applications" } */
      results: z.array(z.object({ value: z.string(), label: z.string() })).default([]),
      /** Right-hand image column. Each entry is ONE ROW of 1, 2 or 3 images. */
      gallery: z.array(z.array(galleryImage(image)).min(1).max(3)).default([]),
    }),
});

const roles = defineCollection({
  loader: file('./src/data/roles.yaml'),
  schema: z.object({ order: z.number(), label: z.string(), icon: z.string() }),
});

const skills = defineCollection({
  loader: file('./src/data/skills.yaml'),
  schema: z.object({
    order: z.number(),
    title: z.string(),
    icon: z.string(),
    image: z.string().optional(),
    tags: z.array(z.string()).default([]),
    description: z.string(),
  }),
});

const reviews = defineCollection({
  loader: file('./src/data/reviews.yaml'),
  schema: z.object({ order: z.number(), quote: z.string(), org: z.string(), role: z.string() }),
});

export const collections = { work, skills, reviews, roles };
