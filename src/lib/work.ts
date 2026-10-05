import { getCollection, type CollectionEntry } from 'astro:content';

export type Work = CollectionEntry<'work'>;

/** All published projects, sorted by `order`. */
export async function getAllWork(): Promise<Work[]> {
  const all = await getCollection('work', ({ data }) => !data.draft);
  return all.sort((a, b) => a.data.order - b.data.order || a.data.title.localeCompare(b.data.title));
}

/** Projects shown in the homepage carousel. */
export async function getFeaturedWork(): Promise<Work[]> {
  return (await getAllWork()).filter((p) => p.data.featured);
}
