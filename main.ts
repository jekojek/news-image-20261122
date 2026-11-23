// News-image entry for 22 November 2026: copies the front-page image
// beside this file to the output directory. Node 22, standard library
// only, no network. The grader runs it twice; both runs must write
// the same bytes, so this is a plain byte copy with a check.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);

if (!existsSync(src)) {
  console.error('entry.png missing next to main.ts');
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, 'entry.png'));

const written = readFileSync(join(outDir, 'entry.png'));
const original = readFileSync(src);
if (!written.equals(original)) {
  console.error('entry.png copy mismatch');
  process.exit(1);
}
