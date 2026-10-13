/**
 * sitemap.xml — homepage, the work index and every published project.
 * (Hand-rolled instead of @astrojs/sitemap: no extra dependency, and /404 + /styleguide stay out.)
 */
import type { APIRoute } from 'astro';
import { getAllWork } from '../lib/work';

export const GET: APIRoute = async ({ site }) => {
  const work = await getAllWork();
  const paths = ['/', '/work/', ...work.map((w) => `/work/${w.id}/`)];
  const urls = paths.map((p) => `  <url><loc>${new URL(p, site)}</loc></url>`).join('\n');
  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`,
    { headers: { 'Content-Type': 'application/xml; charset=utf-8' } },
  );
};
