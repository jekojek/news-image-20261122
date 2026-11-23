// News image entry: writes the 22 November 2026 world-news front page to the output directory.
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

// Fail loudly if the copy did not land byte-identical: the grader runs the
// program twice and both runs must write the same bytes.
const written = readFileSync(join(outDir, 'entry.png'));
const original = readFileSync(src);
if (!written.equals(original)) {
  console.error('entry.png copy mismatch');
  process.exit(1);
}
