/**
 * Downloads Peter's project images from the old Squarespace site into src/assets/work/<project>/
 * (replacing the grey placeholders) and converts them to WebP.
 *
 *   npm run images            # download everything listed in scripts/work-images.json
 *   npm run images -- annual  # only files whose path contains "annual"
 *
 * Run once, check the pages, then commit the images. After that this script isn't needed.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const list = JSON.parse(await fs.readFile(path.join(root, 'scripts/work-images.json'), 'utf8'));
const filter = process.argv[2];
const todo = filter ? list.filter((x) => x.file.includes(filter)) : list;

let done = 0, failed = 0;
async function one({ file, url }) {
  const res = await fetch(`${url}?format=2500w`, { headers: { 'User-Agent': 'Mozilla/5.0' } });
  if (!res.ok) throw new Error(`${res.status} ${url}`);
  const buf = Buffer.from(await res.arrayBuffer());
  const out = path.join(root, file);
  await fs.mkdir(path.dirname(out), { recursive: true });
  await sharp(buf).rotate().resize({ width: 2400, withoutEnlargement: true }).webp({ quality: 82 }).toFile(out);
}
const queue = [...todo];
await Promise.all(Array.from({ length: 6 }, async () => {
  while (queue.length) {
    const item = queue.shift();
    try { await one(item); done++; process.stdout.write(`\r${done}/${todo.length}`); }
    catch (e) { failed++; console.error(`\n✗ ${item.file}: ${e.message}`); }
  }
}));
console.log(`\nDone: ${done} downloaded, ${failed} failed.`);
if (failed) process.exitCode = 1;
