import { defineCollection } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';

/**
 * WORK — one Markdown file per project in src/content/work/.
 * Add a project: copy src/content/work/_template.md, rename, fill in.
 * Files starting with "_" are ignored.
 */
const work = defineCollection({
  loader: glob({ pattern: ['**/*.md', '!**/_*.md'], base: './src/content/work' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      /** Optional title for the homepage card. Use \n to force a line break. */
      cardTitle: z.string().optional(),
      /** One-line outcome shown on the card and under the project title. */
      summary: z.string(),
      cover: image(),
      coverAlt: z.string(),
      /** Lower numbers appear first in the carousel. */
      order: z.number().default(100),
      /** Show in the homepage carousel. */
      featured: z.boolean().default(true),
      draft: z.boolean().default(false),
      client: z.string().optional(),
      role: z.string().optional(),
      year: z.union([z.string(), z.number()]).optional(),
      services: z.array(z.string()).default([]),
      /** Headline results, e.g. { value: "50%+", label: "more applications" } */
      results: z.array(z.object({ value: z.string(), label: z.string() })).default([]),
      /** Image gallery shown after the write-up. layout: full | half */
      gallery: z
        .array(
          z.object({
            src: image(),
            alt: z.string(),
            caption: z.string().optional(),
            layout: z.enum(['full', 'half']).default('full'),
          }),
        )
        .default([]),
    }),
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

export const collections = { work, skills, reviews };
