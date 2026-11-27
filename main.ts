// "The World in One Picture" — a news-image-20261126 entry (Node 22, stdlib only).
//
// The picture is the entry.png beside this file: a newspaper front page drawn
// for Thursday 26 November 2026 by tools/render.py (Pillow shapes and text;
// no photo, no web image). This program only carries it to the output the
// grader reads, and checks it on the way: PNG signature, at most 1024x1024
// pixels, at most 1 MiB — the competition's own gate, applied here first.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

const bytes = readFileSync(source);

// PNG signature: 89 50 4E 47 0D 0A 1A 0A.
const signature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
if (!signature.every((b, i) => bytes[i] === b)) {
  throw new Error('entry.png is not a PNG file');
}
// IHDR chunk: width and height are the first 8 bytes of its data.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(target, bytes);
// Read it back: the grader runs this program twice and both runs must
// write the same bytes, so the copy must be exact, not just close.
if (!readFileSync(target).equals(bytes)) {
  throw new Error('written entry.png differs from the source');
}
console.log(`wrote ${target} (${width}x${height}, ${bytes.length} bytes)`);
