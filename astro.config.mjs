// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://peterrebik.com',
  output: 'static',
  trailingSlash: 'ignore',
  prefetch: { prefetchAll: false, defaultStrategy: 'hover' },
  // Inline all CSS (about 15 KB compressed on the homepage) so first paint
  // doesn't wait on separate stylesheet requests.
  build: { inlineStylesheets: 'always' },
  image: { responsiveStyles: false },
});
