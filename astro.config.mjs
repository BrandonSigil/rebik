// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://peterrebik.com',
  output: 'static',
  trailingSlash: 'ignore',
  prefetch: { prefetchAll: false, defaultStrategy: 'hover' },
  build: { inlineStylesheets: 'auto' },
  image: { responsiveStyles: false },
});
