// Entry point for the news-image-20261122 entry.
//
// Runs the Python drawing program and writes the finished front page to
// <output dir>/entry.png. The output directory comes from
// MAKEFUN_OUTPUT_DIR (the grader sets it to /output); without it the image
// goes to ./out/entry.png. Standard library only, no network, deterministic:
// the drawing program writes the same bytes on every run.
import { execFileSync } from "node:child_process";
import { mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "out";
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, "entry.png");

execFileSync("python3", ["draw_news.py", outPath], {
  cwd: repoRoot,
  stdio: "inherit",
});
